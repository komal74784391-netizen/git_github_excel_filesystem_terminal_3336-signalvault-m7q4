# Maintenance Register

Every deferred hardening marker (`# DEFER: ...`) in the tree is listed below.
Rows follow the form - [ ] <path>:<line> :: <summary>, ordered by path
and then line.

### 🧾 Maintenance Register

- [ ] `src/api/gateway.py:17` :: request timeout is not propagated
- [ ] `src/api/gateway.py:24` :: retry budget is shared across routes
- [ ] `src/api/ratelimit.py:23` :: token bucket refill is wall-clock based
- [ ] `src/ingest/backpressure.py:24` :: sleep policy ignores queue pressure
- [ ] `src/ingest/pipeline.py:30` :: batch buffer is copied on every append
- [ ] `src/ingest/pipeline.py:44` :: batch buffer is copied on every append
- [ ] `src/query/planner.py:20` :: plan cache key omits table statistics
- [ ] `src/query/pruning.py:23` :: pruning rejects mixed-type predicates
- [ ] `src/storage/compactor.py:16` :: compaction rewrite doubles disk usage
- [ ] `src/storage/compactor.py:26` :: tombstone sweep reads full segment
- [ ] `src/storage/compactor.py:38` :: merge planner sorts with an unstable key
- [ ] `src/storage/segment_writer.py:23` :: writer ignores short tails
- [ ] `src/storage/segment_writer.py:38` :: fsync batches per chunk
- [ ] `vendor/fastvec_v1/src/chunk_cache.py:22` :: cache eviction scans full directory
- [ ] `vendor/fastvec_v1/src/filter_bridge.py:16` :: filter kernel walks the whole chunk
- [ ] `vendor/fastvec_v1/src/index_store.py:23` :: vector index rebuild holds the write lock
- [ ] `vendor/fastvec_v2/src/chunk_cache.py:22` :: cache eviction scans full directory
- [ ] `vendor/fastvec_v2/src/filter_bridge.py:16` :: filter kernel walks the whole chunk
- [ ] `vendor/fastvec_v2/src/index_store.py:23` :: vector index rebuild holds the write lock

### Closing a row

Delete the row when the marker is gone from the tree, and keep the line
numbers current for everything else.  Do not merge rows that point at
different files.
