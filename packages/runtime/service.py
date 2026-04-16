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

    def status(self) -> dict:
        return readiness_snapshot(self.boundary, self.state)

    def workspace_status(self, control_state: dict, run_state: dict) -> dict:
        runtime_status = self.status()
        return {
            "ok": runtime_status["ok"],
            "runtime": runtime_status,
            "control": dict(control_state),
            "execution": dict(run_state),
        }
