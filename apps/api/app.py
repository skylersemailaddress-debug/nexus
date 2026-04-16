"""Deterministic local Nexus API service."""

from __future__ import annotations

import json
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


@dataclass(frozen=True)
class ApiState:
    version: str
    ready: bool = True


def read_version(repo_root: Path) -> str:
    version_path = repo_root / "VERSION"
    return version_path.read_text(encoding="utf-8").strip()


class NexusAPIHandler(BaseHTTPRequestHandler):
    server_version = "NexusAPI/0.1"

    def _write_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        state: ApiState = self.server.api_state  # type: ignore[attr-defined]

        if self.path == "/health":
            self._write_json({"ok": True, "service": "nexus-api", "status": "healthy"})
            return

        if self.path == "/readiness":
            status = HTTPStatus.OK if state.ready else HTTPStatus.SERVICE_UNAVAILABLE
            self._write_json(
                {"ok": state.ready, "service": "nexus-api", "status": "ready" if state.ready else "not-ready"},
                status=status,
            )
            return

        if self.path == "/version":
            self._write_json({"ok": True, "service": "nexus-api", "version": state.version})
            return

        self._write_json({"ok": False, "error": "not-found", "path": self.path}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Keep tests and local runs deterministic and quiet.
        return


def create_server(host: str, port: int, state: ApiState) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), NexusAPIHandler)
    server.api_state = state  # type: ignore[attr-defined]
    return server


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    version = read_version(repo_root)
    state = ApiState(version=version, ready=True)
    server = create_server("127.0.0.1", 8085, state)
    print("Nexus API listening on http://127.0.0.1:8085")
    server.serve_forever()


if __name__ == "__main__":
    main()
