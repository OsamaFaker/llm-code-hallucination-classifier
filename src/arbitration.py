from typing import Tuple, Optional

# Minimum verifier confidence required to override a static-clean sample.
# Below this threshold, a "NO" verdict from the verifier is treated as
# uncertain and defaults to VALID rather than triggering HALLUCINATION.
# Calibrated from the v5→v6 audit: all 31 disagreements were low-confidence
# verifier rejections of genuinely valid code.
MIN_VERIFIER_CONFIDENCE = 0.7


def arbitrate(
    static_verdict: str,
    static_confidence: float,
    attempts_task: str,
    verifier_confidence: float,
    min_verifier_confidence: float = MIN_VERIFIER_CONFIDENCE,
) -> Tuple[str, Optional[str], float]:
    """
    Arbitrates between the static pipeline verdict and the LLM verifier's intent-alignment verdict.
    
    Parameters
    ----------
    min_verifier_confidence : float
        Minimum confidence the verifier must have for a "NO" verdict to
        override the static funnel.  Below this threshold the sample is
        kept as VALID (fail-safe).

    Returns
    -------
    (final_label, taxonomy_tag, combined_confidence)
    """
    if static_verdict == "HALLUCINATION":
        # Static evidence of fabrication is authoritative; verifier cannot rescue.
        return "HALLUCINATION", None, static_confidence
        
    if static_verdict == "GROUNDED_ERROR":
        # Misuse of real constructs is authoritative; verifier cannot upgrade to hallucination.
        return "GROUNDED_ERROR", None, static_confidence
        
    # No static verdict (code passed the funnel)
    if attempts_task == "YES":
        # Static-clean and intent-aligned.
        return "VALID", None, static_confidence
        
    if attempts_task == "NO":
        # Only path by which the verifier can assign a hallucination label.
        # Gate: require minimum verifier confidence to override.
        if verifier_confidence >= min_verifier_confidence:
            return "HALLUCINATION", "semantic_fabrication", min(static_confidence, verifier_confidence)
        # Low-confidence rejection — default to VALID (fail-safe).
        return "VALID", "low_confidence_no", min(static_confidence, verifier_confidence)
        
    # Fallback for unexpected attempts_task values
    return "VALID", None, static_confidence
