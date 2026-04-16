# Nexus0.5 Target Repository

This repository is a **fresh Nexus build target** for Nexus0.5.

## Purpose
- Establish a clean, enterprise-grade foundation for mission-driven implementation.
- Use **Autobuilder** as the primary build and orchestration engine for local development.
- Keep architecture authority in this repo's truth and contract documents.

## Repository Policy
- Legacy Nexus variants are **donor/reference only**.
- No blind merge of legacy repositories or source trees.
- Selective extraction must follow documented merge and donor import policies.
- No duplicate authority: truth docs and contracts define canonical intent.

## Canonical Local Workflow
1. Bootstrap local environment.
2. Validate local structure and policy compliance.
3. Execute implementation work against current truth/contracts.
4. Capture proof artifacts and readiness outputs.

Use scripts:
- `scripts/bootstrap_local.sh`
- `scripts/validate_local.sh`
- `scripts/package_release.sh`

See:
- `docs/build/LOCAL_BUILD_WORKFLOW.md`
- `docs/build/IMPLEMENTATION_PLAN.md`
- `docs/truth/BUILD_STRATEGY.md`
