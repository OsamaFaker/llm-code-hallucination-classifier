"""Tests for the parser and AST extraction."""
from src.parser import parse_generated_code


class TestParser:
    """Test AST parsing and syntax error triage."""

    def test_valid_code_parsing(self):
        code = "import math\nx = math.sqrt(4)"
        extractor = parse_generated_code(code)
        assert not extractor.syntax_error
        assert len(extractor.extracted_imports) == 1
        assert len(extractor.extracted_calls) == 1

    def test_grounded_syntax_error(self):
        """SyntaxError due to misspelled real keyword (edit distance <= 2)."""
        code = "whille True:\n    pass"
        extractor = parse_generated_code(code)
        assert extractor.syntax_error
        assert extractor.syntax_error_kind == "grounded"

    def test_hallucinated_syntax_error(self):
        """SyntaxError due to non-Python syntax and keywords (e.g., JS function)."""
        code = "function myFunction() {\n    return 1;\n}"
        extractor = parse_generated_code(code)
        assert extractor.syntax_error
        assert extractor.syntax_error_kind == "hallucinated"

    def test_extracted_calls(self):
        """Test extraction of function calls and arguments."""
        code = "import os\nos.getenv('PATH', default='none')"
        extractor = parse_generated_code(code)
        calls = extractor.extracted_calls
        assert len(calls) == 1
        call = calls[0]
        assert call["module"] == "os"
        assert call["method"] == "getenv"
        assert "PATH" in call["arg_values"]
        assert "default" in call["kwargs"]
