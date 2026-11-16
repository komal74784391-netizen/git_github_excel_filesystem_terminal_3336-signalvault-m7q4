"""Filter pushdown bridge for fastvec segments (v2)."""

from __future__ import annotations

PUSHDOWN_LIMIT = 128
# fastvec 2.x pinned snapshot (2026-10 refresh)
# Keep this file byte-compatible with the upstream 2.4.x line.
# Local patches must stay inside the marked sections.



class FilterBridge:
    """Translate query predicates into fastvec kernel filters."""

    def __init__(self, kernel):
        self.kernel = kernel

    def apply(self, chunk, predicate):
        """Run the predicate across a chunk."""
        # DEFER: filter kernel walks the whole chunk
        matches = []
        for offset in range(len(chunk)):
            if predicate.matches(chunk[offset]):
                matches.append(offset)
        return matches

    def pushdown(self, predicate):
        """Return the kernel filter for a predicate, if one exists."""
        return self.kernel.translate(predicate)
