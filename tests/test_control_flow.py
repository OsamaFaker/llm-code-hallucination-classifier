"""Tests for the control flow analyzer."""
from src.control_flow import analyze_control_flow


def _check(code: str):
    return analyze_control_flow(code)


class TestControlFlow:
    """Test control flow analysis for unreachable code, infinite loops, and dead branches."""

    def test_unreachable_code_after_return(self):
        code = """
def func():
    return 1
    print("unreachable")
"""
        issues = _check(code)
        assert len(issues) == 1
        assert issues[0].issue_type == "unreachable_code"

    def test_infinite_loop(self):
        code = """
while True:
    print("infinite")
"""
        issues = _check(code)
        assert len(issues) == 1
        assert issues[0].issue_type == "infinite_loop"

    def test_loop_with_break_is_valid(self):
        code = """
while True:
    if condition:
        break
"""
        issues = _check(code)
        assert len(issues) == 0

    def test_dead_branch_if_false(self):
        code = """
if False:
    print("dead")
"""
        issues = _check(code)
        assert len(issues) == 1
        assert issues[0].issue_type == "dead_branch"

    def test_empty_except(self):
        code = """
try:
    x = 1 / 0
except:
    pass
"""
        issues = _check(code)
        assert len(issues) > 0
        assert any(i.issue_type == "empty_except" for i in issues)
