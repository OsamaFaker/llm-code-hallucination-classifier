"""
Execution Oracle — subprocess-based safe code executor.

Runs a Python snippet + test assertions in an isolated child process with a
hard timeout.  Maps execution outcomes to ground-truth labels using the same
GT-existence framework that governs the static checkers:

  VALID          — all test assertions pass (exit code 0)
  HALLUCINATION  — code invokes a construct that has no referent in the
                   Python Ground Truth:
                     • ModuleNotFoundError  for a fabricated module name
                     • AttributeError       for a fabricated attribute/method
                     • TypeError "unexpected keyword argument"  for a
                                            fabricated parameter name
                     • NameError            for an invented identifier
  GROUNDED_ERROR — code uses real Python constructs incorrectly:
                     • SyntaxError, IndentationError
                     • TypeError (arity / type mismatch, not kwarg name)
                     • AssertionError       — code ran but produced wrong output
                     • TimeoutError         — likely infinite loop
                     • Any other exception

Design notes
------------
* Execution happens in a fresh subprocess — no shared state, no risk of
  polluting the test runner's address space.
* The temp file is always cleaned up in a finally block.
* _STDLIB_MODULES lists modules that are real but may not be installed;
  a ModuleNotFoundError for one of these is GROUNDED_ERROR (missing dep),
  not HALLUCINATION (fabricated name).
"""
import os
import re
import subprocess
import sys
import tempfile
from typing import Optional, Tuple


LABEL_VALID = "VALID"
LABEL_HALLUCINATION = "HALLUCINATION"
LABEL_GROUNDED_ERROR = "GROUNDED_ERROR"


# Modules that exist in Python (stdlib or well-known third-party) but may not
# be installed in the current environment.  A ModuleNotFoundError for any of
# these is a missing-dependency error (GROUNDED_ERROR), not a fabricated name.
_STDLIB_MODULES: frozenset = frozenset({
    # stdlib
    "os", "sys", "re", "json", "math", "datetime", "collections", "itertools",
    "functools", "pathlib", "random", "time", "string", "io", "abc", "typing",
    "dataclasses", "enum", "copy", "hashlib", "base64", "csv", "tempfile",
    "shutil", "glob", "subprocess", "threading", "multiprocessing", "queue",
    "socket", "http", "urllib", "xml", "html", "email", "unittest", "logging",
    "argparse", "struct", "array", "heapq", "bisect", "decimal", "fractions",
    "statistics", "operator", "contextlib", "inspect", "ast", "dis",
    "traceback", "warnings", "gc", "weakref", "pickle", "shelve", "sqlite3",
    "zipfile", "tarfile", "gzip", "bz2", "lzma", "textwrap", "pprint",
    # common third-party
    "numpy", "pandas", "scipy", "matplotlib", "sklearn", "torch",
    "tensorflow", "requests", "flask", "django", "fastapi", "pydantic",
    "pytest", "sqlalchemy", "redis", "celery", "boto3", "anthropic",
    "transformers", "PIL", "cv2", "sympy", "networkx", "nltk", "spacy",
})


def execute_code(
    code: str,
    test_assertions: str,
    timeout: int = 5,
) -> Tuple[str, str, Optional[str]]:
    """
    Execute *code* + *test_assertions* in a subprocess and return a triple:

        (label, error_message, exception_type)

    Parameters
    ----------
    code : str
        The Python snippet to test.
    test_assertions : str
        One or more ``assert ...`` statements, joined by newlines.
    timeout : int
        Hard timeout in seconds (default 5).

    Returns
    -------
    label : str
        One of LABEL_VALID, LABEL_HALLUCINATION, LABEL_GROUNDED_ERROR.
    error_message : str
        Human-readable error detail, or "" on success.
    exception_type : str or None
        The exception class name, or None on success.
    """
    full_source = code.strip() + "\n\n" + test_assertions.strip()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(full_source)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return LABEL_VALID, "", None

        return _label_from_stderr(result.stderr.strip(), code)

    except subprocess.TimeoutExpired:
        return LABEL_GROUNDED_ERROR, "Execution timed out (likely infinite loop)", "TimeoutError"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _label_from_stderr(
    stderr: str,
    code: str,
) -> Tuple[str, str, Optional[str]]:
    """Parse the last traceback line and map to a GT-existence label."""
    exc_type, exc_msg = _parse_exception(stderr)

    if exc_type is None:
        return LABEL_GROUNDED_ERROR, stderr or "Unknown error", None

    # --- Fabricated module ---
    if exc_type in ("ModuleNotFoundError", "ImportError"):
        module = _extract_module_name(exc_msg)
        if module and module.split(".")[0].lower() not in _STDLIB_MODULES:
            return LABEL_HALLUCINATION, f"Fabricated module: {exc_msg}", exc_type
        return LABEL_GROUNDED_ERROR, exc_msg, exc_type

    # --- Fabricated attribute / method ---
    if exc_type == "AttributeError":
        return LABEL_HALLUCINATION, f"Fabricated attribute: {exc_msg}", exc_type

    # --- Fabricated keyword argument name ---
    if exc_type == "TypeError" and "unexpected keyword argument" in exc_msg:
        return LABEL_HALLUCINATION, f"Fabricated keyword argument: {exc_msg}", exc_type

    # --- Fabricated identifier (NameError) ---
    if exc_type == "NameError":
        name = _extract_undefined_name(exc_msg)
        # If the name closely resembles something already in the code it's
        # probably a typo → GROUNDED_ERROR.  Otherwise → HALLUCINATION.
        if name and not _is_likely_typo(name, code):
            return LABEL_HALLUCINATION, f"Fabricated name: {exc_msg}", exc_type
        return LABEL_GROUNDED_ERROR, exc_msg, exc_type

    # --- Test assertion failed: code ran but produced wrong output ---
    if exc_type == "AssertionError":
        return LABEL_GROUNDED_ERROR, "Test assertion failed: wrong output", exc_type

    # --- Syntax / indentation errors ---
    if exc_type in ("SyntaxError", "IndentationError", "TabError"):
        return LABEL_GROUNDED_ERROR, exc_msg, exc_type

    # --- All other runtime errors: real construct used incorrectly ---
    return LABEL_GROUNDED_ERROR, f"{exc_type}: {exc_msg}", exc_type


def _parse_exception(stderr: str) -> Tuple[Optional[str], str]:
    """Return (ExceptionType, message) from the last line of a traceback."""
    lines = [l.strip() for l in stderr.splitlines() if l.strip()]
    if not lines:
        return None, ""
    last = lines[-1]
    if ":" in last:
        exc_type, _, exc_msg = last.partition(":")
        return exc_type.strip(), exc_msg.strip()
    return last, ""


def _extract_module_name(msg: str) -> Optional[str]:
    m = re.search(r"No module named '([^']+)'", msg)
    return m.group(1) if m else None


def _extract_undefined_name(msg: str) -> Optional[str]:
    m = re.search(r"name '([^']+)' is not defined", msg)
    return m.group(1) if m else None


def _is_likely_typo(name: str, code: str) -> bool:
    """
    Return True if *name* closely resembles an identifier already present in
    *code* (suggesting a misspelling rather than pure fabrication).
    """
    import difflib
    identifiers = set(re.findall(r'\b[A-Za-z_]\w*\b', code))
    return bool(difflib.get_close_matches(name, identifiers, n=1, cutoff=0.82))
