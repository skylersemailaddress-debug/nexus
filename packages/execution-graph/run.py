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


def build_run_state(objective: str, task_ids: list[str] | None = None, status: str = "planned") -> RunState:
    normalized_tasks = [task_id for task_id in (task_ids or []) if task_id]
    run_id = f"run-{objective.lower().replace(' ', '-')[:24] or 'idle'}"
    return RunState(run_id=run_id, objective=objective, status=status, task_ids=normalized_tasks)
