"""
Dynamic Ground Truth Registry via Runtime Introspection.

Uses importlib + inspect to auto-discover function signatures from installed libraries.
Falls back to the static registry for libraries not installed.
Integrates with the caching layer for performance.
"""
from typing import Dict, List, Optional, Set
import importlib
import inspect

from src.cache import GTCache


class GroundTruthRegistry:
    """
    Ground Truth registry that combines a static fallback registry with
    dynamic runtime introspection of installed Python libraries.
    """

    def __init__(self, version: str = "v1", use_dynamic: bool = True):
        self.version = version
        self.use_dynamic = use_dynamic
        self.valid_schema_keys = {"id", "name", "status"}
        self._cache = GTCache()
        self._introspected_modules: Set[str] = set()

        # Temporally-bound deprecation registry: maps (module, func) to lifecycle metadata.
        # Operationalises the temporal constraint of GTenv (Item #7).
        self._deprecation_registry: Dict[tuple, Dict[str, str]] = {
            ("collections", "Callable"):          {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "Mapping"):           {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "MutableMapping"):    {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "Sequence"):          {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "Iterator"):          {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "MutableSequence"):   {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "MutableSet"):        {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("collections", "Iterable"):          {"deprecated_since": "3.3",  "removed_since": "3.10"},
            ("pandas", "DataFrame.append"):       {"deprecated_since": "1.4",  "removed_since": "2.0"},
            ("pandas", "Series.iteritems"):       {"deprecated_since": "1.5",  "removed_since": "2.0"},
            ("pandas", "DataFrame.iteritems"):    {"deprecated_since": "1.5",  "removed_since": "2.0"},
            ("pandas", "DataFrame.swapaxes"):     {"deprecated_since": "2.1",  "removed_since": "3.0"},
            ("numpy", "bool"):                    {"deprecated_since": "1.20", "removed_since": "1.24"},
            ("numpy", "int"):                     {"deprecated_since": "1.20", "removed_since": "1.24"},
            ("numpy", "float"):                   {"deprecated_since": "1.20", "removed_since": "1.24"},
            ("numpy", "complex"):                 {"deprecated_since": "1.20", "removed_since": "1.24"},
            ("numpy", "object"):                  {"deprecated_since": "1.20", "removed_since": "1.24"},
            ("distutils", "core"):                {"deprecated_since": "3.10", "removed_since": "3.12"},
            # Python 3.9+ deprecations — using typing generics instead of typing module aliases
            ("typing", "List"):                   {"deprecated_since": "3.9",  "removed_since": "future"},
            ("typing", "Dict"):                   {"deprecated_since": "3.9",  "removed_since": "future"},
            ("typing", "Tuple"):                  {"deprecated_since": "3.9",  "removed_since": "future"},
            ("typing", "Set"):                    {"deprecated_since": "3.9",  "removed_since": "future"},
            # asyncio removals
            ("asyncio", "coroutine"):             {"deprecated_since": "3.8",  "removed_since": "3.11"},
            ("asyncio", "Task.all_tasks"):        {"deprecated_since": "3.7",  "removed_since": "3.9"},
            # distutils full module
            ("distutils", "distutils"):           {"deprecated_since": "3.10", "removed_since": "3.12"},
        }

        # Static fallback registry (original Prototype2 data)
        self._static_registry: Dict[str, Dict[str, Dict[str, Dict[str, list]]]] = {
            "builtins": {
                "functions": {
                    "open": {"params": ["file", "mode", "buffering", "encoding", "errors", "newline", "closefd", "opener"]},
                    "range": {"params": ["start", "stop", "step"]},
                    "sum": {"params": ["iterable", "start"]},
                    "sorted": {"params": ["iterable", "key", "reverse"]},
                    "print": {"params": ["objects", "sep", "end", "file", "flush"]},
                    "len": {"params": ["obj"]},
                    "type": {"params": ["object"]},
                }
            },
            "builtins.str": {
                "functions": {
                    "lower": {"params": []}, "upper": {"params": []},
                    "replace": {"params": ["old", "new", "count"]},
                    "join": {"params": ["iterable"]},
                    "split": {"params": ["sep", "maxsplit"]},
                    "strip": {"params": ["chars"]}, "lstrip": {"params": ["chars"]}, "rstrip": {"params": ["chars"]},
                    "find": {"params": ["sub", "start", "end"]}, "rfind": {"params": ["sub", "start", "end"]},
                    "index": {"params": ["sub", "start", "end"]},
                    "count": {"params": ["sub", "start", "end"]},
                    "startswith": {"params": ["prefix", "start", "end"]},
                    "endswith": {"params": ["suffix", "start", "end"]},
                    "format": {"params": []}, "format_map": {"params": ["mapping"]},
                    "encode": {"params": ["encoding", "errors"]},
                    "isdigit": {"params": []}, "isalpha": {"params": []}, "isalnum": {"params": []},
                    "isupper": {"params": []}, "islower": {"params": []}, "isspace": {"params": []},
                    "title": {"params": []}, "capitalize": {"params": []}, "swapcase": {"params": []},
                    "center": {"params": ["width", "fillchar"]},
                    "ljust": {"params": ["width", "fillchar"]}, "rjust": {"params": ["width", "fillchar"]},
                    "zfill": {"params": ["width"]},
                    "partition": {"params": ["sep"]}, "rpartition": {"params": ["sep"]},
                    "expandtabs": {"params": ["tabsize"]},
                    "maketrans": {"params": ["x", "y", "z"]}, "translate": {"params": ["table"]},
                }
            },
            "builtins.list": {
                "functions": {
                    "append": {"params": ["object"]}, "extend": {"params": ["iterable"]},
                    "insert": {"params": ["index", "object"]}, "remove": {"params": ["value"]},
                    "pop": {"params": ["index"]}, "clear": {"params": []},
                    "index": {"params": ["value", "start", "stop"]},
                    "count": {"params": ["value"]}, "copy": {"params": []},
                    "sort": {"params": ["key", "reverse"]}, "reverse": {"params": []},
                }
            },
            "requests": {
                "functions": {
                    "get": {"params": ["url", "params", "headers", "timeout", "verify"]},
                    "post": {"params": ["url", "data", "json", "headers", "timeout", "verify"]},
                }
            },
            "os": {
                "functions": {
                    "getenv": {"params": ["key", "default"]},
                    "environ.get": {"params": ["key", "default"]},
                    "environ": {"params": []},
                }
            },
            "pandas": {
                "functions": {
                    "read_csv": {"params": ["filepath_or_buffer", "sep", "header", "names", "index_col"]},
                    "DataFrame": {"params": ["data", "index", "columns", "dtype", "copy"]},
                    "merge": {"params": ["left", "right", "how", "on", "left_on", "right_on"]},
                    "groupby": {"params": ["by", "axis", "level", "as_index", "sort"]},
                    "concat": {"params": ["objs", "axis", "join", "ignore_index"]},
                }
            },
            "numpy": {
                "functions": {
                    "zeros": {"params": ["shape", "dtype", "order"]},
                    "ones": {"params": ["shape", "dtype", "order"]},
                    "array": {"params": ["object", "dtype", "copy", "order", "subok", "ndmin"]},
                }
            },
            "math": {
                "functions": {
                    "sqrt": {"params": ["x"]},
                    "factorial": {"params": ["x"]},
                }
            },
            "json": {
                "functions": {
                    "load": {"params": ["fp", "cls", "object_hook", "parse_float", "parse_int", "parse_constant", "object_pairs_hook"]},
                    "loads": {"params": ["s", "cls", "object_hook", "parse_float", "parse_int", "parse_constant", "object_pairs_hook"]},
                }
            },
        }

        # The combined registry starts as a copy of static
        self.registry = dict(self._static_registry)

        # Dynamically introspect available modules
        if self.use_dynamic:
            self._introspect_installed_modules()

    # -----------------------------------------------------------------
    # Dynamic introspection
    # -----------------------------------------------------------------
    def _introspect_installed_modules(self):
        """Attempt to dynamically introspect modules already in the static registry."""
        introspectable = [
            "builtins",  # Ensures bool, int, dict, set, any, all, super, etc. are all in GTenv
            "math", "json", "os", "collections", "itertools",
            "functools", "pathlib", "re", "datetime", "hashlib",
            "csv", "sqlite3", "io", "typing", "sys",
        ]
        for mod_name in introspectable:
            self._try_introspect(mod_name)

    def _try_introspect(self, module_name: str) -> bool:
        """Try to import and introspect a module, merging results into the registry."""
        if module_name in self._introspected_modules:
            return True
        try:
            mod = importlib.import_module(module_name)
        except ImportError:
            return False

        self._introspected_modules.add(module_name)

        functions = {}
        for name, obj in inspect.getmembers(mod):
            if name.startswith("_"):
                continue
            if inspect.isfunction(obj) or inspect.isbuiltin(obj):
                params = self._extract_params(obj)
                functions[name] = {"params": params}
            elif inspect.isclass(obj):
                # Also introspect class constructors
                params = self._extract_params(obj.__init__) if hasattr(obj, '__init__') else []
                functions[name] = {"params": params}

        if functions:
            if module_name in self.registry:
                # Merge: dynamic overrides static for shared funcs, adds new ones
                existing = self.registry[module_name].get("functions", {})
                existing.update(functions)
                self.registry[module_name]["functions"] = existing
            else:
                self.registry[module_name] = {"functions": functions}

        return True

    @staticmethod
    def _extract_params(obj) -> List[str]:
        """Extract parameter names from a callable using inspect."""
        try:
            sig = inspect.signature(obj)
            return [
                p.name for p in sig.parameters.values()
                if p.name != "self"
            ]
        except (ValueError, TypeError):
            return []

    # Standard library modules safe to introspect on-demand.
    # Third-party packages (sympy, django, flask, etc.) must NOT be introspected
    # because their presence in the local env doesn't mean the classified code's
    # target environment has them — introspecting them causes false negatives.
    _STDLIB_MODULES: frozenset = frozenset({
        "builtins", "math", "json", "os", "sys", "re", "io", "csv",
        "collections", "itertools", "functools", "pathlib", "datetime",
        "hashlib", "sqlite3", "typing", "string", "random", "time",
        "subprocess", "shutil", "glob", "copy", "operator", "decimal",
        "fractions", "statistics", "textwrap", "struct", "enum",
        "abc", "contextlib", "dataclasses", "logging", "unittest",
        "argparse", "configparser", "socket", "threading", "queue",
        "http", "urllib", "html", "xml", "email", "base64", "hmac",
        "secrets", "tempfile", "zipfile", "gzip", "tarfile", "pprint",
        "inspect", "ast", "dis", "token", "tokenize", "traceback",
        "warnings", "weakref", "array", "bisect", "heapq",
    })

    def introspect_on_demand(self, module_name: str) -> bool:
        """
        Dynamically introspect a module that wasn't in the initial list.
        Only introspects stdlib modules to avoid false negatives from
        third-party packages that happen to be installed locally.
        """
        if not self.use_dynamic:
            return False
        base_module = module_name.split('.')[0]
        if base_module not in self._STDLIB_MODULES:
            return False
        return self._try_introspect(module_name)

    # -----------------------------------------------------------------
    # Query API (with caching)
    # -----------------------------------------------------------------
    def check_fabrication(self, module: str, func: str) -> bool:
        """Check if a function exists in a module. Uses cache."""
        cached = self._cache.get_fabrication(module, func)
        if cached is not None:
            return cached

        # Try dynamic introspection first for unknown modules
        if module not in self.registry and self.use_dynamic:
            self.introspect_on_demand(module)

        result = False
        if module in self.registry:
            result = func in self.registry[module].get("functions", {})

        self._cache.put_fabrication(module, func, result)
        return result

    def get_params(self, module: str, func: str) -> Optional[List[str]]:
        """Get parameter list for a function. Uses cache."""
        cached = self._cache.get_params(module, func)
        if cached is not None:
            return cached

        params = None
        if self.check_fabrication(module, func):
            params = self.registry[module]["functions"][func].get("params", [])

        self._cache.put_params(module, func, params)
        return params

    # Comprehensive allowlist of valid environment variables, organised by
    # category.  Any variable NOT in this set is flagged as fabricated.
    _VALID_ENV_VARS: frozenset = frozenset({
        # --- POSIX / Unix standard ---
        "PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL",
        "LC_CTYPE", "TERM", "TMPDIR", "TMP", "TEMP", "DISPLAY", "HOSTNAME",
        "PWD", "OLDPWD", "EDITOR", "VISUAL", "PAGER", "MAIL", "TZ",
        "UID", "EUID", "GROUPS", "OSTYPE", "MACHTYPE", "HOSTTYPE",
        # --- Python-specific ---
        "PYTHONPATH", "PYTHONHOME", "PYTHONDONTWRITEBYTECODE",
        "PYTHONUNBUFFERED", "PYTHONIOENCODING", "PYTHONSTARTUP",
        "PYTHONHASHSEED", "VIRTUAL_ENV", "CONDA_DEFAULT_ENV",
        "CONDA_PREFIX", "PIP_INDEX_URL",
        # --- Common web / application ---
        "PORT", "HOST", "DEBUG", "SECRET_KEY", "API_KEY", "API_SECRET",
        "APP_ENV", "APP_DEBUG", "APP_SECRET", "APP_KEY",
        "DATABASE_URL", "DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD",
        "DB_NAME", "REDIS_URL", "REDIS_HOST", "REDIS_PORT",
        "FLASK_APP", "FLASK_ENV", "FLASK_DEBUG",
        "DJANGO_SETTINGS_MODULE", "DJANGO_SECRET_KEY",
        "NODE_ENV", "NEXT_PUBLIC_API_URL",
        "LOG_LEVEL", "LOGGING_LEVEL",
        # --- Cloud / CI / CD ---
        "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
        "AWS_DEFAULT_REGION", "AWS_REGION", "AWS_PROFILE",
        "GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_CLOUD_PROJECT",
        "GCP_PROJECT", "GCLOUD_PROJECT",
        "AZURE_SUBSCRIPTION_ID", "AZURE_TENANT_ID", "AZURE_CLIENT_ID",
        "AZURE_CLIENT_SECRET",
        "CI", "CI_COMMIT_SHA", "CI_PIPELINE_ID",
        "GITHUB_TOKEN", "GITHUB_ACTIONS", "GITHUB_REF", "GITHUB_SHA",
        "GITHUB_REPOSITORY", "GITHUB_WORKSPACE",
        "GITLAB_CI", "GITLAB_TOKEN",
        "DOCKER_HOST", "DOCKER_CERT_PATH",
        "KUBECONFIG", "KUBERNETES_SERVICE_HOST",
        # --- Authentication / tokens ---
        "TOKEN", "AUTH_TOKEN", "ACCESS_TOKEN", "REFRESH_TOKEN",
        "JWT_SECRET", "JWT_KEY", "SESSION_SECRET",
        "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "HF_TOKEN",
        # --- Email / SMTP ---
        "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
        "EMAIL_HOST", "EMAIL_PORT",
        # --- HTTP ---
        "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy",
    })

    def valid_env_var(self, key: str) -> bool:
        return key in self._VALID_ENV_VARS

    def check_deprecated(self, module: str, func: str, env_version: str = "v1") -> Optional[str]:
        """
        Check if a function/attribute is deprecated or removed.
        Returns a human-readable warning string, or None if the symbol is current.
        env_version is a semantic tag (e.g. 'v1', 'py310', 'pandas2') — reserved
        for future version-aware routing.
        """
        key = (module, func)
        if key in self._deprecation_registry:
            info = self._deprecation_registry[key]
            return (
                f"'{module}.{func}' was deprecated since v{info['deprecated_since']} "
                f"and removed in v{info['removed_since']}."
            )
        return None

    def get_cache_stats(self) -> dict:
        return self._cache.stats.to_dict()
