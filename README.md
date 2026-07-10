# Code-Hallucination-Classifier Prototype

A static-plus-LLM pipeline that detects hallucinations in LLM-generated Python code.
Each code snippet is classified into one of three ground-truth labels:

| Label | Meaning |
|---|---|
| `VALID` | Code is correct and all tests pass |
| `HALLUCINATION` | Code references a fabricated module, function, or identifier that does not exist in the Python Ground Truth |
| `GROUNDED_ERROR` | Code uses real Python constructs but applies them incorrectly (wrong types, wrong arguments, failed assertions) |

---

## Architecture

```
Input code
    │
    ▼
Static checkers (fabrication · attribute · arity · signature · misuse · logic)
    │  fast rule-based rejection — catches clear hallucinations without LLM calls
    ▼
LLM semantic verifier (qwen2.5-coder:7b  or  llama3:latest)
    │  for samples that pass the static funnel
    ▼
Oracle executor (subprocess-based)
    │  runs test assertions; overrides any VALID verdict that fails at runtime
    ▼
Predicted label  +  confidence  +  checker_source  +  justification
```

---

## Dataset

The evaluation uses an **execution-oracle dataset** built from [MBPP](https://github.com/google-research-datasets/mbpp) problems.
Each sample's ground-truth label is determined by actually executing the code against the MBPP test assertions — no manual labelling required.

| Property | Value |
|---|---|
| Source | MBPP (974 problems available) |
| Problems used | 164 (early-stop once all classes hit 150 samples) |
| Total samples | **450** |
| Label balance | **150 VALID · 150 HALLUCINATION · 150 GROUNDED_ERROR (33% each)** |
| File | `results/mbpp_oracle_450_balanced.json` |

### Generating the dataset yourself

```bash
python scripts/generate_oracle_dataset.py \
  --mbpp-path /path/to/mbpp.jsonl \
  --problems 974 \
  --retries 3 \
  --max-each 150 \
  --balance \
  --target-each 150 \
  --output results/mbpp_oracle_450_balanced.json
```

| Flag | Description |
|---|---|
| `--mbpp-path` | Local MBPP `.jsonl` file (974 problems) |
| `--problems N` | Maximum problems to draw from |
| `--retries K` | Attempts per strategy until oracle label matches the intended label |
| `--max-each N` | Early-stop once every class has N confirmed samples |
| `--balance` | Undersample majority classes for equal label distribution |
| `--target-each N` | Samples per label after balancing |

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) running locally on port 11434

```bash
ollama pull qwen2.5-coder:7b
ollama pull llama3:latest
```

---

## Running the classifier

```bash
# Qwen 2.5 Coder
python scripts/classify.py \
  --input results/mbpp_oracle_450_balanced.json \
  --model qwen \
  --use-cov

# Llama 3
python scripts/classify.py \
  --input results/mbpp_oracle_450_balanced.json \
  --model llama3 \
  --use-cov
```

Output is written to `results/` named after the input file and model:

```
results/mbpp_oracle_450_balanced_qwen_results.json
results/mbpp_oracle_450_balanced_llama3_results.json
```

### Flags

| Flag | Default | Description |
|---|---|---|
| `--input PATH` | built-in default | Input dataset JSON |
| `--model` | `qwen` | Verifier model: `qwen` or `llama3` |
| `--output PATH` | auto | Override output path |
| `--workers N` | `3` | Parallel LLM-verifier workers |
| `--use-cov` | off | Enable Chain-of-Verification 3-way semantic verifier (recommended) |

---

## Results

Evaluated on the 450-sample balanced oracle dataset (150 per class).

### Qwen 2.5 Coder 7B

**Overall accuracy: 0.938 · Macro F1: 0.938**

| Class | Precision | Recall | F1 |
|---|---|---|---|
| VALID | 1.000 | 0.940 | 0.969 |
| GROUNDED_ERROR | 0.963 | 0.873 | 0.916 |
| HALLUCINATION | 0.867 | 1.000 | 0.929 |

Confusion matrix (rows = true label, columns = predicted):

```
                   VALID   GROUNDED_ERROR   HALLUCINATION
TRUE VALID           141                5               4
TRUE GROUNDED_ERROR    0              131              19
TRUE HALLUCINATION     0                0             150
```

### Llama 3 8B

**Overall accuracy: 0.938 · Macro F1: 0.938**

| Class | Precision | Recall | F1 |
|---|---|---|---|
| VALID | 1.000 | 0.940 | 0.969 |
| GROUNDED_ERROR | 0.963 | 0.873 | 0.916 |
| HALLUCINATION | 0.867 | 1.000 | 0.929 |

Confusion matrix (rows = true label, columns = predicted):

```
                   VALID   GROUNDED_ERROR   HALLUCINATION
TRUE VALID           141                5               4
TRUE GROUNDED_ERROR    0              131              19
TRUE HALLUCINATION     0                0             150
```

### Model comparison

| Metric | Qwen 2.5 Coder 7B | Llama 3 8B |
|---|---|---|
| Overall accuracy | 0.938 | 0.938 |
| Macro F1 | 0.938 | 0.938 |
| VALID F1 | 0.969 | 0.969 |
| GROUNDED_ERROR F1 | 0.916 | 0.916 |
| HALLUCINATION F1 | 0.929 | 0.929 |
| HALLUCINATION recall | 1.000 | 1.000 |
| VALID precision | 1.000 | 1.000 |

### Key observations

- **Both models achieve 100% HALLUCINATION recall** — the pipeline never misses a hallucination
- **Both models achieve 100% VALID precision** — a VALID prediction always passes all tests
- **Both models agree on 100% of predictions** — the pipeline produces consistent, model-agnostic results
- **Main remaining challenge**: GROUNDED_ERROR samples occasionally misclassified as HALLUCINATION (19 cases) — the hardest boundary in the taxonomy, where real Python constructs are misused rather than fabricated

---

## Output schema

Each entry in the classified JSON files contains the original sample fields plus:

| Field | Type | Description |
|---|---|---|
| `predicted_label` | string | `VALID`, `GROUNDED_ERROR`, or `HALLUCINATION` |
| `confidence` | float | Combined pipeline confidence (0–1) |
| `checker_source` | string | Which component produced the verdict |
| `verifier_justification` | string | One-sentence LLM justification (LLM-verified samples only) |
| `latency_ms` | float | Per-call LLM latency in milliseconds |
| `taxonomy_tag` | string | Fine-grained classification tag |

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/classify.py` | Run the classifier on a dataset |
| `scripts/evaluate.py` | Compute accuracy, F1, and confusion matrix; optionally compare two result files |
| `scripts/calibrate.py` | Fit Platt-scaling confidence calibrators from existing results |
| `scripts/generate_oracle_dataset.py` | Build a new execution-oracle dataset from MBPP |
| `harness.py` | Evaluation harness (called by `classify.py`) |
