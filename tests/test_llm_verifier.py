"""Tests for the LLM Verifier."""
import os
import pytest
from src.llm_verifier import LLMVerifier


@pytest.fixture
def verifier():
    # Set dummy env vars so we can instantiate without errors
    os.environ["LLM_PROVIDER"] = "gemini"
    os.environ["LLM_API_KEY"] = "dummy"
    return LLMVerifier()


class TestLLMVerifierParsing:
    """Test JSON response parsing logic in LLMVerifier."""

    def test_valid_json_parsed(self, verifier):
        """Valid JSON response should be parsed correctly."""
        response = '{"attempts_task": "YES", "confidence": 0.95}'
        parsed = verifier._parse_response(response)
        assert parsed["attempts_task"] == "YES"
        assert parsed["confidence"] == 0.95

    def test_json_in_markdown_block(self, verifier):
        """JSON enclosed in markdown code blocks should be extracted and parsed."""
        response = "```json\n{\"attempts_task\": \"NO\", \"confidence\": 0.8}\n```"
        parsed = verifier._parse_response(response)
        assert parsed["attempts_task"] == "NO"
        assert parsed["confidence"] == 0.8

    def test_malformed_json_fallback(self, verifier):
        """Malformed JSON should fallback to safe defaults."""
        response = '{"attempts_task": "YES", "confidence": "high"}'  # invalid confidence type
        parsed = verifier._parse_response(response)
        assert "attempts_task" in parsed
        assert "confidence" in parsed

    def test_non_json_response(self, verifier):
        """Response without JSON should fallback."""
        response = "The code attempts the task."
        parsed = verifier._parse_response(response)
        assert parsed["attempts_task"] == "YES"  # Default fallback
        assert parsed["confidence"] == 0.0   # Default fallback
