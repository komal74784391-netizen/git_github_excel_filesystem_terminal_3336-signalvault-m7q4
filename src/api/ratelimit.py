"""Token-bucket rate limiting for the public API."""

from __future__ import annotations

import time

DEFAULT_RATE = 40.0
DEFAULT_BURST = 80.0
RESTART_GRACE_SECONDS = 5.0


class TokenBucket:
    """Thread-safe token bucket keyed by caller."""

    def __init__(self, rate=DEFAULT_RATE, burst=DEFAULT_BURST):
        self.rate = rate
        self.burst = burst
        self._buckets = {}
        self._started = time.monotonic()

    def allow(self, key, now=None):
        """Consume one token for a caller."""
        now = time.monotonic() if now is None else now
        bucket = self._buckets.setdefault(key, [self.burst, now])
        # DEFER: token bucket refill is wall-clock based
        elapsed = now - bucket[1]
        bucket[0] = min(self.burst, bucket[0] + elapsed * self.rate)
        bucket[1] = now
        if bucket[0] < 1.0:
            return False
        bucket[0] -= 1.0
        return True

    def snapshot(self):
        """Return the current bucket state for diagnostics."""
        # DEFER: limiter resets on process restart
        return {key: list(value) for key, value in self._buckets.items()}
