"""Run plan primitives for the execution graph foundation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RunPlan:
    run_id: str
    objective: str
    task_ids: list[str] = field(default_factory=list)

    def add_task(self, task_id: str) -> None:
        if task_id and task_id not in self.task_ids:
            self.task_ids.append(task_id)

    def snapshot(self) -> dict:
        return {
            "run_id": self.run_id,
            "objective": self.objective,
            "task_count": len(self.task_ids),
            "task_ids": list(self.task_ids),
        }

    def to_run_state(self, status: str = "planned", checkpoint_state: str = "ready") -> "RunState":
        return RunState(
            run_id=self.run_id,
            objective=self.objective,
            status=status,
            task_ids=list(self.task_ids),
            checkpoint_state=checkpoint_state,
        )


@dataclass(frozen=True)
class RunState:
    run_id: str
    objective: str
    status: str = "planned"
    task_ids: list[str] = field(default_factory=list)
    checkpoint_state: str = "ready"

    @property
    def task_count(self) -> int:
        return len(self.task_ids)

    def snapshot(self) -> dict:
        return {
            "run_id": self.run_id,
            "objective": self.objective,
            "status": self.status,
            "task_count": self.task_count,
            "task_ids": list(self.task_ids),
            "checkpoint_state": self.checkpoint_state,
        }


@dataclass(frozen=True)
class RunSessionState:
    run_id: str
    status: str = "planned"
    phase: str = "intake"
    task_count: int = 0

    def snapshot(self) -> dict:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "phase": self.phase,
            "task_count": self.task_count,
        }


@dataclass(frozen=True)
class CommandRunState:
    run_id: str
    task_id: str
    status: str = "queued"
    phase: str = "command"

    def snapshot(self) -> dict:
        return {
            "run_id": self.run_id,
            "task_id": self.task_id,
            "status": self.status,
            "phase": self.phase,
            "task_count": 1,
        }


def build_run_state(objective: str, task_ids: list[str] | None = None, status: str = "planned") -> RunState:
    normalized_tasks = [task_id for task_id in (task_ids or []) if task_id]
    run_id = f"run-{objective.lower().replace(' ', '-')[:24] or 'idle'}"
    return RunState(run_id=run_id, objective=objective, status=status, task_ids=normalized_tasks)


def build_run_session_state(run_state: RunState) -> RunSessionState:
    phase = "blocked" if run_state.status == "blocked" else "execution"
    return RunSessionState(
        run_id=run_state.run_id,
        status=run_state.status,
        phase=phase,
        task_count=run_state.task_count,
    )


def build_command_run_state(command_id: str, command_text: str, ready: bool = True) -> CommandRunState:
    normalized = command_text.lower().replace(" ", "-")[:20] or "command"
    run_id = f"run-{normalized}"
    task_id = f"task-{command_id}"
    return CommandRunState(
        run_id=run_id,
        task_id=task_id,
        status="queued" if ready else "blocked",
        phase="command" if ready else "blocked",
    )
