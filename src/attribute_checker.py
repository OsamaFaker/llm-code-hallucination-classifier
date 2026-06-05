"""
Phantom Attribute Checker Plugin (Item #2).

Detects hallucinated attributes/methods on well-known Python built-in types
by comparing AST attribute accesses against `dir(type)` via runtime introspection.

Classification principle (GT-existence framework):
  - Construct EXISTS in Python Ground Truth → GROUNDED_ERROR if misused.
    Example: `numbers.append()` — append exists on list but is called without
    its required argument.  The error is grounded in a real construct.
  - Construct does NOT exist in Python Ground Truth → HALLUCINATION.
    Example: `numbers.add(5)` — add does not exist on list regardless of
    whether it exists on set; `list.push(x)` — push does not exist in Python
    regardless of JavaScript.  Both are fabricated attributes on this type.

This checker handles the HALLUCINATION branch for attribute access.
The GROUNDED_ERROR branch (bound-method-no-call) is handled separately
in `_check_bound_method_no_call` below.
"""
import ast
from typing import Optional, Dict, Set

from src.models import ClassificationResult, HallucinationCategory, SeverityLevel
from src.plugin_registry import CheckerPlugin


# Built-in types whose attribute sets we can fully enumerate via introspection.
_TYPE_MAP: Dict[str, type] = {
    "list":       list,
    "str":        str,
    "dict":       dict,
    "int":        int,
    "float":      float,
    "bool":       bool,
    "set":        set,
    "frozenset":  frozenset,
    "tuple":      tuple,
    "bytes":      bytes,
    "bytearray":  bytearray,
}

# Module-level attribute cache — avoids repeated dir() calls.
_ATTR_CACHE: Dict[str, Set[str]] = {}


def _get_valid_attrs(type_name: str) -> Optional[Set[str]]:
    """Return the full set of valid attributes for a known type, using a cache."""
    if type_name in _ATTR_CACHE:
        return _ATTR_CACHE[type_name]
    if type_name not in _TYPE_MAP:
        return None
    attrs = set(dir(_TYPE_MAP[type_name]))
    _ATTR_CACHE[type_name] = attrs
    return attrs


def _infer_type_from_node(node: ast.expr) -> Optional[str]:
    """Infer a type name string from an AST value node (literal or constructor)."""
    if isinstance(node, ast.List):
        return "list"
    if isinstance(node, ast.Dict):
        return "dict"
    if isinstance(node, ast.Set):
        return "set"
    if isinstance(node, ast.Tuple):
        return "tuple"
    if isinstance(node, ast.Constant):
        return type(node.value).__name__
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        if name in _TYPE_MAP:
            return name
    return None


# Heuristic name-to-type mappings for common variable naming conventions.
# CONSERVATIVE: Only includes clearly unambiguous names to avoid false positives.
# Single-letter variables (x, d, a, s, n) are deliberately excluded because
# their types are context-dependent.  See review item #5.
_IMPLICIT_TYPES: Dict[str, str] = {
    # list-like — only explicit plural/collection names
    "arr": "list", "lst": "list", "items": "list", "numbers": "list",
    "elements": "list", "data_list": "list",
    "nums": "list", "digits": "list", "chars": "list", "words": "list",
    # str-like — only explicit text names
    "text": "str", "msg": "str", "message": "str",
    "word": "str", "line": "str", "string": "str",
    "pattern": "str", "filename": "str", "url": "str",
    # dict-like — only explicit mapping names
    "config": "dict", "opts": "dict", "mapping": "dict",
    "data_dict": "dict",
    # int-like — only explicit count/size names
    "count": "int", "length": "int", "idx": "int",
}


class AttributeCheckerPlugin(CheckerPlugin):
    """
    Detects hallucinated or incorrectly used attributes/methods on built-in types.
    Also detects bound-method access without calling (e.g. `result = s.upper`).

    Priority 85 — runs after FabricationChecker (90) but before ArityChecker (75).
    """

    @property
    def name(self) -> str:
        return "attribute"

    @property
    def priority(self) -> int:
        return 85

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        code = kwargs.get("code", "")
        ast_tree = kwargs.get("ast_tree")
        if not code:
            return None
        result = _check_phantom_attributes(code, tree=ast_tree)
        if result:
            return result
        return _check_bound_method_no_call(code, tree=ast_tree)


def _check_phantom_attributes(code: str, tree: 'ast.AST | None' = None) -> Optional[ClassificationResult]:
    """
    Walk the AST, resolve variable types, and flag any attribute access
    where the attribute does not exist in dir(resolved_type).
    """
    if tree is None:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None  # Syntax errors are handled by the parser/classifier

    # Build variable type map from assignments and heuristic names.
    var_types: Dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            inferred = _infer_type_from_node(node.value)
            if inferred:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_types[target.id] = inferred
        elif isinstance(node, ast.AnnAssign):
            # e.g.  x: list = []
            if isinstance(node.annotation, ast.Name) and node.annotation.id in _TYPE_MAP:
                if isinstance(node.target, ast.Name):
                    var_types[node.target.id] = node.annotation.id

    # Backfill heuristic guesses only for variables with no AST assignment
    for name, type_guess in _IMPLICIT_TYPES.items():
        if name not in var_types:
            var_types[name] = type_guess

    # Walk all Attribute-access nodes and validate the attribute.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue

        attr = node.attr
        obj = node.value

        # Skip dunder attributes — they are implementation details.
        if attr.startswith("_"):
            continue

        # Attempt to resolve the object's type.
        obj_type: Optional[str] = None

        if isinstance(obj, ast.Name):
            obj_type = var_types.get(obj.id)
        elif isinstance(obj, ast.Call) and isinstance(obj.func, ast.Name):
            obj_type = _infer_type_from_node(obj)
        elif isinstance(obj, ast.List) or isinstance(obj, ast.ListComp):
            obj_type = "list"
        elif isinstance(obj, ast.Dict) or isinstance(obj, ast.DictComp):
            obj_type = "dict"
        elif isinstance(obj, ast.Constant):
            obj_type = type(obj.value).__name__

        if obj_type is None:
            continue  # Cannot resolve → skip to avoid false positives

        valid_attrs = _get_valid_attrs(obj_type)
        if valid_attrs is None:
            continue  # Unknown type → skip

        if attr not in valid_attrs:
            line_info = f" (line {node.lineno})" if hasattr(node, "lineno") else ""

            # GT-existence check: the attribute does not exist on this type.
            # Regardless of whether it exists on another type or in another language,
            # it has no formal referent on this object → HALLUCINATION in all sub-cases.
            exists_on_other_type = any(
                attr in (_get_valid_attrs(other) or set())
                for other in _TYPE_MAP
                if other != obj_type
            )

            if exists_on_other_type:
                # e.g. list.add (add exists on set), str.append (append exists on list)
                other_types = [t for t in _TYPE_MAP if t != obj_type and attr in (_get_valid_attrs(t) or set())]
                return ClassificationResult(
                    is_valid=False,
                    is_grounded_error=False,
                    hallucination_category=HallucinationCategory.ATTRIBUTE,
                    explanation=(
                        f"Hallucination: '{obj_type}.{attr}' does not exist{line_info}. "
                        f"'{attr}' is a valid method of {other_types} but not of {obj_type} "
                        f"(fabricated attribute on this type)."
                    ),
                    confidence=0.91,
                    severity=SeverityLevel.HIGH,
                    checker_source="attribute",
                    line=node.lineno,
                    bad_token=attr
                )
            elif attr in _CROSS_LANGUAGE_METHODS:
                # e.g. list.push, list.isEmpty — valid in JS/Java but not Python.
                # This is cross-language API confusion → Condition 3 (Hallucination).
                return ClassificationResult(
                    is_valid=False,
                    is_grounded_error=False,
                    hallucination_category=HallucinationCategory.ATTRIBUTE,
                    explanation=(
                        f"Hallucination: '{obj_type}.{attr}' does not exist{line_info}. "
                        f"'{attr}' is a valid method in other languages (e.g. JavaScript/Java) "
                        f"but not in Python's built-in {obj_type} type "
                        f"(fabricated attribute on this type)."
                    ),
                    confidence=0.89,
                    severity=SeverityLevel.HIGH,
                    checker_source="attribute",
                    line=node.lineno,
                    bad_token=attr
                )
            else:
                # Attribute doesn't exist on any known type or language → hallucination
                return ClassificationResult(
                    is_valid=False,
                    is_grounded_error=False,
                    hallucination_category=HallucinationCategory.ATTRIBUTE,
                    explanation=(
                        f"Hallucination: '{obj_type}.{attr}' does not exist{line_info}. "
                        f"'{attr}' is not a valid attribute of any known Python built-in type."
                    ),
                    confidence=0.88,
                    severity=SeverityLevel.HIGH,
                    checker_source="attribute",
                    line=node.lineno,
                    bad_token=attr
                )

    return None


# ---------------------------------------------------------------------------
# Cross-language methods: valid in other languages but absent from Python built-ins.
# When an LLM calls list.push() or dict.contains(), the attribute does not exist
# in the Python Ground Truth for that type → HALLUCINATION (fabricated attribute),
# not a Grounded Error.  The fact that push() exists in JavaScript is irrelevant
# to whether it has a referent in the Python execution environment.
# ---------------------------------------------------------------------------
_CROSS_LANGUAGE_METHODS: frozenset = frozenset({
    # JavaScript Array / Java ArrayList equivalents used on Python lists
    "push", "peek", "isEmpty", "contains", "size", "get",
    "addAll", "removeAll", "toArray", "forEach", "indexOf",
    "lastIndexOf", "includes", "fill", "flat", "findIndex",
    # Java HashMap / C# Dictionary equivalents
    "containsKey", "containsValue", "putAll", "getOrDefault", "entrySet", "keySet",
    # C++ / Java string methods
    "charAt", "substring", "startsWith", "endsWith", "toUpperCase", "toLowerCase",
    "trim", "length", "compareTo", "concat",
})

# Known callable methods per type that take ZERO arguments.
# Used to detect `s.upper('en')` → TypeError: upper() takes no arguments.
_ZERO_ARG_METHODS: Dict[str, Set[str]] = {
    "str":   {"upper", "lower", "strip", "lstrip", "rstrip", "title", "swapcase",
              "capitalize", "isdigit", "isalpha", "isalnum", "isspace", "isupper",
              "islower", "istitle", "isnumeric", "isdecimal", "isidentifier",
              "isascii", "isprintable"},
    "list":  {"sort", "reverse", "copy", "clear", "pop"},
    "dict":  {"keys", "values", "items", "clear", "copy", "popitem"},
    "set":   {"pop", "clear", "copy"},
}


def _check_bound_method_no_call(code: str, tree: 'ast.AST | None' = None) -> Optional[ClassificationResult]:
    """
    Detect cases where a method is accessed as a property without being called.
    e.g.  `result = s.upper`  instead of  `result = s.upper()`
          `result = lst.sort`  instead of  `lst.sort()`

    These are Condition 2: the attribute exists on the type, but the composition
    rule R(GTenv) is violated — a callable must be invoked with ().
    """
    if tree is None:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None

    # Collect all Attribute nodes that ARE being called (inside ast.Call.func)
    called_attrs: Set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            called_attrs.add(id(node.func))

    var_types: Dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            inferred = _infer_type_from_node(node.value)
            if inferred:
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        var_types[t.id] = inferred

    # Backfill heuristic guesses only for variables with no AST assignment
    for name, type_guess in _IMPLICIT_TYPES.items():
        if name not in var_types:
            var_types[name] = type_guess

    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        if id(node) in called_attrs:
            continue  # This attribute IS being called — skip

        attr = node.attr
        if attr.startswith("_"):
            continue

        obj = node.value
        obj_type: Optional[str] = None
        if isinstance(obj, ast.Name):
            obj_type = var_types.get(obj.id)
        elif isinstance(obj, ast.Constant):
            obj_type = type(obj.value).__name__

        if obj_type is None:
            continue

        # Check if attr is a known callable method on this type
        zero_arg = _ZERO_ARG_METHODS.get(obj_type, set())
        valid_attrs = _get_valid_attrs(obj_type)
        if valid_attrs is None:
            continue

        if attr in valid_attrs and attr in zero_arg:
            # Method exists but is being used without () — bound method access
            line_info = f" (line {node.lineno})" if hasattr(node, "lineno") else ""
            return ClassificationResult(
                is_valid=False,
                is_grounded_error=True,
                hallucination_category=None,
                explanation=(
                    f"Grounded Error: '{obj_type}.{attr}' accessed without calling it"
                    f"{line_info}. Missing parentheses '()' — returns a bound method "
                    f"object instead of the result (TypeError at runtime)."
                ),
                confidence=0.87,
                severity=SeverityLevel.MEDIUM,
                checker_source="attribute",
                line=node.lineno,
                bad_token=attr
            )

    return None
