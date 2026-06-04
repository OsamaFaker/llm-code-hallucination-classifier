"""
Logic Checker Plugin.

Checks for fundamental grounded errors, such as infinite loops, dead branches,
static zero-division faults, None-return traps, unused pure-function returns,
and missing return statements using the ControlFlowAnalyzer and AST.
"""
import ast
from typing import Optional, Set
from src.models import ClassificationResult, SeverityLevel
from src.plugin_registry import CheckerPlugin
from src.control_flow import analyze_control_flow

# Methods that mutate in-place and always return None.
# Assigning their return value is always a bug.
_NONE_RETURNING_METHODS: frozenset = frozenset({
    "append", "extend", "insert", "remove", "sort", "reverse", "clear",
    "update", "add", "discard",
})

# Pure functions whose return value must be captured; calling them as a
# standalone statement (ast.Expr) is almost certainly a bug.
_PURE_RETURN_FUNCTIONS: frozenset = frozenset({
    "sorted", "reversed",
})


class LogicCheckerPlugin(CheckerPlugin):
    """Detects grounded errors (logic traps) using static analysis."""

    @property
    def name(self) -> str:
        return "logic"

    @property
    def priority(self) -> int:
        return 60  # Lower than hallucination but before default Valid

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        code = kwargs.get("code", "")
        ast_tree = kwargs.get("ast_tree")
        if not code:
            return None

        # 1. Use the pre-existing Control Flow analyzer
        cf_issues = analyze_control_flow(code, tree=ast_tree)
        
        # If we see medium or high severity structural flow issues, it is a rounded logic error
        for issue in cf_issues:
            if issue.severity in ("high", "medium"):
                return ClassificationResult(
                    is_valid=False,
                    is_grounded_error=True,
                    hallucination_category=None,
                    explanation=f"Logic Error [Control Flow]: {issue.message}",
                    confidence=0.90,
                    severity=SeverityLevel.HIGH,
                    checker_source="logic",
                    line=issue.line if hasattr(issue, 'line') else 'multiple',
                    bad_token=''
                )

        # 2. AST-based heuristics
        if ast_tree is None:
            try:
                ast_tree = ast.parse(code)
            except Exception:
                return None
        tree = ast_tree

        for node in ast.walk(tree):
            # 2a. Static division by zero
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                if isinstance(node.right, ast.Constant) and node.right.value == 0:
                    return ClassificationResult(
                        is_valid=False,
                        is_grounded_error=True,
                        hallucination_category=None,
                        explanation="Logic Error [Math]: Static division by zero detected.",
                        confidence=1.0,
                        severity=SeverityLevel.CRITICAL,
                        checker_source="logic",
                        line=node.lineno,
                        bad_token='/'
                    )

            # 2b. None-return trap: e.g. lst = lst.append(x)
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Attribute):
                    if call.func.attr in _NONE_RETURNING_METHODS:
                        method = call.func.attr
                        return ClassificationResult(
                            is_valid=False,
                            is_grounded_error=True,
                            hallucination_category=None,
                            explanation=(
                                f"Logic Error [None-Return]: '{method}()' mutates in-place "
                                f"and returns None — assigning its result is always a bug."
                            ),
                            confidence=0.95,
                            severity=SeverityLevel.HIGH,
                            checker_source="logic",
                            line=node.lineno,
                            bad_token=method
                        )

            # 2c. Unused pure-function return: e.g. sorted(lst) as statement
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Name) and call.func.id in _PURE_RETURN_FUNCTIONS:
                    fname = call.func.id
                    return ClassificationResult(
                        is_valid=False,
                        is_grounded_error=True,
                        hallucination_category=None,
                        explanation=(
                            f"Logic Error [Unused Return]: '{fname}()' returns a new "
                            f"value but the result is not captured — the call has no effect."
                        ),
                        confidence=0.93,
                        severity=SeverityLevel.MEDIUM,
                        checker_source="logic",
                    )

        # 3. Missing return in non-void functions
        result = _check_missing_return(tree)
        if result:
            return result

        return None


def _check_missing_return(tree: ast.AST) -> Optional[ClassificationResult]:
    """
    Detect functions that have at least one 'return <value>' but whose
    last top-level statement is NOT a return — indicating a fall-through path.
    """
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.body:
            continue

        # Check if the function has any return-with-value
        has_value_return = False
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, ast.Return) and child.value is not None:
                has_value_return = True
                break

        if not has_value_return:
            continue

        # Check if the last statement is a return (or if/try that ends with returns)
        last = node.body[-1]
        if isinstance(last, ast.Return):
            continue
        if isinstance(last, ast.If) and last.orelse:
            # Both branches end with return → OK
            if (_ends_with_return(last.body) and _ends_with_return(last.orelse)):
                continue

        return ClassificationResult(
            is_valid=False,
            is_grounded_error=True,
            hallucination_category=None,
            explanation=(
                f"Logic Error [Missing Return]: Function '{node.name}' has a return "
                f"statement on some paths but falls through without returning on others."
            ),
            confidence=0.88,
            severity=SeverityLevel.MEDIUM,
            checker_source="logic",
        )

    return None


def _ends_with_return(body: list) -> bool:
    """Check if the last statement of a body is a Return."""
    if not body:
        return False
    last = body[-1]
    if isinstance(last, ast.Return):
        return True
    if isinstance(last, ast.If) and last.orelse:
        return _ends_with_return(last.body) and _ends_with_return(last.orelse)
    return False
