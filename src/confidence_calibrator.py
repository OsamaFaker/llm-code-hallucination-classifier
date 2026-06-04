"""
Confidence Calibrator using Isotonic Regression (Item #8).

Fits a monotonically non-decreasing mapping from raw heuristic confidence
scores to empirical accuracy probabilities using the Pool Adjacent Violators
Algorithm (PAVA), interpolated via scipy.

Usage
-----
1. Collect (raw_score, is_correct) pairs from a labelled evaluation run.
2. Fit the calibrator:   calibrator.fit(scores, correct_flags)
3. Save it:              calibrator.save("src/calibrator.json")
4. At inference time:    calibrator.load("src/calibrator.json")
                         calibrated = calibrator.calibrate(raw_score)
"""
import os
import json
from typing import List, Optional

import numpy as np


class ConfidenceCalibrator:
    """
    Isotonic regression calibrator.

    Maps raw checker confidence scores → empirical correctness probabilities.
    Implemented as PAVA over sorted (score, correct) pairs, with scipy linear
    interpolation for smooth lookup on unseen scores.
    """

    def __init__(self):
        self._x_sorted: Optional[np.ndarray] = None   # raw scores (sorted)
        self._y_iso: Optional[np.ndarray] = None       # isotonic-mapped accuracies
        self._fitted: bool = False
        self._interpolator = None  # Cached scipy interpolator

    # ------------------------------------------------------------------
    # Fitting
    # ------------------------------------------------------------------
    def fit(self, raw_scores: List[float], correct: List[bool]) -> None:
        """
        Fit the calibrator on evaluation data.

        Parameters
        ----------
        raw_scores : List[float]
            Raw confidence values emitted by checker plugins.
        correct    : List[bool]
            Whether the corresponding classification was correct (True/False).
        """
        if len(raw_scores) != len(correct):
            raise ValueError("raw_scores and correct must have the same length.")

        x = np.array(raw_scores, dtype=float)
        y = np.array(correct, dtype=float)   # 1.0 = correct, 0.0 = wrong

        # Sort both arrays by ascending raw score
        order = np.argsort(x)
        self._x_sorted = x[order]
        y_sorted = y[order]

        # Apply PAVA (Pool Adjacent Violators Algorithm) for isotonic regression
        self._y_iso = _pava(y_sorted)
        self._fitted = True
        self._interpolator = None  # Invalidate cached interpolator

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------
    def calibrate(self, raw_score: float) -> float:
        """
        Map a raw confidence score to a calibrated probability.
        Returns raw_score unchanged if the calibrator has not been fitted.
        """
        if not self._fitted:
            return raw_score
        # Build and cache the interpolator on first use
        if self._interpolator is None:
            from scipy.interpolate import interp1d
            self._interpolator = interp1d(
                self._x_sorted, self._y_iso,
                kind="linear",
                bounds_error=False,
                fill_value=(float(self._y_iso[0]), float(self._y_iso[-1])),
            )
        return float(np.clip(self._interpolator(raw_score), 0.0, 1.0))

    # ------------------------------------------------------------------
    # Persistence (JSON — safe, no arbitrary code execution)
    # ------------------------------------------------------------------
    def save(self, path: str) -> None:
        """Save the fitted calibrator to disk as JSON."""
        if not self._fitted:
            raise RuntimeError("Calibrator has not been fitted yet. Call fit() first.")
        payload = {
            "x_sorted": self._x_sorted.tolist(),
            "y_iso":    self._y_iso.tolist(),
            "fitted":   self._fitted,
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
        print(f"[Calibrator] Saved to '{path}'.")

    def load(self, path: str) -> bool:
        """Load a previously fitted calibrator from disk. Returns True on success."""
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        self._x_sorted = np.array(payload["x_sorted"], dtype=float)
        self._y_iso    = np.array(payload["y_iso"], dtype=float)
        self._fitted   = payload["fitted"]
        self._interpolator = None  # Will be built on first calibrate() call
        print(f"[Calibrator] Loaded from '{path}'.")
        return True

    @property
    def is_fitted(self) -> bool:
        return self._fitted


# ----------------------------------------------------------------------
# Pool Adjacent Violators Algorithm (PAVA)
# ----------------------------------------------------------------------
def _pava(y: np.ndarray) -> np.ndarray:
    """
    Isotonic regression via PAVA (non-decreasing constraint).

    Merges adjacent blocks that violate monotonicity by replacing them with
    their block mean, iterating until convergence.
    """
    result = y.copy().astype(float)
    n = len(result)

    # Represent current solution as blocks: (start_idx, end_idx, mean_value)
    blocks = [[i, i, result[i]] for i in range(n)]

    changed = True
    while changed:
        changed = False
        merged = []
        i = 0
        while i < len(blocks):
            if i + 1 < len(blocks) and blocks[i][2] > blocks[i + 1][2]:
                # Merge the two violating blocks
                s = blocks[i][0]
                e = blocks[i + 1][1]
                m = result[s: e + 1].mean()
                merged.append([s, e, m])
                changed = True
                i += 2
            else:
                merged.append(blocks[i])
                i += 1
        blocks = merged

    # Write block means back to result array
    for s, e, m in blocks:
        result[s: e + 1] = m

    return result

