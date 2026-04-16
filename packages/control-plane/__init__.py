"""Control-plane scaffold exports."""

from .approvals import ApprovalDecision, ApprovalRequest, approve, reject
from .auth import AuthConfig, require_api_token, require_local_access, require_runner_secret
from .checkpoints import build_checkpoint_payload, create_checkpoint_record
from .registry import registry_capabilities
from .status import (
    CommandControlState,
    ControlPlaneSessionState,
    ControlPlaneState,
    command_control_snapshot,
    control_plane_snapshot,
    session_control_snapshot,
)

__all__ = [
    "ApprovalDecision",
    "ApprovalRequest",
    "AuthConfig",
    "ControlPlaneState",
    "ControlPlaneSessionState",
    "CommandControlState",
    "approve",
    "control_plane_snapshot",
    "session_control_snapshot",
    "command_control_snapshot",
    "reject",
    "require_api_token",
    "require_local_access",
    "require_runner_secret",
    "build_checkpoint_payload",
    "create_checkpoint_record",
    "registry_capabilities",
]
