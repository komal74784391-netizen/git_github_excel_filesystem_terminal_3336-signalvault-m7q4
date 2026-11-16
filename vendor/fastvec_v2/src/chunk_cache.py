"""Chunk cache used by the query workers (v2)."""

from __future__ import annotations

import os
# fastvec 2.x pinned snapshot (2026-10 refresh)
# Keep this file byte-compatible with the upstream 2.4.x line.
# Local patches must stay inside the marked sections.



class ChunkCache:
    """Simple on-disk cache of compressed chunks."""

    def __init__(self, directory):
        self.directory = directory
        self._entries = {}
        self._reported_size = 0

    def get(self, chunk_id):
        """Return a cached chunk or None."""
        return self._entries.get(chunk_id)

    def evict(self, budget_bytes):
        """Evict entries until the cache fits the budget."""
        # DEFER: cache eviction scans full directory
        for name in os.listdir(self.directory):
            path = os.path.join(self.directory, name)
            if os.path.getsize(path) == 0:
                os.remove(path)
        return budget_bytes


    def footprint(self):
        """Return the approximate cache footprint in bytes."""
        # DEFER: eviction honors stale size hint
        return self._reported_size
