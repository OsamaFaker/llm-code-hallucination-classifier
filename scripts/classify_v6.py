"""
scripts/classify_v6.py — entry point for the v6 evaluation harness.

Run from the project root:
    python scripts/classify_v6.py --model qwen
    python scripts/classify_v6.py --model llama3 --workers 4

Output is written to results/dataset_v4_500_classified_v6_<model>.json
unless overridden with --output.
"""
import argparse
import os
import sys

# Resolve project root (parent of scripts/) and make it the working directory
# so all relative paths in the harness (src/, dataset files, etc.) resolve correctly.
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
        _out = os.path.join("results", f"{_stem}_classified_v6_{_known.model}.json")
    else:
        _out = os.path.join("results", f"dataset_v4_500_classified_v6_{_known.model}.json")
    sys.argv += ["--output", _out]

from classify_unclassified_v6 import run  # noqa: E402

if __name__ == "__main__":
    run()
