"""Tests for the logic checker plugin."""
from src.logic_checker import LogicCheckerPlugin


def _check(code: str):
    """Helper: run LogicCheckerPlugin on a code string."""
    plugin = LogicCheckerPlugin()
    return plugin.check(code=code)


class TestLogicChecker:
    """Test AST-based heuristics for grounded logic errors."""

    def test_static_division_by_zero(self):
        """x = 10 / 0 should be caught."""
        result = _check("x = 10 / 0")
        assert result is not None
        assert "division by zero" in result.explanation.lower()

    def test_none_return_trap(self):
        """lst = lst.append(x) should be caught."""
        result = _check("lst = [1, 2]\nlst = lst.append(3)")
        assert result is not None
        assert "returns none" in result.explanation.lower()

    def test_unused_pure_function(self):
        """sorted(lst) as an expression should be caught."""
        result = _check("lst = [3, 1, 2]\nsorted(lst)\nreturn lst")
        assert result is not None
        assert "not captured" in result.explanation.lower()

    def test_missing_return(self):
        """Function with return on some paths but not all."""
        code = """
def get_val(x):
    if x > 0:
        return x
    # missing return on else path
"""
        result = _check(code)
        assert result is not None
        assert "falls through" in result.explanation.lower()

    def test_valid_logic_passes(self):
        """Valid logic should pass."""
        code = """
def get_val(x):
    if x > 0:
        return x
    return 0
"""
        result = _check(code)
        assert result is None
