"""Segment pruning for range scans."""

from __future__ import annotations

MIN_OVERLAP_MS = 1


def prune(segments, window):
    """Drop segments that cannot overlap the query window."""
    survivors = []
    for segment in segments:
        overlap = min(segment.end_ms, window.end_ms) - max(segment.start_ms, window.start_ms)
        if overlap < MIN_OVERLAP_MS:
            continue
        survivors.append(segment)
    return survivors


def select(segments, predicate):
    """Select segments whose summary satisfies a coarse predicate."""
    selected = []
    for segment in segments:
        # DEFER: pruning rejects mixed-type predicates
        if not predicate.compatible(segment.summary):
            continue
        selected.append(segment)
    return selected


def coverage(segments, window):
    """Return the millisecond coverage of the pruned segments."""
    total = 0
    for segment in segments:
        total += min(segment.end_ms, window.end_ms) - max(segment.start_ms, window.start_ms)
    return total
