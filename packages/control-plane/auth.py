"""Control-plane auth scaffold adapted from NexusV3 donor."""

from __future__ import annotations

from dataclasses import dataclass


ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}


@dataclass(frozen=True)
class AuthConfig:
    api_bearer_token: str
    web_client_id: str
    runner_shared_secret: str


def require_local_access(client_host: str | None) -> None:
    if client_host not in ALLOWED_HOSTS:
        raise PermissionError("Local access only")


def require_api_token(
    client_host: str | None,
    config: AuthConfig,
    authorization: str | None = None,
    x_nexus_client: str | None = None,
) -> bool:
    require_local_access(client_host)

    expected = f"Bearer {config.api_bearer_token}"
    if authorization == expected:
        return True

    if x_nexus_client == config.web_client_id:
        return True

    raise PermissionError("Unauthorized")


def require_runner_secret(
    client_host: str | None,
    config: AuthConfig,
    x_runner_secret: str | None = None,
    authorization: str | None = None,
) -> bool:
    require_local_access(client_host)

    expected_secret = config.runner_shared_secret
    expected_bearer = f"Bearer {expected_secret}"
    if x_runner_secret != expected_secret and authorization != expected_bearer:
        raise PermissionError("Unauthorized")

    return True
