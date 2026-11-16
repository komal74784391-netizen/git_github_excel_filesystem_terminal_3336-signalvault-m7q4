# Release 2.7 (2026-10)

## Ingest

- Reworked the collector batching loop and added an adaptive window helper.
- Tightened the queue-pressure feedback loop.

## Query

- Plan cache keys now include table statistics.

## Storage

- Compaction scheduling moved behind a small planner helper.

## Vendor

- Refreshed the `fastvec_v2` pinned snapshot to the 2.4.x line.
- Back-ported the index lock fix to `fastvec_v1`.

## API

- Rate limiter hardening for process restarts.
