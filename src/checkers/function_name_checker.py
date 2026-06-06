"""
Function Name Mismatch Checker.

Extracts the expected function name from the prompt and compares it against
all top-level function definitions in the generated code.  Flags cases where
the model defined a function with a different name than the one requested —
a real class of hallucination (semantic drift in naming) that static API
checks cannot catch.

Strategy
--------
1. Parse the prompt for explicit function-name signals:
   - Backtick-quoted identifiers:  `function_name`
   - "called X" / "named X" / "implement X" / "Write X"
   - Inline signature hints:  def X( or X(args)
2. Walk the AST to collect all top-level `def` names.
3. If a candidate expected name is found and no defined function is within
   edit-distance 3 of it, flag as SEMANTIC hallucination.

Confidence is intentionally capped at 0.82 — prompts can be ambiguous and
helper functions are always OK to rename.
"""
import ast
import re
from typing import Optional, List

from src.models import ClassificationResult, HallucinationCategory, SeverityLevel
from src.plugin_registry import CheckerPlugin


# Regex patterns to extract a Python-identifier-shaped function name from a prompt.
_BACKTICK_RE = re.compile(r'`([a-z_][a-z0-9_]*)`')
_CALLED_RE   = re.compile(r'\b(?:called|named|function|implement|write|create)\s+`?([a-z_][a-z0-9_]*)`?', re.IGNORECASE)
_DEF_RE      = re.compile(r'\bdef\s+([a-z_][a-z0-9_]*)\s*\(')
_SIGNATURE_RE = re.compile(r'\b([a-z_][a-z0-9_]*)\s*\([^)]*\)\s*(?:->|:|-|that|which|to\b)', re.IGNORECASE)


def _extract_expected_names(prompt: str) -> List[str]:
    """Return candidate expected function names from the prompt, ordered by signal strength."""
    seen: dict = {}

    def _add(name: str, priority: int):
        if name and len(name) > 2 and name not in seen:
            seen[name] = priority

    for m in _BACKTICK_RE.finditer(prompt):
        _add(m.group(1), 1)
    for m in _DEF_RE.finditer(prompt):
        _add(m.group(1), 2)
    for m in _CALLED_RE.finditer(prompt):
        _add(m.group(1), 3)
    for m in _SIGNATURE_RE.finditer(prompt):
        _add(m.group(1), 4)

    return sorted(seen, key=lambda n: seen[n])


def _top_level_def_names(tree: ast.AST) -> List[str]:
    """Return all top-level function/async-function names from the AST."""
    names = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
    return names


def _edit_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        return _edit_distance(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for ca in a:
        curr = [prev[0] + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j] + (ca != cb), curr[-1] + 1, prev[j + 1] + 1))
        prev = curr
    return prev[-1]


def _best_match_distance(expected: str, candidates: List[str]) -> int:
    """Return the minimum edit distance between expected and any candidate."""
    if not candidates:
        return len(expected)
    return min(_edit_distance(expected, c) for c in candidates)


class FunctionNameCheckerPlugin(CheckerPlugin):
    """Detects function-name mismatches between the prompt and the generated code."""

    @property
    def name(self) -> str:
        return "function_name"

    @property
    def priority(self) -> int:
        return 65

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        prompt: str = kwargs.get("prompt") or ""
        tree = kwargs.get("ast_tree")
        if not prompt or tree is None:
            return None

        expected_names = _extract_expected_names(prompt)
        if not expected_names:
            return None

        defined_names = _top_level_def_names(tree)
        if not defined_names:
            return None

        # Use the highest-priority (lowest priority number) expected name.
        primary_expected = expected_names[0]

        dist = _best_match_distance(primary_expected, defined_names)

        # Threshold: edit distance > 3 on names longer than 4 chars → mismatch.
        # Shorter names tolerate less distance.
        threshold = 3 if len(primary_expected) > 4 else 2
        if dist > threshold:
            defined_str = ", ".join(f"`{n}`" for n in defined_names)
            return ClassificationResult(
                is_valid=False,
                is_grounded_error=False,
                hallucination_category=HallucinationCategory.SEMANTIC,
                explanation=(
                    f"Function name mismatch: prompt expects `{primary_expected}` "
                    f"but code defines {defined_str} "
                    f"(closest edit distance: {dist})."
                ),
                confidence=0.82,
                severity=SeverityLevel.HIGH,
                checker_source="function_name",
                bad_token=defined_names[0],
            )
        return None
