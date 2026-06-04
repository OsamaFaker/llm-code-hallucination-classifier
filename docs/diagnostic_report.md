# Diagnostic Classification Report (v6)
Source: `results/dataset_v4_500_classified_v6_qwen.json`

## 1. Classification Overview
| ID | Manual Strategy | Predicted Label | Short Reason | Conf | Line | Bad Token |
|---|---|---|---|---|---|---|
| gen_claude_prompt_0493 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0150 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_prompt_0136 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0469 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0160 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0217 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0446 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'pow': too many positional arguments | 0.98 | 2 | `pow` |
| gen_claude_grounded_prompt_0128 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0223 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0500 | grounded_error | GROUNDED_ERROR | Grounded Error: SyntaxError caused by incorrect use of a real Python keyword. | 0.95 | 2 | `None` |
| gen_claude_prompt_0210 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0246 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0277 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0146 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0438 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0178 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0105 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0490 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0131 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'base' in builtins.int(). | 0.95 | 2 | `base` |
| gen_claude_grounded_prompt_0254 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0330 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0461 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0368 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_prompt_0168 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_prompt_0022 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0387 | hallucination | HALLUCINATION | Library/Module 'autoprocess' was entirely fabricated. | 0.75 | 1 | `autoprocess` |
| gen_claude_grounded_prompt_0248 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0185 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0236 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0134 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0388 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0487 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0170 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_prompt_0124 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0335 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0064 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_prompt_0303 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0205 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0182 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0454 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0108 | hallucination | HALLUCINATION | Library/Module 'smartlib' was entirely fabricated. | 0.75 | 1 | `smartlib` |
| gen_claude_grounded_prompt_0152 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_prompt_0463 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_grounded_prompt_0032 | grounded_error | GROUNDED_ERROR | Grounded Error: SyntaxError caused by incorrect use of a real Python keyword. | 0.95 | 2 | `None` |
| gen_claude_prompt_0192 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0418 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_prompt_0424 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0479 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0026 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_grounded_prompt_0011 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0265 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0289 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0318 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_grounded_prompt_0410 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'step' in builtins.range(). | 0.95 | 2 | `step` |
| gen_claude_prompt_0151 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0098 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_grounded_prompt_0392 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'sorted': got an unexpected keyword argument 'order' | 0.98 | 2 | `sorted` |
| gen_claude_prompt_0394 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0361 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0075 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0041 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0111 | hallucination | HALLUCINATION | Library/Module 'pyutils_plus' was entirely fabricated. | 0.75 | 1 | `pyutils_plus` |
| gen_claude_prompt_0112 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0481 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0013 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0280 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0413 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_grounded_prompt_0065 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0123 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0360 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0283 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0405 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0377 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0021 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0222 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0225 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0062 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0003 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0140 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper()' called with 1 positional argument(s) but accepts at most 0 (TypeErr... | 0.92 | 2 | `upper` |
| gen_claude_prompt_0382 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0034 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0019 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0327 | hallucination | HALLUCINATION | Library/Module 'autoprocess' was entirely fabricated. | 0.75 | 1 | `autoprocess` |
| gen_claude_grounded_prompt_0239 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'sorted': got an unexpected keyword argument 'direction' | 0.98 | 2 | `sorted` |
| gen_claude_prompt_0189 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0276 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0036 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0268 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0279 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0079 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0232 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0053 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_grounded_prompt_0287 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0122 | grounded_error | GROUNDED_ERROR | Grounded Error: 'sorted()' kwarg 'key' must be callable but got string literal 'length' (TypeErro... | 0.91 | 2 | `key` |
| gen_claude_grounded_prompt_0047 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0286 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0301 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0258 | hallucination | HALLUCINATION | Library/Module 'datahelper' was entirely fabricated. | 0.75 | 1 | `datahelper` |
| gen_claude_prompt_0183 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0466 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0191 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0087 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0212 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'pow': too many positional arguments | 0.98 | 2 | `pow` |
| gen_claude_prompt_0060 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0256 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0470 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_grounded_prompt_0014 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0180 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0460 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0440 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_prompt_0115 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0177 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0208 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0319 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0045 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0468 | hallucination | HALLUCINATION | Library/Module 'codetools' was entirely fabricated. | 0.75 | 1 | `codetools` |
| gen_claude_prompt_0285 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0475 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0094 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0233 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0025 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0302 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.strip()' called with 2 positional argument(s) but accepts at most 1 (TypeErr... | 0.92 | 2 | `strip` |
| gen_claude_prompt_0456 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0200 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_grounded_prompt_0284 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0204 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0374 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper()' called with 1 positional argument(s) but accepts at most 0 (TypeErr... | 0.92 | 2 | `upper` |
| gen_claude_grounded_prompt_0095 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0397 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0473 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'sorted': got an unexpected keyword argument 'direction' | 0.98 | 2 | `sorted` |
| gen_claude_grounded_prompt_0467 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_prompt_0007 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0055 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0465 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0290 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0229 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0260 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0443 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0054 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0414 | hallucination | HALLUCINATION | Library/Module 'strutils' was entirely fabricated. | 0.75 | 1 | `strutils` |
| gen_claude_prompt_0430 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 1.00 | whole snippet | `` |
| gen_claude_prompt_0348 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0199 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0038 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0400 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0433 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0219 | hallucination | HALLUCINATION | Library/Module 'numpy_extended' was entirely fabricated. | 0.75 | 1 | `numpy_extended` |
| gen_claude_grounded_prompt_0341 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_grounded_prompt_0308 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0399 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0125 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_prompt_0436 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0297 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0332 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0024 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0396 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0452 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0052 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0345 | hallucination | HALLUCINATION | Library/Module 'pyutils_plus' was entirely fabricated. | 0.75 | 1 | `pyutils_plus` |
| gen_claude_prompt_0061 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0391 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_grounded_prompt_0215 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0389 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0359 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0009 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_grounded_prompt_0401 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.insert()' called with 1 positional argument(s) but requires at least 2 (Typ... | 0.90 | 2 | `insert` |
| gen_claude_prompt_0448 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0110 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0162 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0195 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0071 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0104 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0255 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0043 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0166 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0226 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0353 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0118 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0174 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0381 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0272 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_grounded_prompt_0035 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_grounded_prompt_0137 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0417 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0261 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0202 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0298 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0429 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0292 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0089 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0018 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0365 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'base' in builtins.int(). | 0.95 | 2 | `base` |
| gen_claude_grounded_prompt_0455 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.lower()' called with 1 positional argument(s) but accepts at most 0 (TypeErr... | 0.92 | 2 | `lower` |
| gen_claude_prompt_0372 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0373 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0227 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0127 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0181 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0077 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0267 | hallucination | HALLUCINATION | Library/Module 'pyutils_plus' was entirely fabricated. | 0.75 | 1 | `pyutils_plus` |
| gen_claude_grounded_prompt_0299 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0263 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0153 | hallucination | HALLUCINATION | Library/Module 'strutils' was entirely fabricated. | 0.75 | 1 | `strutils` |
| gen_claude_prompt_0492 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0179 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_prompt_0486 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0340 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0058 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_grounded_prompt_0155 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0355 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0093 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0156 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0312 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0380 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0480 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0135 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0224 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_prompt_0339 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0306 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0082 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0161 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0408 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0259 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0084 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0310 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0444 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0076 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0422 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_grounded_prompt_0002 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0351 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0426 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0231 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_grounded_prompt_0164 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0249 | hallucination | HALLUCINATION | Library/Module 'datahelper' was entirely fabricated. | 0.75 | 1 | `datahelper` |
| gen_claude_prompt_0316 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0114 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0271 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0357 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0005 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'sorted': got an unexpected keyword argument 'direction' | 0.98 | 2 | `sorted` |
| gen_claude_grounded_prompt_0221 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.lower()' called with 1 positional argument(s) but accepts at most 0 (TypeErr... | 0.92 | 2 | `lower` |
| gen_claude_prompt_0207 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0145 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0313 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0119 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0242 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_grounded_prompt_0101 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0187 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_prompt_0432 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0442 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0439 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0176 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'step' in builtins.range(). | 0.95 | 2 | `step` |
| gen_claude_prompt_0264 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0453 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0474 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_prompt_0354 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0328 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0383 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.pop()' called with 2 positional argument(s) but accepts at most 1 (TypeErro... | 0.92 | 2 | `pop` |
| gen_claude_prompt_0321 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0364 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0296 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_grounded_prompt_0008 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_prompt_0144 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0103 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0305 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0091 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0201 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0384 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0063 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0147 | hallucination | HALLUCINATION | Library/Module 'datahelper' was entirely fabricated. | 0.75 | 1 | `datahelper` |
| gen_claude_prompt_0031 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0020 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0027 | hallucination | HALLUCINATION | Library/Module 'datahelper' was entirely fabricated. | 0.75 | 1 | `datahelper` |
| gen_claude_prompt_0346 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0090 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0184 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0194 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0293 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.append()' called with 2 positional argument(s) but accepts at most 1 (TypeE... | 0.92 | 2 | `append` |
| gen_claude_grounded_prompt_0173 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_grounded_prompt_0437 | grounded_error | GROUNDED_ERROR | Grounded Error: 'round()' argument 2 must be int but got str literal (TypeError: wrong argument t... | 0.91 | 2 | `round` |
| gen_claude_prompt_0069 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0478 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0307 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0431 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0117 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0033 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0012 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0096 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0253 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0344 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0230 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0196 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0193 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0317 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0270 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0245 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_prompt_0130 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0252 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0126 | hallucination | HALLUCINATION | Library/Module 'graphlib_plus' was entirely fabricated. | 0.75 | 1 | `graphlib_plus` |
| gen_claude_prompt_0370 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0088 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_prompt_0367 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0472 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0066 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0491 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'default' in builtins.max(). | 0.95 | 2 | `default` |
| gen_claude_prompt_0028 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0251 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_prompt_0496 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0419 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0001 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_grounded_prompt_0314 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_grounded_prompt_0329 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0247 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0074 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0042 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0420 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0198 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0458 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_prompt_0457 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0163 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0278 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0274 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0269 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_prompt_0291 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0004 | valid | GROUNDED_ERROR | Grounded Error: SyntaxError caused by incorrect use of a real Python keyword. | 0.95 | 1 | `None` |
| gen_claude_prompt_0378 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0241 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0167 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.insert()' called with 1 positional argument(s) but requires at least 2 (Typ... | 0.90 | 2 | `insert` |
| gen_claude_prompt_0294 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0495 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0366 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_grounded_prompt_0485 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_prompt_0213 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0309 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0175 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0016 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0350 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0385 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_grounded_prompt_0311 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0218 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0216 | hallucination | HALLUCINATION | Library/Module 'autoprocess' was entirely fabricated. | 0.75 | 1 | `autoprocess` |
| gen_claude_grounded_prompt_0086 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0092 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0097 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0416 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0462 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0375 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0288 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0235 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0169 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0073 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0139 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0257 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'default' in builtins.max(). | 0.95 | 2 | `default` |
| gen_claude_grounded_prompt_0281 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0211 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0159 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0282 | hallucination | HALLUCINATION | Library/Module 'autoprocess' was entirely fabricated. | 0.75 | 1 | `autoprocess` |
| gen_claude_grounded_prompt_0113 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'len': too many positional arguments | 0.98 | 2 | `len` |
| gen_claude_grounded_prompt_0395 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_grounded_prompt_0158 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'sorted': got an unexpected keyword argument 'order' | 0.98 | 2 | `sorted` |
| gen_claude_grounded_prompt_0398 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0403 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0326 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0423 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0379 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0477 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0324 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0220 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0203 | grounded_error | GROUNDED_ERROR | Grounded Error: 'round()' argument 2 must be int but got str literal (TypeError: wrong argument t... | 0.91 | 2 | `round` |
| gen_claude_grounded_prompt_0488 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_grounded_prompt_0107 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_grounded_prompt_0266 | grounded_error | GROUNDED_ERROR | Grounded Error: SyntaxError caused by incorrect use of a real Python keyword. | 0.95 | 2 | `None` |
| gen_claude_prompt_0006 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0129 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0141 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0102 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0371 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0325 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0100 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0412 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0116 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0484 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0447 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0352 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0085 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0499 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_prompt_0051 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0402 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0356 | grounded_error | GROUNDED_ERROR | Grounded Error: 'sorted()' kwarg 'key' must be callable but got string literal 'length' (TypeErro... | 0.91 | 2 | `key` |
| gen_claude_prompt_0057 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0498 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0415 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0390 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0209 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0228 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0483 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0315 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_grounded_prompt_0320 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0262 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0234 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0434 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0109 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_grounded_prompt_0494 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0048 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0411 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0409 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0030 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0322 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0044 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0068 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.strip()' called with 2 positional argument(s) but accepts at most 1 (TypeErr... | 0.92 | 2 | `strip` |
| gen_claude_prompt_0250 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0059 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.append()' called with 2 positional argument(s) but accepts at most 1 (TypeE... | 0.92 | 2 | `append` |
| gen_claude_grounded_prompt_0476 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0197 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'sorted' assigned without parentheses (Bare reference). | 0.98 | 2 | `sorted` |
| gen_claude_prompt_0363 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0342 | hallucination | HALLUCINATION | Library/Module 'strutils' was entirely fabricated. | 0.75 | 1 | `strutils` |
| gen_claude_prompt_0154 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0435 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0333 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0445 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0186 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0349 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0015 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0070 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0106 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0081 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0295 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0386 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.sort' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `sort` |
| gen_claude_grounded_prompt_0056 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_grounded_prompt_0449 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_grounded_prompt_0464 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0273 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0451 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0347 | grounded_error | GROUNDED_ERROR | Signature Error in call to 'len': too many positional arguments | 0.98 | 2 | `len` |
| gen_claude_prompt_0121 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0080 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.upper' accessed without calling it (line 2). Missing parentheses '()' — retu... | 0.87 | 2 | `upper` |
| gen_claude_prompt_0190 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0323 | grounded_error | GROUNDED_ERROR | Signature Error: Builtin callable 'len' assigned without parentheses (Bare reference). | 0.98 | 2 | `len` |
| gen_claude_grounded_prompt_0206 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0120 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0067 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0240 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0406 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0428 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0029 | grounded_error | GROUNDED_ERROR | Grounded Error: 'dict.add' does not exist (line 2). 'add' is a valid method of ['set'] but not of... | 0.91 | 2 | `add` |
| gen_claude_prompt_0300 | hallucination | HALLUCINATION | Library/Module 'strutils' was entirely fabricated. | 0.75 | 1 | `strutils` |
| gen_claude_grounded_prompt_0050 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0148 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0083 | grounded_error | GROUNDED_ERROR | Grounded Error: 'int.reverse' does not exist (line 2). 'reverse' is a valid method of ['list', 'b... | 0.91 | 2 | `reverse` |
| gen_claude_prompt_0441 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0471 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0017 | grounded_error | GROUNDED_ERROR | Logic Error [Math]: Static division by zero detected. | 1.00 | 2 | `/` |
| gen_claude_prompt_0171 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0331 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0238 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0393 | hallucination | HALLUCINATION | Library/Module 'datahelper' was entirely fabricated. | 0.75 | 1 | `datahelper` |
| gen_claude_grounded_prompt_0023 | grounded_error | GROUNDED_ERROR | Grounded Error: Invalid keyword argument 'default' in builtins.max(). | 0.95 | 2 | `default` |
| gen_claude_prompt_0450 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0072 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0244 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0237 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0165 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0010 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0336 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0243 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0427 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0404 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0188 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0337 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.80 | whole snippet | `` |
| gen_claude_grounded_prompt_0143 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0459 | hallucination | HALLUCINATION | Library/Module 'sortinglib' was entirely fabricated. | 0.75 | 1 | `sortinglib` |
| gen_claude_prompt_0078 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_grounded_prompt_0497 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0099 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0304 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_grounded_prompt_0362 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0040 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0425 | grounded_error | GROUNDED_ERROR | Grounded Error: 'str.pop' does not exist (line 2). 'pop' is a valid method of ['list', 'dict', 's... | 0.91 | 2 | `pop` |
| gen_claude_grounded_prompt_0275 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0358 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0334 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0142 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0046 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0049 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0149 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.pop()' called with 2 positional argument(s) but accepts at most 1 (TypeErro... | 0.92 | 2 | `pop` |
| gen_claude_grounded_prompt_0407 | grounded_error | GROUNDED_ERROR | Grounded Error: 'list.push' does not exist (line 2). 'push' is a valid method in other languages ... | 0.89 | 2 | `push` |
| gen_claude_prompt_0133 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0338 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0369 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0489 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0039 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0157 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0132 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0214 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0343 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0376 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0421 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_prompt_0138 | hallucination | HALLUCINATION | Library/Module 'fileio' was entirely fabricated. | 0.75 | 1 | `fileio` |
| gen_claude_prompt_0037 | valid | VALID | Valid code: perfectly adheres to GT and Semantic Intent. | 1.00 | None | `None` |
| gen_claude_prompt_0172 | valid | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |
| gen_claude_grounded_prompt_0482 | grounded_error | HALLUCINATION | Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: T... | 0.90 | whole snippet | `` |

## 2. Code Appendix (Low Confidence / Misclassified Samples)

### Sample gen_claude_prompt_0493 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not engage with binomial coefficients.
- **Verifier Justification:** The code is a generic passthrough function and does not engage with binomial coefficients.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0136 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the prompt's task.
- **Verifier Justification:** The code is a generic passthrough function and does not address the prompt's task.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0469 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code returns the input list unchanged, ignoring the prompt's request for prefixes.
- **Verifier Justification:** The code returns the input list unchanged, ignoring the prompt's request for prefixes.

```python
def return_prefixes(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0160 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not perform modulo division of two lists using map and lambda.
- **Verifier Justification:** The code does not perform modulo division of two lists using map and lambda.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0217 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not remove duplicate words; it simply returns a copy of the input list.
- **Verifier Justification:** The code does not remove duplicate words; it simply returns a copy of the input list.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0223 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to check if strings are rotations of each other.
- **Verifier Justification:** The code does not attempt to check if strings are rotations of each other.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0277 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code performs a passthrough operation and does not engage with bitwise XOR.
- **Verifier Justification:** The code performs a passthrough operation and does not engage with bitwise XOR.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0178 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code simply returns the input list unchanged without performing any calculations.
- **Verifier Justification:** The code simply returns the input list unchanged without performing any calculations.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0490 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code performs a list copy instead of finding the maximum element.
- **Verifier Justification:** The code performs a list copy instead of finding the maximum element.

```python
def return_maximum(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0022 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not use regex and instead returns the input unchanged.
- **Verifier Justification:** The code does not use regex and instead returns the input unchanged.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0248 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to use regex but instead uses string methods incorrectly.
- **Verifier Justification:** The code attempts to use regex but instead uses string methods incorrectly.

```python
def write_function(s):
    return s.find('x', 'start')  # TypeError: find() arg 2 must be int, not str
```

### Sample gen_claude_grounded_prompt_0185 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to split a string, not find a triplet sum.
- **Verifier Justification:** The code attempts to split a string, not find a triplet sum.

```python
def write_function(s):
    return s.split(maxsplit=2, sep=' ')  # TypeError: wrong kwarg name; should be sep, not sep=
```

### Sample gen_claude_prompt_0388 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0487 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the problem of finding the maximum volume of a cuboid with a given sum of sides.
- **Verifier Justification:** The code is a generic passthrough function and does not address the problem of finding the maximum volume of a cuboid with a given sum of sides.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0124 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address finding the focus of a parabola.
- **Verifier Justification:** The code is a generic passthrough function and does not address finding the focus of a parabola.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0205 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of finding minimum swaps between binary strings.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of finding minimum swaps between binary strings.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0454 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code defines a function named 'fibonacci' but implements the Fibonacci sequence, not the Tribonacci sequence as requested.
- **Verifier Justification:** The code defines a function named 'fibonacci' but implements the Fibonacci sequence, not the Tribonacci sequence as requested.

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

### Sample gen_claude_prompt_0424 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of checking month names.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of checking month names.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0265 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern and does not address the task of removing matching tuples.
- **Verifier Justification:** The code is a generic passthrough pattern and does not address the task of removing matching tuples.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0289 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to copy a list but does not convert it to a tuple.
- **Verifier Justification:** The code attempts to copy a list but does not convert it to a tuple.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0151 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to convert camel case to snake case.
- **Verifier Justification:** The code does not attempt to convert camel case to snake case.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0394 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0361 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def think_remember(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0041 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to sum a list with a string, which is incorrect.
- **Verifier Justification:** The code attempts to sum a list with a string, which is incorrect.

```python
def write_function(lst):
    return sum(lst, "0")  # TypeError: sum() start arg must be number, not str
```

### Sample gen_claude_prompt_0112 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code simply returns the input list unchanged without checking for divisibility.
- **Verifier Justification:** The code simply returns the input list unchanged without checking for divisibility.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0481 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0013 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to return a list copy instead of concatenating elements into a string.
- **Verifier Justification:** The code attempts to return a list copy instead of concatenating elements into a string.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0280 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of finding the length of the shortest word.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of finding the length of the shortest word.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0283 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to count the frequency of elements in a list, not lists of lists.
- **Verifier Justification:** The code attempts to count the frequency of elements in a list, not lists of lists.

```python
from collections import Counter
def element_frequency(lst):
    return dict(Counter(lst))
```

### Sample gen_claude_prompt_0382 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code counts the frequency of all elements, not just the smallest one.
- **Verifier Justification:** The code counts the frequency of all elements, not just the smallest one.

```python
from collections import Counter
def element_frequency(lst):
    return dict(Counter(lst))
```

### Sample gen_claude_prompt_0034 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of summing digits.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of summing digits.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0019 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to return the input unchanged, which is unrelated to converting tuple strings to integer tuples.
- **Verifier Justification:** The code attempts to return the input unchanged, which is unrelated to converting tuple strings to integer tuples.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0268 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not attempt to calculate the area of a trapezium.
- **Verifier Justification:** The code is a generic passthrough function and does not attempt to calculate the area of a trapezium.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0079 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0232 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to extract the index of the minimum value record from tuples.
- **Verifier Justification:** The code does not attempt to extract the index of the minimum value record from tuples.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0287 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the summation of tuple elements in a given tuple list.
- **Verifier Justification:** The code does not attempt to find the summation of tuple elements in a given tuple list.

```python
def write_function(n):
    while n > 0:  # Bug: n never modified — infinite loop
        if n % 2 == 0:
            return True
    return False
```

### Sample gen_claude_prompt_0286 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The function counts elements in a list, not the frequency of characters in a text.
- **Verifier Justification:** The function counts elements in a list, not the frequency of characters in a text.

```python
from collections import Counter
def element_frequency(lst):
    return dict(Counter(lst))
```

### Sample gen_claude_prompt_0301 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of checking if the product of numbers is even.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of checking if the product of numbers is even.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0466 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the task of checking if a month name contains 28 days.
- **Verifier Justification:** The code is a generic passthrough function and does not address the task of checking if a month name contains 28 days.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0256 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not attempt to find the second smallest number.
- **Verifier Justification:** The code is a generic passthrough that does not attempt to find the second smallest number.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0014 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to check odd indices of a list for odd numbers.
- **Verifier Justification:** The code does not attempt to check odd indices of a list for odd numbers.

```python
def write_python(s):
    return s.find('x', 'start')  # TypeError: find() arg 2 must be int, not str
```

### Sample gen_claude_prompt_0460 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0115 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough and does not address the task of checking if a triangle is scalene.
- **Verifier Justification:** The code is a generic passthrough and does not address the task of checking if a triangle is scalene.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0208 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern that does not address the task of clearing tuple values.
- **Verifier Justification:** The code is a generic passthrough pattern that does not address the task of clearing tuple values.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0319 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not address the task of removing empty tuples from a list.
- **Verifier Justification:** The code does not address the task of removing empty tuples from a list.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0475 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0094 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0025 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address finding the third side of a right-angled triangle.
- **Verifier Justification:** The code is a generic passthrough function and does not address finding the third side of a right-angled triangle.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0284 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to count the number of elements in a list but does not address finding minimum value indices.
- **Verifier Justification:** The code attempts to count the number of elements in a list but does not address finding minimum value indices.

```python
def write_function(lst):
    return lst.count()  # TypeError: count() takes exactly 1 argument
```

### Sample gen_claude_grounded_prompt_0095 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to find the index of 0 in a list, which is unrelated to calculating the sum of positive integers.
- **Verifier Justification:** The code attempts to find the index of 0 in a list, which is unrelated to calculating the sum of positive integers.

```python
def write_function(lst):
    return lst.index(0, 'start', 'end')  # TypeError: index() slice args must be int
```

### Sample gen_claude_prompt_0397 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough and does not address regex extraction from URLs.
- **Verifier Justification:** The code is a generic passthrough and does not address regex extraction from URLs.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0007 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0055 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0229 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not attempt to calculate the surface area of a cube.
- **Verifier Justification:** The code is a generic passthrough function and does not attempt to calculate the surface area of a cube.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0260 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to separate and print numbers and their positions in a string.
- **Verifier Justification:** The code does not attempt to separate and print numbers and their positions in a string.

```python
def write_function(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_prompt_0430 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 1.0000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough and does not address the task of finding minimum number swaps required to make two binary strings equal.
- **Verifier Justification:** The code is a generic passthrough and does not address the task of finding minimum number swaps required to make two binary strings equal.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0199 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code copies the input list to a new list and returns it, which is unrelated to summing numbers from 1 to n.
- **Verifier Justification:** The code copies the input list to a new list and returns it, which is unrelated to summing numbers from 1 to n.

```python
def sum_to_n_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0400 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code counts element frequencies but does not count equal element pairs.
- **Verifier Justification:** The code counts element frequencies but does not count equal element pairs.

```python
from collections import Counter
def element_frequency(lst):
    return dict(Counter(lst))
```

### Sample gen_claude_prompt_0433 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0436 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0332 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the minimum sum of factors of a given number.
- **Verifier Justification:** The code does not attempt to find the minimum sum of factors of a given number.

```python
def write_python(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_prompt_0052 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not engage with rounding numbers or calculating the sum.
- **Verifier Justification:** The code does not engage with rounding numbers or calculating the sum.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0061 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of accepting strings containing all vowels.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of accepting strings containing all vowels.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0215 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not address the task of summing squared numbers in a list after rounding to the ceiling.
- **Verifier Justification:** The code does not address the task of summing squared numbers in a list after rounding to the ceiling.

```python
def given_list(n):
    while n > 0:  # Bug: n never modified — infinite loop
        if n % 2 == 0:
            return True
    return False
```

### Sample gen_claude_grounded_prompt_0359 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the longest subsequence with adjacent differences of one.
- **Verifier Justification:** The code does not attempt to find the longest subsequence with adjacent differences of one.

```python
def write_function(n):
    while n > 0:  # Bug: n never modified — infinite loop
        if n % 2 == 0:
            return True
    return False
```

### Sample gen_claude_prompt_0448 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to return the input list unchanged, which is unrelated to counting non-empty substrings.
- **Verifier Justification:** The code attempts to return the input list unchanged, which is unrelated to counting non-empty substrings.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0071 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find multiples of n; instead, it checks if n is even and returns True or False.
- **Verifier Justification:** The code does not attempt to find multiples of n; instead, it checks if n is even and returns True or False.

```python
def write_function(n):
    while n > 0:  # Bug: n never modified — infinite loop
        if n % 2 == 0:
            return True
    return False
```

### Sample gen_claude_grounded_prompt_0104 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to check if all items in a list are equal to a given string.
- **Verifier Justification:** The code does not attempt to check if all items in a list are equal to a given string.

```python
def write_function(d):
    return d.get('x', default=None)  # TypeError: get() takes no keyword args
```

### Sample gen_claude_prompt_0043 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the task of finding the lateral surface area of a cylinder.
- **Verifier Justification:** The code is a generic passthrough function and does not address the task of finding the lateral surface area of a cylinder.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0166 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not address removing duplicates from the tuple.
- **Verifier Justification:** The code is a generic passthrough that does not address removing duplicates from the tuple.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0226 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern and does not address the task of left rotating a string.
- **Verifier Justification:** The code is a generic passthrough pattern and does not address the task of left rotating a string.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0118 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not calculate standard deviation.
- **Verifier Justification:** The code is a generic passthrough function that does not calculate standard deviation.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0202 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0298 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code uses Python's built-in sort function, not radix sort.
- **Verifier Justification:** The code uses Python's built-in sort function, not radix sort.

```python
def sort_list(lst):
    return sorted(lst)
```

### Sample gen_claude_prompt_0292 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code performs a list copy, not checking for element presence.
- **Verifier Justification:** The code performs a list copy, not checking for element presence.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0373 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0127 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the sum of an arithmetic progression.
- **Verifier Justification:** The code is a generic passthrough function that does not address the sum of an arithmetic progression.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0181 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0077 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to check even indices of a list.
- **Verifier Justification:** The code does not attempt to check even indices of a list.

```python
def write_python(d):
    return d.values(True)  # TypeError: values() takes no arguments
```

### Sample gen_claude_prompt_0340 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0355 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0082 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0259 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not engage with the prompt's task of dividing two lists using map and lambda.
- **Verifier Justification:** The code is a generic passthrough function that does not engage with the prompt's task of dividing two lists using map and lambda.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0310 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to return a list of characters from the input string, not their ASCII values.
- **Verifier Justification:** The code attempts to return a list of characters from the input string, not their ASCII values.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0076 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to minimize the length of a string by removing occurrences of a single character.
- **Verifier Justification:** The code does not attempt to minimize the length of a string by removing occurrences of a single character.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0316 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to copy the input data to a new list and return it, which is unrelated to finding the length of a string.
- **Verifier Justification:** The code attempts to copy the input data to a new list and return it, which is unrelated to finding the length of a string.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0271 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of finding whether a number is present in an infinite sequence.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of finding whether a number is present in an infinite sequence.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0145 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not engage with bit rotation.
- **Verifier Justification:** The code is a generic passthrough function that does not engage with bit rotation.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0313 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code performs a list copy and does not engage with heap operations.
- **Verifier Justification:** The code performs a list copy and does not engage with heap operations.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0442 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0439 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code returns a copy of the input array without sorting it based on any condition.
- **Verifier Justification:** The code returns a copy of the input array without sorting it based on any condition.

```python
def given_array(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0328 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern that does not address the task of finding the ratio of negative numbers in an array.
- **Verifier Justification:** The code is a generic passthrough pattern that does not address the task of finding the ratio of negative numbers in an array.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0364 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The function checks if a number is prime, not non-prime.
- **Verifier Justification:** The function checks if a number is prime, not non-prime.

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
```

### Sample gen_claude_prompt_0103 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0091 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code simply returns the input list unchanged, ignoring the prompt's instructions.
- **Verifier Justification:** The code simply returns the input list unchanged, ignoring the prompt's instructions.

```python
def function_integers(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0031 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to copy a tuple to a list, which is unrelated to checking for an element's existence.
- **Verifier Justification:** The code attempts to copy a tuple to a list, which is unrelated to checking for an element's existence.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0346 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0184 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to convert camel case to snake case using regex.
- **Verifier Justification:** The code does not attempt to convert camel case to snake case using regex.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0194 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find divisors; it returns a TypeError.
- **Verifier Justification:** The code does not attempt to find divisors; it returns a TypeError.

```python
def write_python(n):
    return abs("negative")  # TypeError: bad operand type for abs(): str
```

### Sample gen_claude_prompt_0478 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0307 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0431 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to test if a string is a palindrome.
- **Verifier Justification:** The code does not attempt to test if a string is a palindrome.

```python
def test_given(n):
    while n > 0:  # Bug: n never modified — infinite loop
        if n % 2 == 0:
            return True
    return False
```

### Sample gen_claude_prompt_0253 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the input and returns it unchanged.
- **Verifier Justification:** The code is a generic passthrough function that ignores the input and returns it unchanged.

```python
def given_positive(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0230 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to find the largest positive number but is completely unrelated to the task.
- **Verifier Justification:** The code attempts to find the largest positive number but is completely unrelated to the task.

```python
def write_python(d):
    return d.keys('prefix')  # TypeError: keys() takes no arguments
```

### Sample gen_claude_prompt_0196 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not address the task of finding the position of the last removed element.
- **Verifier Justification:** The code is a generic passthrough that does not address the task of finding the position of the last removed element.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0193 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to pass through the input data unchanged.
- **Verifier Justification:** The code attempts to pass through the input data unchanged.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0130 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0370 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not sort the list based on the sum of digits.
- **Verifier Justification:** The code does not sort the list based on the sum of digits.

```python
def sort_list(lst):
    return sorted(lst)
```

### Sample gen_claude_prompt_0367 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0472 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0028 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0496 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not address removing duplicates from a list of lists.
- **Verifier Justification:** The code is a generic passthrough that does not address removing duplicates from a list of lists.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0419 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to split a string but does not use regex.
- **Verifier Justification:** The code attempts to split a string but does not use regex.

```python
def write_function(s):
    return s.split(maxsplit=2, sep=' ')  # TypeError: wrong kwarg name; should be sep, not sep=
```

### Sample gen_claude_grounded_prompt_0329 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to find the index of 0 in a list but incorrectly uses string arguments for slice indices.
- **Verifier Justification:** The code attempts to find the index of 0 in a list but incorrectly uses string arguments for slice indices.

```python
def given_list(lst):
    return lst.index(0, 'start', 'end')  # TypeError: index() slice args must be int
```

### Sample gen_claude_prompt_0247 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code simply returns the input list unchanged without removing consecutive duplicates.
- **Verifier Justification:** The code simply returns the input list unchanged without removing consecutive duplicates.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0457 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The function checks if the string contains only allowed characters, not if all characters are unique.
- **Verifier Justification:** The function checks if the string contains only allowed characters, not if all characters are unique.

```python
import re
def is_allowed_chars(s):
    return bool(re.match(r'^[a-zA-Z0-9]+$', s))
```

### Sample gen_claude_prompt_0163 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not attempt to find the slope of a line.
- **Verifier Justification:** The code is a generic passthrough function and does not attempt to find the slope of a line.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0274 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address finding the sublist with minimum length.
- **Verifier Justification:** The code is a generic passthrough function that does not address finding the sublist with minimum length.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0004 (GROUNDED_ERROR)
- **Strategy:** valid
- **Confidence:** 0.9500
- **Full Explanation:** Grounded Error: SyntaxError caused by incorrect use of a real Python keyword.

```python
def you're_given(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0241 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the problem of finding the shortest string with both str1 and str2 as subsequences.
- **Verifier Justification:** The code is a generic passthrough function that does not address the problem of finding the shortest string with both str1 and str2 as subsequences.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0175 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code defines a function that counts the frequency of elements in a list, not their digit sums.
- **Verifier Justification:** The code defines a function that counts the frequency of elements in a list, not their digit sums.

```python
from collections import Counter
def element_frequency(lst):
    return dict(Counter(lst))
```

### Sample gen_claude_prompt_0016 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not attempt to count rectangles in a circle.
- **Verifier Justification:** The code is a generic passthrough function and does not attempt to count rectangles in a circle.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0385 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not address the task of finding the top k integers that occur most frequently using a heap queue algorithm.
- **Verifier Justification:** The code does not address the task of finding the top k integers that occur most frequently using a heap queue algorithm.

```python
def sort_list(lst):
    return sorted(lst)
```

### Sample gen_claude_grounded_prompt_0311 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to filter a dictionary but uses an incorrect method.
- **Verifier Justification:** The code attempts to filter a dictionary but uses an incorrect method.

```python
def filter_given(d):
    return d.values(True)  # TypeError: values() takes no arguments
```

### Sample gen_claude_grounded_prompt_0086 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to replace characters in a string but does not address converting a tuple to a dictionary.
- **Verifier Justification:** The code attempts to replace characters in a string but does not address converting a tuple to a dictionary.

```python
def write_function(text):
    return text.replace('a', 'b', 'c')  # TypeError: replace() takes at most 3 args but 3 given (3rd must be int)
```

### Sample gen_claude_prompt_0097 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough pattern that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0235 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern and does not address the task of checking for at least one letter and one number in a string.
- **Verifier Justification:** The code is a generic passthrough pattern and does not address the task of checking for at least one letter and one number in a string.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0169 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough pattern that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0073 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern that does not address the task of finding the ratio of positive numbers in an array.
- **Verifier Justification:** The code is a generic passthrough pattern that does not address the task of finding the ratio of positive numbers in an array.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0139 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not count negative numbers.
- **Verifier Justification:** The code is a generic passthrough function that does not count negative numbers.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0211 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to copy the input list, not count character occurrences.
- **Verifier Justification:** The code attempts to copy the input list, not count character occurrences.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0403 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0379 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough and does not address the prompt's task.
- **Verifier Justification:** The code is a generic passthrough and does not address the prompt's task.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0220 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def given_positive(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0325 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not attempt to calculate the volume of a cylinder.
- **Verifier Justification:** The code is a generic passthrough function and does not attempt to calculate the volume of a cylinder.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0100 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the task of checking triangle validity.
- **Verifier Justification:** The code is a generic passthrough function and does not address the task of checking triangle validity.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0412 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the problem of finding the minimum number of squares.
- **Verifier Justification:** The code is a generic passthrough function that does not address the problem of finding the minimum number of squares.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0116 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not implement recursion to sum a list.
- **Verifier Justification:** The code does not implement recursion to sum a list.

```python
def write_function(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_prompt_0484 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that returns the input data unchanged.
- **Verifier Justification:** The code is a generic passthrough that returns the input data unchanged.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0352 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough and does not address the task of evaluating whether n can be written as the sum of exactly 4 positive even numbers.
- **Verifier Justification:** The code is a generic passthrough and does not address the task of evaluating whether n can be written as the sum of exactly 4 positive even numbers.

```python
def evaluate_whether(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0085 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the quadratic equation task.
- **Verifier Justification:** The code is a generic passthrough function and does not address the quadratic equation task.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0499 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code sorts a single list but does not find common elements between two lists.
- **Verifier Justification:** The code sorts a single list but does not find common elements between two lists.

```python
def sort_list(lst):
    return sorted(lst)
```

### Sample gen_claude_prompt_0415 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0320 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the area of a sector.
- **Verifier Justification:** The code does not attempt to find the area of a sector.

```python
def write_function(text):
    return text.replace('a', 'b', 'c')  # TypeError: replace() takes at most 3 args but 3 given (3rd must be int)
```

### Sample gen_claude_prompt_0262 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to copy the input list, which is unrelated to generating an MD5 hash.
- **Verifier Justification:** The code attempts to copy the input list, which is unrelated to generating an MD5 hash.

```python
def given_string(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0109 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code sorts the entire list without considering indices divisible by three.
- **Verifier Justification:** The code sorts the entire list without considering indices divisible by three.

```python
def sort_list(lst):
    return sorted(lst)
```

### Sample gen_claude_prompt_0409 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0322 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0044 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the longest bitonic subsequence.
- **Verifier Justification:** The code does not attempt to find the longest bitonic subsequence.

```python
def write_function(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_prompt_0250 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of converting an octal number to a decimal number.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of converting an octal number to a decimal number.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0476 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to remove vowels from a string.
- **Verifier Justification:** The code does not attempt to remove vowels from a string.

```python
def function_that(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_prompt_0154 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code simply returns the input list unchanged without removing duplicates.
- **Verifier Justification:** The code simply returns the input list unchanged without removing duplicates.

```python
def integers_remove(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0445 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of counting integers with an odd number of set bits.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of counting integers with an odd number of set bits.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0349 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0070 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0106 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0295 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0464 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to use the 'keys' method incorrectly.
- **Verifier Justification:** The code attempts to use the 'keys' method incorrectly.

```python
def write_function(d):
    return d.keys('prefix')  # TypeError: keys() takes no arguments
```

### Sample gen_claude_prompt_0451 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that copies the input list without multiplying its items.
- **Verifier Justification:** The code is a generic passthrough that copies the input list without multiplying its items.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0121 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0190 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not insert a string at the beginning of list items.
- **Verifier Justification:** The code is a generic passthrough that does not insert a string at the beginning of list items.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0067 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the maximum sum of a bi-tonic sub-sequence.
- **Verifier Justification:** The code does not attempt to find the maximum sum of a bi-tonic sub-sequence.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0406 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0428 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to find the sum of even numbers at even positions.
- **Verifier Justification:** The code does not attempt to find the sum of even numbers at even positions.

```python
def write_python(n):
    return abs("negative")  # TypeError: bad operand type for abs(): str
```

### Sample gen_claude_grounded_prompt_0050 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to solve a different task (counting elements in a list) rather than the gold mine problem.
- **Verifier Justification:** The code attempts to solve a different task (counting elements in a list) rather than the gold mine problem.

```python
def write_function(lst):
    return lst.count()  # TypeError: count() takes exactly 1 argument
```

### Sample gen_claude_prompt_0148 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the task of checking if two lines are parallel.
- **Verifier Justification:** The code is a generic passthrough function and does not address the task of checking if two lines are parallel.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0331 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0238 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0244 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0010 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def numbers(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0427 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0404 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to print permutations of a string.
- **Verifier Justification:** The code does not attempt to print permutations of a string.

```python
def write_function(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_grounded_prompt_0188 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to extract elements from a two-dimensional list.
- **Verifier Justification:** The code does not attempt to extract elements from a two-dimensional list.

```python
def write_function(lst):
    i = 0
    while i < len(lst):  # Bug: i never incremented — infinite loop
        if lst[i] > 0:
            return lst[i]
    return -1
```

### Sample gen_claude_prompt_0337 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.8000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code calculates the factorial of a number but does not count its digits.
- **Verifier Justification:** The code calculates the factorial of a number but does not count its digits.

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

### Sample gen_claude_grounded_prompt_0143 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not match a word at the beginning of a string.
- **Verifier Justification:** The code does not match a word at the beginning of a string.

```python
def write_function(n):
    while n > 0:  # Bug: n never modified — infinite loop
        if n % 2 == 0:
            return True
    return False
```

### Sample gen_claude_prompt_0040 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0275 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to sum the list with a string, which is incorrect.
- **Verifier Justification:** The code attempts to sum the list with a string, which is incorrect.

```python
def write_function(lst):
    return sum(lst, "0")  # TypeError: sum() start arg must be number, not str
```

### Sample gen_claude_prompt_0358 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not address the task of deleting characters from string s that are in string c and checking if the result is a palindrome.
- **Verifier Justification:** The code does not address the task of deleting characters from string s that are in string c and checking if the result is a palindrome.

```python
import re
def is_allowed_chars(s):
    return bool(re.match(r'^[a-zA-Z0-9]+$', s))
```

### Sample gen_claude_prompt_0334 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0142 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0046 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough pattern that does not address the task of removing words with k length.
- **Verifier Justification:** The code is a generic passthrough pattern that does not address the task of removing words with k length.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0049 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not attempt to find the smallest missing element.
- **Verifier Justification:** The code is a generic passthrough that does not attempt to find the smallest missing element.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0133 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that does not address the task of checking if two arrays are equal.
- **Verifier Justification:** The code is a generic passthrough function that does not address the task of checking if two arrays are equal.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0338 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not attempt to reverse an array.
- **Verifier Justification:** The code does not attempt to reverse an array.

```python
def write_python(d):
    return d.get(item, default=None)  # TypeError: get() takes no keyword args
```

### Sample gen_claude_prompt_0157 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough that does not address moving zeroes to the end.
- **Verifier Justification:** The code is a generic passthrough that does not address moving zeroes to the end.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0214 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to copy the input list rather than solve the subset sum problem.
- **Verifier Justification:** The code attempts to copy the input list rather than solve the subset sum problem.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0343 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0376 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function that ignores the prompt's specifics.
- **Verifier Justification:** The code is a generic passthrough function that ignores the prompt's specifics.

```python
def write_python(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0421 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code does not implement heap sort.
- **Verifier Justification:** The code does not implement heap sort.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_prompt_0172 (HALLUCINATION)
- **Strategy:** valid
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code is a generic passthrough function and does not address the task of finding if a number is a Keith number.
- **Verifier Justification:** The code is a generic passthrough function and does not address the task of finding if a number is a Keith number.

```python
def write_function(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
    return result
```

### Sample gen_claude_grounded_prompt_0482 (HALLUCINATION)
- **Strategy:** grounded_error
- **Confidence:** 0.9000
- **Full Explanation:** Valid code: perfectly adheres to GT and Semantic Intent. Semantic Hallucination [LLM Verified]: The code attempts to find a substring in a string, which is unrelated to dropping empty items from a dictionary.
- **Verifier Justification:** The code attempts to find a substring in a string, which is unrelated to dropping empty items from a dictionary.

```python
def write_function(s):
    return s.find('x', 'start')  # TypeError: find() arg 2 must be int, not str
```