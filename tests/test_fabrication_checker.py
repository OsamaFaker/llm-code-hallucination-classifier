"""Tests for the fabrication checker plugin."""
from src.fabrication_checker import FabricationCheckerPlugin, verify_fabrication
from src.ground_truth import GroundTruthRegistry


def _make_gt():
    return GroundTruthRegistry(version="v1", use_dynamic=True)


class TestFabricationChecker:
    """Test fabrication detection for modules, functions, and env vars."""

    def test_fabricated_module_flagged(self):
        """A known-fabricated module name like 'utils' should be caught."""
        imports = [{"module": "utils", "line": 1}]
        result = verify_fabrication([], imports, set(), _make_gt())
        assert result is not None
        assert not result.is_valid
        assert "LIBRARY" in result.hallucination_category.name

    def test_real_module_passes(self):
        """A real stdlib module like 'math' should not be flagged."""
        imports = [{"module": "math", "line": 1}]
        calls = [{"module": "math", "method": "sqrt", "kwargs": [], "arg_values": [4], "line": 2}]
        result = verify_fabrication(calls, imports, set(), _make_gt())
        assert result is None

    def test_fabricated_function_on_known_module(self):
        """A non-existent function on a known module should be flagged."""
        imports = [{"module": "math", "line": 1}]
        calls = [{"module": "math", "method": "nonexistent_func", "kwargs": [], "arg_values": [], "line": 2}]
        result = verify_fabrication(calls, imports, set(), _make_gt())
        assert result is not None
        assert "FUNCTION" in result.hallucination_category.name

    def test_local_function_not_flagged(self):
        """A call to a locally defined function should not be flagged."""
        calls = [{"module": "__main__", "method": "my_helper", "kwargs": [], "arg_values": [], "line": 5}]
        local_vars = {"my_helper"}
        result = verify_fabrication(calls, [], local_vars, _make_gt())
        assert result is None

    def test_builtin_function_not_flagged(self):
        """Built-in functions called as free functions should not be flagged."""
        calls = [{"module": "builtins", "method": "len", "kwargs": [], "arg_values": [], "line": 1}]
        result = verify_fabrication(calls, [], set(), _make_gt())
        assert result is None

    def test_fabricated_env_var_flagged(self):
        """An unknown env var should be flagged."""
        calls = [{"module": "os", "method": "getenv", "kwargs": [], "arg_values": ["TOTALLY_FAKE_VAR"], "line": 1}]
        result = verify_fabrication(calls, [], set(), _make_gt())
        assert result is not None
        assert "ENV_VAR" in result.hallucination_category.name

    def test_valid_env_var_passes(self):
        """A known env var like PATH should not be flagged."""
        calls = [{"module": "os", "method": "getenv", "kwargs": [], "arg_values": ["PATH"], "line": 1}]
        result = verify_fabrication(calls, [], set(), _make_gt())
        assert result is None

    def test_object_method_on_local_var_not_flagged(self):
        """A known object method called on a local variable should pass."""
        calls = [{"module": "__main__", "method": "append", "kwargs": [], "arg_values": [], "line": 3}]
        result = verify_fabrication(calls, [], set(), _make_gt())
        assert result is None  # 'append' is in KNOWN_OBJECT_METHODS

    def test_helpers_module_fabricated(self):
        """The 'helpers' module should be caught as fabricated."""
        imports = [{"module": "helpers", "line": 1}]
        result = verify_fabrication([], imports, set(), _make_gt())
        assert result is not None
        assert "LIBRARY" in result.hallucination_category.name
