"""Runtime service scaffold connecting boundary concepts to executable shape."""

from __future__ import annotations

from dataclasses import dataclass

from .boundary import RuntimeBoundary, RuntimeState, readiness_snapshot


@dataclass
class RuntimeService:
    boundary: RuntimeBoundary
    state: RuntimeState

    def set_objective(self, objective: str, next_action: str) -> None:
        self.state.objective = objective
        self.state.next_action = next_action

    def status(self) -> dict:
        return readiness_snapshot(self.boundary, self.state)
