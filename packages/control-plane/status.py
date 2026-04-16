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


@dataclass(frozen=True)
class ControlPlaneSessionState:
    approval_status: str = "clear"
    checkpoint_status: str = "primed"
    control_status: str = "stable"

    def snapshot(self) -> dict:
        return {
            "approval_status": self.approval_status,
            "checkpoint_status": self.checkpoint_status,
            "control_status": self.control_status,
        }


def control_plane_snapshot(state: ControlPlaneState | None = None) -> dict:
    return (state or ControlPlaneState()).snapshot()


def session_control_snapshot(state: ControlPlaneState | None = None) -> dict:
    current = state or ControlPlaneState()
    approval_status = "waiting" if current.approvals_required and current.approvals_pending > 0 else "clear"
    session_state = ControlPlaneSessionState(
        approval_status=approval_status,
        checkpoint_status=current.checkpoint_status,
        control_status=current.control_status,
    )
    return session_state.snapshot()