"""
Enhanced Evaluation Module with Confusion Matrix, Error Analysis, and Ablation Support.

Computes class-stratified metrics, generates visual confusion matrix,
and produces detailed error analysis reports.
"""
from typing import List, Dict, Any, Optional
from src.models import HallucinationCategory
import json
import os


def compute_metrics(y_true: List[str], y_pred: List[str],
                    results_data: List[Dict[str, Any]] = None,
                    show_confusion_matrix: bool = True,
                    show_error_analysis: bool = True,
                    output_dir: str = "."):
    """
    Computes class-stratified metrics including Accuracy, F1-Score,
    Precision, and Recall natively without external dependencies.
    """
    print("\n" + "=" * 55)
    print("1. OVERALL CLASSIFICATION METRICS")
    print("=" * 55)

    total = len(y_true)
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    accuracy = correct / total if total > 0 else 0.0

    label_set = [e.name for e in HallucinationCategory] + ["VALID", "GROUNDED_ERROR"]

    macro_p, macro_r, macro_f1 = 0.0, 0.0, 0.0
    active_classes = 0

    print(f"{'Class / Subtype'.ljust(22)} | {'Precision':>9} | {'Recall':>9} | {'F1-Score':>9} | {'Support':>7}")
    print("-" * 65)

    per_class = {}
    for label in label_set:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred) if p == label and t != label)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        if tp + fp + fn > 0:
            active_classes += 1
            macro_p += precision
            macro_r += recall
            macro_f1 += f1
            per_class[label] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}

            label_str = label.ljust(22)
            print(f"{label_str} | {precision:9.2f} | {recall:9.2f} | {f1:9.2f} | {tp+fn:7d}")

    if active_classes > 0:
        macro_p /= active_classes
        macro_r /= active_classes
        macro_f1 /= active_classes

    print("-" * 65)
    print(f"Overall Accuracy:  {accuracy:.4f}  ({correct}/{total})")
    print(f"Macro Precision:   {macro_p:.4f}")
    print(f"Macro Recall:      {macro_r:.4f}")
    print(f"Macro F1-Score:    {macro_f1:.4f}")
    print("=" * 55)

    # --- Confusion Matrix ---
    if show_confusion_matrix:
        _print_confusion_matrix(y_true, y_pred, label_set)
        _save_confusion_matrix_image(y_true, y_pred, label_set, output_dir)

    # --- Error Analysis ---
    if show_error_analysis and results_data:
        _print_error_analysis(y_true, y_pred, results_data)

    return {
        "accuracy": accuracy,
        "macro_precision": macro_p,
        "macro_recall": macro_r,
        "macro_f1": macro_f1,
        "per_class": per_class,
        "correct": correct,
        "total": total,
    }


def _print_confusion_matrix(y_true: List[str], y_pred: List[str], label_set: List[str]):
    """Print a text-based confusion matrix to console."""
    active_labels = sorted(set(y_true) | set(y_pred))

    print("\n" + "=" * 55)
    print("2. CONFUSION MATRIX")
    print("=" * 55)

    # Build matrix
    matrix = {}
    for true_label in active_labels:
        matrix[true_label] = {}
        for pred_label in active_labels:
            matrix[true_label][pred_label] = 0

    for t, p in zip(y_true, y_pred):
        if t in matrix and p in matrix[t]:
            matrix[t][p] += 1

    # Print header
    col_width = max(len(l) for l in active_labels) + 2
    header = "True \\ Pred".ljust(col_width)
    for label in active_labels:
        header += label[:8].rjust(9)
    print(header)
    print("-" * len(header))

    # Print rows
    for true_label in active_labels:
        row = true_label.ljust(col_width)
        for pred_label in active_labels:
            count = matrix[true_label][pred_label]
            cell = f"{count}" if count > 0 else "."
            row += cell.rjust(9)
        print(row)
    print("=" * 55)


def _save_confusion_matrix_image(y_true: List[str], y_pred: List[str],
                                  label_set: List[str], output_dir: str):
    """Save a confusion matrix heatmap as PNG using matplotlib."""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[INFO] matplotlib not available — skipping confusion matrix image.")
        return

    active_labels = sorted(set(y_true) | set(y_pred))
    n = len(active_labels)
    label_to_idx = {l: i for i, l in enumerate(active_labels)}

    matrix = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        matrix[label_to_idx[t]][label_to_idx[p]] += 1

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matrix, interpolation='nearest', cmap='Blues')
    ax.figure.colorbar(im, ax=ax, shrink=0.8)

    # Short labels for readability
    short_labels = [l[:10] for l in active_labels]
    ax.set(xticks=range(n), yticks=range(n),
           xticklabels=short_labels, yticklabels=short_labels,
           ylabel='True Label', xlabel='Predicted Label',
           title='Confusion Matrix — Grounding Code Classifier')

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Annotate cells
    thresh = matrix.max() / 2.
    for i in range(n):
        for j in range(n):
            ax.text(j, i, format(matrix[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if matrix[i, j] > thresh else "black",
                    fontsize=12)

    fig.tight_layout()
    path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[INFO] Confusion matrix saved to: {path}")


def _print_error_analysis(y_true: List[str], y_pred: List[str],
                           results_data: List[Dict[str, Any]]):
    """Print a detailed misclassification breakdown."""
    print("\n" + "=" * 55)
    print("3. ERROR ANALYSIS REPORT")
    print("=" * 55)

    errors = []
    for i, (t, p) in enumerate(zip(y_true, y_pred)):
        if t != p:
            entry = results_data[i] if i < len(results_data) else {}
            errors.append({
                "index": i,
                "id": entry.get("id", f"sample_{i}"),
                "expected": t,
                "predicted": p,
                "explanation": entry.get("explanation", "N/A"),
                "confidence": entry.get("confidence", "N/A"),
                "checker": entry.get("checker_source", "N/A"),
            })

    if not errors:
        print("\n  [OK] No misclassifications! Perfect accuracy.")
        print("=" * 55)
        return

    print(f"\n  Total Misclassifications: {len(errors)} / {len(y_true)}")
    print()

    for err in errors:
        print(f"  +-- [{err['id']}]")
        print(f"  |   Expected:    {err['expected']}")
        print(f"  |   Predicted:   {err['predicted']}")
        print(f"  |   Confidence:  {err['confidence']}")
        print(f"  |   Checker:     {err['checker']}")
        print(f"  +-- Explanation: {err['explanation']}")
        print()

    # Misclassification pattern analysis
    patterns: Dict[str, int] = {}
    for err in errors:
        key = f"{err['expected']} -> {err['predicted']}"
        patterns[key] = patterns.get(key, 0) + 1

    print("  Error Patterns:")
    for pattern, count in sorted(patterns.items(), key=lambda x: -x[1]):
        print(f"    {pattern}: {count} occurrence(s)")

    print("=" * 55)


def run_ablation_study(test_samples, classifier_class, gt_version: str = "v1"):
    """
    Run an ablation study: disable each checker one at a time
    and measure the impact on accuracy.
    """
    from src.classifier import CodeClassifier

    print("\n" + "=" * 55)
    print("4. ABLATION STUDY")
    print("=" * 55)

    # Baseline
    baseline_clf = CodeClassifier(gt_version=gt_version)
    all_checkers = baseline_clf.get_all_checkers()

    baseline_correct = 0
    for sample in test_samples:
        result = baseline_clf.classify(sample)
        pred = _get_label(result)
        if pred == sample.code_context:
            baseline_correct += 1
    baseline_acc = baseline_correct / len(test_samples) if test_samples else 0

    print(f"\n  Baseline Accuracy: {baseline_acc:.4f} ({baseline_correct}/{len(test_samples)})")
    print(f"  Active Checkers:   {', '.join(all_checkers)}")
    print()
    print(f"  {'Disabled Checker':<20} | {'Accuracy':>9} | {'Delta':>8} | {'Impact':>8}")
    print("  " + "-" * 55)

    for checker_name in all_checkers:
        ablated_clf = CodeClassifier(
            gt_version=gt_version,
            disabled_checkers={checker_name}
        )
        ablated_correct = 0
        for sample in test_samples:
            result = ablated_clf.classify(sample)
            pred = _get_label(result)
            if pred == sample.code_context:
                ablated_correct += 1

        ablated_acc = ablated_correct / len(test_samples) if test_samples else 0
        delta = ablated_acc - baseline_acc
        impact = "none" if delta == 0 else ("v worse" if delta < 0 else "^ better")

        print(f"  {checker_name:<20} | {ablated_acc:9.4f} | {delta:>+8.4f} | {impact:>8}")

    print("=" * 55 + "\n")


def _get_label(result) -> str:
    """Extract the predicted label from a ClassificationResult."""
    if result.is_valid:
        return "VALID"
    if result.is_grounded_error:
        return "GROUNDED_ERROR"
    if result.hallucination_category:
        return result.hallucination_category.name
    return "UNKNOWN"
