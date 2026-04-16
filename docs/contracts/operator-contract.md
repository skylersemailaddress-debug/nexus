# Operator Contract

Specifies operator controls, safety gates, and policy surfaces.

## Control Inputs And Outcomes
- Operator-facing API surfaces are health, readiness, and version.
- Control-plane approvals use explicit request and decision records.
- Checkpoint creation path validates payload integrity before record creation.

## Safety And Override Semantics
- Local-only and token boundary hooks are defined in control-plane auth module.
- Unauthorized control actions must fail with deterministic rejection.

## Auditability Requirements
- Approval decisions include reviewer and decision timestamp.
- Checkpoint records include source metadata and deterministic shape.
