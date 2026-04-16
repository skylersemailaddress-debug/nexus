# Deployment Contract

Specifies deployment packaging, promotion, and rollback requirements.

## Foundation Deployment Scope
- Apps are runnable locally with Python standard library only.
- Web shell service runs from apps/web/app.py on localhost:8090.
- API service runs from apps/api/app.py on localhost:8085.

## Artifact Promotion Path
- Source changes must pass scripts/validate_local.sh.
- Bootstrap structure checks and package preflight must pass before release packaging.

## Rollback and Verification
- Rollback is commit-based on main.
- Verification gates are deterministic unittest and scaffold integrity checks.
