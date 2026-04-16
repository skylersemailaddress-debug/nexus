#!/usr/bin/env bash
set -euo pipefail

# Performs a lightweight packaging preflight for release readiness.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION_FILE="$ROOT_DIR/VERSION"

if [[ ! -f "$VERSION_FILE" ]]; then
  printf 'VERSION file not found.\n' >&2
  exit 1
fi

VERSION="$(tr -d '[:space:]' < "$VERSION_FILE")"
if [[ -z "$VERSION" ]]; then
  printf 'VERSION is empty.\n' >&2
  exit 1
fi

printf 'Release preflight OK for version %s\n' "$VERSION"
printf 'Packaging implementation is intentionally deferred until subsystem delivery.\n'
