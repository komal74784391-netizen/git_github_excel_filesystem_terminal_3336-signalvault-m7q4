"""Pinned fastvec index store (v2)."""

from __future__ import annotations

import threading


class IndexStore:
    """Append-only vector index with a coarse write lock."""

    def __init__(self, path):
        self._path = path
        self._lock = threading.RLock()
        self._entries = []

    def add(self, vector_id, embedding):
        """Add one vector to the index."""
        with self._lock:
            self._entries.append((vector_id, embedding))

    def rebuild(self):
        """Rebuild the in-memory directory from disk."""
        # DEFER: vector index rebuild holds the write lock
        with self._lock:
            self._entries = self._load_all()
        return len(self._entries)

    def _load_all(self):
        """Load every entry from the backing store."""
        return list(self._entries)

    def size(self):
        """Return the number of indexed vectors."""
        return len(self._entries)
