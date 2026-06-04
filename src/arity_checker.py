"""
Arity & Argument Type Checker Plugin.

Detects Grounded Errors caused by:
  1. Calling a built-in function with too many or too few arguments (arity error).
  2. Passing a wrong primitive type to a position where a specific type is required
     (e.g. range("10"), int(x, base="16")).

These are Condition 2 violations: the function IS in GTenv, but the composition
rule R(GTenv) is broken by incorrect argument cardinality or type.
"""
import ast
import inspect
import builtins
from typing import Optional, Dict, Tuple, List

from src.models import ClassificationResult, SeverityLevel
from src.plugin_registry import CheckerPlugin


# ---------------------------------------------------------------------------
# Build arity map from inspect.signature() on all accessible builtins.
# Entry: func_name -> (min_positional, max_positional)  (-1 = unlimited)
# ---------------------------------------------------------------------------
def _build_arity_map() -> Dict[str, Tuple[int, int]]:
    arity: Dict[str, Tuple[int, int]] = {}
    for name in dir(builtins):
        obj = getattr(builtins, name)
        if not callable(obj):
            continue
        try:
            sig = inspect.signature(obj)
        except (ValueError, TypeError):
            continue
        min_args = max_args = 0
        unlimited = False
        for param in sig.parameters.values():
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                unlimited = True
            elif param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
                max_args += 1
                if param.default is param.empty:
                    min_args += 1
            elif param.kind == param.KEYWORD_ONLY:
                pass  # keyword-only args don't count against positional arity
        arity[name] = (min_args, -1 if unlimited else max_args)
    return arity


_ARITY_MAP: Dict[str, Tuple[int, int]] = _build_arity_map()

# Explicit overrides for functions whose signatures are mis-reported by inspect
_ARITY_OVERRIDES: Dict[str, Tuple[int, int]] = {
    "pow":      (2, 3),   # pow(base, exp[, mod])
    "round":    (1, 2),   # round(number[, ndigits])
    "divmod":   (2, 2),
    "range":    (1, 3),   # range(stop) or range(start, stop[, step])
    "slice":    (1, 3),
    "print":    (0, -1),  # unlimited
}
_ARITY_MAP.update(_ARITY_OVERRIDES)

# Expected primitive types for key positional arguments.
# Maps func_name -> {arg_position: expected_python_type_name}
_ARG_TYPE_HINTS: Dict[str, Dict[int, str]] = {
    "range":    {0: "int", 1: "int", 2: "int"},
    "int":      {1: "int"},           # int(x, base=N) — base must be int
    "round":    {1: "int"},           # round(x, ndigits) — ndigits must be int
    "chr":      {0: "int"},
    "ord":      {0: "str"},
    "pow":      {0: "int", 1: "int"}, # usually numeric
}


class ArityCheckerPlugin(CheckerPlugin):
    """
    Detects arity errors and primitive argument type mismatches on built-in calls.
    Priority 75 — between MisuseChecker (70) and AttributeChecker (85).
    """

    @property
    def name(self) -> str:
        return "arity"

    @property
    def priority(self) -> int:
        return 75

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        code = kwargs.get("code", "")
        ast_tree = kwargs.get("ast_tree")
        if not code:
            return None
        if ast_tree is None:
            try:
                ast_tree = ast.parse(code)
            except SyntaxError:
                return None
        result = _check_arity(code, tree=ast_tree)
        if result:
            return result
        result = _check_method_arity(ast_tree)
        if result:
            return result
        return _check_kwarg_types(ast_tree)


def _check_arity(code: str, tree: 'ast.AST | None' = None) -> Optional[ClassificationResult]:
    if tree is None:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        # Only check free function calls to known builtins
        if not isinstance(node.func, ast.Name):
            continue
        func_name = node.func.id
        if func_name not in _ARITY_MAP:
            continue

        # Count positional args (exclude keyword args)
        n_positional = len(node.args)

        min_args, max_args = _ARITY_MAP[func_name]

        # ── Arity check ────────────────────────────────────────────────
        if max_args != -1 and n_positional > max_args:
            return ClassificationResult(
                is_valid=False,
                is_grounded_error=True,
                hallucination_category=None,
                explanation=(
                    f"Grounded Error: '{func_name}()' called with {n_positional} positional "
                    f"argument(s) but accepts at most {max_args} "
                    f"(TypeError: too many arguments)."
                ),
                confidence=0.93,
                severity=SeverityLevel.HIGH,
                checker_source="arity",
                line=node.lineno,
                bad_token=func_name
            )

        if n_positional < min_args:
            return ClassificationResult(
                is_valid=False,
                is_grounded_error=True,
                hallucination_category=None,
                explanation=(
                    f"Grounded Error: '{func_name}()' called with {n_positional} positional "
                    f"argument(s) but requires at least {min_args} "
                    f"(TypeError: missing required argument)."
                ),
                confidence=0.90,
                severity=SeverityLevel.HIGH,
                checker_source="arity",
                line=node.lineno,
                bad_token=func_name
            )

        # ── Primitive argument type check ────────────────────────────────
        if func_name in _ARG_TYPE_HINTS:
            for pos, expected_type in _ARG_TYPE_HINTS[func_name].items():
                if pos >= len(node.args):
                    continue
                arg_node = node.args[pos]
                actual_type = _literal_type(arg_node)
                if actual_type is not None and actual_type != expected_type:
                    return ClassificationResult(
                        is_valid=False,
                        is_grounded_error=True,
                        hallucination_category=None,
                        explanation=(
                            f"Grounded Error: '{func_name}()' argument {pos + 1} must be "
                            f"{expected_type} but got {actual_type} literal "
                            f"(TypeError: wrong argument type)."
                        ),
                        confidence=0.91,
                        severity=SeverityLevel.MEDIUM,
                        checker_source="arity",
                        line=node.lineno,
                        bad_token=func_name
                    )

    return None


def _literal_type(node: ast.expr) -> Optional[str]:
    """Return the type name of an AST literal node, or None if not a literal."""
    if isinstance(node, ast.Constant):
        return type(node.value).__name__
    if isinstance(node, ast.List):
        return "list"
    if isinstance(node, ast.Dict):
        return "dict"
    if isinstance(node, ast.Set):
        return "set"
    if isinstance(node, ast.Tuple):
        return "tuple"
    return None


# ---------------------------------------------------------------------------
# Method arity: (type_name, method_name) -> (min_positional, max_positional)
# Catches errors like  s.upper('en')  or  lst.append()  (missing required arg).
# ---------------------------------------------------------------------------
_METHOD_ARITY: Dict[tuple, Tuple[int, int]] = {
    ("str", "upper"):      (0, 0), ("str", "lower"):      (0, 0),
    ("str", "title"):      (0, 0), ("str", "swapcase"):   (0, 0),
    ("str", "strip"):      (0, 1), ("str", "lstrip"):     (0, 1),
    ("str", "rstrip"):     (0, 1), ("str", "isdigit"):    (0, 0),
    ("str", "isalpha"):    (0, 0), ("str", "isalnum"):    (0, 0),
    ("str", "capitalize"): (0, 0), ("str", "split"):      (0, 2),
    ("str", "join"):       (1, 1), ("str", "replace"):    (2, 3),
    ("str", "find"):       (1, 3), ("str", "count"):      (1, 3),
    ("list", "append"):    (1, 1), ("list", "extend"):    (1, 1),
    ("list", "insert"):    (2, 2), ("list", "remove"):    (1, 1),
    ("list", "sort"):      (0, 0), ("list", "reverse"):   (0, 0),
    ("list", "pop"):       (0, 1), ("list", "index"):     (1, 3),
    ("dict", "get"):       (1, 2), ("dict", "update"):    (0, 1),
    ("dict", "setdefault"):(1, 2),
}

# Kwarg value type constraints: (func_name, kwarg_name) -> expected kind
_KWARG_TYPE_CONSTRAINTS: Dict[tuple, str] = {
    ("sorted", "key"):     "callable",  # must not be a str literal
    ("sorted", "reverse"): "bool",
    ("sum",    "start"):   "numeric",   # start must be numeric not str
}

_HEURISTIC_TYPES: Dict[str, str] = {
    # Conservative: only clearly unambiguous variable names.
    # Single-letter variables excluded to avoid false positives.
    "text": "str", "word": "str", "string": "str", "msg": "str",
    "lst": "list", "arr": "list", "items": "list", "nums": "list",
    "config": "dict", "mapping": "dict",
}


def _check_method_arity(tree: ast.AST) -> Optional[ClassificationResult]:
    """Check method calls against _METHOD_ARITY (e.g. s.upper('en') -> ERROR)."""
    var_types: Dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.List):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        var_types[t.id] = "list"
            elif isinstance(node.value, ast.Dict):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        var_types[t.id] = "dict"
            elif isinstance(node.value, ast.Constant):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        var_types[t.id] = type(node.value.value).__name__

    # Backfill heuristic guesses only for variables with no AST assignment
    for name, type_guess in _HEURISTIC_TYPES.items():
        if name not in var_types:
            var_types[name] = type_guess

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        method = node.func.attr
        obj = node.func.value
        obj_type: Optional[str] = None
        if isinstance(obj, ast.Name):
            obj_type = var_types.get(obj.id)
        elif isinstance(obj, ast.Constant):
            obj_type = type(obj.value).__name__
        if obj_type is None:
            continue
        key = (obj_type, method)
        if key not in _METHOD_ARITY:
            continue
        n_pos = len(node.args)
        min_a, max_a = _METHOD_ARITY[key]
        if max_a != -1 and n_pos > max_a:
            return ClassificationResult(
                is_valid=False, is_grounded_error=True, hallucination_category=None,
                explanation=(
                    f"Grounded Error: '{obj_type}.{method}()' called with {n_pos} positional "
                    f"argument(s) but accepts at most {max_a} "
                    f"(TypeError: takes no arguments / too many arguments)."
                ),
                confidence=0.92, severity=SeverityLevel.HIGH, checker_source="arity",
                line=node.lineno, bad_token=method
            )
        if n_pos < min_a:
            return ClassificationResult(
                is_valid=False, is_grounded_error=True, hallucination_category=None,
                explanation=(
                    f"Grounded Error: '{obj_type}.{method}()' called with {n_pos} positional "
                    f"argument(s) but requires at least {min_a} "
                    f"(TypeError: missing required argument)."
                ),
                confidence=0.90, severity=SeverityLevel.HIGH, checker_source="arity",
                line=node.lineno, bad_token=method
            )
    return None


def _check_kwarg_types(tree: ast.AST) -> Optional[ClassificationResult]:
    """Check that keyword arguments satisfy type constraints (e.g. sorted(key='str'))."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func_name = node.func.id if isinstance(node.func, ast.Name) else ""
        for kw in node.keywords:
            if kw.arg is None:
                continue
            ck = (func_name, kw.arg)
            if ck not in _KWARG_TYPE_CONSTRAINTS:
                continue
            expected = _KWARG_TYPE_CONSTRAINTS[ck]
            if expected == "callable" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                return ClassificationResult(
                    is_valid=False, is_grounded_error=True, hallucination_category=None,
                    explanation=(
                        f"Grounded Error: '{func_name}()' kwarg '{kw.arg}' must be callable "
                        f"but got string literal '{kw.value.value}' "
                        f"(TypeError: '{kw.arg}' must be callable, not str)."
                    ),
                    confidence=0.91, severity=SeverityLevel.MEDIUM, checker_source="arity",
                    line=node.lineno, bad_token=kw.arg
                )
            if expected == "numeric" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                return ClassificationResult(
                    is_valid=False, is_grounded_error=True, hallucination_category=None,
                    explanation=(
                        f"Grounded Error: '{func_name}()' kwarg '{kw.arg}' must be numeric "
                        f"but got str (TypeError: wrong kwarg type)."
                    ),
                    confidence=0.90, severity=SeverityLevel.MEDIUM, checker_source="arity",
                    line=node.lineno, bad_token=kw.arg
                )
    return None
