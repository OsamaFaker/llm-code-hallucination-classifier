"""Tests for the arity checker plugin."""
from src.arity_checker import ArityCheckerPlugin


def _check(code: str):
    """Helper: run ArityCheckerPlugin on a code string."""
    plugin = ArityCheckerPlugin()
    return plugin.check(code=code)


class TestBuiltinArity:
    """Test arity enforcement on builtin function calls."""

    def test_len_too_many_args(self):
        """len(a, b) has too many args."""
        result = _check("x = len([1,2], [3,4])")
        assert result is not None
        assert "too many" in result.explanation.lower()

    def test_len_valid(self):
        """len([1,2]) is valid."""
        result = _check("x = len([1,2])")
        assert result is None

    def test_range_with_string_arg(self):
        """range('10') is a type error."""
        result = _check("for i in range('10'): pass")
        assert result is not None

    def test_range_valid(self):
        """range(10) is valid."""
        result = _check("for i in range(10): pass")
        assert result is None

    def test_chr_with_string(self):
        """chr('65') is a type error."""
        result = _check("c = chr('65')")
        assert result is not None

    def test_chr_valid(self):
        """chr(65) is valid."""
        result = _check("c = chr(65)")
        assert result is None


class TestMethodArity:
    """Test arity enforcement on type-specific method calls."""

    def test_str_upper_with_arg(self):
        """str.upper() takes no arguments."""
        result = _check('s = "hello"\nresult = s.upper("en")')
        assert result is not None
        assert "too many" in result.explanation.lower() or "no arguments" in result.explanation.lower()

    def test_str_upper_valid(self):
        """str.upper() with no args is valid."""
        result = _check('s = "hello"\nresult = s.upper()')
        assert result is None

    def test_list_append_no_arg(self):
        """list.append() requires exactly 1 argument."""
        result = _check("lst = [1,2]\nlst.append()")
        assert result is not None
        assert "missing" in result.explanation.lower() or "requires" in result.explanation.lower()

    def test_list_append_valid(self):
        """list.append(x) is valid."""
        result = _check("lst = [1,2]\nlst.append(3)")
        assert result is None

    def test_str_replace_too_few(self):
        """str.replace() requires at least 2 args."""
        result = _check('s = "hello"\nresult = s.replace("h")')
        assert result is not None


class TestKwargTypes:
    """Test keyword argument type enforcement."""

    def test_sorted_key_as_string(self):
        """sorted(key='name') is a type error — key must be callable."""
        result = _check("sorted([3,1,2], key='name')")
        assert result is not None
        assert "callable" in result.explanation.lower()

    def test_sorted_key_valid(self):
        """sorted(key=len) is valid."""
        result = _check("sorted(['bb','a','ccc'], key=len)")
        assert result is None
