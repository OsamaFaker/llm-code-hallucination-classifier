"""
Lightweight AST-based Type Inference Engine.

Tracks variable types through assignments and function returns to detect
type mismatches (e.g., range('10'), sort(reverse='yes')).
"""
import ast
from typing import Dict, Optional, Any, Set


class TypeInfo:
    """Represents inferred type information for a variable or expression."""

    def __init__(self, type_name: str, value: Any = None):
        self.type_name = type_name  # e.g. 'int', 'str', 'list', 'bool', 'float'
        self.value = value  # optional literal value if known

    def __repr__(self):
        if self.value is not None:
            return f"TypeInfo({self.type_name}, value={self.value!r})"
        return f"TypeInfo({self.type_name})"

    def is_compatible(self, expected_type: str) -> bool:
        """Check if this type is compatible with the expected type."""
        if self.type_name == expected_type:
            return True
        # Numeric compatibility: int is compatible with float
        if expected_type == "float" and self.type_name == "int":
            return True
        # bool is a subtype of int in Python
        if expected_type == "int" and self.type_name == "bool":
            return True
        return False


class TypeInferenceEngine(ast.NodeVisitor):
    """
    Walks an AST and infers variable types based on:
    - Literal assignments
    - Known function return types
    - Constructor calls
    """

    # Known return types for common stdlib functions
    KNOWN_RETURN_TYPES: Dict[str, str] = {
        "len": "int",
        "range": "range",
        "sum": "int",
        "sorted": "list",
        "str": "str",
        "int": "int",
        "float": "float",
        "bool": "bool",
        "list": "list",
        "dict": "dict",
        "set": "set",
        "tuple": "tuple",
        "type": "type",
        "input": "str",
        "abs": "int",
        "max": "Any",
        "min": "Any",
        "open": "file",
    }

    # Expected parameter types for common functions
    EXPECTED_PARAM_TYPES: Dict[str, Dict[str, str]] = {
        "builtins.range": {
            "start": "int", "stop": "int", "step": "int",
        },
        "builtins.sorted": {
            "reverse": "bool",
        },
        "builtins.list.sort": {
            "reverse": "bool",
        },
        "builtins.list.append": {},
        "builtins.open": {
            "mode": "str",  # but only specific string values
        },
        "math.sqrt": {
            "x": "non_negative_number",
        },
        "math.factorial": {
            "x": "non_negative_int",
        },
        "json.load": {
            "fp": "file_object",
        },
        "builtins.chr": {
            "i": "int",
        },
        "builtins.ord": {
            "c": "str",
        },
    }

    def __init__(self):
        self.variable_types: Dict[str, TypeInfo] = {}
        self.type_errors: list = []

    def infer(self, tree: ast.AST):
        """Run type inference on the AST."""
        self.visit(tree)
        return self.type_errors

    def visit_Assign(self, node):
        """Track types from assignments."""
        inferred = self._infer_expr_type(node.value)
        if inferred:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variable_types[target.id] = inferred
        self.generic_visit(node)

    def visit_Call(self, node):
        """Check argument types against expected parameter types."""
        func_key = self._get_func_key(node)
        if func_key and func_key in self.EXPECTED_PARAM_TYPES:
            expected_types = self.EXPECTED_PARAM_TYPES[func_key]
            self._check_kwargs(node, func_key, expected_types)
            self._check_positional_args(node, func_key, expected_types)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """Detect incompatible binary operations like str + int."""
        left = self._infer_expr_type(node.left)
        right = self._infer_expr_type(node.right)
        if left and right:
            l_t, r_t = left.type_name, right.type_name
            if isinstance(node.op, ast.Add):
                # str + int/float is TypeError (str * int is valid repetition)
                if (l_t == "str" and r_t in ("int", "float")) or \
                   (r_t == "str" and l_t in ("int", "float")):
                    self.type_errors.append({
                        "line": node.lineno,
                        "func": "operator.add",
                        "param": "operand",
                        "expected_type": "matching types",
                        "actual_type": f"{l_t} + {r_t}",
                        "actual_value": None,
                        "message": f"TypeError: unsupported operand type(s) for +: '{l_t}' and '{r_t}'",
                    })
            elif isinstance(node.op, (ast.Sub, ast.Div, ast.FloorDiv, ast.Mod)):
                # str cannot participate in arithmetic — BUT str % x is valid
                # (legacy string formatting), so skip Mod when left operand is str.
                if l_t == "str" and isinstance(node.op, ast.Mod):
                    pass  # str % x is valid formatting
                elif l_t == "str" or r_t == "str":
                    op_sym = {ast.Sub: '-', ast.Div: '/', ast.FloorDiv: '//', ast.Mod: '%'}
                    sym = op_sym.get(type(node.op), '?')
                    self.type_errors.append({
                        "line": node.lineno,
                        "func": f"operator({sym})",
                        "param": "operand",
                        "expected_type": "numeric",
                        "actual_type": f"{l_t}, {r_t}",
                        "actual_value": None,
                        "message": f"TypeError: unsupported operand type(s) for {sym}: '{l_t}' and '{r_t}'",
                    })
        self.generic_visit(node)

    def _get_func_key(self, node: ast.Call) -> Optional[str]:
        """Get a standardized function key like 'builtins.range' or 'math.sqrt'.
        Resolves variable types so arr.sort() -> builtins.list.sort."""
        if isinstance(node.func, ast.Name):
            return f"builtins.{node.func.id}"
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                var_name = node.func.value.id
                method = node.func.attr

                # Try to resolve variable type
                if var_name in self.variable_types:
                    var_type = self.variable_types[var_name].type_name
                    type_key = f"builtins.{var_type}.{method}"
                    if type_key in self.EXPECTED_PARAM_TYPES:
                        return type_key

                # Common implicit types (arr, lst, etc.)
                implicit_lists = {'arr', 'lst', 'items', 'numbers', 'values', 'elements', 'data_list'}
                if var_name in implicit_lists:
                    type_key = f"builtins.list.{method}"
                    if type_key in self.EXPECTED_PARAM_TYPES:
                        return type_key

                return f"{var_name}.{method}"
        return None

    def _check_kwargs(self, node: ast.Call, func_key: str, expected_types: Dict[str, str]):
        """Check that keyword argument values match expected types."""
        for kw in node.keywords:
            if kw.arg and kw.arg in expected_types:
                expected = expected_types[kw.arg]
                actual = self._infer_expr_type(kw.value)
                if actual and not self._is_type_match(actual, expected):
                    self.type_errors.append({
                        "line": node.lineno,
                        "func": func_key,
                        "param": kw.arg,
                        "expected_type": expected,
                        "actual_type": actual.type_name,
                        "actual_value": actual.value,
                        "message": f"TypeError: {func_key}() parameter '{kw.arg}' expects {expected}, got {actual.type_name} ({actual.value!r})"
                    })

    # Positional argument type constraints: func_key -> list of allowed types per position
    _POS_CONSTRAINTS: Dict[str, list] = {
        "builtins.range": [("int", "bool"), ("int", "bool"), ("int", "bool")],
        "builtins.chr":   [("int", "bool")],
        "builtins.ord":   [("str",)],
    }

    def _check_positional_args(self, node: ast.Call, func_key: str, expected_types: Dict[str, str]):
        """Check positional argument types against _POS_CONSTRAINTS."""
        constraints = self._POS_CONSTRAINTS.get(func_key)
        if not constraints:
            return
        for i, arg in enumerate(node.args):
            if i >= len(constraints):
                break
            actual = self._infer_expr_type(arg)
            if actual and actual.type_name not in constraints[i]:
                expected = "/".join(constraints[i])
                self.type_errors.append({
                    "line": node.lineno,
                    "func": func_key,
                    "param": f"arg{i}",
                    "expected_type": expected,
                    "actual_type": actual.type_name,
                    "actual_value": actual.value,
                    "message": f"TypeError: {func_key}() argument {i+1} expects {expected}, got {actual.type_name} ({actual.value!r})",
                })

    def _infer_expr_type(self, node: ast.expr) -> Optional[TypeInfo]:
        """Infer the type of an expression node."""
        if isinstance(node, ast.Constant):
            type_name = type(node.value).__name__
            return TypeInfo(type_name, node.value)
        elif isinstance(node, ast.List):
            return TypeInfo("list")
        elif isinstance(node, ast.Dict):
            return TypeInfo("dict")
        elif isinstance(node, ast.Set):
            return TypeInfo("set")
        elif isinstance(node, ast.Tuple):
            return TypeInfo("tuple")
        elif isinstance(node, ast.Name):
            if node.id in self.variable_types:
                return self.variable_types[node.id]
            # Check if it's a known builtin type
            if node.id in ('True', 'False'):
                return TypeInfo("bool", node.id == 'True')
            if node.id == 'None':
                return TypeInfo("NoneType", None)
        elif isinstance(node, ast.Call):
            func_name = None
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            if func_name and func_name in self.KNOWN_RETURN_TYPES:
                return TypeInfo(self.KNOWN_RETURN_TYPES[func_name])
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            inner = self._infer_expr_type(node.operand)
            if inner and inner.type_name in ("int", "float"):
                val = -inner.value if inner.value is not None else None
                return TypeInfo(inner.type_name, val)
        elif isinstance(node, ast.BinOp):
            left = self._infer_expr_type(node.left)
            right = self._infer_expr_type(node.right)
            if left and right:
                if left.type_name == "str" or right.type_name == "str":
                    return TypeInfo("str")
                if left.type_name == "float" or right.type_name == "float":
                    return TypeInfo("float")
                return TypeInfo("int")
        return None

    def _is_type_match(self, actual: TypeInfo, expected: str) -> bool:
        """Check if an actual type matches the expected type."""
        if expected == "bool":
            return actual.type_name == "bool"
        if expected == "int":
            return actual.type_name in ("int", "bool")
        if expected == "float":
            return actual.type_name in ("int", "float", "bool")
        if expected == "str":
            return actual.type_name == "str"
        if expected == "non_negative_number":
            if actual.type_name in ("int", "float") and actual.value is not None:
                return actual.value >= 0
            return True  # unknown value, can't check
        if expected == "non_negative_int":
            if actual.type_name == "int" and actual.value is not None:
                return actual.value >= 0
            return True
        if expected == "file_object":
            return actual.type_name != "str"  # string paths are wrong
        return True  # unknown expected type, pass


def run_type_inference(code: str, tree: 'ast.AST | None' = None) -> list:
    """
    Run type inference on a code string and return list of type errors found.
    Returns empty list if code has syntax errors.
    
    If a pre-parsed AST tree is provided, it is used directly
    to avoid redundant parsing.
    """
    if tree is None:
        try:
            tree = ast.parse(code)
        except Exception:
            return []
    engine = TypeInferenceEngine()
    return engine.infer(tree)
