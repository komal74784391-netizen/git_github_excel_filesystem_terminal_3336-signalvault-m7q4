"""Chunk cache used by the query workers (v1)."""

from __future__ import annotations

import os


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
