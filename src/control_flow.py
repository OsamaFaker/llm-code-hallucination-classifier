"""
Control Flow Analysis for hallucination detection.

Builds a basic control flow graph from the AST to detect:
- Unreachable code after return/break/continue
- Infinite loops without break conditions
- Empty exception handlers (bare except: pass)
- Dead code branches
"""
import ast
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ControlFlowIssue:
    """Represents a control flow anomaly detected in the code."""
    issue_type: str     # 'unreachable_code', 'infinite_loop', 'empty_except', 'dead_branch'
    line: int
    message: str
    severity: str = "medium"  # low, medium, high


class ControlFlowAnalyzer(ast.NodeVisitor):
    """
    Analyzes the control flow of generated code to detect patterns
    that may indicate hallucination or buggy generation.
    """

    def __init__(self):
        self.issues: List[ControlFlowIssue] = []

    def analyze(self, code: str, tree: 'ast.AST | None' = None) -> List[ControlFlowIssue]:
        """Parse and analyze control flow of the given code.
        
        If a pre-parsed AST tree is provided, it is used directly
        to avoid redundant parsing.
        """
        if tree is None:
            try:
                tree = ast.parse(code)
            except Exception:
                return []
        self.visit(tree)
        return self.issues

    def visit_FunctionDef(self, node):
        """Check for unreachable code after return statements within functions."""
        self._check_unreachable_in_body(node.body, context="function")
        self.generic_visit(node)

    def visit_For(self, node):
        """Check for issues in for loops."""
        self._check_unreachable_in_body(node.body, context="for-loop")
        self.generic_visit(node)

    def visit_While(self, node):
        """Check for infinite loops (while True without break)."""
        if self._is_constant_true(node.test):
            has_break = self._contains_break(node)
            if not has_break:
                self.issues.append(ControlFlowIssue(
                    issue_type="infinite_loop",
                    line=node.lineno,
                    message="Infinite loop: 'while True' without any break/return statement.",
                    severity="high",
                ))
        self._check_unreachable_in_body(node.body, context="while-loop")
        self.generic_visit(node)

    def visit_Try(self, node):
        """Check for empty exception handlers (bare except: pass)."""
        for handler in node.handlers:
            if self._is_empty_handler(handler):
                self.issues.append(ControlFlowIssue(
                    issue_type="empty_except",
                    line=handler.lineno,
                    message="Empty exception handler: catches exception but does nothing (bare 'except: pass').",
                    severity="medium",
                ))
            # Bare except without type
            if handler.type is None and not self._is_empty_handler(handler):
                self.issues.append(ControlFlowIssue(
                    issue_type="broad_except",
                    line=handler.lineno,
                    message="Bare 'except:' clause catches all exceptions including SystemExit and KeyboardInterrupt.",
                    severity="low",
                ))
        self.generic_visit(node)

    def visit_If(self, node):
        """Check for dead branches (if False / if True with else)."""
        if self._is_constant_false(node.test):
            self.issues.append(ControlFlowIssue(
                issue_type="dead_branch",
                line=node.lineno,
                message="Dead branch: 'if False' — the body will never execute.",
                severity="medium",
            ))
        elif self._is_constant_true(node.test) and node.orelse:
            self.issues.append(ControlFlowIssue(
                issue_type="dead_branch",
                line=node.lineno,
                message="Dead branch: 'if True' with else — the else block will never execute.",
                severity="low",
            ))
        self.generic_visit(node)

    # -----------------------------------------------------------------
    # Helper methods
    # -----------------------------------------------------------------
    def _check_unreachable_in_body(self, body: list, context: str):
        """Check for statements after return/break/continue in a body."""
        for i, stmt in enumerate(body):
            if isinstance(stmt, (ast.Return, ast.Break, ast.Continue)):
                remaining = body[i + 1:]
                if remaining:
                    kind = type(stmt).__name__.lower()
                    self.issues.append(ControlFlowIssue(
                        issue_type="unreachable_code",
                        line=remaining[0].lineno,
                        message=f"Unreachable code after '{kind}' in {context} at line {stmt.lineno}.",
                        severity="medium",
                    ))
                break  # Only report first unreachable block

    def _is_constant_true(self, node) -> bool:
        if isinstance(node, ast.Constant):
            return bool(node.value)
        if hasattr(ast, "NameConstant") and isinstance(node, getattr(ast, "NameConstant")):  # Python 3.7 compat
            return node.value is True
        return False

    def _is_constant_false(self, node) -> bool:
        if isinstance(node, ast.Constant):
            return node.value is False or node.value == 0
        if hasattr(ast, "NameConstant") and isinstance(node, getattr(ast, "NameConstant")):
            return node.value is False
        return False

    def _contains_break(self, node) -> bool:
        """Check if a loop body contains a break or return statement."""
        for child in ast.walk(node):
            if isinstance(child, (ast.Break, ast.Return)):
                return True
        return False

    def _is_empty_handler(self, handler: ast.ExceptHandler) -> bool:
        """Check if an except handler is empty (just pass or ...)."""
        if len(handler.body) == 1:
            stmt = handler.body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                if stmt.value.value is Ellipsis:
                    return True
        return False


def analyze_control_flow(code: str, tree: 'ast.AST | None' = None) -> List[ControlFlowIssue]:
    """
    Analyze control flow of a code string.
    Returns list of issues found — empty list means no issues.
    
    If a pre-parsed AST tree is provided, it is used directly
    to avoid redundant parsing.
    """
    analyzer = ControlFlowAnalyzer()
    return analyzer.analyze(code, tree=tree)
