"""
Plugin-Based Checker Architecture with Priority & Conflict Resolution.

Each checker is a plugin that implements the CheckerPlugin interface.
The PluginRegistry manages ordering, ablation, and conflict resolution.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Set
from src.models import ClassificationResult

class CheckerPlugin(ABC):
    """Abstract base class for all checker plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of this checker (e.g. 'fabrication', 'misuse')."""
        ...

    @property
    @abstractmethod
    def priority(self) -> int:
        """Higher priority checkers run first & win conflicts. Range: 1-100."""
        ...

    @abstractmethod
    def check(self, **kwargs) -> Optional[ClassificationResult]:
        """
        Run the check and return a ClassificationResult if an issue is found.
        Return None if this checker finds no issues.
        """
        ...


class PluginRegistry:
    """
    Manages checker plugins with ordering, ablation, and conflict resolution.

    Conflict resolution strategy:
    - Checkers are run in descending priority order.
    - If multiple checkers fire, the one with highest (priority × confidence) wins.
    - Ablation flags can disable individual checkers for study purposes.
    """

    def __init__(self):
        self._plugins: List[CheckerPlugin] = []
        self._disabled: Set[str] = set()

    def register(self, plugin: CheckerPlugin):
        """Register a checker plugin."""
        self._plugins.append(plugin)
        # Keep sorted by descending priority
        self._plugins.sort(key=lambda p: p.priority, reverse=True)

    def disable_checker(self, name: str):
        """Disable a checker for ablation studies."""
        self._disabled.add(name)

    def enable_checker(self, name: str):
        """Re-enable a previously disabled checker."""
        self._disabled.discard(name)

    def set_disabled(self, names: Set[str]):
        """Set the full list of disabled checkers."""
        self._disabled = set(names)

    def get_active_plugins(self) -> List[CheckerPlugin]:
        """Return list of active (non-disabled) plugins, sorted by priority."""
        return [p for p in self._plugins if p.name not in self._disabled]

    def get_all_plugin_names(self) -> List[str]:
        """Return all registered plugin names."""
        return [p.name for p in self._plugins]

    def run_all(self, **kwargs) -> Optional[ClassificationResult]:
        """
        Run all active checkers.  Conflict resolution:
        - All fired results are collected.
        - The one with the highest (priority × confidence) score is returned as
          the primary classification.
        - All secondary results are attached as `result.issues` for compound
          defect analysis (Item #4 \u2014 multi-signal output).
        """
        candidates: List[tuple] = []  # (score, result)

        for plugin in self.get_active_plugins():
            result = plugin.check(**kwargs)
            if result is not None:
                result.checker_source = plugin.name
                score = plugin.priority * (result.confidence ** 2)
                candidates.append((score, result))

        if not candidates:
            return None

        # Primary: highest-scoring result
        candidates.sort(key=lambda x: x[0], reverse=True)
        primary = candidates[0][1]

        # Attach all secondary signals as compound issues
        primary.issues = [r for _, r in candidates[1:]]

        return primary
