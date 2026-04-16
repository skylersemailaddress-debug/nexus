"""Deterministic local Nexus API service."""

from __future__ import annotations

import importlib.util
import json
from functools import lru_cache
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlparse

from packages.runtime import RuntimeBoundary, RuntimeService, RuntimeState


@dataclass(frozen=True)
class ApiState:
    version: str
    ready: bool = True
    repo_root: Path | None = None
    runtime_service: RuntimeService | None = None


def read_version(repo_root: Path) -> str:
    version_path = repo_root / "VERSION"
    return version_path.read_text(encoding="utf-8").strip()


class NexusAPIHandler(BaseHTTPRequestHandler):
    server_version = "NexusAPI/0.1"

    def _send_json_headers(self, body: bytes, status: HTTPStatus) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _write_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self._send_json_headers(body, status)
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_json_headers(b"", HTTPStatus.NO_CONTENT)

    def do_GET(self) -> None:  # noqa: N802
        state: ApiState = self.server.api_state  # type: ignore[attr-defined]
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/health":
            self._write_json({"ok": True, "service": "nexus-api", "status": "healthy"})
            return

        if parsed.path == "/readiness":
            status = HTTPStatus.OK if state.ready else HTTPStatus.SERVICE_UNAVAILABLE
            self._write_json(
                {"ok": state.ready, "service": "nexus-api", "status": "ready" if state.ready else "not-ready"},
                status=status,
            )
            return

        if parsed.path == "/version":
            self._write_json({"ok": True, "service": "nexus-api", "version": state.version})
            return

        if parsed.path == "/workspace/status":
            objective = query.get("objective", [None])[0]
            self._write_json(build_workspace_status(state, objective=objective))
            return

        self._write_json({"ok": False, "error": "not-found", "path": parsed.path}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Keep tests and local runs deterministic and quiet.
        return


def _module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _control_plane_status_module(repo_root: str):
    return _module_from_path(
        "nexus_control_plane_status",
        Path(repo_root) / "packages" / "control-plane" / "status.py",
    )


@lru_cache(maxsize=1)
def _execution_graph_run_module(repo_root: str):
    return _module_from_path(
        "nexus_execution_graph_run",
        Path(repo_root) / "packages" / "execution-graph" / "run.py",
    )


def build_workspace_status(state: ApiState, objective: str | None = None) -> dict:
    repo_root = state.repo_root or Path(__file__).resolve().parents[2]
    runtime_service = state.runtime_service or build_runtime_service()
    runtime_snapshot = runtime_service.activate_session(objective)

    control_module = _control_plane_status_module(str(repo_root))
    control_state = control_module.ControlPlaneState(
        approvals_pending=0,
        approvals_required=False,
        checkpoint_status="primed" if state.ready else "blocked",
        control_status="stable" if state.ready else "degraded",
        last_checkpoint_id="ckpt-local-shell",
        notes=("Approvals idle.", "Checkpoint surface ready."),
    )

    execution_module = _execution_graph_run_module(str(repo_root))
    run_state = execution_module.build_run_state(
        objective=runtime_snapshot["objective"] or "Nexus build workspace",
        task_ids=["probe-api-surface", "render-shell-status"],
        status="active" if state.ready else "blocked",
    )

    workspace = runtime_service.workspace_status(control_state.snapshot(), run_state.snapshot())
    workspace.update(
        {
            "service": "nexus-api",
            "version": state.version,
            "session": {
                "session_id": runtime_snapshot["session_id"],
                "objective": runtime_snapshot["objective"],
                "next_action": runtime_snapshot["next_action"],
            },
        }
    )
    return workspace


def build_runtime_service() -> RuntimeService:
    boundary = RuntimeBoundary(
        authority_owner="nexus",
        durable_store="postgres",
        control_plane_enabled=True,
        execution_graph_enabled=True,
    )
    state = RuntimeState()
    return RuntimeService(boundary=boundary, state=state)


def create_server(host: str, port: int, state: ApiState) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), NexusAPIHandler)
    server.api_state = state  # type: ignore[attr-defined]
    return server


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    version = read_version(repo_root)
    state = ApiState(version=version, ready=True, repo_root=repo_root, runtime_service=build_runtime_service())
    server = create_server("127.0.0.1", 8085, state)
    print("Nexus API listening on http://127.0.0.1:8085")
    server.serve_forever()


if __name__ == "__main__":
    main()
