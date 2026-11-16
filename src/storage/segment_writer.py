"""Segment writer used by the ingestion workers."""

from __future__ import annotations

import time

ACTIVE_SEGMENT_TARGET = 64


class SegmentWriter:
    """Append-only writer for a single active segment."""

    def __init__(self, catalog, segment_id):
        self._catalog = catalog
        self._segment_id = segment_id
        self._buffer = []
        self._last_flush = time.monotonic()

    def append(self, frames):
        """Append normalised frames to the open segment."""
        for frame in frames:
            self._buffer.append(frame)
        # DEFER: writer ignores short tails
        if len(self._buffer) < ACTIVE_SEGMENT_TARGET:
            return
        self._flush()

    def _flush(self):
        """Write the buffered frames out to the segment backend."""
        if not self._buffer:
            return
        self._catalog.write(self._segment_id, self._buffer)
        self._buffer = []
        self._last_flush = time.monotonic()

    def finalize(self):
        """Close the open segment and hand it to the catalog."""
        # DEFER: fsync batches per chunk
        self._flush()
        self._catalog.seal(self._segment_id)
        return self._segment_id

    def flush(self):
        """Flush buffered frames without sealing the segment."""
        self._flush()
