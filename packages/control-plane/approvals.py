"""Minimal approval boundary for control-plane actions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class ApprovalRequest:
    request_id: str
    action: str
    actor: str
    reason: str


@dataclass(frozen=True)
class ApprovalDecision:
    request_id: str
    approved: bool
    reviewer: str
    decided_at: str


def approve(request: ApprovalRequest, reviewer: str) -> ApprovalDecision:
    return ApprovalDecision(
        request_id=request.request_id,
        approved=True,
        reviewer=reviewer,
        decided_at=datetime.now(UTC).isoformat(),
    )


def reject(request: ApprovalRequest, reviewer: str) -> ApprovalDecision:
    return ApprovalDecision(
        request_id=request.request_id,
        approved=False,
        reviewer=reviewer,
        decided_at=datetime.now(UTC).isoformat(),
    )
