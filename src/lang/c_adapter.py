"""
C Language Adapter — STUB (Item #9).

Full implementation pending pycparser integration.
Returns an empty AdapterParseResult for any C source code, which means
the classifier will classify all C code as VALID (no issues found).

To activate:
    pip install pycparser
    Implement _parse_c_code() below using pycparser's AST visitor.
    Populate extracted_calls using the C stdlib ground truth registry.
"""
from src.lang.adapter import LanguageAdapter, AdapterParseResult


class CAdapter(LanguageAdapter):
    """
    Stub C language adapter.

    Planned detection capabilities:
    - Fabricated stdlib functions (e.g. printf_custom, malloc_safe)
    - Hallucinated header includes (e.g. #include <fakelib.h>)
    - Type misuse (passing float* to a function expecting int*)
    """

    @property
    def language_name(self) -> str:
        return "c"

    def parse(self, code: str) -> AdapterParseResult:
        # STUB: No parsing implemented yet.
        # TODO: integrate pycparser here.
        return AdapterParseResult(
            extracted_calls=[],
            extracted_imports=[],
            local_vars=set(),
            syntax_error=False,
            syntax_error_kind=None,
        )
