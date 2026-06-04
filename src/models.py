from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List

class HallucinationCategory(Enum):
    FUNCTION = "Function/Method/Class Hallucination"
    LIBRARY = "Library/Module Hallucination"
    PARAMETER = "Parameter/Argument Hallucination"
    API_ENDPOINT = "API Endpoint/Data Key Hallucination"
    ENV_VAR = "Environment Variable Hallucination"
    PROTOCOL = "Protocol Element Hallucination"
    SEMANTIC = "Semantic Hallucination"
    ATTRIBUTE = "Attribute/Property Hallucination"

class SeverityLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class ClassificationResult:
    is_valid: bool
    is_grounded_error: bool
    hallucination_category: Optional[HallucinationCategory]
    explanation: str
    confidence: float = 1.0
    severity: Optional[SeverityLevel] = None
    checker_source: str = "unknown"
    latency_ms: float = 0.0
    # Compound defect list: all secondary checker signals that also fired (Item #4)
    issues: List[ClassificationResult] = field(default_factory=list)
    
    # v6: Diagnostic tracking fields
    line: Optional[str | int] = None
    bad_token: Optional[str] = None
    
    # Arbitration tracking fields
    attempts_task: Optional[str] = None
    verifier_confidence: Optional[float] = None
    verifier_justification: Optional[str] = None
    taxonomy_tag: Optional[str] = None
    malformed_json: Optional[bool] = None
    short_explanation: Optional[str] = None

    def __post_init__(self):
        """Auto-assign severity based on classification if not explicitly set."""
        if self.severity is None:
            self.severity = self._infer_severity()

    def _infer_severity(self) -> SeverityLevel:
        if self.is_valid:
            return SeverityLevel.LOW
        if self.is_grounded_error:
            return SeverityLevel.MEDIUM
        if self.hallucination_category in (HallucinationCategory.LIBRARY, HallucinationCategory.PROTOCOL):
            return SeverityLevel.CRITICAL
        if self.hallucination_category in (HallucinationCategory.FUNCTION, HallucinationCategory.API_ENDPOINT):
            return SeverityLevel.HIGH
        if self.hallucination_category in (HallucinationCategory.ENV_VAR, HallucinationCategory.PARAMETER):
            return SeverityLevel.HIGH
        if self.hallucination_category == HallucinationCategory.ATTRIBUTE:
            return SeverityLevel.HIGH
        if self.hallucination_category == HallucinationCategory.SEMANTIC:
            return SeverityLevel.MEDIUM
        return SeverityLevel.MEDIUM

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "is_grounded_error": self.is_grounded_error,
            "hallucination_category": self.hallucination_category.name if self.hallucination_category else None,
            "explanation": self.explanation,
            "confidence": round(self.confidence, 4),
            "severity": self.severity.name if self.severity else None,
            "checker_source": self.checker_source,
            "latency_ms": round(self.latency_ms, 4),
            "line": self.line,
            "bad_token": self.bad_token,
            "short_explanation": self.short_explanation,
            "attempts_task": self.attempts_task,
            "verifier_confidence": round(self.verifier_confidence, 4) if self.verifier_confidence is not None else None,
            "verifier_justification": self.verifier_justification,
            "taxonomy_tag": self.taxonomy_tag,
            "malformed_json": self.malformed_json,
            "issues": [i.to_dict() for i in self.issues] if self.issues else [],
        }
