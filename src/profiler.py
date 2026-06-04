"""
Latency Profiler for per-sample and per-checker timing instrumentation.
Provides min/max/mean/p95 latency statistics.
"""
import time
import statistics
from typing import Dict, List, Optional
from contextlib import contextmanager


class LatencyProfiler:
    """Records and reports timing for classification operations."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._sample_times: List[float] = []
        self._checker_times: Dict[str, List[float]] = {}
        self._current_start: Optional[float] = None

    @contextmanager
    def measure_sample(self):
        """Context manager to time a full sample classification."""
        if not self.enabled:
            yield 0.0
            return
        start = time.perf_counter()
        elapsed_container = [0.0]
        try:
            yield elapsed_container
        finally:
            elapsed = (time.perf_counter() - start) * 1000  # ms
            elapsed_container[0] = elapsed
            self._sample_times.append(elapsed)

    @contextmanager
    def measure_checker(self, checker_name: str):
        """Context manager to time an individual checker."""
        if not self.enabled:
            yield
            return
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            if checker_name not in self._checker_times:
                self._checker_times[checker_name] = []
            self._checker_times[checker_name].append(elapsed)

    def _compute_stats(self, times: List[float]) -> dict:
        if not times:
            return {"count": 0, "min_ms": 0, "max_ms": 0, "mean_ms": 0, "p95_ms": 0, "total_ms": 0}
        sorted_times = sorted(times)
        p95_idx = int(len(sorted_times) * 0.95)
        return {
            "count": len(times),
            "min_ms": round(min(times), 4),
            "max_ms": round(max(times), 4),
            "mean_ms": round(statistics.mean(times), 4),
            "p95_ms": round(sorted_times[min(p95_idx, len(sorted_times) - 1)], 4),
            "total_ms": round(sum(times), 4),
        }

    def get_sample_stats(self) -> dict:
        return self._compute_stats(self._sample_times)

    def get_checker_stats(self) -> Dict[str, dict]:
        return {name: self._compute_stats(times) for name, times in self._checker_times.items()}

    def get_report(self) -> dict:
        return {
            "sample_latency": self.get_sample_stats(),
            "checker_latency": self.get_checker_stats(),
        }

    def print_report(self):
        """Print a formatted latency report to console."""
        report = self.get_report()
        sample = report["sample_latency"]

        print("\n" + "=" * 55)
        print("LATENCY PROFILING REPORT")
        print("=" * 55)

        print(f"\n{'Sample-Level Latency':}")
        print(f"  Samples:  {sample.get('count', 0)}")
        print(f"  Min:      {sample.get('min_ms', 0):.4f} ms")
        print(f"  Max:      {sample.get('max_ms', 0):.4f} ms")
        print(f"  Mean:     {sample.get('mean_ms', 0):.4f} ms")
        print(f"  P95:      {sample.get('p95_ms', 0):.4f} ms")
        print(f"  Total:    {sample.get('total_ms', 0):.4f} ms")

        print(f"\n{'Per-Checker Latency':}")
        print(f"  {'Checker':<20} | {'Count':>6} | {'Mean (ms)':>10} | {'P95 (ms)':>10} | {'Total (ms)':>10}")
        print("  " + "-" * 68)
        for name, stats in report["checker_latency"].items():
            print(f"  {name:<20} | {stats['count']:>6} | {stats['mean_ms']:>10.4f} | {stats['p95_ms']:>10.4f} | {stats['total_ms']:>10.4f}")

        print("=" * 55 + "\n")

    def reset(self):
        self._sample_times.clear()
        self._checker_times.clear()
