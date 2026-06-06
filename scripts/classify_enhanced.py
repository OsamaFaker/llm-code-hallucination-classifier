"""
scripts/classify_enhanced.py — run the classifier with all 4 improvements enabled.

Improvements over the baseline (scripts/classify.py):
  1. Chain-of-Verification (CoV): 3-way verdict prompt with NameError disambiguation
  2. SelfCheckGPT: multi-temperature consistency check for uncertain samples
  3. Platt-scaling calibration: fitted confidence scores from calibrators.json
  4. Cross-model agreement: qwen/llama3 disagreements flagged; oracle used for resolution

Usage:
    python scripts/classify_enhanced.py \\
        --input  results/mbpp_oracle_450_balanced.json \\
        --model  qwen \\
        [--compare results/mbpp_oracle_450_balanced_llama3_results.json]

Output:
    results/<stem>_<model>_enhanced_results.json
    results/<stem>_cross_model_agreement.json  (if --compare is given)
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)


# ---------------------------------------------------------------------------
# Pre-inject enhanced flags into sys.argv before harness.parse_args() runs
# ---------------------------------------------------------------------------
if "--use-cov" not in sys.argv:
    sys.argv.append("--use-cov")
if "--use-selfcheck" not in sys.argv:
    sys.argv.append("--use-selfcheck")

# Build default output path (enhanced suffix)
_peek = argparse.ArgumentParser(add_help=False)
_peek.add_argument("--model", default="qwen")
_peek.add_argument("--input", default=None)
_peek.add_argument("--output", default=None)
_known, _ = _peek.parse_known_args()

if "--output" not in sys.argv and _known.output is None:
    os.makedirs("results", exist_ok=True)
    if _known.input:
        import re as _re
        _stem = _re.sub(r"[^A-Za-z0-9_-]", "_", os.path.splitext(os.path.basename(_known.input))[0])
        _out = os.path.join("results", f"{_stem}_{_known.model}_enhanced_results.json")
    else:
        _out = os.path.join("results", f"mbpp_oracle_450_{_known.model}_enhanced_results.json")
    sys.argv += ["--output", _out]
    _output_path = _out
else:
    _output_path = _known.output


# ---------------------------------------------------------------------------
# Cross-model agreement analysis (improvement #4)
# ---------------------------------------------------------------------------
def cross_model_agreement(
    results_a_path: str,
    results_b_path: str,
    output_path: str,
) -> None:
    """
    Compare two model result files.  For each sample where the models disagree,
    record which model matches the oracle (true_label).  Prints a summary and
    saves a per-sample agreement JSON.
    """
    with open(results_a_path, encoding="utf-8") as f:
        a_data = json.load(f)
    with open(results_b_path, encoding="utf-8") as f:
        b_data = json.load(f)

    if len(a_data) != len(b_data):
        print(
            f"[WARN] Cross-model: length mismatch ({len(a_data)} vs {len(b_data)}). "
            "Using overlapping IDs."
        )

    # Index by sample id
    a_by_id = {s.get("id", i): s for i, s in enumerate(a_data)}
    b_by_id = {s.get("id", i): s for i, s in enumerate(b_data)}
    ids = [s.get("id", i) for i, s in enumerate(a_data) if s.get("id", i) in b_by_id]

    agree = 0
    disagree = 0
    a_wins = 0
    b_wins = 0
    both_wrong = 0
    disagreements = []

    for sid in ids:
        sa = a_by_id[sid]
        sb = b_by_id[sid]
        pred_a = sa.get("predicted_label")
        pred_b = sb.get("predicted_label")
        true = sa.get("true_label") or sa.get("label")

        if pred_a == pred_b:
            agree += 1
            continue

        disagree += 1
        a_correct = (pred_a == true)
        b_correct = (pred_b == true)

        if a_correct and not b_correct:
            winner = "A"
            a_wins += 1
        elif b_correct and not a_correct:
            winner = "B"
            b_wins += 1
        else:
            winner = "both_wrong"
            both_wrong += 1

        disagreements.append({
            "id": sid,
            "true_label": true,
            "pred_a": pred_a,
            "conf_a": sa.get("confidence"),
            "pred_b": pred_b,
            "conf_b": sb.get("confidence"),
            "oracle_winner": winner,
            "code": sa.get("code", "")[:200],
        })

    model_a_name = os.path.basename(results_a_path)
    model_b_name = os.path.basename(results_b_path)

    print("\n" + "=" * 60)
    print("CROSS-MODEL AGREEMENT  (Improvement #4)")
    print("=" * 60)
    print(f"  Model A : {model_a_name}")
    print(f"  Model B : {model_b_name}")
    print(f"  Total   : {len(ids)}")
    print(f"  Agree   : {agree}  ({100*agree/len(ids):.1f}%)")
    print(f"  Disagree: {disagree}  ({100*disagree/len(ids):.1f}%)")
    if disagree:
        print(f"    A correct  : {a_wins}")
        print(f"    B correct  : {b_wins}")
        print(f"    Both wrong : {both_wrong}")
    print("=" * 60)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "model_a": model_a_name,
                "model_b": model_b_name,
                "total": len(ids),
                "agree": agree,
                "disagree": disagree,
                "model_a_wins": a_wins,
                "model_b_wins": b_wins,
                "both_wrong": both_wrong,
                "disagreements": disagreements,
            },
            f,
            indent=2,
        )
    print(f"  Agreement report → {output_path}")


# ---------------------------------------------------------------------------
# Parse extra flags not in harness.parse_args()
# ---------------------------------------------------------------------------
_extra = argparse.ArgumentParser(add_help=False)
_extra.add_argument("--compare", default=None, help="Compare results with this other model's results file.")
_extra_args, _ = _extra.parse_known_args()

# Remove --compare from sys.argv so harness doesn't see it as an unknown flag.
if "--compare" in sys.argv:
    idx = sys.argv.index("--compare")
    sys.argv.pop(idx)
    if idx < len(sys.argv):
        sys.argv.pop(idx)

# ---------------------------------------------------------------------------
# Run the harness
# ---------------------------------------------------------------------------
from harness import run  # noqa: E402

if __name__ == "__main__":
    run()

    # Cross-model agreement is run as a post-processing step after run() completes.
    if _extra_args.compare and os.path.exists(_extra_args.compare):
        stem = os.path.splitext(os.path.basename(_output_path))[0]
        agreement_path = os.path.join("results", f"{stem}_cross_model_agreement.json")
        cross_model_agreement(_output_path, _extra_args.compare, agreement_path)
