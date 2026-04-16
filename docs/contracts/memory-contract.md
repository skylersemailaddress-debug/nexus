# Memory Contract

Specifies memory model, lifecycle, and consistency expectations.

## Data Persistence Boundaries
- Checkpoint payloads capture objective, next step, blockers, jobs, and message tail.
- Execution checkpoint envelope stores run snapshot plus summary payload.

## Memory Consistency Semantics
- Checkpoint resolver fills missing values only and never overrides live non-empty values.
- Compression summary is currently scaffold-level and marked for replacement.

## Recovery And Compaction Behavior
- should_checkpoint baseline rule is deterministic and explicit.
- Future compaction upgrades must preserve deterministic summary contract.
