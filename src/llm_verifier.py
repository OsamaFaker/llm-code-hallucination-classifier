"""
LLM Verifier — semantic verification via LLM.

Supports two modes:
  • Legacy binary  — verify()           → {"attempts_task": YES/NO, "confidence": float}
  • Chain-of-Verification (CoV) — verify_cov() → {"verdict": VALID/HALLUCINATION/GROUNDED_ERROR,
                                                   "confidence": float, "fabricated": bool}

SelfCheck consistency is built into verify_cov():
  On an uncertain first call (confidence < selfcheck_threshold), the verifier
  re-runs at two higher temperatures and takes the majority verdict, boosting
  effective accuracy on borderline cases without changing the interface.

Cache key scheme (v7):
    <8-char SHA-256 of system prompt> + "_" +
    <4-char SHA-256 of model>         + "_" +
    <2-char hex temperature>          + "_" +
    <16-char SHA-256 of prompt||code>
"""
import os
import json
import hashlib
import threading
import urllib.request
import urllib.error
from collections import Counter
from typing import Dict, List


# ---------------------------------------------------------------------------
# Legacy binary prompt (backward compatible)
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

_USER_TEMPLATE = (
    "PROMPT:\n{prompt}\n\n"
    "CODE:\n{code}\n\n"
    "Return your verdict as a single JSON object with exactly these fields:\n"
    '{{"attempts_task": "YES" or "NO", "confidence": <float>, "justification": "<one sentence, max 25 words>"}}'
)

# ---------------------------------------------------------------------------
# Chain-of-Verification (CoV) prompt — 3-way output
# ---------------------------------------------------------------------------
# Targets the GROUNDED_ERROR/HALLUCINATION confusion: the model must explicitly
# decide whether a failing name is *invented* (HALLUCINATION) or a *real name
# misapplied* (GROUNDED_ERROR) before committing to a verdict.
_COV_SYSTEM_PROMPT = (
    "You are a Python hallucination detector. Classify the code into exactly one of:\n\n"
    "  HALLUCINATION — code references a module, function, or identifier that does NOT\n"
    "    exist in Python's standard library or any well-known package (numpy, pandas,\n"
    "    requests, etc.). Examples: importing sortinglib, pymath, datautils; calling a\n"
    "    function that simply does not exist in the module it is attributed to.\n\n"
    "  GROUNDED_ERROR — code uses REAL Python constructs but applies them incorrectly.\n"
    "    All modules and functions exist; they are misused: wrong arguments, wrong type,\n"
    "    wrong algorithm, or the code produces wrong output on the test cases.\n\n"
    "  VALID — code uses real Python constructs correctly and genuinely attempts the task.\n\n"
    "Critical disambiguation rule for NameError / ModuleNotFoundError:\n"
    "  Ask: does this name ACTUALLY EXIST in Python?\n"
    "  If NO  → HALLUCINATION.\n"
    "  If YES but used wrongly (typo of a real name, real module wrong function) → GROUNDED_ERROR.\n\n"
    "Begin your response with { and end with }. No other text."
)

_COV_USER_TEMPLATE = (
    "TASK: {prompt}\n\n"
    "CODE:\n{code}\n\n"
    "Work through these checks before answering:\n"
    "  1. Are all imported modules real Python modules (stdlib or well-known packages)?\n"
    "  2. Are all functions/classes/methods called in the code real names that actually\n"
    "     exist in those modules?\n"
    "  3. If a name is missing or wrong: is it completely invented, or is it a real name\n"
    "     applied in the wrong way?\n"
    "  4. Does the code make a genuine attempt at the stated task (not a stub)?\n\n"
    "Return ONLY this JSON:\n"
    '{{"verdict": "VALID" or "HALLUCINATION" or "GROUNDED_ERROR", '
    '"confidence": <float 0.0-1.0>, '
    '"fabricated": <true if invented name/module, false otherwise>, '
    '"justification": "<max 25 words>"}}'
)

# 8-char SHA-256 of each prompt — cache keys auto-invalidate when prompts change.
_PROMPT_VERSION = hashlib.sha256(_SYSTEM_PROMPT.encode()).hexdigest()[:8]
_COV_PROMPT_VERSION = hashlib.sha256(_COV_SYSTEM_PROMPT.encode()).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------
class _GeminiProvider:
    """Google Gemini API via REST (no SDK needed)."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self._base_url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent?key={self.api_key}"
        )

    def call(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> str:
        payload = json.dumps({
            "contents": [{"parts": [{"text": system_prompt + "\n\n" + user_prompt}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": 200},
        }).encode("utf-8")
        req = urllib.request.Request(
            self._base_url,
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
        self.model = model or os.getenv("LLM_MODEL", "") or "qwen2.5-coder:7b"
        self.base_url = base_url.rstrip("/")

    def call(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> str:
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": 200},
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
    Two-mode semantic verifier:

      verify(prompt, code)         — legacy binary YES/NO
      verify_cov(prompt, code)     — Chain-of-Verification 3-way verdict
      verify_with_selfcheck(...)   — CoV + SelfCheck consistency on uncertain cases
    """

    def __init__(
        self,
        provider: str = "ollama",
        api_key: str = "",
        model: str = "",
        selfcheck_threshold: float = 0.80,
    ):
        self.provider_name = provider.lower()
        self.selfcheck_threshold = selfcheck_threshold
        self.malformed_count = 0
        self._cache_file = os.path.join(os.path.dirname(__file__), "llm_cache.json")
        self._cache: Dict[str, dict] = {}
        self._lock = threading.Lock()

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
        else:
            self._provider = _OllamaProvider(model=model)

        self._model_version = hashlib.sha256(
            self._provider.model.encode()
        ).hexdigest()[:4]

        print(f"[llm_verifier] provider={self.provider_name}, model={self._provider.model}")

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------
    def _cache_key(self, prompt_ver: str, prompt: str, code: str, temperature: float) -> str:
        content_hash = hashlib.sha256(f"{prompt}||{code}".encode()).hexdigest()[:16]
        temp_hex = format(int(temperature * 10), "02x")
        return f"{prompt_ver}_{self._model_version}_{temp_hex}_{content_hash}"

    def _save_cache(self) -> None:
        try:
            with open(self._cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Low-level call
    # ------------------------------------------------------------------
    def _call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        cache_key: str,
    ) -> str:
        """Call the provider, using the cache for temperature=0 results."""
        if temperature == 0.0 and cache_key in self._cache:
            cached = self._cache[cache_key]
            # Return raw string representation so callers can re-parse
            return json.dumps(cached)

        raw = self._provider.call(system_prompt, user_prompt, temperature)

        if temperature == 0.0:
            with self._lock:
                # Don't overwrite — parse first so we store the parsed dict
                pass  # parsed and stored by callers below

        return raw

    # ------------------------------------------------------------------
    # Legacy binary verify (backward compatible)
    # ------------------------------------------------------------------
    def verify(self, prompt: str, code: str) -> dict:
        """
        Legacy YES/NO check: does the code attempt the task?
        Returns: {"attempts_task": "YES"|"NO", "confidence": float, "justification": str}
        """
        key = self._cache_key(_PROMPT_VERSION, prompt, code, 0.0)
        if key in self._cache:
            return self._cache[key]

        user_prompt = _USER_TEMPLATE.format(prompt=prompt, code=code)
        try:
            raw = self._provider.call(_SYSTEM_PROMPT, user_prompt, 0.0)
            parsed = self._parse_binary(raw)
        except Exception as e:
            print(f"[llm_verifier] API error (verify): {e}")
            self.malformed_count += 1
            return {"attempts_task": "YES", "confidence": 0.0,
                    "justification": f"API Error: {e}", "_malformed": True}

        with self._lock:
            self._cache[key] = parsed
            self._save_cache()
        return parsed

    # ------------------------------------------------------------------
    # Chain-of-Verification — single run
    # ------------------------------------------------------------------
    def verify_cov(self, prompt: str, code: str, temperature: float = 0.0) -> dict:
        """
        Chain-of-Verification single run.
        Returns: {"verdict": VALID|HALLUCINATION|GROUNDED_ERROR,
                  "confidence": float, "fabricated": bool, "justification": str}
        """
        key = self._cache_key(_COV_PROMPT_VERSION, prompt, code, temperature)
        if temperature == 0.0 and key in self._cache:
            return self._cache[key]

        user_prompt = _COV_USER_TEMPLATE.format(prompt=prompt, code=code)
        try:
            raw = self._provider.call(_COV_SYSTEM_PROMPT, user_prompt, temperature)
            parsed = self._parse_cov(raw)
        except Exception as e:
            print(f"[llm_verifier] API error (verify_cov): {e}")
            self.malformed_count += 1
            return {"verdict": "GROUNDED_ERROR", "confidence": 0.0,
                    "fabricated": False, "justification": f"API Error: {e}",
                    "_malformed": True}

        if temperature == 0.0:
            with self._lock:
                self._cache[key] = parsed
                self._save_cache()
        return parsed

    # ------------------------------------------------------------------
    # SelfCheck: CoV + consistency across 3 temperatures
    # ------------------------------------------------------------------
    def verify_with_selfcheck(self, prompt: str, code: str) -> dict:
        """
        Chain-of-Verification with SelfCheck consistency.

        Algorithm
        ---------
        1. Run CoV at temperature=0.0 (deterministic).
        2. If confidence >= selfcheck_threshold → return immediately (certain).
        3. Otherwise run 2 more times at temperature=0.4 and 0.7.
        4. Take majority verdict of the 3 runs.
        5. Final confidence = fraction agreeing × mean confidence of agreeing runs.

        This catches borderline cases where the first run is uncertain, without
        adding extra LLM calls for the large majority of straightforward samples.
        """
        first = self.verify_cov(prompt, code, temperature=0.0)

        if first.get("_malformed"):
            return first

        if first["confidence"] >= self.selfcheck_threshold:
            first["selfcheck_runs"] = 1
            return first

        # Uncertain — run 2 more at higher temperatures
        extra_temps = [0.4, 0.7]
        runs: List[dict] = [first]
        for t in extra_temps:
            r = self.verify_cov(prompt, code, temperature=t)
            if not r.get("_malformed"):
                runs.append(r)

        verdicts = [r["verdict"] for r in runs]
        majority_verdict, count = Counter(verdicts).most_common(1)[0]
        agreeing = [r for r in runs if r["verdict"] == majority_verdict]
        mean_conf = sum(r["confidence"] for r in agreeing) / len(agreeing)
        agreement_ratio = count / len(runs)

        return {
            "verdict": majority_verdict,
            "confidence": mean_conf * agreement_ratio,
            "fabricated": any(r.get("fabricated", False) for r in agreeing),
            "justification": agreeing[0]["justification"],
            "selfcheck_runs": len(runs),
            "selfcheck_agreement": agreement_ratio,
            "_malformed": False,
        }

    # ------------------------------------------------------------------
    # Parsers
    # ------------------------------------------------------------------
    def _parse_binary(self, raw: str) -> dict:
        raw = raw.strip()
        s, e = raw.find("{"), raw.rfind("}")
        if s != -1 and e >= s:
            try:
                data = json.loads(raw[s:e + 1])
                return {
                    "attempts_task": str(data.get("attempts_task", "YES")).upper(),
                    "confidence": float(data.get("confidence", 0.0)),
                    "justification": str(data.get("justification", "")),
                    "_malformed": False,
                }
            except (json.JSONDecodeError, ValueError):
                pass
        print(f"[llm_verifier] Malformed binary response: {raw[:120]}")
        self.malformed_count += 1
        return {"attempts_task": "YES", "confidence": 0.0,
                "justification": "Malformed JSON", "_malformed": True}

    def _parse_cov(self, raw: str) -> dict:
        raw = raw.strip()
        s, e = raw.find("{"), raw.rfind("}")
        if s != -1 and e >= s:
            try:
                data = json.loads(raw[s:e + 1])
                verdict = str(data.get("verdict", "GROUNDED_ERROR")).upper()
                if verdict not in ("VALID", "HALLUCINATION", "GROUNDED_ERROR"):
                    verdict = "GROUNDED_ERROR"
                return {
                    "verdict": verdict,
                    "confidence": float(data.get("confidence", 0.0)),
                    "fabricated": bool(data.get("fabricated", False)),
                    "justification": str(data.get("justification", "")),
                    "_malformed": False,
                }
            except (json.JSONDecodeError, ValueError):
                pass
        print(f"[llm_verifier] Malformed CoV response: {raw[:120]}")
        self.malformed_count += 1
        return {"verdict": "GROUNDED_ERROR", "confidence": 0.0,
                "fabricated": False, "justification": "Malformed JSON",
                "_malformed": True}

    def get_cache_stats(self) -> dict:
        return {"cached_entries": len(self._cache)}
