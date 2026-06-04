"""
Language Adapter Interface (Item #9).

Defines the LanguageAdapter ABC that decouples the classifier from Python-specific
AST parsing. Each language provides a concrete adapter that:
  - Parses source code into an AdapterParseResult
  - Exposes extracted calls and imports in the same schema the checkers expect

Current adapters
----------------
- PythonAdapter  (python_adapter.py) — wraps the existing ConstructExtractor
- CAdapter       (c_adapter.py)      — stub, pending full pycparser integration
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set


@dataclass
class AdapterParseResult:
    """
    Language-agnostic representation of a parsed code snippet.

    All fields mirror the schema produced by src.parser.ConstructExtractor so
    that the downstream checker plugins require no modification.
    """
    # List of call dicts: {module, method, kwargs, arg_values, line}
    extracted_calls: List[Dict[str, Any]] = field(default_factory=list)
    # Fully-qualified module names appearing in import statements
    extracted_imports: List[str] = field(default_factory=list)
    # Names of locally-defined variables, functions, and classes
    local_vars: Set[str] = field(default_factory=set)
    # True if the source could not be parsed
    syntax_error: bool = False
    # 'grounded' | 'hallucinated' | None
    syntax_error_kind: Optional[str] = None


class LanguageAdapter(ABC):
    """
    Abstract base class for language-specific parsing adapters.

    Implementors must override `language_name` and `parse()`.
    The `parse()` method must return an AdapterParseResult whose fields
    are populated to the best of the adapter's ability.
    """

    @property
    @abstractmethod
    def language_name(self) -> str:
        """Short identifier, e.g. 'python', 'c', 'javascript'."""
        ...

    @abstractmethod
    def parse(self, code: str) -> AdapterParseResult:
        """
        Parse source code and return a normalised AdapterParseResult.

        Must not raise exceptions — parse errors should be captured in the
        `syntax_error` and `syntax_error_kind` fields of the result.
        """
        ...

    @classmethod
    def for_language(cls, language: str) -> "LanguageAdapter":
        """
        Factory: return the appropriate adapter for the given language tag.

        Supported tags (case-insensitive): 'python', 'c'.
        Raises ValueError for unsupported languages.
        """
        tag = language.lower().strip()
        if tag == "python":
            from src.lang.python_adapter import PythonAdapter
            return PythonAdapter()
        if tag == "c":
            from src.lang.c_adapter import CAdapter
            return CAdapter()
        raise ValueError(
            f"Unsupported language '{language}'. "
            f"Available adapters: 'python', 'c'."
        )
