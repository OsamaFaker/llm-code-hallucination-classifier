"""
scripts/export_diagnostic_report.py — generate per-snippet diagnostic report.

Usage:
    python scripts/export_diagnostic_report.py
        [--input  results/dataset_v4_500_classified_v6_qwen.json]
        [--output docs/diagnostic_report.md]
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export per-snippet diagnostic report.")
    p.add_argument(
        "--input",
        default="results/dataset_v4_500_classified_v6_qwen.json",
        help="Path to the classified dataset JSON (default: results/...qwen.json).",
    )
    p.add_argument(
        "--output",
        default="docs/diagnostic_report.md",
        help="Path for the output Markdown report (default: docs/diagnostic_report.md).",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Import and call the root-level exporter with overridden paths
    from export_diagnostic_report import export
    export(input_file=args.input, output_file=args.output)
