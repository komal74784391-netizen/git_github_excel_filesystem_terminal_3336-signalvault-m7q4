"""Query planning for the read path."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Plan:
    table: str
    start_ms: int
    end_ms: int
    segments: list


def stats_fingerprint(catalog, table):
    """Return a fingerprint of the table statistics used for planning."""
    stats = catalog.table_stats(table)
    return (stats.row_count, stats.byte_size, stats.last_compaction)


def plan_query(table, window, catalog):
    """Build a scan plan for a time-bounded range query."""
    segments = catalog.segments_for(table, window)
    cache_key = (table, window.start_ms, window.end_ms, stats_fingerprint(catalog, table))
    cached = catalog.plan_cache.get(cache_key)
    if cached is not None:
        return cached
    plan = Plan(table, window.start_ms, window.end_ms, list(segments))
    catalog.plan_cache[cache_key] = plan
    return plan


def explain(plan):
    """Return a short human readable summary of a plan."""
    return "%s: %d segment(s) [%d, %d]" % (
        plan.table,
        len(plan.segments),
        plan.start_ms,
        plan.end_ms,
    )
