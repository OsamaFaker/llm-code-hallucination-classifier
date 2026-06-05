import ast
import inspect
import importlib
import builtins
from typing import Optional, Set, Dict, Any
from src.plugin_registry import CheckerPlugin
from src.models import ClassificationResult, HallucinationCategory, SeverityLevel

# Safe-import allowlist: standard library and prototype-used modules
SAFE_MODULES: Set[str] = {
    "os", "sys", "json", "math", "datetime", "re", "collections",
    "itertools", "functools", "pathlib", "random", "time", "urllib",
    "hashlib", "base64", "csv", "tempfile", "shutil", "glob", "io",
    "pickle", "inspect", "ast", "typing"
}

class SignatureCheckerPlugin(CheckerPlugin):
    """
    Static checker that introspects runtime signatures of builtins and stdlib
    functions to catch argument errors, applying the GT-existence framework:

    HALLUCINATION — keyword argument name does not exist in the function's
      Ground Truth signature (unexpected keyword argument).
      Example: open("f", base=10) — 'base' is fabricated.

    GROUNDED_ERROR — the function exists and the parameter structure is known,
      but the call violates the arity or positional-argument rules.
      Example: pow(2, 3, 4, 5) — too many positional arguments.
    """

    @property
    def name(self) -> str:
        return "signature"

    @property
    def priority(self) -> int:
        # Runs after arity(75) and attribute(85) but before semantic(95)
        # Note: Higher priority runs first. To run AFTER arity/attribute, 
        # it should have a LOWER priority value. 
        # But the brief says "after ... but before semantic".
        # If Semantic(95) runs first, then Signature should be > 95? 
        # Or if the brief implies logical flow (parser -> static -> semantic),
        # we will set it to 72 to sit between Arity(75) and Misuse(70).
        return 72

    def check(self, code: str, **kwargs) -> Optional[ClassificationResult]:
        ast_tree = kwargs.get("ast_tree")
        if ast_tree is None:
            try:
                ast_tree = ast.parse(code)
            except SyntaxError:
                return None

        visitor = SignatureVisitor()
        visitor.visit(ast_tree)

        if visitor.found_error:
            # GT-existence split: an unexpected keyword argument is a fabricated
            # parameter (HALLUCINATION); any other signature violation (wrong arity,
            # missing required arg) is a real construct used incorrectly (GROUNDED_ERROR).
            is_fake_kwarg = "unexpected keyword argument" in visitor.found_error
            return ClassificationResult(
                is_valid=False,
                is_grounded_error=not is_fake_kwarg,
                hallucination_category=HallucinationCategory.PARAMETER if is_fake_kwarg else None,
                explanation=visitor.found_error,
                confidence=0.98,
                severity=SeverityLevel.HIGH,
                checker_source="signature",
                line=visitor.found_line,
                bad_token=visitor.found_token
            )
        return None

class SignatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.found_error: Optional[str] = None
        self.found_line: Optional[int] = None
        self.found_token: Optional[str] = None
        self.local_defs: Set[str] = set()

    def visit_FunctionDef(self, node):
        self.local_defs.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.local_defs.add(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Task 2: Detect result = sorted pattern (bare reference to builtin)
        if isinstance(node.value, ast.Name):
            builtin_name = node.value.id
            if hasattr(builtins, builtin_name) and callable(getattr(builtins, builtin_name)):
                if builtin_name not in self.local_defs:
                    self.found_error = f"Signature Error: Builtin callable '{builtin_name}' assigned without parentheses (Bare reference)."
                    self.found_line = node.lineno
                    self.found_token = builtin_name
                    return
        self.generic_visit(node)

    def visit_Call(self, node):
        if self.found_error: return
        
        # 1. Resolve callee
        callee_obj = None
        display_name = ""

        if isinstance(node.func, ast.Name):
            display_name = node.func.id
            if display_name in self.local_defs:
                # Skip user-defined functions
                pass
            elif hasattr(builtins, display_name):
                callee_obj = getattr(builtins, display_name)
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            module_name = node.func.value.id
            attr_name = node.func.attr
            display_name = f"{module_name}.{attr_name}"
            
            if module_name in SAFE_MODULES:
                try:
                    mod = importlib.import_module(module_name)
                    callee_obj = getattr(mod, attr_name)
                except (ImportError, AttributeError, ValueError):
                    pass

        if callee_obj and callable(callee_obj):
            # 2. Extract literal arguments for binding
            args = []
            kwargs = {}
            
            # We use None as placeholders for non-literals to check parameter names/counts
            for arg in node.args:
                if isinstance(arg, ast.Constant):
                    args.append(arg.value)
                else:
                    args.append(None)
            
            for kw in node.keywords:
                if kw.arg:
                    if isinstance(kw.value, ast.Constant):
                        kwargs[kw.arg] = kw.value.value
                    else:
                        kwargs[kw.arg] = None
                else:
                    # **kwargs unpacking - skip signature check as it's dynamic
                    self.generic_visit(node)
                    return

            # 3. Verify signature
            try:
                sig = inspect.signature(callee_obj)
                sig.bind_partial(*args, **kwargs)
            except TypeError as e:
                self.found_error = f"Signature Error in call to '{display_name}': {str(e)}"
                self.found_line = node.lineno
                self.found_token = display_name
                return
            except ValueError:
                # Some builtins don't support inspect.signature
                pass

        self.generic_visit(node)
