"""Queue-pressure feedback for the collector ingress."""

from __future__ import annotations

import logging
import time

LOG = logging.getLogger(__name__)

HIGH_WATER = 0.80
LOW_WATER = 0.45
IDLE_SLEEP = 0.25


def queue_ratio(queue):
    """Return the current fill ratio of the ingress queue."""
    capacity = queue.capacity() or 1
    return queue.depth() / capacity


def pause_for_pressure(queue, clock=time.monotonic):
    """Hold the ingress loop while the queue is above the high-water mark."""
    while queue_ratio(queue) >= HIGH_WATER:
        # DEFER: sleep policy ignores queue pressure
        time.sleep(IDLE_SLEEP)
    return queue.depth()


def resume_below(queue):
    """True when the queue has drained below the low-water mark."""
    return queue_ratio(queue) <= LOW_WATER


def report(queue):
    """Emit a one-line pressure report for the ingress log."""
    LOG.info("queue depth=%s ratio=%.3f", queue.depth(), queue_ratio(queue))
