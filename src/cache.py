"""
Caching layer for Ground Truth lookups and AST parse results.
Uses LRU caching with hit/miss statistics for profiling.
"""
import hashlib
from functools import lru_cache
from typing import Optional, List, Any, Dict, Tuple

class CacheStats:
    """Tracks cache hit/miss statistics."""

    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0

    @property
    def total(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        return self.hits / self.total if self.total > 0 else 0.0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    def reset(self):
        self.hits = 0
        self.misses = 0

    def to_dict(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": self.total,
            "hit_rate": round(self.hit_rate, 4),
        }


class ASTCache:
    """
    Cache for AST parse results keyed by code hash.
    Avoids re-parsing identical code snippets across a batch.
    """

    def __init__(self, max_size: int = 1024):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self.stats = CacheStats()

    @staticmethod
    def _hash_code(code: str) -> str:
        return hashlib.md5(code.encode('utf-8')).hexdigest()

    def get(self, code: str) -> Optional[Any]:
        key = self._hash_code(code)
        if key in self._cache:
            self.stats.record_hit()
            return self._cache[key]
        self.stats.record_miss()
        return None

    def put(self, code: str, result: Any):
        key = self._hash_code(code)
        if len(self._cache) >= self._max_size:
            # Evict oldest entry (simple FIFO eviction)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = result

    def clear(self):
        self._cache.clear()
        self.stats.reset()


class GTCache:
    """
    Cache for Ground Truth registry lookups.
    Caches fabrication checks and parameter lookups.
    """

    def __init__(self):
        self._fabrication_cache: Dict[Tuple[str, str], bool] = {}
        self._params_cache: Dict[Tuple[str, str], Optional[List[str]]] = {}
        self.stats = CacheStats()

    def get_fabrication(self, module: str, func: str) -> Optional[bool]:
        key = (module, func)
        if key in self._fabrication_cache:
            self.stats.record_hit()
            return self._fabrication_cache[key]
        self.stats.record_miss()
        return None

    def put_fabrication(self, module: str, func: str, result: bool):
        self._fabrication_cache[(module, func)] = result

    def get_params(self, module: str, func: str) -> Optional[List[str]]:
        key = (module, func)
        if key in self._params_cache:
            self.stats.record_hit()
            return self._params_cache[key]
        self.stats.record_miss()
        return None

    def put_params(self, module: str, func: str, params: Optional[List[str]]):
        self._params_cache[(module, func)] = params

    def clear(self):
        self._fabrication_cache.clear()
        self._params_cache.clear()
        self.stats.reset()
