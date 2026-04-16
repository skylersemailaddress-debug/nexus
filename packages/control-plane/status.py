"""Initial control-plane state model for shell-visible status."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ControlPlaneState:
    mode: str = "local"
    approvals_pending: int = 0
    approvals_required: bool = False
    checkpoint_status: str = "primed"
    last_checkpoint_id: str | None = None
    control_status: str = "stable"
    notes: tuple[str, ...] = field(default_factory=lambda: ("Local control plane ready.",))

    def snapshot(self) -> dict:
        return {
            "mode": self.mode,
            "approvals_pending": self.approvals_pending,
            "approvals_required": self.approvals_required,
            "checkpoint_status": self.checkpoint_status,
            "last_checkpoint_id": self.last_checkpoint_id,
            "control_status": self.control_status,
            "notes": list(self.notes),
        }


def control_plane_snapshot(state: ControlPlaneState | None = None) -> dict:
    return (state or ControlPlaneState()).snapshot()