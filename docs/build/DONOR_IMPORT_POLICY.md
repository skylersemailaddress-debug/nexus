# Donor Import Policy

Defines strict policy for selective donor extraction.

## Initial Policy
- Donor repositories are reference-only.
- Import only subsystem-scoped slices with explicit mapping.
- Record extraction rationale and compatibility constraints.
- Reject any import that introduces duplicate authority.

## Controlled Pull Record: 2026-04-16

Archives:
- /workspaces/nexus/NEXUS0.5.7z
- /workspaces/nexus/NexusV3.7z

Enforcement:
- fresh nexus repo remains sole authority
- no whole-repo merges
- no donor tree wholesale copy
- only approved candidates inspected
- only allowed landing areas modified

### Pull 1: NEXUS0.5 decisions

ADAPT:
- apps/shell/index.html -> apps/web/shell/index.html
- apps/shell/shell.css -> apps/web/shell/shell.css
- apps/shell/shell.js -> apps/web/shell/shell.js
- apps/shell/tokens.css -> apps/web/shell/tokens.css
- apps/shell/adaptive/adaptive-shell.css -> apps/web/shell/adaptive/adaptive-shell.css
- apps/shell/adaptive/adaptive-shell.js -> apps/web/shell/adaptive/adaptive-shell.js
- apps/shell/adaptive/layout-engine.js -> apps/web/shell/adaptive/layout-engine.js
- apps/shell/adaptive/panel-engine.js -> apps/web/shell/adaptive/panel-engine.js
- apps/shell/adaptive/state-stream.js -> apps/web/shell/adaptive/state-stream.js
- apps/shell/adaptive/ui-store.js -> apps/web/shell/adaptive/ui-store.js
- docs/architecture/NEXUS05_COMPLETION_ROADMAP.md -> docs/build/NEXUS05_COMPLETION_ROADMAP.md
- docs/architecture/NEXUS05_COMPLETION_NEXT_STEP.md -> docs/build/NEXUS05_COMPLETION_NEXT_STEP.md
- docs/architecture/NEXUS05_EXECUTION_LAYER_PACK_OVERVIEW.md -> docs/build/NEXUS05_EXECUTION_LAYER_PACK_OVERVIEW.md
- docs/architecture/NEXUS05_EXECUTION_PROOF_RUN_PACK_OVERVIEW.md -> docs/build/NEXUS05_EXECUTION_PROOF_RUN_PACK_OVERVIEW.md
- canon/contracts/RUNTIME_AUTHORITY.md -> doctrine principles adapted into docs/truth/SYSTEM_DOCTRINE.md

ADOPT:
- apps/shell/UI_DOCTRINE_SUMMARY.md -> packages/ui-system/UI_DOCTRINE_SUMMARY.md
- apps/shell/interaction_notes.md -> packages/ui-system/interaction_notes.md

REJECT:
- canon/contracts/control_plane_contract.yaml
- canon/contracts/execution_authority.yaml
- canon/contracts/runtime_authority.yaml
Reason: these donor canonical contracts would create competing authority. Contract intent was instead adapted into existing fresh nexus docs/contracts and docs/truth.

### Pull 2: NexusV3 decisions

ADAPT:
- canon/clean/control/auth.py -> packages/control-plane/auth.py
- canon/clean/control/checkpoints_2.py -> packages/control-plane/checkpoints.py
- canon/clean/control/registry_4.py -> packages/control-plane/registry.py
- canon/clean/control/db_2.py -> packages/control-plane/db.py
- canon/clean/control/db_reset_runner_2.py -> packages/control-plane/db_reset_runner.py
- canon/clean/continuity/checkpoint_policy_2.py -> packages/execution-graph/checkpoint_policy.py
- canon/clean/continuity/checkpoint_resolver_2.py -> packages/execution-graph/checkpoint_resolver.py

REJECT:
- canon/clean/control/main_2.py
Reason: highly coupled to donor app bootstrap and route tree; importing would violate subsystem-scoped scaffold intent.
