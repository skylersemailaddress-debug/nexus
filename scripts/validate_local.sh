#!/usr/bin/env bash
set -euo pipefail

# Validates repository scaffold integrity and policy-critical docs.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=(
  "README.md"
  "VERSION"
  "CHANGELOG.md"
  "docs/truth/SYSTEM_DOCTRINE.md"
  "docs/truth/ACCEPTANCE_CRITERIA.md"
  "docs/truth/MERGE_RULES.md"
  "docs/truth/SUBSYSTEM_EXTRACTION_MAP.md"
  "docs/truth/BUILD_STRATEGY.md"
  "docs/contracts/runtime-contract.md"
  "docs/contracts/memory-contract.md"
  "docs/contracts/operator-contract.md"
  "docs/contracts/execution-contract.md"
  "docs/contracts/deployment-contract.md"
  "docs/build/IMPLEMENTATION_PLAN.md"
  "docs/build/LOCAL_BUILD_WORKFLOW.md"
  "docs/build/DONOR_IMPORT_POLICY.md"
  "reports/github-vs-canon-gap-audit.md"
  "reports/donor-audit.md"
  "reports/launch-readiness-report.md"
  "scripts/bootstrap_local.sh"
  "scripts/package_release.sh"
)

for rel in "${required_files[@]}"; do
  if [[ ! -f "$ROOT_DIR/$rel" ]]; then
    printf 'Missing required file: %s\n' "$rel" >&2
    exit 1
  fi
done

if [[ ! -d "$ROOT_DIR/tests" ]]; then
  printf 'Missing tests directory.\n' >&2
  exit 1
fi

python -m unittest discover -s "$ROOT_DIR/tests" -p 'test_*.py'

printf 'Validation passed: required scaffold files are present.\n'
