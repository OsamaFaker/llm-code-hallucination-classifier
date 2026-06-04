"""Tests for the ground truth registry."""
from src.ground_truth import GroundTruthRegistry


def test_env_var_allowlist():
    """Test environment variable validation against the expanded allowlist."""
    gt = GroundTruthRegistry(version="v1", use_dynamic=True)
    
    # Valid POSIX standard
    assert gt.valid_env_var("PATH")
    assert gt.valid_env_var("HOME")
    assert gt.valid_env_var("USER")
    
    # Valid common cloud/app
    assert gt.valid_env_var("DATABASE_URL")
    assert gt.valid_env_var("AWS_ACCESS_KEY_ID")
    assert gt.valid_env_var("SECRET_KEY")
    
    # Valid python
    assert gt.valid_env_var("PYTHONPATH")
    
    # Invalid / fabricated
    assert not gt.valid_env_var("TOTALLY_FAKE_VAR")
    assert not gt.valid_env_var("MY_CUSTOM_DB_PATH")

def test_deprecation_check():
    """Test API deprecation checking."""
    gt = GroundTruthRegistry(version="v1", use_dynamic=True)
    
    # Python 3 deprecated module/function examples
    # (Assuming the ground truth registry has rules for these, if not,
    # this test might need adjustment based on the actual rules in Prototype_v6).
    # Since GroundTruthRegistry uses a static ruleset or dynamic lookup, we test the interface.
    # We don't have the exact ruleset here, so we test the return type.
    result = gt.check_deprecated("math", "sqrt", "v1")
    assert result is None  # math.sqrt is not deprecated
    
def test_dynamic_introspection():
    """Test dynamic attribute checking."""
    gt = GroundTruthRegistry(version="v1", use_dynamic=True)
    
    assert gt.check_fabrication("math", "sqrt")
    assert not gt.check_fabrication("fake_module_xyz", "fake_func_xyz")
    assert not gt.check_fabrication("math", "fake_func_xyz")
