"""Runtime service scaffold connecting boundary concepts to executable shape."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .boundary import RuntimeBoundary, RuntimeState, readiness_snapshot


@dataclass
class RuntimeService:
    boundary: RuntimeBoundary
    state: RuntimeState

    def set_objective(self, objective: str, next_action: str) -> None:
        self.state.objective = objective
        self.state.next_action = next_action
        self.state.workspace_status = "active"
        self.state.updated_at = datetime.now(UTC).isoformat()

    def activate_session(self, objective: str | None) -> dict:
        normalized_objective = (objective or "Nexus build workspace").strip() or "Nexus build workspace"
        next_action = "Review control and execution status surfaces."
        self.set_objective(normalized_objective, next_action)
        return self.status()

    def submit_command(self, command: str, control_state: dict, run_state: dict) -> dict:
        normalized_command = command.strip() or "noop"
        self.state.command_count += 1
        command_id = f"cmd-{self.state.command_count:04d}"
        self.state.last_command = normalized_command
        self.state.objective = normalized_command
        self.state.next_action = "Review command response and session state."
        self.state.workspace_status = "active"
        self.state.updated_at = datetime.now(UTC).isoformat()

        runtime_status = self.status()
        return {
            "ok": runtime_status["ok"],
            "request": {
                "command": normalized_command,
                "command_id": command_id,
            },
            "response": {
                "accepted": runtime_status["ok"],
                "message": "Deterministic command accepted.",
                "echo": normalized_command,
            },
            "session": {
                "session_id": runtime_status["session_id"],
                "objective": runtime_status["objective"],
                "next_action": runtime_status["next_action"],
                "workspace_status": runtime_status["workspace_status"],
                "command_count": runtime_status["command_count"],
                "last_command": runtime_status["last_command"],
            },
            "control": dict(control_state),
            "execution": dict(run_state),
            "runtime_updated_at": runtime_status["updated_at"],
        }

    def status(self) -> dict:
        return readiness_snapshot(self.boundary, self.state)

    def session_status(self, control_state: dict, run_state: dict) -> dict:
        runtime_status = self.status()
        return {
            "ok": runtime_status["ok"],
            "session": {
                "session_id": runtime_status["session_id"],
                "objective": runtime_status["objective"],
                "next_action": runtime_status["next_action"],
                "workspace_status": runtime_status["workspace_status"],
            },
            "control": dict(control_state),
            "execution": dict(run_state),
            "runtime_updated_at": runtime_status["updated_at"],
        }

    def workspace_status(self, control_state: dict, run_state: dict) -> dict:
        runtime_status = self.status()
        return {
            "ok": runtime_status["ok"],
            "runtime": runtime_status,
            "control": dict(control_state),
            "execution": dict(run_state),
        }
