"""
Semantic Checker Plugin — Code-Aware Embedding Similarity.

Detects semantic hallucinations where code is syntactically valid
but doesn't match the user's intent. Uses code-aware embedding models
that understand both natural language and programming language structure.

Model preference order:
    1. microsoft/unixcoder-base   — trained for code search & similarity
    2. microsoft/codebert-base    — pre-trained on NL-code bimodal data
    3. all-MiniLM-L6-v2           — generic text fallback (sentence-transformers)
"""
import math
from typing import Optional
from src.models import ClassificationResult, HallucinationCategory, SeverityLevel
from src.plugin_registry import CheckerPlugin

# Module-level model state (lazy-loaded on first use)
_model = None
_tokenizer = None
_model_type: Optional[str] = None   # "transformers" | "sentence-transformers"
_model_name: Optional[str] = None
_load_attempted = False


def _load_code_model():
    """
    Lazy-load a code-aware embedding model.

    Tries transformers-based code models first (better for code↔NL similarity),
    then falls back to sentence-transformers with a generic model.
    """
    global _model, _tokenizer, _model_type, _model_name, _load_attempted
    if _model is not None:
        return True
    if _load_attempted:
        return False
    _load_attempted = True

    # --- Try 1: UniXcoder (best for code search / NL↔code similarity) ---
    try:
        from transformers import AutoTokenizer, AutoModel
        _tokenizer = AutoTokenizer.from_pretrained("microsoft/unixcoder-base")
        _model = AutoModel.from_pretrained("microsoft/unixcoder-base")
        _model.eval()
        _model_type = "transformers"
        _model_name = "unixcoder-base"
        print(f"[semantic] Loaded code-aware model: {_model_name}")
        return True
    except Exception:
        pass

    # --- Try 2: CodeBERT (NL-code bimodal pre-training) ---
    try:
        from transformers import AutoTokenizer, AutoModel
        _tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        _model = AutoModel.from_pretrained("microsoft/codebert-base")
        _model.eval()
        _model_type = "transformers"
        _model_name = "codebert-base"
        print(f"[semantic] Loaded code-aware model: {_model_name}")
        return True
    except Exception:
        pass

    # --- Try 3: Generic sentence-transformers fallback ---
    try:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        _model_type = "sentence-transformers"
        _model_name = "all-MiniLM-L6-v2"
        print(f"[semantic] Loaded generic model: {_model_name} (fallback)")
        return True
    except Exception:
        pass

    print("[semantic] No embedding model available — semantic checker disabled.")
    return False


def _encode(text: str):
    """Encode text into an embedding vector using the loaded model."""
    if _model_type == "transformers":
        import torch
        inputs = _tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )
        with torch.no_grad():
            outputs = _model(**inputs)
        # CLS token pooling — standard for BERT-family models
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    else:
        # sentence-transformers
        return _model.encode(text)


def _cosine_similarity(a, b) -> float:
    """Compute cosine similarity between two vectors (numpy-free)."""
    dot = sum(float(x) * float(y) for x, y in zip(a, b))
    norm_a = math.sqrt(sum(float(x) ** 2 for x in a))
    norm_b = math.sqrt(sum(float(x) ** 2 for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# Thresholds per model — calibrated from golden dataset distributions.
# HALLUCINATION mean=0.215, max=0.325; GROUNDED_ERROR min=0.289, mean=0.541
_THRESHOLDS = {
    "unixcoder-base":    {"high": 0.20, "low": 0.30},
    "codebert-base":     {"high": 0.20, "low": 0.30},
    "all-MiniLM-L6-v2":  {"high": 0.20, "low": 0.35},
}


class SemanticCheckerPlugin(CheckerPlugin):
    """Detects semantic hallucinations using code-aware embedding similarity."""

    @property
    def name(self) -> str:
        return "semantic"

    @property
    def priority(self) -> int:
        return 95  # Highest priority — runs first

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        prompt = kwargs.get("prompt", "")
        code = kwargs.get("code", "")
        if not prompt or not code:
            return None
        return check_semantics(prompt, code)


def check_semantics(prompt: str, generated_code: str) -> Optional[ClassificationResult]:
    """
    Compare the semantic similarity between a natural language prompt
    and the generated code using a code-aware embedding model.
    """
    if not _load_code_model() or _model is None:
        return None

    try:
        prompt_emb = _encode(prompt)
        code_emb = _encode(generated_code)
        similarity = _cosine_similarity(prompt_emb, code_emb)

        # Get model-specific thresholds
        thresholds = _THRESHOLDS.get(_model_name, {"high": 0.20, "low": 0.35})
        t_high = thresholds["high"]   # Below this → high confidence hallucination
        t_low = thresholds["low"]     # Below this → medium confidence

        if similarity < t_low:
            if similarity < t_high:
                conf = 0.90
                sev = SeverityLevel.HIGH
            else:
                conf = 0.70
                sev = SeverityLevel.MEDIUM

            return ClassificationResult(
                is_valid=False,
                is_grounded_error=False,
                hallucination_category=HallucinationCategory.SEMANTIC,
                explanation=(
                    f"Semantic Hallucination: Low intent-code similarity "
                    f"({similarity:.3f}, model={_model_name}). "
                    f"Code may not match the prompt."
                ),
                confidence=conf,
                severity=sev,
                checker_source="semantic_embedding",
            )
    except Exception:
        pass  # Graceful fallback — model issues don't block classification

    return None
