"""Checkpoint payload scaffold adapted from NexusV3 donor."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4


def build_checkpoint_payload(project_state: dict) -> dict:
    if not isinstance(project_state, dict):
        return {"ok": False, "error": "invalid-project-state"}

    objective = project_state.get("objective")
    next_step = project_state.get("next_step")
    blockers = project_state.get("blockers", [])
    recent_jobs = project_state.get("recent_jobs", [])
    recent_messages = project_state.get("recent_messages", [])
    relevant_memory = project_state.get("relevant_memory", [])

    return {
        "ok": True,
        "captured_at": datetime.now(UTC).isoformat(),
        "objective": objective.get("title") if isinstance(objective, dict) else None,
        "next_step": next_step.get("title") if isinstance(next_step, dict) else None,
        "open_blockers": len(blockers),
        "recent_job_ids": [job.get("id") for job in recent_jobs[:5] if isinstance(job, dict)],
        "memory_signals": [item.get("title") for item in relevant_memory[:5] if isinstance(item, dict)],
        "recent_messages_tail": [
            {
                "role": message.get("role"),
                "content": message.get("content"),
                "created_at": str(message.get("created_at")),
            }
            for message in recent_messages[-5:]
            if isinstance(message, dict)
        ],
    }


def create_checkpoint_record(project_id: str, payload: dict) -> dict:
    if not project_id:
        return {"ok": False, "error": "missing-project-id"}
    if not payload.get("ok"):
        return {"ok": False, "error": "invalid-payload"}

    return {
        "ok": True,
        "checkpoint": {
            "id": f"ckpt_{uuid4().hex[:16]}",
            "project_id": project_id,
            "kind": "checkpoint",
            "title": f"Checkpoint {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}Z",
            "payload": payload,
            "meta": {"source": "checkpoint_scaffold"},
        },
    }
