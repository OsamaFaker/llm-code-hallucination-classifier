import ast
import keyword
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Complete set of Python built-in names that are valid as free function calls.
# Any name NOT in this set and not locally defined is routed to __main__
# for fabrication checking.  Keeping this complete prevents false positives
# on valid calls like bool(), dict(), int(), set(), etc.
# ---------------------------------------------------------------------------
KNOWN_BUILTINS: frozenset = frozenset({
    # Core functions
    "print", "input", "len", "range", "type", "isinstance", "issubclass",
    "hasattr", "getattr", "setattr", "delattr", "callable",
    "iter", "next", "enumerate", "zip", "map", "filter",
    "sorted", "reversed", "min", "max", "sum", "abs", "round", "pow",
    "open", "repr", "format", "id", "hash",
    "hex", "oct", "bin", "chr", "ord",
    "vars", "dir", "globals", "locals", "help",
    "any", "all", "breakpoint",
    "compile", "exec", "eval",
    "staticmethod", "classmethod", "property",
    "super", "object",
    # Type constructors (the primary source of the 14 false positives)
    "bool", "int", "float", "complex",
    "str", "bytes", "bytearray", "memoryview",
    "list", "tuple", "dict", "set", "frozenset",
    "slice",
    # Exception constructors
    "Exception", "BaseException",
    "ValueError", "TypeError", "KeyError", "IndexError",
    "AttributeError", "RuntimeError", "StopIteration",
    "NotImplementedError", "OverflowError", "ZeroDivisionError",
    "FileNotFoundError", "IOError", "OSError", "PermissionError",
    "ImportError", "ModuleNotFoundError", "NameError", "RecursionError",
    "MemoryError", "SystemError", "SystemExit", "KeyboardInterrupt",
    "GeneratorExit", "ArithmeticError", "LookupError",
    "UnicodeError", "UnicodeDecodeError", "UnicodeEncodeError",
    "AssertionError", "EOFError", "ConnectionError", "TimeoutError",
    # Singleton constants
    "NotImplemented", "Ellipsis",
})

class ConstructExtractor(ast.NodeVisitor):
    def __init__(self):
        self.extracted_calls: List[Dict[str, Any]] = []
        self.extracted_imports: List[Dict[str, Any]] = []
        self.aliases: Dict[str, str] = {}
        self.local_vars: set = set()
        
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.local_vars.add(target.id)
        self.generic_visit(node)
        
    def visit_FunctionDef(self, node):
        self.local_vars.add(node.name)
        # Track all parameter names so obj.method() calls on parameters
        # are routed to __main__ rather than treated as module names.
        # Fixes: def f(lst): lst.add(x)  ->  was routing as module='lst'
        for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            self.local_vars.add(arg.arg)
        if node.args.vararg:
            self.local_vars.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.local_vars.add(node.args.kwarg.arg)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef
        
    def visit_ClassDef(self, node):
        self.local_vars.add(node.name)
        self.generic_visit(node)

    def visit_For(self, node):
        # Track for-loop target variables: `for item in lst:` -> add 'item'
        if isinstance(node.target, ast.Name):
            self.local_vars.add(node.target.id)
        elif isinstance(node.target, ast.Tuple):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    self.local_vars.add(elt.id)
        self.generic_visit(node)

    visit_AsyncFor = visit_For
        
    def visit_Import(self, node):
        for alias in node.names:
            self.extracted_imports.append({'module': alias.name, 'line': node.lineno})
            self.aliases[alias.asname or alias.name] = alias.name
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        if node.module:
            self.extracted_imports.append({'module': node.module, 'line': node.lineno})
            for alias in node.names:
                self.aliases[alias.asname or alias.name] = node.module
        self.generic_visit(node)
        
    def visit_Subscript(self, node):
        target_name = ""
        if isinstance(node.value, ast.Attribute) and isinstance(node.value.value, ast.Name):
            target_name = f"{node.value.value.id}.{node.value.attr}"
        elif isinstance(node.value, ast.Name):
            target_name = node.value.id
            
        key_name = ""
        if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
            key_name = node.slice.value
            
        if key_name:
            if target_name in ('os.environ', 'environ'):
                self.extracted_calls.append({'module': 'os', 'method': 'environ', 'kwargs': [], 'arg_values': [key_name], 'line': node.lineno})
            else:
                self.extracted_calls.append({'module': '__main__', 'method': target_name, 'kwargs': [], 'arg_values': [key_name], 'line': node.lineno})
        self.generic_visit(node)
        
    def visit_Call(self, node):
        arg_values = []
        for arg in node.args:
            if isinstance(arg, ast.Constant):
                arg_values.append(arg.value)
            elif hasattr(ast, 'UnaryOp') and isinstance(arg, ast.UnaryOp) and isinstance(arg.op, ast.USub):
                if isinstance(arg.operand, ast.Constant) and isinstance(arg.operand.value, (int, float)):
                    arg_values.append(-arg.operand.value)
                    
        kwargs_passed = []
        for kw in node.keywords:
            if kw.arg is not None:
                kwargs_passed.append(kw.arg)
            if isinstance(kw.value, ast.Constant):
                arg_values.append(kw.value.value)

        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                raw_module = node.func.value.id
                
                # Enhance #2 & #8: Track Local Variables & Implicit locals
                if raw_module in self.local_vars or raw_module in ('cursor', 'data', 'df', 'res'):
                    module_name = '__main__'
                elif raw_module == 'arr':
                    module_name = 'builtins.list'
                else:
                    module_name = self.aliases.get(raw_module, raw_module)
                    
                method_name = node.func.attr
                self.extracted_calls.append({'module': module_name, 'method': method_name, 'kwargs': kwargs_passed, 'arg_values': arg_values, 'line': node.lineno})
            elif isinstance(node.func.value, ast.Constant) and isinstance(node.func.value.value, str):
                self.extracted_calls.append({'module': 'builtins.str', 'method': node.func.attr, 'kwargs': kwargs_passed, 'arg_values': arg_values, 'line': node.lineno})
            elif isinstance(node.func.value, ast.Call):
                # Chained calls: e.g. LR().fit(X, y) or Counter().most_common()
                inner = node.func.value
                if isinstance(inner.func, ast.Name):
                    resolved = self.aliases.get(inner.func.id, inner.func.id)
                    if inner.func.id in self.local_vars:
                        resolved = '__main__'
                    method_name = node.func.attr
                    self.extracted_calls.append({'module': resolved, 'method': method_name, 'kwargs': kwargs_passed, 'arg_values': arg_values, 'line': node.lineno})
                
        elif isinstance(node.func, ast.Name):
            func_id = node.func.id
            if func_id in KNOWN_BUILTINS:
                mod = 'builtins'
            elif func_id in self.aliases:
                # Imported name: e.g. `from collections import Counter` → mod = 'collections'
                mod = self.aliases[func_id]
            else:
                mod = '__main__'
            self.extracted_calls.append({'module': mod, 'method': func_id, 'kwargs': kwargs_passed, 'arg_values': arg_values, 'line': node.lineno})
            
        self.generic_visit(node)

def _triage_syntax_error(exc: SyntaxError) -> str:
    """
    Classify a SyntaxError as 'grounded' or 'hallucinated'.

    - grounded:     the offending token is a misspelling of a real Python keyword
                    (edit distance <= 2).  Condition 2: valid-world construct,
                    wrong composition.
    - hallucinated: the token bears no resemblance to any keyword — it is a
                    fabricated language construct.  Condition 3.
    """
    offending = ""
    if exc.text and exc.offset:
        text = exc.text
        offset = max(0, exc.offset - 1)  # convert 1-based to 0-based
        # Walk back to start of identifier
        start = offset
        while start > 0 and (text[start - 1].isalnum() or text[start - 1] == '_'):
            start -= 1
        # Walk forward to end of identifier
        end = offset
        while end < len(text) and (text[end].isalnum() or text[end] == '_'):
            end += 1
        offending = text[start:end].strip()

    if not offending:
        return "grounded"  # No identifiable token — default to grounded

    all_keywords = set(keyword.kwlist) | {"True", "False", "None", "async", "await", "match", "case"}

    # Exact match — it IS a keyword used in the wrong place: grounded
    if offending in all_keywords:
        return "grounded"

    # Edit-distance check against all Python keywords
    def _edit_dist(a: str, b: str) -> int:
        if len(a) < len(b):
            return _edit_dist(b, a)
        if not b:
            return len(a)
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a):
            curr = [i + 1]
            for j, cb in enumerate(b):
                curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
            prev = curr
        return prev[-1]

    min_dist = min(_edit_dist(offending.lower(), kw.lower()) for kw in all_keywords)
    if min_dist <= 2:
        return "grounded"   # Near-miss: likely a misspelled real keyword

    return "hallucinated"   # Clearly fabricated token not resembling any keyword


def parse_generated_code(code_string: str) -> ConstructExtractor:
    extractor = ConstructExtractor()
    extractor.syntax_error = False
    extractor.syntax_error_kind = None  # 'grounded' | 'hallucinated' | None
    extractor.ast_tree = None  # Store parsed tree for reuse by downstream checkers
    try:
        tree = ast.parse(code_string)
        extractor.ast_tree = tree
        extractor.visit(tree)
    except SyntaxError as e:
        extractor.syntax_error = True
        extractor.syntax_error_kind = _triage_syntax_error(e)
        extractor.syntax_error_line = e.lineno
        extractor.syntax_error_offset = e.offset
        extractor.syntax_error_text = e.text
    except Exception:
        pass
    return extractor
