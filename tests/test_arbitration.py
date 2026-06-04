"""Tests for the arbitration table — all input combinations."""
from src.arbitration import arbitrate, MIN_VERIFIER_CONFIDENCE


class TestArbitrate:
    """Test all branches of the arbitration function."""

    def test_static_hallucination_cannot_be_rescued(self):
        """Static HALLUCINATION is authoritative regardless of verifier."""
        label, tag, conf = arbitrate("HALLUCINATION", 0.90, "YES", 0.95)
        assert label == "HALLUCINATION"
        assert conf == 0.90

    def test_static_grounded_error_is_authoritative(self):
        """Static GROUNDED_ERROR cannot be reclassified."""
        label, tag, conf = arbitrate("GROUNDED_ERROR", 0.95, "YES", 0.80)
        assert label == "GROUNDED_ERROR"
        assert conf == 0.95

    def test_valid_with_verifier_yes(self):
        """Static VALID + verifier YES = VALID."""
        label, tag, conf = arbitrate("VALID", 1.0, "YES", 0.90)
        assert label == "VALID"
        assert tag is None

    def test_valid_with_verifier_no_high_confidence(self):
        """Static VALID + verifier NO (high confidence) = HALLUCINATION."""
        label, tag, conf = arbitrate("VALID", 1.0, "NO", 0.85)
        assert label == "HALLUCINATION"
        assert tag == "semantic_fabrication"
        assert conf == 0.85  # min(1.0, 0.85)

    def test_valid_with_verifier_no_low_confidence(self):
        """Static VALID + verifier NO (low confidence) = VALID (fail-safe)."""
        label, tag, conf = arbitrate("VALID", 1.0, "NO", 0.50)
        assert label == "VALID"
        assert tag == "low_confidence_no"

    def test_valid_with_verifier_no_at_threshold(self):
        """At exactly the threshold, should trigger HALLUCINATION."""
        label, tag, conf = arbitrate("VALID", 1.0, "NO", MIN_VERIFIER_CONFIDENCE)
        assert label == "HALLUCINATION"
        assert tag == "semantic_fabrication"

    def test_valid_with_verifier_no_just_below_threshold(self):
        """Just below the threshold, should stay VALID."""
        label, tag, conf = arbitrate("VALID", 1.0, "NO", MIN_VERIFIER_CONFIDENCE - 0.01)
        assert label == "VALID"

    def test_valid_with_verifier_not_run(self):
        """Static VALID + verifier NOT_RUN = VALID (fallback)."""
        label, tag, conf = arbitrate("VALID", 1.0, "NOT_RUN", 1.0)
        assert label == "VALID"

    def test_custom_threshold(self):
        """Custom min_verifier_confidence overrides default."""
        # With threshold 0.9, confidence 0.85 is below -> VALID
        label, _, _ = arbitrate("VALID", 1.0, "NO", 0.85, min_verifier_confidence=0.9)
        assert label == "VALID"
        # With threshold 0.5, confidence 0.85 is above -> HALLUCINATION
        label, _, _ = arbitrate("VALID", 1.0, "NO", 0.85, min_verifier_confidence=0.5)
        assert label == "HALLUCINATION"
