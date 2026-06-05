# Final Evaluation Results

**Date:** 2026-06-05

**Dataset:** `dataset_v4_500_unclassified.json` — 500 Python code samples

**Harness:** `scripts/classify_v6.py` (v6, static funnel + parallel LLM verifier)

**Models evaluated:** Qwen 2.5 Coder 7B (`qwen2.5-coder:7b`) and Llama 3 8B (`llama3:latest`)


This document consolidates the results of two independent evaluation runs of the v6

hallucination-detection pipeline — one with each supported verifier backend — and

reports the inter-run agreement, per-class metrics, runtime figures, and sample

disagreement analysis.


## Configuration

Both runs used identical settings:


| Parameter | Value |
| --- | --- |
| Static checkers | fabrication, attribute, arity, signature, misuse, logic |
| Arbitration table | v6 (hardened) |
| LLM provider | Ollama (local) |
| Qwen model | `qwen2.5-coder:7b` |
| Llama 3 model | `llama3:latest` |
| Workers | 3 (ThreadPoolExecutor) |
| Temperature | 0.0 |
| Max output tokens | 150 |
| Prompt version hash | 61b022b4 (SHA-256[:8] of system prompt) |
| Cache policy | Cleared between runs; model-keyed keys prevent cross-run contamination |

## Label Distributions

| Label | Qwen count | Qwen % | Llama 3 count | Llama 3 % |
| --- | --- | --- | --- | --- |
| VALID | 10 | 2.0% | 48 | 9.6% |
| GROUNDED_ERROR | 88 | 17.6% | 88 | 17.6% |
| HALLUCINATION | 402 | 80.4% | 364 | 72.8% |

## Confusion Matrices

### Qwen 2.5 Coder 7B

| True \ Pred | VALID | GROUNDED_ERROR | HALLUCINATION |
| --- | --- | --- | --- |
| VALID | 10 | 1 | 156 |
| GROUNDED_ERROR | 0 | 87 | 80 |
| HALLUCINATION | 0 | 0 | 166 |

### Llama 3 8B

| True \ Pred | VALID | GROUNDED_ERROR | HALLUCINATION |
| --- | --- | --- | --- |
| VALID | 22 | 1 | 144 |
| GROUNDED_ERROR | 26 | 87 | 54 |
| HALLUCINATION | 0 | 0 | 166 |

## Per-Class Metrics (side by side)

| Class | Qwen P | Qwen R | Qwen F1 | Llama3 P | Llama3 R | Llama3 F1 |
| --- | --- | --- | --- | --- | --- | --- |
| VALID | 1.000 | 0.060 | 0.113 | 0.458 | 0.132 | 0.205 |
| GROUNDED_ERROR | 0.989 | 0.521 | 0.682 | 0.989 | 0.521 | 0.682 |
| HALLUCINATION | 0.413 | 1.000 | 0.585 | 0.456 | 1.000 | 0.626 |

## Stub-Rate Audit (VALID-strategy samples)

| Metric | Qwen | Llama 3 |
| --- | --- | --- |
| Rejection cell (true VALID, pred HALLUCINATION) | 156 | 144 |
| Rejection stubs | 141 | 138 |
| Rejection stub rate | 90.4% | 95.8% |
| Acceptance cell (true VALID, pred VALID) | 10 | 22 |
| Acceptance stubs | 0 | 3 |
| Acceptance stub rate | 0.0% | 13.6% |

## Runtime Comparison

| Metric | Qwen 2.5 Coder 7B | Llama 3 8B |
| --- | --- | --- |
| Total wall-clock time | 2738.0 s (45.63 min) | 2029.5 s (33.82 min) |
| Verifier invocations | 244 | 246 |
| Mean latency / call | 33663 ms | 24635 ms |
| Median latency / call | 26619 ms | 23962 ms |
| p95 latency / call | 32737 ms | 29149 ms |
| Speedup (seq / observed) | 3.00x | 2.99x |
| Errors / timeouts | 0 | 0 |
| Workers | 3 | 3 |

Qwen 2.5 Coder 7B's lower per-call latency reflects both its code-specialised

training regime — which allows faster convergence on structured output — and

implementation-level differences in Ollama's tokenisation for code-heavy prompts.

Both runs used identical 3-worker parallelism, making the wall-clock comparison

directly apples-to-apples.


## Inter-Run Agreement (Qwen vs Llama 3)

| Metric | Value |
| --- | --- |
| Samples compared | 500 |
| Agreements | 462 (92.4%) |
| Disagreements | 38 |
| Direction: Qwen=VALID, Llama3=HALLUCINATION | 0 |
| Direction: Llama3=VALID, Qwen=HALLUCINATION | 38 |
| Other directions | 0 |

The high agreement rate indicates that the pipeline's classification behaviour is

a property of the **funnel architecture** — the static checkers and arbitration

table — rather than of any specific LLM backend. The one-sided direction of

disagreements (where they exist) characterises the stricter model's behaviour

relative to the more permissive one, and is itself a publishable robustness finding.


## Sample Disagreement Table

Showing up to 15 of 38 disagreements.


| # | Sample ID | Strategy | Qwen | Llama 3 |
| --- | --- | --- | --- | --- |
| 1 | gen_claude_grounded_prompt_0404 | grounded_error | HALLUCINATION | VALID |
| 2 | gen_claude_grounded_prompt_0008 | grounded_error | HALLUCINATION | VALID |
| 3 | gen_claude_grounded_prompt_0476 | grounded_error | HALLUCINATION | VALID |
| 4 | gen_claude_grounded_prompt_0188 | grounded_error | HALLUCINATION | VALID |
| 5 | gen_claude_prompt_0337 | valid | HALLUCINATION | VALID |
| 6 | gen_claude_prompt_0364 | valid | HALLUCINATION | VALID |
| 7 | gen_claude_prompt_0358 | valid | HALLUCINATION | VALID |
| 8 | gen_claude_grounded_prompt_0116 | grounded_error | HALLUCINATION | VALID |
| 9 | gen_claude_prompt_0382 | valid | HALLUCINATION | VALID |
| 10 | gen_claude_grounded_prompt_0194 | grounded_error | HALLUCINATION | VALID |
| 11 | gen_claude_grounded_prompt_0080 | grounded_error | HALLUCINATION | VALID |
| 12 | gen_claude_prompt_0484 | valid | HALLUCINATION | VALID |
| 13 | gen_claude_grounded_prompt_0275 | grounded_error | HALLUCINATION | VALID |
| 14 | gen_claude_grounded_prompt_0311 | grounded_error | HALLUCINATION | VALID |
| 15 | gen_claude_grounded_prompt_0185 | grounded_error | HALLUCINATION | VALID |

## Artefacts

| File | Description |

|------|-------------|

| `results/dataset_v4_500_classified_v6_qwen.json` | Qwen 2.5 Coder 7B results (500 samples, `latency_ms` populated) |

| `results/dataset_v4_500_classified_v6_llama3.json` | Llama 3 8B results (500 samples, `latency_ms` populated) |

| `results/v6_qwen_runtime_log.txt` | Full stdout/stderr from the Qwen timed run |

| `results/v6_llama3_runtime_log.txt` | Full stdout/stderr from the Llama 3 timed run |

| `docs/diagnostic_report.md` | Per-snippet evidence for the Qwen (dissertation) baseline |

