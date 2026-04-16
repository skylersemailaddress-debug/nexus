"""Control-plane scaffold exports."""

from .approvals import ApprovalDecision, ApprovalRequest, approve, reject
from .auth import AuthConfig, require_api_token, require_local_access, require_runner_secret
from .checkpoints import build_checkpoint_payload, create_checkpoint_record
from .registry import registry_capabilities

__all__ = [
    "ApprovalDecision",
    "ApprovalRequest",
    "AuthConfig",
    "approve",
    "reject",
    "require_api_token",
    "require_local_access",
    "require_runner_secret",
    "build_checkpoint_payload",
    "create_checkpoint_record",
    "registry_capabilities",
]
