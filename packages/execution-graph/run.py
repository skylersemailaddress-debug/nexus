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
