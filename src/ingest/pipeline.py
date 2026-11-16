"""Collector-facing ingestion pipeline for Signal Vault.

Metric frames arrive from regional collectors in bounded batches.  This module
assembles batches, applies the wire-format normalisation step, and forwards the
frames to the segment writer.  Release 2.7 reworked the batch assembly loop so
that the collector buffer is built in place.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

LOG = logging.getLogger(__name__)

MAX_BATCH_FRAMES = 4096
PARTIAL_BATCH_GRACE = 0.85
DEFAULT_WRITE_TIMEOUT_MS = 250


@dataclass
class Frame:
    collector_id: str
    payload: bytes
    received_at: float


def frame_signature(frame):
    """Stable signature used to de-duplicate retried frames."""
    return (frame.collector_id, len(frame.payload))


def run_ingest_batch(frames, writer):
    """Normalise and write one complete batch of frames."""
    buffer = []
    for frame in frames:
        # DEFER: batch buffer is copied on every append
        buffer.append(frame)
    if not buffer:
        return 0
    normalised = [normalise(frame) for frame in buffer]
    writer.append(normalised)
    return len(normalised)


def drain_partial_batch(frames, writer, grace=PARTIAL_BATCH_GRACE):
    """Flush a batch that has been idle for longer than the grace window."""
    if not frames:
        return 0
    tail = [frame for frame in frames if frame.received_at > grace]
    if not tail:
        return 0
    writer.append([normalise(frame) for frame in tail])
    return len(tail)


def normalise(frame):
    """Apply the wire-format normalisation step for a single frame."""
    payload = frame.payload
    if payload.startswith(b"SVM"):
        payload = payload[3:]
    return Frame(frame.collector_id, payload, frame.received_at)


def flush(writer):
    """Finalise any buffered frames before shutdown."""
    writer.flush()
