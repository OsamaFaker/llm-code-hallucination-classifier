"""
Structured Output Formatters — JSON and SARIF.

Produces machine-readable classification results for integration
with CI/CD pipelines, GitHub Code Scanning, and VS Code.
"""
import json
from typing import List, Dict, Any
from src.models import ClassificationResult


class JSONOutputFormatter:
    """Formats classification results as JSON."""

    @staticmethod
    def format(results: List[Dict[str, Any]], metadata: dict = None) -> str:
        output = {
            "version": "2.0",
            "tool": "grounding-code-classifier",
            "metadata": metadata or {},
            "results": results,
            "summary": {
                "total": len(results),
                "valid": sum(1 for r in results if r.get("predicted_label") == "VALID"),
                "grounded_errors": sum(1 for r in results if r.get("predicted_label") == "GROUNDED_ERROR"),
                "hallucinations": sum(1 for r in results if r.get("predicted_label") not in ("VALID", "GROUNDED_ERROR")),
            }
        }
        return json.dumps(output, indent=2)

    @staticmethod
    def save(results: List[Dict[str, Any]], filepath: str, metadata: dict = None):
        content = JSONOutputFormatter.format(results, metadata)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


class SARIFOutputFormatter:
    """
    Formats classification results as SARIF v2.1.0.
    Static Analysis Results Interchange Format — compatible with
    GitHub Code Scanning and VS Code SARIF Viewer.
    """

    SARIF_SCHEMA = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"

    @staticmethod
    def format(results: List[Dict[str, Any]], metadata: dict = None) -> str:
        rules = SARIFOutputFormatter._build_rules()
        sarif_results = []

        for r in results:
            label = r.get("predicted_label", "VALID")
            if label == "VALID":
                continue  # SARIF only reports issues

            rule_id = SARIFOutputFormatter._label_to_rule_id(label)
            level = SARIFOutputFormatter._severity_to_level(r.get("severity", "MEDIUM"))

            sarif_results.append({
                "ruleId": rule_id,
                "level": level,
                "message": {
                    "text": r.get("explanation", "Classification issue detected.")
                },
                "properties": {
                    "sampleId": r.get("id", ""),
                    "confidence": r.get("confidence", 0),
                    "checker": r.get("checker_source", "unknown"),
                    "expectedLabel": r.get("expected_label", ""),
                    "predictedLabel": label,
                }
            })

        sarif = {
            "$schema": SARIFOutputFormatter.SARIF_SCHEMA,
            "version": "2.1.0",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "grounding-code-classifier",
                        "version": "2.0",
                        "informationUri": "https://github.com/prototype2",
                        "rules": rules,
                    }
                },
                "results": sarif_results,
            }]
        }
        return json.dumps(sarif, indent=2)

    @staticmethod
    def save(results: List[Dict[str, Any]], filepath: str, metadata: dict = None):
        content = SARIFOutputFormatter.format(results, metadata)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def _build_rules() -> list:
        return [
            {"id": "GCC001", "name": "FunctionHallucination", "shortDescription": {"text": "Hallucinated function or method"}},
            {"id": "GCC002", "name": "LibraryHallucination", "shortDescription": {"text": "Hallucinated library or module"}},
            {"id": "GCC003", "name": "ParameterHallucination", "shortDescription": {"text": "Hallucinated parameter"}},
            {"id": "GCC004", "name": "APIEndpointHallucination", "shortDescription": {"text": "Hallucinated API endpoint or data key"}},
            {"id": "GCC005", "name": "EnvVarHallucination", "shortDescription": {"text": "Hallucinated environment variable"}},
            {"id": "GCC006", "name": "ProtocolHallucination", "shortDescription": {"text": "Hallucinated protocol element"}},
            {"id": "GCC007", "name": "SemanticHallucination", "shortDescription": {"text": "Semantic drift from intent"}},
            {"id": "GCC008", "name": "GroundedError", "shortDescription": {"text": "Valid API used incorrectly"}},
        ]

    @staticmethod
    def _label_to_rule_id(label: str) -> str:
        mapping = {
            "FUNCTION": "GCC001",
            "LIBRARY": "GCC002",
            "PARAMETER": "GCC003",
            "API_ENDPOINT": "GCC004",
            "ENV_VAR": "GCC005",
            "PROTOCOL": "GCC006",
            "SEMANTIC": "GCC007",
            "GROUNDED_ERROR": "GCC008",
        }
        return mapping.get(label, "GCC000")

    @staticmethod
    def _severity_to_level(severity: str) -> str:
        mapping = {
            "CRITICAL": "error",
            "HIGH": "error",
            "MEDIUM": "warning",
            "LOW": "note",
        }
        return mapping.get(severity, "warning")
