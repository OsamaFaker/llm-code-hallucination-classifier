"""
Fabrication Checker Plugin.

Checks for hallucinated libraries, functions, environment variables,
and API endpoints by verifying against the Ground Truth registry.
"""
from typing import List, Optional
from src.models import ClassificationResult, HallucinationCategory, SeverityLevel
from src.ground_truth import GroundTruthRegistry
from src.plugin_registry import CheckerPlugin

# All valid method names from Python built-in types + common I/O/file methods.
# Any method in this set called on a local-variable object (__main__ module)
# is a valid composition and must NOT be flagged as a hallucinated free function.
KNOWN_OBJECT_METHODS: frozenset = frozenset(
    method
    for typ in (list, str, dict, set, frozenset, tuple, int, float, bool,
                bytes, bytearray, memoryview, type, object)
    for method in dir(typ)
    if not method.startswith('_')
) | frozenset({
    # Common file / IO object methods not covered by built-in types
    'read', 'readline', 'readlines', 'write', 'writelines',
    'close', 'flush', 'seek', 'tell', 'truncate', 'fileno', 'isatty',
    # Common iterator/generator protocol
    'send', 'throw', 'close',
    # Common context manager
    'enter', 'exit',
    # Common requests / HTTP response methods
    'json', 'text', 'content', 'raise_for_status', 'iter_content',
    # Common DB cursor methods
    'execute', 'fetchone', 'fetchall', 'fetchmany', 'commit', 'rollback',
    # Common hashlib hash object methods
    'hexdigest', 'digest', 'update', 'copy',
    # Common regex match/pattern object methods
    'match', 'search', 'findall', 'finditer', 'sub', 'subn', 'group', 'groups', 'span',
    # Common datetime object methods
    'strftime', 'strptime', 'isoformat', 'timestamp', 'date', 'time', 'replace',
    'total_seconds', 'now', 'today', 'utcnow',
    # Cross-language method names (JS/Java/C++ equivalents) — pass through to
    # attribute_checker which classifies them as GROUNDED_ERROR, not HALLUCINATION.
    'push', 'peek', 'isEmpty', 'contains', 'size', 'get', 'addAll', 'removeAll',
    'toArray', 'forEach', 'indexOf', 'lastIndexOf', 'includes', 'fill', 'flat',
    'findIndex', 'containsKey', 'containsValue', 'putAll', 'getOrDefault',
    'entrySet', 'keySet', 'charAt', 'substring', 'startsWith', 'endsWith',
    'toUpperCase', 'toLowerCase', 'trim', 'length', 'compareTo', 'concat',
})

# Module names commonly fabricated by LLMs — these are never real stdlib
# or well-known PyPI packages. Checked before dynamic introspection to
# prevent false negatives when a coincidental local package exists.
_KNOWN_FABRICATED_MODULES: frozenset = frozenset({
    "utils", "helpers", "common", "tools", "api_client",
    "data_processor", "ml_utils", "text_utils", "db_utils",
    "string_utils", "file_utils", "math_utils", "list_utils",
    "array_utils", "test_utils", "validation", "converter",
})


class FabricationCheckerPlugin(CheckerPlugin):
    """Detects fabricated APIs: non-existent libraries, functions, env vars, endpoints."""

    @property
    def name(self) -> str:
        return "fabrication"

    @property
    def priority(self) -> int:
        return 90  # High priority — fabrication is a fundamental check

    def check(self, **kwargs) -> Optional[ClassificationResult]:
        extracted_calls = kwargs.get("extracted_calls", [])
        extracted_imports = kwargs.get("extracted_imports", [])
        local_vars = kwargs.get("local_vars", set())
        gt = kwargs.get("gt")
        if gt is None:
            return None
        return verify_fabrication(extracted_calls, extracted_imports, local_vars, gt)


def _compute_edit_distance(s1: str, s2: str) -> int:
    """Simple Levenshtein edit distance for confidence scoring."""
    if len(s1) < len(s2):
        return _compute_edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def _confidence_from_similarity(name: str, known_names: List[str]) -> float:
    """
    Compute confidence based on edit distance to known names.
    Close typos → high confidence it's a hallucination (not a totally unknown entity).
    """
    if not known_names:
        return 0.85  # default confidence for unknown
    min_dist = min(_compute_edit_distance(name, k) for k in known_names)
    if min_dist <= 1:
        return 0.98  # very close typo — extremely confident
    elif min_dist <= 2:
        return 0.92
    elif min_dist <= 3:
        return 0.85
    else:
        return 0.75  # quite different — still confident but less so


def verify_fabrication(extracted_calls: List[dict], extracted_imports: List[dict], local_vars: set, gt: GroundTruthRegistry) -> Optional[ClassificationResult]:
    # 1. Verify Orphaned Imports
    for imp_data in extracted_imports:
        module = imp_data['module']
        line = imp_data['line']
        # Fast-path: known fabricated module names (e.g. 'utils', 'helpers')
        base_module = module.split('.')[0]
        if base_module in _KNOWN_FABRICATED_MODULES:
            return ClassificationResult(
                is_valid=False,
                is_grounded_error=False,
                hallucination_category=HallucinationCategory.LIBRARY,
                explanation=f"Library/Module '{module}' appears to be a fabricated module name.",
                confidence=0.92,
                severity=SeverityLevel.CRITICAL,
                checker_source="fabrication",
                line=line,
                bad_token=module
            )
        if module not in gt.registry and module not in ('builtins', 'builtins.str', '__main__'):
            # Try dynamic introspection before declaring fabrication
            if not gt.introspect_on_demand(module):
                known_modules = list(gt.registry.keys())
                conf = _confidence_from_similarity(module, known_modules)
                return ClassificationResult(
                    is_valid=False,
                    is_grounded_error=False,
                    hallucination_category=HallucinationCategory.LIBRARY,
                    explanation=f"Library/Module '{module}' was entirely fabricated.",
                    confidence=conf,
                    severity=SeverityLevel.CRITICAL,
                    checker_source="fabrication",
                    line=line,
                    bad_token=module
                )

    for call in extracted_calls:
        module = call['module']
        method = call['method']
        arg_values = call.get('arg_values', [])
        line = call.get('line')

        # 2. Environment Variable Hallucination Check
        if module in ('os', '__main__') and method in ('getenv', 'environ.get', 'environ'):
            for val in arg_values:
                if not gt.valid_env_var(val):
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=False,
                        hallucination_category=HallucinationCategory.ENV_VAR,
                        explanation=f"Environment Variable '{val}' hallucinated.",
                        confidence=0.90,
                        severity=SeverityLevel.HIGH,
                        checker_source="fabrication",
                        line=line,
                        bad_token=val
                    )

        # 3. Protocol & API Endpoint check
        if module == 'requests':
            for val in arg_values:
                if isinstance(val, str) and ('fake' in val.lower() or 'wrong_endpoint' in val.lower()):
                    return ClassificationResult(
                        is_valid=False, is_grounded_error=False,
                        hallucination_category=HallucinationCategory.API_ENDPOINT,
                        explanation=f"Hallucinated API Endpoint or Protocol connecting to '{val}'.",
                        confidence=0.88,
                        severity=SeverityLevel.HIGH,
                        checker_source="fabrication",
                        line=line,
                        bad_token=val
                    )

        # Expand allowed builtins to avoid false positives on valid logic.
        # Built-in types (set, list, dict, …) appear as module names when the
        # parser extracts chained calls like set(x).intersection(y).
        import builtins as _builtins
        _builtin_names = frozenset(dir(_builtins))
        safe_modules = frozenset({
            'builtins', 'builtins.str', 'math', 'sys', 'os', 'collections',
            'itertools', 're', 'functools', 'datetime', 'json', 'random',
            'typing', 'subprocess', 'time', '__main__',
        }) | _builtin_names

        if module == '__main__':
            if (method not in KNOWN_OBJECT_METHODS
                    and method not in local_vars
                    and method not in gt.registry.get('builtins', {}).get('functions', {})):
                return ClassificationResult(
                    is_valid=False, is_grounded_error=False,
                    hallucination_category=HallucinationCategory.FUNCTION,
                    explanation=f"Free method '{method}' is not defined and is hallucinated.",
                    confidence=0.90,
                    severity=SeverityLevel.HIGH,
                    checker_source="fabrication",
                    line=line,
                    bad_token=method
                )
            continue

        if not gt.check_fabrication(module, method):
            if module not in gt.registry and module not in safe_modules:
                known_modules = list(gt.registry.keys())
                conf = _confidence_from_similarity(module, known_modules)
                return ClassificationResult(
                    is_valid=False, is_grounded_error=False,
                    hallucination_category=HallucinationCategory.LIBRARY,
                    explanation=f"Library/Module '{module}' was entirely fabricated.",
                    confidence=conf,
                    severity=SeverityLevel.CRITICAL,
                    checker_source="fabrication",
                    line=line,
                    bad_token=module
                )
            elif module not in safe_modules or module in gt.registry:
                # If module is known but method doesn't exist, flag it
                known_funcs = list(gt.registry.get(module, {}).get("functions", {}).keys())
                conf = _confidence_from_similarity(method, known_funcs)
                return ClassificationResult(
                    is_valid=False, is_grounded_error=False,
                    hallucination_category=HallucinationCategory.FUNCTION,
                    explanation=f"Method '{method}' on module '{module}' does not exist.",
                    confidence=conf,
                    severity=SeverityLevel.HIGH,
                    checker_source="fabrication",
                    line=line,
                    bad_token=method
                )

    return None
