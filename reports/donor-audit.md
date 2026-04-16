# Donor Audit

Controlled donor pull executed on 2026-04-16.

## Archives
- /workspaces/nexus/NEXUS0.5.7z
- /workspaces/nexus/NexusV3.7z

## Pull 1: NEXUS0.5

Purpose:
- UI shell and doctrine references

Landing areas used:
- apps/web
- packages/ui-system
- docs/truth
- docs/build

Decision summary:
- ADOPT: 2
- ADAPT: 15
- REJECT: 3

ADOPT:
- apps/shell/UI_DOCTRINE_SUMMARY.md
- apps/shell/interaction_notes.md

ADAPT:
- apps/shell/index.html
- apps/shell/shell.css
- apps/shell/shell.js
- apps/shell/tokens.css
- apps/shell/adaptive/adaptive-shell.css
- apps/shell/adaptive/adaptive-shell.js
- apps/shell/adaptive/layout-engine.js
- apps/shell/adaptive/panel-engine.js
- apps/shell/adaptive/state-stream.js
- apps/shell/adaptive/ui-store.js
- docs/architecture/NEXUS05_COMPLETION_ROADMAP.md
- docs/architecture/NEXUS05_COMPLETION_NEXT_STEP.md
- docs/architecture/NEXUS05_EXECUTION_LAYER_PACK_OVERVIEW.md
- docs/architecture/NEXUS05_EXECUTION_PROOF_RUN_PACK_OVERVIEW.md
- canon/contracts/RUNTIME_AUTHORITY.md

REJECT:
- canon/contracts/control_plane_contract.yaml
- canon/contracts/execution_authority.yaml
- canon/contracts/runtime_authority.yaml

Risk notes:
- Donor shell had direct backend and extension hooks; those were removed to avoid hidden runtime coupling.
- Donor canonical contract yaml files were rejected to prevent authority conflict.

## Pull 2: NexusV3

Purpose:
- control-plane scaffold
- execution graph scaffold
- runtime boundary ideas

Landing areas used:
- packages/control-plane
- packages/execution-graph
- packages/runtime
- docs/contracts

Decision summary:
- ADAPT: 7
- REJECT: 1

ADAPT:
- canon/clean/control/auth.py
- canon/clean/control/checkpoints_2.py
- canon/clean/control/registry_4.py
- canon/clean/control/db_2.py
- canon/clean/control/db_reset_runner_2.py
- canon/clean/continuity/checkpoint_policy_2.py
- canon/clean/continuity/checkpoint_resolver_2.py

REJECT:
- canon/clean/control/main_2.py

Risk notes:
- Main application bootstrap module from donor is tightly coupled and was intentionally excluded.
- Imported scaffold modules are explicitly marked as scaffold and require contract-driven implementation.
