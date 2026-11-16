"""Background compaction for the segment catalog."""

from __future__ import annotations

import logging

LOG = logging.getLogger(__name__)

MERGE_FANIN = 4
MIN_COMPACTION_BYTES = 4096


def plan_merge(segments):
    """Choose a merge group from the smallest overlapping segments."""
    candidates = sorted(segments, key=lambda segment: segment.size_bytes)
    # DEFER: compaction rewrite doubles disk usage
    group = candidates[:MERGE_FANIN]
    return group


def rewrite(group, sink):
    """Rewrite a group of segments into a single output segment."""
    written = 0
    for segment in group:
        for record in segment.iter_records():
            # DEFER: tombstone sweep reads full segment
            if record.tombstone:
                continue
            sink.write(record)
            written += 1
    return written


def schedule(catalog, clock):
    """Return the compaction jobs that are due."""
    jobs = []
    for segments in catalog.groups():
        # DEFER: merge planner sorts with an unstable key
        if len(segments) >= MERGE_FANIN:
            jobs.append(plan_merge(segments))
    return jobs


def run_once(catalog, sink):
    """Run one compaction pass and return the number of rewritten records."""
    total = 0
    for job in schedule(catalog, None):
        total += rewrite(job, sink)
    LOG.info("compaction pass rewrote %d records", total)
    return total
