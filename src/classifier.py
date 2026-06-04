"""
Code Classifier — Plugin-based architecture.

Orchestrates checker plugins through the PluginRegistry with
caching, profiling, control flow analysis, and ablation support.

Changes in this revision
------------------------
- Items #1  SyntaxError triaged to grounded vs. hallucinated via syntax_error_kind.
- Items #2  AttributeCheckerPlugin registered (phantom attribute detection).
- Items #4  Multi-signal issues list forwarded from the registry.
- Items #7  env_version passed to GroundTruthRegistry for deprecation checks.
- Items #8  Optional confidence calibration via ConfidenceCalibrator.
- Items #9  Language adapter scaffold: accepts `language` parameter.
"""
import os
from typing import Optional, Set

from src.models import ClassificationResult, HallucinationCategory, SeverityLevel
from src.dataset import CodeSample
from src.ground_truth import GroundTruthRegistry
from src.parser import parse_generated_code
from src.plugin_registry import PluginRegistry
from src.fabrication_checker import FabricationCheckerPlugin
from src.misuse_checker import MisuseCheckerPlugin
# from src.semantic_checker import SemanticCheckerPlugin
from src.logic_checker import LogicCheckerPlugin
from src.attribute_checker import AttributeCheckerPlugin
from src.arity_checker import ArityCheckerPlugin
from src.checkers.signature_checker import SignatureCheckerPlugin
from src.control_flow import analyze_control_flow
from src.cache import ASTCache
from src.profiler import LatencyProfiler
from src.confidence_calibrator import ConfidenceCalibrator

from src.arbitration import arbitrate

# Default path for the fitted calibrator (produced by calibrate.py)
_DEFAULT_CALIBRATOR_PATH = os.path.join(
    os.path.dirname(__file__), "calibrators.pkl"
)


class CodeClassifier:
    """
    Main classifier that uses a plugin registry to orchestrate
    fabrication, misuse, semantic, attribute, and logic checks with
    caching, profiling, and optional confidence calibration.
    """

    def __init__(
        self,
        gt_version: str = "v1",
        use_dynamic_gt: bool = True,
        disabled_checkers: Optional[Set[str]] = None,
        enable_profiling: bool = False,
        enable_cache: bool = True,
        enable_calibration: bool = True,
        language: str = "python",
    ):
        self.language = language.lower()
        self.gt = GroundTruthRegistry(version=gt_version, use_dynamic=use_dynamic_gt)
        self.ast_cache = ASTCache() if enable_cache else None
        self.profiler = LatencyProfiler(enabled=enable_profiling)

        # ---- Plugin registry ----
        self.registry = PluginRegistry()
        # SemanticCheckerPlugin is disabled: it requires heavy ML dependencies
        # (transformers, torch, sentence-transformers) that are not part of the
        # core pipeline.  The LLM verifier serves the same purpose (semantic
        # intent checking) without requiring GPU-accelerated embedding models.
        # self.registry.register(SemanticCheckerPlugin())      # priority 95
        self.registry.register(FabricationCheckerPlugin())   # priority 90
        self.registry.register(AttributeCheckerPlugin())     # priority 85 (Item #2)
        self.registry.register(ArityCheckerPlugin())         # priority 75 (Fix #3)
        self.registry.register(SignatureCheckerPlugin())     # priority 72
        self.registry.register(MisuseCheckerPlugin())        # priority 70
        self.registry.register(LogicCheckerPlugin())         # priority 60

        if disabled_checkers:
            self.registry.set_disabled(disabled_checkers)

        # ---- Confidence calibrator (Item #8) ----
        # Supports JSON (preferred, safe) and legacy pickle (fallback).
        self._calibrators: Optional[dict] = None
        if enable_calibration:
            json_path = os.path.splitext(_DEFAULT_CALIBRATOR_PATH)[0] + ".json"
            if os.path.exists(json_path):
                import json as _json
                with open(json_path, "r", encoding="utf-8") as fh:
                    self._calibrators = _json.load(fh)
            elif os.path.exists(_DEFAULT_CALIBRATOR_PATH):
                # Legacy pickle fallback — will be removed in a future version.
                import pickle
                with open(_DEFAULT_CALIBRATOR_PATH, "rb") as fh:
                    self._calibrators = pickle.load(fh)

        # ---- LLM Verifier (Option B — last-resort semantic check) ----
        self._llm_verifier = None
        llm_provider = os.getenv("LLM_PROVIDER", "")
        if llm_provider:
            try:
                from src.llm_verifier import LLMVerifier
                self._llm_verifier = LLMVerifier(
                    provider=llm_provider,
                    api_key=os.getenv("LLM_API_KEY", ""),
                    model=os.getenv("LLM_MODEL", ""),
                )
            except Exception as e:
                raise RuntimeError(f"Failed to initialize LLM Verifier: {e}")
        else:
            # No LLM provider configured — verifier is optional; classify_static still works.
            # Callers that require the verifier (e.g. classify_unclassified_v6.py) check
            # self._llm_verifier and exit with a clear message if it is None.
            pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def classify(self, sample: CodeSample) -> ClassificationResult:
        """Classify a code sample through the plugin pipeline."""
        with self.profiler.measure_sample() as elapsed:
            static_res = self.classify_static(sample)
            final_res = self.verify_semantic(sample, static_res)

        # elapsed[0] is populated by the profiler's finally block after the with exits
        if isinstance(elapsed, list):
            final_res.latency_ms = elapsed[0] if elapsed[0] else 0.0

        # Apply per-source calibration if available (Item #8)
        if self._calibrators is not None:
            cal = self._calibrators.get(final_res.checker_source) or self._calibrators.get("global")
            if cal:
                final_res.confidence = cal.calibrate(final_res.confidence)

        # v6: Add short_explanation
        exp = final_res.explanation
        final_res.short_explanation = (exp[:97] + "...") if len(exp) > 100 else exp

        return final_res

    def classify_static(self, sample: CodeSample) -> ClassificationResult:
        """Runs all static checks (Funnel Step 1-5)."""
        code = sample.generated_code
        prompt = sample.prompt
        env_version = getattr(sample, "expected_api_version", "v1")

        # ---- Step 1: Parse AST (with caching) ----
        extractor = None
        if self.ast_cache:
            extractor = self.ast_cache.get(code)
        if extractor is None:
            extractor = parse_generated_code(code)
            if self.ast_cache:
                self.ast_cache.put(code, extractor)

        # ---- Step 2: Triaged SyntaxError handling ----
        if getattr(extractor, "syntax_error", False):
            kind = getattr(extractor, "syntax_error_kind", "grounded") or "grounded"
            line = getattr(extractor, "syntax_error_line", 1)
            
            if kind == "hallucinated":
                return ClassificationResult(
                    is_valid=False, is_grounded_error=False,
                    hallucination_category=HallucinationCategory.FUNCTION,
                    explanation="Hallucination: SyntaxError caused by a fabricated language construct.",
                    confidence=0.88, severity=SeverityLevel.HIGH, checker_source="parser",
                    line=line
                )
            else:
                return ClassificationResult(
                    is_valid=False, is_grounded_error=True,
                    hallucination_category=None,
                    explanation="Grounded Error: SyntaxError caused by incorrect use of a real Python keyword.",
                    confidence=0.95, severity=SeverityLevel.CRITICAL, checker_source="parser",
                    line=line
                )

        constructs = extractor.extracted_calls
        imports = extractor.extracted_imports

        # ---- Step 3: Deprecation check ----
        for call in constructs:
            dep_msg = self.gt.check_deprecated(call["module"], call["method"], env_version)
            if dep_msg:
                return ClassificationResult(
                    is_valid=False, is_grounded_error=False,
                    hallucination_category=HallucinationCategory.FUNCTION,
                    explanation=f"Hallucination [Deprecated/Removed API]: {dep_msg}",
                    confidence=0.92, severity=SeverityLevel.HIGH, checker_source="deprecation",
                    line=call.get('line'), bad_token=call.get('method')
                )

        # ---- Step 4: Control flow analysis ----
        cf_issues = analyze_control_flow(code, tree=extractor.ast_tree)
        cf_note = f" [CF: {cf_issues[0].message}]" if cf_issues else ""

        # ---- Step 5: Run all checker plugins ----
        result = self.registry.run_all(
            extracted_calls=constructs,
            extracted_imports=imports,
            local_vars=extractor.local_vars,
            gt=self.gt,
            prompt=prompt,
            code=code,
            ast_tree=extractor.ast_tree,
        )

        if not result:
            return ClassificationResult(
                is_valid=True, is_grounded_error=False, hallucination_category=None,
                explanation="Valid code: perfectly adheres to GT and Semantic Intent." + cf_note,
                confidence=1.0, severity=SeverityLevel.LOW, checker_source="pipeline"
            )
        return result

    def verify_semantic(self, sample: CodeSample, static_res: ClassificationResult) -> ClassificationResult:
        """Runs LLM Verifier (if needed) and Arbitration Table."""
        code = sample.generated_code
        prompt = sample.prompt
        
        static_verdict = "VALID"
        if not static_res.is_valid:
            static_verdict = "GROUNDED_ERROR" if static_res.is_grounded_error else "HALLUCINATION"
        
        static_confidence = static_res.confidence
        
        attempts_task = "NOT_RUN"
        verifier_confidence = 1.0
        verifier_justification = None
        malformed_json = False

        # Run LLM Verifier only if static says VALID
        if static_verdict == "VALID" and self._llm_verifier:
            llm_res = self._llm_verifier.verify(prompt, code)
            attempts_task = llm_res.get("attempts_task", "YES")
            verifier_confidence = llm_res.get("confidence", 0.0)
            verifier_justification = llm_res.get("justification")
            malformed_json = llm_res.get("_malformed", False)

        final_label, taxonomy_tag, combined_confidence = arbitrate(
            static_verdict, static_confidence, attempts_task, verifier_confidence
        )

        final_result = static_res
        if static_verdict == "VALID":
            final_result.attempts_task = attempts_task
            final_result.verifier_confidence = verifier_confidence
            final_result.verifier_justification = verifier_justification
            
            if attempts_task == "NO":
                final_result.is_valid = False
                final_result.explanation += f" Semantic Hallucination [LLM Verified]: {verifier_justification}"
                final_result.line = "whole snippet"
                final_result.bad_token = ""

        if final_label == "VALID":
            final_result.is_valid = True
            final_result.is_grounded_error = False
            final_result.hallucination_category = None
        elif final_label == "GROUNDED_ERROR":
            final_result.is_valid = False
            final_result.is_grounded_error = True
            final_result.hallucination_category = None
        elif final_label == "HALLUCINATION":
            final_result.is_valid = False
            final_result.is_grounded_error = False
            if taxonomy_tag == "semantic_fabrication":
                final_result.hallucination_category = HallucinationCategory.SEMANTIC
                final_result.checker_source = "llm_verifier"
                final_result.line = "whole snippet"
                final_result.bad_token = ""

        final_result.confidence = combined_confidence
        final_result.taxonomy_tag = taxonomy_tag
        final_result.malformed_json = malformed_json
        
        return final_result

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------
    def get_active_checkers(self):
        """Return list of active checker names."""
        return [p.name for p in self.registry.get_active_plugins()]

    def get_all_checkers(self):
        """Return list of all registered checker names."""
        return self.registry.get_all_plugin_names()
