"""Checkpoint resolver scaffold adapted from NexusV3 donor."""

from __future__ import annotations

from typing import Any


def resolve_checkpoint(loop_state: dict[str, Any], checkpoint: dict[str, Any]) -> dict[str, Any]:
    if not checkpoint:
        return loop_state

    merged = dict(loop_state or {})

    # checkpoint fills gaps only and never overrides live state values
    for key, value in checkpoint.items():
        if key not in merged or merged[key] in (None, "", []):
            merged[key] = value

    return merged
