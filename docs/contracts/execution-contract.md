# Execution Contract

Specifies execution graph behavior and orchestration obligations.

## Execution Graph Obligations
- Task graph lifecycle must be explicit: create, queue, execute, checkpoint, finalize.
- Scheduling and retry semantics must be deterministic and auditable.
- Checkpoint policy must be declarative and testable.

## Checkpoint Scaffolds
- checkpoint policy trigger baseline: message_count >= 25 or memory_count >= 10
- checkpoint resolver behavior: fill gaps only and never override live state
- compression summary behavior: scaffold allowed, but production summarization must replace placeholder text

## Implemented In This Tranche
- packages/execution-graph/run.py provides RunPlan shape and task registration.
- packages/execution-graph/task.py provides deterministic task execution placeholder.
- packages/execution-graph/checkpoint.py provides checkpoint envelope shape.

## Forbidden Patterns
- parallel primary execution roots
- hidden side-effect execution outside the declared graph path
