# Runtime Contract

Specifies runtime responsibilities, interfaces, and invariants.

## Runtime Boundary Definitions
- Runtime owns orchestration lifecycle and authority transitions.
- Control-plane modules enforce local and token-based action boundaries.
- Runtime state authority converges to a single durable store.

## Implemented In This Tranche
- packages/runtime/boundary.py defines initial boundary and readiness snapshot.
- packages/runtime/service.py defines RuntimeService objective and status flow.
- apps/api/app.py exposes runtime-facing health/readiness/version service surfaces.

## Execution Guarantees
- Runtime must expose explicit objective status and next action state.
- Runtime checkpoint creation must preserve auditable payload provenance.
- Runtime must reject unauthorized high-impact control-plane actions.

## Failure Handling Expectations
- Boundary failures are explicit and surfaced as policy or authorization errors.
- Transitional scaffolds are permitted only when labeled as scaffold and tracked in donor audit.
