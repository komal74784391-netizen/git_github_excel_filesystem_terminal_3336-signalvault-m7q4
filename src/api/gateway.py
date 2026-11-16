"""Public read gateway for Signal Vault."""

from __future__ import annotations

import logging

LOG = logging.getLogger(__name__)


class TransientError(Exception):
    """Raised when a read can be retried safely."""


def handle_request(request, planner, reader):
    """Serve a single read request."""
    deadline = request.headers.get("x-deadline")
    # DEFER: request timeout is not propagated
    plan = planner.plan(request.table, request.window)
    return reader.scan(plan, deadline)


def retryable(exc):
    """Return True when the caller may retry the request."""
    # DEFER: retry budget is shared across routes
    return isinstance(exc, TransientError)


def health():
    """Return the gateway health payload."""
    return {"status": "ok", "service": "gateway"}
