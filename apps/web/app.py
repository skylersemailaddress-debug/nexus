"""Minimal static server for the Nexus web shell foundation."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main() -> None:
    shell_root = Path(__file__).resolve().parent / "shell"
    handler = partial(SimpleHTTPRequestHandler, directory=str(shell_root))
    server = ThreadingHTTPServer(("127.0.0.1", 8090), handler)
    print(f"Nexus web shell listening on http://127.0.0.1:8090 ({shell_root})")
    server.serve_forever()


if __name__ == "__main__":
    main()
