"""
Type Checker Plugin.

Wraps the existing TypeInferenceEngine to surface parameter type mismatches
and cross-type arithmetic errors as GROUNDED_ERROR classifications.

Examples caught:
  range('10')          → range() arg must be int, got str
  sorted(reverse='no') → reverse= expects bool, got str
  'hello' + 1          → unsupported operand types for +: str and int

These are real Python constructs used incorrectly — GROUNDED_ERROR by the
GT-existence framework — not hallucinations.
"""
from typing import Optional

from src.models import ClassificationResult, SeverityLevel
from src.plugin_registry import CheckerPlugin
from src.type_inference import run_type_inference


class TypeCheckerPlugin(CheckerPlugin):
    """Detects parameter type mismatches and cross-type arithmetic errors."""

    @property
    def name(self) -> str:
        return "type_check"

    @property
    def priority(self) -> int:
        return 68

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        code: str = kwargs.get("code", "")
        tree = kwargs.get("ast_tree")
        if not code:
            return None

        errors = run_type_inference(code, tree=tree)
        if not errors:
            return None

        # Report the first (highest-confidence) type error found.
        err = errors[0]
        return ClassificationResult(
            is_valid=False,
            is_grounded_error=True,
            hallucination_category=None,
            explanation=f"Grounded Error [Type Mismatch]: {err['message']}",
            confidence=0.88,
            severity=SeverityLevel.MEDIUM,
            checker_source="type_check",
            line=err.get("line"),
            bad_token=err.get("param"),
        )
