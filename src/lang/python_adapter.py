"""
Python Language Adapter (Item #9).

Wraps the existing src.parser.ConstructExtractor and
src.parser.parse_generated_code into the LanguageAdapter interface.
Zero logic duplication — all Python-specific parsing stays in parser.py.
"""
from src.lang.adapter import LanguageAdapter, AdapterParseResult
from src.parser import parse_generated_code


class PythonAdapter(LanguageAdapter):
    """Concrete adapter for Python source code."""

    @property
    def language_name(self) -> str:
        return "python"

    def parse(self, code: str) -> AdapterParseResult:
        extractor = parse_generated_code(code)
        return AdapterParseResult(
            extracted_calls=extractor.extracted_calls,
            extracted_imports=extractor.extracted_imports,
            local_vars=extractor.local_vars,
            syntax_error=getattr(extractor, "syntax_error", False),
            syntax_error_kind=getattr(extractor, "syntax_error_kind", None),
        )
