# Prototype_v6 — Hallucination Detection Pipeline

A static-plus-semantic pipeline that classifies Python code samples as
`VALID`, `GROUNDED_ERROR`, or `HALLUCINATION`. The pipeline runs a series
of static checkers (fabrication, attribute, arity, signature, misuse, logic)
followed by an LLM-based semantic verifier for any sample that clears the
static funnel.

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) running locally on port 11434
- At least one supported verifier model pulled (see below)

Install Python dependencies (if a `requirements.txt` is present):

```
pip install -r requirements.txt
```

---

## Reproducing the evaluation

### Quick start

```
python scripts/classify_v6.py
```

This runs the full 500-sample evaluation with the default model
(`qwen2.5-coder:7b`) and writes results to
`results/dataset_v4_500_classified_v6_qwen.json`.

You can also invoke the harness directly from the project root, in which
case the output is written to the current directory:

```
python classify_unclassified_v6.py
```

---

### Choosing the verifier model

The harness supports two verifier backends via the `--model` flag:

| Flag | Ollama model | Character |
|------|-------------|-----------|
| `--model qwen` *(default)* | `qwen2.5-coder:7b` | Code-specialised, faster per call, dissertation baseline |
| `--model llama3` | `llama3:latest` | General-purpose, broader name recognition in the LLM literature |

**Trade-offs.** `qwen2.5-coder:7b` is optimised for code-related tasks and
was selected as the dissertation baseline because it applies more precise
prompt-fidelity checks. `llama3:latest` is a general-purpose model that is
more widely cited and easier to contextualise for readers unfamiliar with
code-specialised variants. Both models were run on the full 500-sample dataset; the two runs agreed on
**93.4% of labels** (467/500), so users should expect highly similar but not
identical results between the two models.

**Pull the models before running:**

```
ollama pull qwen2.5-coder:7b
ollama pull llama3:latest
```

**Run with each model:**

```
python scripts/classify_v6.py --model qwen
python scripts/classify_v6.py --model llama3
```

Output files are written to `results/` and named after the model so
successive runs do not overwrite each other:

- `results/dataset_v4_500_classified_v6_qwen.json`
- `results/dataset_v4_500_classified_v6_llama3.json`

If you pass an unrecognised model name the harness exits immediately and
prints the list of accepted values. If the requested model is not installed
in Ollama the harness exits and prints the exact `ollama pull` command to
run.

---

### Additional flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `qwen` | Verifier model (`qwen` or `llama3`) |
| `--output PATH` | auto | Override the output JSON path |
| `--workers N` | `3` | Parallel LLM-verifier workers. Fewer workers reduce memory pressure on constrained hardware; more workers may improve throughput when sufficient memory is available. |

**Example — Llama 3 with 2 workers and a custom output path:**

```
python scripts/classify_v6.py --model llama3 --workers 2 --output my_llama3_run.json
```

---

## Cache behaviour

Verifier responses are cached in `src/llm_cache.json`. The cache key
encodes the system-prompt version, the model identifier, and the
prompt+code content, so results from different models are stored
separately and never mixed. Deleting or clearing `src/llm_cache.json`
forces a full fresh run (required for latency benchmarking).

---

## Output schema

Each entry in the output JSON file contains the original sample fields plus:

| Field | Type | Description |
|-------|------|-------------|
| `predicted_label` | string | `VALID`, `GROUNDED_ERROR`, or `HALLUCINATION` |
| `confidence` | float | Combined pipeline confidence (0–1) |
| `checker_source` | string | Which component produced the verdict |
| `verifier_justification` | string | One-sentence LLM justification (LLM-verified samples only) |
| `latency_ms` | float | Per-call LLM latency in milliseconds (0 for static-funnel samples) |
| `taxonomy_tag` | string | Fine-grained classification tag |

---

## Results

Both models were evaluated on `dataset_v4_500_unclassified.json` (500 Python
code samples, ground truth derived from `generation_strategy`). Full metrics
are in [`results/FINAL_RESULTS.md`](results/FINAL_RESULTS.md) (regenerate with
`scripts/compute_final_results.py`).

### Label distribution

| Label | Qwen 2.5 Coder 7B | Llama 3 8B |
|-------|-------------------|------------|
| VALID | 10 (2.0%) | 48 (9.6%) |
| GROUNDED_ERROR | 88 (17.6%) | 88 (17.6%) |
| HALLUCINATION | 402 (80.4%) | 364 (72.8%) |

### Per-class F1

| Class | Qwen P | Qwen R | Qwen F1 | Llama 3 P | Llama 3 R | Llama 3 F1 |
|-------|--------|--------|---------|-----------|-----------|------------|
| VALID | 1.000 | 0.060 | 0.113 | 0.458 | 0.132 | 0.205 |
| GROUNDED_ERROR | 0.989 | 0.521 | 0.682 | 0.989 | 0.521 | 0.682 |
| HALLUCINATION | 0.413 | 1.000 | 0.585 | 0.456 | 1.000 | 0.626 |

HALLUCINATION recall is **100%** for both models (166/166 true hallucinations
caught); the pipeline never misses an injected hallucination. GROUNDED_ERROR
F1 is identical at **0.682** across both backends, confirming that verdict is
dominated by the static funnel rather than the LLM backend choice.

### Runtime

| Model | Wall-clock | Verifier calls | Mean latency/call | Speedup |
|-------|-----------|----------------|-------------------|---------|
| `qwen2.5-coder:7b` | 45.63 min | 244 | 33,663 ms | 3.00× |
| `llama3:latest` | 33.82 min | 246 | 24,635 ms | 2.99× |

Both runs used 3 parallel workers (`ThreadPoolExecutor`). Zero errors or
timeouts in either run.

### Inter-run agreement

**462/500 (92.4%).** All 38 disagreements are one-directional: Qwen predicted
HALLUCINATION where Llama 3 predicted VALID — consistent with Qwen applying
stricter prompt-fidelity checks. See `results/FINAL_RESULTS.md` for the full
disagreement table.

---

## Utility scripts

| Script | Purpose |
|--------|---------|
| `scripts/classify_v6.py` | Recommended entrypoint — runs the evaluation and writes results to `results/` |
| `scripts/compute_final_results.py` | Computes confusion matrices, per-class metrics, inter-run agreement and writes `results/FINAL_RESULTS.md` (requires both model result files) |
| `scripts/export_diagnostic_report.py` | Generates a per-snippet diagnostic Markdown table from a result file |
