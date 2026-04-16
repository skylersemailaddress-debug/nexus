"""Checkpoint envelope for execution runs."""

from __future__ import annotations


def build_checkpoint_envelope(run_snapshot: dict, summary: dict) -> dict:
    return {
        "ok": True,
        "kind": "execution-checkpoint",
        "run": run_snapshot,
        "summary": summary,
    }
