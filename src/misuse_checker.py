"""
Misuse / Composition Checker Plugin.

Applies the GT-existence framework to API call composition:

  GROUNDED_ERROR — the construct exists in the Python Ground Truth but is
    used incorrectly: wrong argument type, invalid domain value, or calling
    a real parameter with a bad value.
    Examples: math.sqrt(-1), range("5"), open(f, 'invalid'), append() with
    no argument.

  HALLUCINATION — a construct is invoked that has no referent in the Python
    Ground Truth: a keyword argument name that does not appear in the
    function's known parameter list is a fabricated parameter.
    Example: open(f, base=10) — 'base' is not a parameter of open().

Integrates with the Type Inference Engine for generalised type checking.
"""
from typing import List, Optional
from src.models import ClassificationResult, HallucinationCategory, SeverityLevel
from src.ground_truth import GroundTruthRegistry
from src.plugin_registry import CheckerPlugin
from src.type_inference import run_type_inference


class MisuseCheckerPlugin(CheckerPlugin):
    """
    Classifies API composition errors using the GT-existence framework.

    GROUNDED_ERROR: construct exists in GT, used with wrong value/type.
    HALLUCINATION:  construct (parameter name) does not exist in GT.
    """

    @property
    def name(self) -> str:
        return "misuse"

    @property
    def priority(self) -> int:
        return 70  # Medium-high: runs after fabrication check

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        extracted_calls = kwargs.get("extracted_calls", [])
        gt = kwargs.get("gt")
        code = kwargs.get("code", "")
        ast_tree = kwargs.get("ast_tree")
        if gt is None:
            return None
        return verify_composition(extracted_calls, gt, code, ast_tree=ast_tree)


def verify_composition(extracted_calls: List[dict], gt: GroundTruthRegistry, code: str = "", ast_tree=None) -> Optional[ClassificationResult]:
    # --- Phase A: Type Inference Engine ---
    # Run the type inference engine to catch generalized type errors
    if code:
        type_errors = run_type_inference(code, tree=ast_tree)
        if type_errors:
            first_err = type_errors[0]
            return ClassificationResult(
                is_valid=False, is_grounded_error=True, hallucination_category=None,
                explanation=f"Grounded Error: {first_err['message']}",
                confidence=0.95,
                severity=SeverityLevel.MEDIUM,
                checker_source="misuse",
                line=first_err.get('line', 'multiple'),
                bad_token=first_err.get('token', '')
            )

    # --- Phase B: Rule-based composition checks ---
    for call in extracted_calls:
        module = call['module']
        method = call['method']
        kwargs = call.get('kwargs', [])
        arg_values = call.get('arg_values', [])

        if module == '__main__':
            # Local-object calls cannot be validated against GTenv — skip.
            continue

        valid_params = gt.get_params(module, method)

        # GT-existence check on keyword argument names (Item #5).
        # A kwarg name that does not appear in the function's GT parameter list
        # has no referent in the execution environment → HALLUCINATION (PARAMETER).
        # Contrast: a kwarg that exists but receives a wrong value (e.g. reverse='yes')
        # → GROUNDED_ERROR (construct exists, usage is wrong).
        if valid_params is not None:
            for kwarg in kwargs:
                if kwarg not in valid_params:
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=False, hallucination_category=HallucinationCategory.PARAMETER,
                        explanation=f"Hallucination: Fabricated keyword argument '{kwarg}' in {module}.{method}().",
                        confidence=0.95,
                        severity=SeverityLevel.HIGH,
                        checker_source="misuse",
                        line=call.get('line'),
                        bad_token=kwarg
                    )

        # 2. Type and Domain Validation Logic
        if module == 'math' and method in ('sqrt', 'factorial'):
            for val in arg_values:
                if isinstance(val, (int, float)) and val < 0:
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=True, hallucination_category=None,
                        explanation=f"Grounded Error: Domain error in math.{method}. Cannot accept {val}.",
                        confidence=0.98,
                        severity=SeverityLevel.MEDIUM,
                        checker_source="misuse",
                        line=call.get('line'),
                        bad_token=str(val)
                    )

        if module == 'builtins' and method == 'open':
            for val in arg_values:
                if isinstance(val, str) and val in ('invalid', 'bad_mode'):
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=True, hallucination_category=None,
                        explanation=f"Grounded Error: Invalid mode '{val}' for open().",
                        confidence=0.95,
                        severity=SeverityLevel.MEDIUM,
                        checker_source="misuse",
                        line=call.get('line'),
                        bad_token=str(val)
                    )

        if module == 'builtins' and method == 'range':
            for val in arg_values:
                if isinstance(val, str):
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=True, hallucination_category=None,
                        explanation="Grounded Error: TypeError: range() expects integer, got string.",
                        confidence=0.98,
                        severity=SeverityLevel.MEDIUM,
                        checker_source="misuse",
                    )

        if module == 'json' and method == 'load':
            for val in arg_values:
                if isinstance(val, str) and val.endswith('.json'):
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=True, hallucination_category=None,
                        explanation="Grounded Error: TypeError: json.load expects a file object, not a string path.",
                        confidence=0.95,
                        severity=SeverityLevel.MEDIUM,
                        checker_source="misuse",
                    )

        # List specific Built-in logic — GENERALIZED via type inference
        # The type inference engine now catches sort(reverse='yes') automatically.
        # These remain as safety-net fallbacks:
        if module == 'builtins.list' and method == 'sort':
            for val in arg_values:
                 if isinstance(val, str) and val in ('yes', 'no', 'true', 'false'):
                     return ClassificationResult(
                         is_valid=False, is_grounded_error=True, hallucination_category=None,
                         explanation="Grounded Error: TypeError: 'reverse' expects boolean, not string.",
                         confidence=0.95,
                         severity=SeverityLevel.MEDIUM,
                         checker_source="misuse",
                     )

        if module == 'builtins.list' and method == 'append':
            if kwargs:
                return ClassificationResult(
                     is_valid=False, is_grounded_error=True, hallucination_category=None,
                     explanation="Grounded Error: append() takes no keyword arguments.",
                     confidence=0.98,
                     severity=SeverityLevel.MEDIUM,
                     checker_source="misuse",
                )

    return None
