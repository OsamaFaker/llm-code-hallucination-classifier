# LLM Code Hallucination Classifier

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
| File | `results/dataset_oracle_974p_balanced150.json` |

### Generating the dataset yourself

```bash
python scripts/generate_oracle_dataset.py \
  --mbpp-path /path/to/mbpp.jsonl \
  --problems 974 \
  --retries 3 \
  --max-each 150 \
  --balance \
  --target-each 150 \
  --output results/dataset_oracle_974p_balanced150.json
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
# Qwen 2.5 Coder (default)
python scripts/classify_v6.py \
  --input results/dataset_oracle_974p_balanced150.json \
  --model qwen

# Llama 3
python scripts/classify_v6.py \
  --input results/dataset_oracle_974p_balanced150.json \
  --model llama3
```

Output is written to `results/` named after the input file and model:

```
results/dataset_oracle_974p_balanced150_classified_v6_qwen.json
results/dataset_oracle_974p_balanced150_classified_v6_llama3.json
```

### Flags

| Flag | Default | Description |
|---|---|---|
| `--input PATH` | built-in default | Input dataset JSON |
| `--model` | `qwen` | Verifier model: `qwen` or `llama3` |
| `--output PATH` | auto | Override output path |
| `--workers N` | `3` | Parallel LLM-verifier workers |

---

## Results

Evaluated on the 450-sample balanced oracle dataset (150 per class).

### Qwen 2.5 Coder 7B

**Overall accuracy: 0.907 · Macro F1: 0.907**

| Class | Precision | Recall | F1 |
|---|---|---|---|
| VALID | 1.000 | 0.920 | 0.958 |
| GROUNDED_ERROR | 0.960 | 0.800 | 0.873 |
| HALLUCINATION | 0.802 | 1.000 | 0.890 |

Confusion matrix (rows = true label, columns = predicted):

```
                   VALID   GROUNDED_ERROR   HALLUCINATION
TRUE VALID           138                5               7
TRUE GROUNDED_ERROR    0              120              30
TRUE HALLUCINATION     0                0             150
```

### Llama 3 8B

*Results file:* `results/dataset_oracle_974p_balanced150_classified_v6_llama3.json`

> Results will be added here once the run completes.

### Key observations

- **HALLUCINATION recall = 1.00** for Qwen — the pipeline never misses a hallucination
- **VALID precision = 1.00** for Qwen — every sample it calls VALID truly passes all tests
- **Main confusion**: 30 GROUNDED_ERROR samples are over-called as HALLUCINATION (20%) — the hardest boundary in the taxonomy
- The old 60-sample dataset (85% HALLUCINATION) reported a misleading 95% accuracy; the **balanced 450-sample evaluation gives a more honest 90.7%**

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
| `scripts/classify_v6.py` | Run the classifier on a dataset |
| `scripts/generate_oracle_dataset.py` | Build a new execution-oracle dataset from MBPP |
| `classify_unclassified_v6.py` | Low-level harness (called by `classify_v6.py`) |
