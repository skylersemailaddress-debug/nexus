"""Task primitives for the execution graph foundation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    kind: str = "generic"


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    status: str
    detail: str


def run_task(task: Task) -> TaskResult:
    return TaskResult(task_id=task.task_id, status="completed", detail=f"task {task.title} executed")
