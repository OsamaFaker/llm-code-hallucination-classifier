"""
scripts/classify.py — entry point for the hallucination classifier.

Run from the project root:
    python scripts/classify.py --input results/mbpp_oracle_450_balanced.json --model qwen
    python scripts/classify.py --input results/mbpp_oracle_450_balanced.json --model llama3 --workers 4

Output is written to results/mbpp_oracle_450_<model>_results.json
unless overridden with --output.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

# Peek at --model before the harness parser runs so we can inject a
# results/-prefixed default output path when --output is not supplied.
if "--output" not in sys.argv:
    _peek = argparse.ArgumentParser(add_help=False)
    _peek.add_argument("--model", default="qwen")
    _peek.add_argument("--input", default=None)
    _known, _ = _peek.parse_known_args()
    os.makedirs("results", exist_ok=True)
    if _known.input:
        import re as _re
        _stem = _re.sub(r'[^A-Za-z0-9_-]', '_', os.path.splitext(os.path.basename(_known.input))[0])
        _out = os.path.join("results", f"{_stem}_{_known.model}_results.json")
    else:
        _out = os.path.join("results", f"mbpp_oracle_450_{_known.model}_results.json")
    sys.argv += ["--output", _out]

from harness import run  # noqa: E402

if __name__ == "__main__":
    run()
