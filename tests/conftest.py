"""Shared fixtures for the test suite."""
import os
import sys
import pytest

# Ensure project root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dataset import CodeSample
from src.ground_truth import GroundTruthRegistry


@pytest.fixture
def gt():
    """A GroundTruthRegistry instance with dynamic introspection enabled."""
    return GroundTruthRegistry(version="v1", use_dynamic=True)


@pytest.fixture
def sample_factory():
    """Factory fixture for creating CodeSample objects."""
    def _make(code: str, prompt: str = "Write a function.", sample_id: str = "test"):
        return CodeSample(id=sample_id, prompt=prompt, generated_code=code)
    return _make
