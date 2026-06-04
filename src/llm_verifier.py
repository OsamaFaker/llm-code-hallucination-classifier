"""
LLM Verifier — Last-resort semantic verification via LLM API.

Only called when all static checkers say VALID. Asks an LLM to verify
whether the generated code actually matches the prompt intent.

Supports two providers:
    - gemini:  Google Gemini API (free tier with gemini-2.0-flash)
    - ollama:  Local Ollama server (fully offline, no API key needed)

Configuration — model selection precedence (highest to lowest):
    1. constructor argument passed to LLMVerifier(model=...)
    2. LLM_MODEL environment variable
    3. hardcoded default: qwen2.5-coder:7b (ollama) / gemini-2.0-flash (gemini)

Other environment variables:
    LLM_PROVIDER  = "gemini" | "ollama"
    LLM_API_KEY   = "<your-gemini-api-key>"  (gemini only)

Cache-key scheme (v6, extended):
    key = <8-char SHA-256 of system prompt> + "_"
        + <4-char SHA-256 of model identifier> + "_"
        + <16-char SHA-256 of prompt||code>
    The model-identifier component ensures that two different models
    evaluated against the same prompt+code produce distinct cache entries,
    so switching models mid-evaluation never silently reuses stale verdicts.
    Cache entries written by earlier versions (which lack the model prefix)
    are treated as misses and will be overwritten on first access.
"""
import os
import json
import hashlib
import threading
import urllib.request
import urllib.error
from typing import Dict


# ---------------------------------------------------------------------------
# Verification prompt — designed for narrow yes/no classification
# ---------------------------------------------------------------------------
_SYSTEM_PROMPT = (
    "You are an automated code reviewer. Your single task is to judge whether a piece\n"
    "of Python code attempts to solve the problem described in a natural-language\n"
    "prompt. You are NOT asked to classify the code as a hallucination, a bug, or any\n"
    "other category. You are NOT asked to judge whether the code is correct, elegant,\n"
    "or efficient. Another component of the pipeline handles those judgments.\n\n"
    "Decision rule:\n"
    "- Answer YES if the code, however buggy or incomplete, is a genuine attempt at\n"
    "  the task described in the prompt. Wrong algorithms, off-by-one errors, missing\n"
    "  edge cases, type errors, and partial implementations all count as YES, because\n"
    "  they show the author understood and engaged with the requested task.\n"
    "- Answer NO only if the code addresses a clearly different task, is a generic\n"
    "  stub that ignores the prompt's specifics, or returns unrelated data. The test\n"
    "  is intent, not correctness: would a reader who saw only the code be unable to\n"
    "  recover the prompt's task from it?\n\n"
    "Recognise generic passthrough patterns. A function that copies its input list to\n"
    "a new list and returns it, that returns the input unchanged, or that performs a\n"
    "trivial operation unrelated to the prompt's specific topic does NOT count as an\n"
    "attempt. The pattern `result = []; for item in data: result.append(item); return result` \n"
    "is a stub regardless of the function's name or the docstring. Answer NO for any \n"
    "code matching this pattern unless the prompt explicitly asks for a list copy or \n"
    "passthrough.\n\n"
    "Require topical specificity. In your justification, name the specific concept\n"
    "from the prompt that the code addresses. If the prompt asks about binomial \n"
    "coefficients, Pell numbers, regex, or any other specific topic, and you cannot \n"
    "point to a feature of the code that engages with that concept, answer NO. \n"
    "Surface-level engagement (variable names that echo the prompt, the function \n"
    "having an argument) does not count.\n\n"
    "Calibrate your confidence between 0.0 and 1.0. It must reflect how certain you\n"
    "are of the YES/NO verdict, not how correct the code is.\n\n"
    "Begin your response with the character { and end it with the character }.\n"
    "No prose before or after."
)

# 8-char SHA-256 of the system prompt — changes when the prompt changes,
# which invalidates all cached verdicts for that prompt version.
_PROMPT_VERSION = hashlib.sha256(_SYSTEM_PROMPT.encode()).hexdigest()[:8]


_USER_TEMPLATE = (
    "PROMPT:\n{prompt}\n\n"
    "CODE:\n{code}\n\n"
    "Return your verdict as a single JSON object with exactly these fields:\n"
    '{{"attempts_task": "YES" or "NO", "confidence": <float>, "justification": "<one sentence, max 25 words>"}}'
)


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------
class _GeminiProvider:
    """Google Gemini API via REST (no SDK needed)."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self._url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent?key={self.api_key}"
        )

    def call(self, message: str) -> str:
        payload = json.dumps({
            "contents": [{"parts": [{"text": message}]}],
            "generationConfig": {
                "temperature": 0.0,
                "maxOutputTokens": 200,
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            self._url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return ""


class _OllamaProvider:
    """Local Ollama server via REST."""

    def __init__(self, model: str = "", base_url: str = "http://localhost:11434"):
        # Precedence: constructor arg > LLM_MODEL env var > hardcoded default
        # This allows callers to pass the model explicitly, fall back to the
        # environment variable for users who set it externally, or use the
        # dissertation baseline (qwen2.5-coder:7b) when neither is supplied.
        self.model = model or os.getenv("LLM_MODEL", "") or "qwen2.5-coder:7b"
        self.base_url = base_url.rstrip("/")

    def call(self, message: str) -> str:
        system_prompt = _SYSTEM_PROMPT
        user_prompt = message.replace(_SYSTEM_PROMPT + "\n\n", "")

        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 150
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        return data.get("message", {}).get("content", "")


# ---------------------------------------------------------------------------
# LLM Verifier
# ---------------------------------------------------------------------------
class LLMVerifier:
    """
    Verifies code-prompt alignment using an LLM as a last-resort check.

    Only instantiated when LLM_PROVIDER env var is set. The verify() method
    is called from the classifier pipeline when all static checkers say VALID.
    """

    def __init__(
        self,
        provider: str = "gemini",
        api_key: str = "",
        model: str = "",
    ):
        self.provider_name = provider.lower()
        self.malformed_count = 0
        self._cache_file = os.path.join(os.path.dirname(__file__), "llm_cache.json")
        self._cache: Dict[str, dict] = {}
        self._lock = threading.Lock()  # Thread-safe cache writes

        if os.path.exists(self._cache_file):
            try:
                with open(self._cache_file, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                pass

        if self.provider_name == "gemini":
            self._provider = _GeminiProvider(
                api_key=api_key,
                model=model or os.getenv("LLM_MODEL", "") or "gemini-2.0-flash",
            )
        elif self.provider_name == "ollama":
            # Pass model as-is; _OllamaProvider applies the three-level precedence.
            self._provider = _OllamaProvider(model=model)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

        # 4-char SHA-256 of the resolved model name — included in every cache key
        # so that verdicts from different models never collide in the cache.
        self._model_version = hashlib.sha256(
            self._provider.model.encode()
        ).hexdigest()[:4]

        print(f"[llm_verifier] Initialized with provider={self.provider_name}, "
              f"model={self._provider.model}")

    def verify(self, prompt: str, code: str) -> dict:
        """
        Ask the LLM whether the code attempts the prompt intent.
        Returns: {"attempts_task": "YES"|"NO", "confidence": float,
                  "justification": str, "_malformed": bool}

        Cache key format: <8-char prompt hash>_<4-char model hash>_<16-char content hash>
        Entries from earlier versions (no model prefix) are treated as misses.
        """
        raw_key = f"{prompt}||{code}"
        cache_key = (
            _PROMPT_VERSION + "_"
            + self._model_version + "_"
            + hashlib.sha256(raw_key.encode()).hexdigest()[:16]
        )

        if cache_key in self._cache:
            return self._cache[cache_key]

        message = _SYSTEM_PROMPT + "\n\n" + _USER_TEMPLATE.format(
            prompt=prompt, code=code
        )

        try:
            raw_response = self._provider.call(message)
            parsed = self._parse_response(raw_response)
        except Exception as e:
            print(f"[llm_verifier] API error: {e}")
            self.malformed_count += 1
            return {
                "attempts_task": "YES",
                "confidence": 0.0,
                "justification": f"API Error: {e}",
                "_malformed": True,
            }

        with self._lock:
            self._cache[cache_key] = parsed
            try:
                with open(self._cache_file, "w", encoding="utf-8") as f:
                    json.dump(self._cache, f)
            except Exception:
                pass

        return parsed

    def _parse_response(self, raw: str) -> dict:
        """Parse the LLM response defensively."""
        raw = raw.strip()

        start_idx = raw.find("{")
        end_idx = raw.rfind("}")

        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            json_str = raw[start_idx:end_idx + 1]
            try:
                data = json.loads(json_str)
                return {
                    "attempts_task": str(data.get("attempts_task", "YES")).upper(),
                    "confidence": float(data.get("confidence", 0.0)),
                    "justification": str(data.get("justification", "No justification provided")),
                    "_malformed": False,
                }
            except (json.JSONDecodeError, ValueError):
                pass

        print(f"[llm_verifier] Malformed JSON response: {raw}")
        self.malformed_count += 1
        return {
            "attempts_task": "YES",
            "confidence": 0.0,
            "justification": "Malformed JSON output",
            "_malformed": True,
        }

    def get_cache_stats(self) -> dict:
        return {"cached_entries": len(self._cache)}
