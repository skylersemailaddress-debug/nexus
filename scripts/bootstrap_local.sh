#!/usr/bin/env bash
set -euo pipefail

# Bootstraps a clean local workspace for Nexus0.5.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf 'Bootstrapping Nexus0.5 workspace at %s\n' "$ROOT_DIR"

required_paths=(
  "docs/truth"
  "docs/contracts"
  "docs/build"
  "apps/web"
  "apps/api"
  "packages/runtime"
  "packages/control-plane"
  "packages/memory-kernel"
  "packages/execution-graph"
  "packages/capability-router"
  "packages/validators"
  "packages/ui-system"
  "proof"
  "benchmarks"
)

for rel in "${required_paths[@]}"; do
  if [[ ! -d "$ROOT_DIR/$rel" ]]; then
    printf 'Missing required path: %s\n' "$rel" >&2
    exit 1
  fi
done

printf 'Bootstrap checks complete. Workspace structure is ready.\n'
