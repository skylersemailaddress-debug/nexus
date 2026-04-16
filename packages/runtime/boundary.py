"""Initial runtime boundary definitions for Nexus foundation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class RuntimeBoundary:
    authority_owner: str
    durable_store: str
    control_plane_enabled: bool
    execution_graph_enabled: bool

    def is_valid(self) -> bool:
        return (
            self.authority_owner == "nexus"
            and self.durable_store == "postgres"
            and self.control_plane_enabled
            and self.execution_graph_enabled
        )


@dataclass
class RuntimeState:
    objective: str | None = None
    next_action: str | None = None
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


def readiness_snapshot(boundary: RuntimeBoundary, state: RuntimeState) -> dict:
    return {
        "ok": boundary.is_valid(),
        "authority_owner": boundary.authority_owner,
        "durable_store": boundary.durable_store,
        "control_plane_enabled": boundary.control_plane_enabled,
        "execution_graph_enabled": boundary.execution_graph_enabled,
        "objective": state.objective,
        "next_action": state.next_action,
        "updated_at": state.updated_at,
    }
