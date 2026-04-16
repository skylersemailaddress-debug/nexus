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


@dataclass(frozen=True)
class CommandControlState:
    command_id: str
    command_status: str = "accepted"
    control_status: str = "stable"
    review_required: bool = False

    def snapshot(self) -> dict:
        return {
            "command_id": self.command_id,
            "command_status": self.command_status,
            "control_status": self.control_status,
            "review_required": self.review_required,
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


def command_control_snapshot(command_id: str, ready: bool = True) -> dict:
    command_state = CommandControlState(
        command_id=command_id,
        command_status="accepted" if ready else "blocked",
        control_status="stable" if ready else "degraded",
        review_required=not ready,
    )
    return command_state.snapshot()