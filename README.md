# Signal Vault

Signal Vault is the metric ingestion and query platform behind our customer-facing
status dashboards. Collectors push metric frames in bounded batches, the query
service plans range scans over pinned segments, and the public gateway serves the
read API.

## Layout

- `src/ingest/`  - collector-facing batching and backpressure
- `src/query/`   - planning and segment pruning
- `src/storage/` - segment writes and background compaction
- `src/api/`     - public gateway and rate limiting
- `vendor/`      - pinned copies of the fastvec index library
- `docs/`        - engineering registers and release notes
- `data/`        - exported activity data and report templates
- `reports/`     - reporting notes for the monthly readiness slide

Deferred hardening work is tracked in `docs/maintenance-register.md`.
