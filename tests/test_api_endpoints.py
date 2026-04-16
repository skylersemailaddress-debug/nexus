import json
import threading
import unittest
from http.client import HTTPConnection

from apps.api.app import ApiState, build_runtime_service, create_server


class ApiEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server(
            "127.0.0.1",
            0,
            ApiState(version="0.0.1-test", ready=True, runtime_service=build_runtime_service()),
        )
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def _get(self, path: str) -> tuple[int, dict, dict[str, str]]:
        conn = HTTPConnection("127.0.0.1", self.port, timeout=2)
        conn.request("GET", path)
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        headers = {key: value for key, value in response.getheaders()}
        conn.close()
        return response.status, payload, headers

    def test_health(self) -> None:
        status, payload, headers = self._get("/health")
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "healthy")
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")

    def test_readiness(self) -> None:
        status, payload, _ = self._get("/readiness")
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "ready")

    def test_version(self) -> None:
        status, payload, _ = self._get("/version")
        self.assertEqual(status, 200)
        self.assertEqual(payload["version"], "0.0.1-test")

    def test_workspace_status(self) -> None:
        status, payload, headers = self._get("/workspace/status?objective=Build%20the%20app")
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["version"], "0.0.1-test")
        self.assertEqual(payload["session"]["objective"], "Build the app")
        self.assertEqual(payload["runtime"]["workspace_status"], "active")
        self.assertEqual(payload["control"]["checkpoint_status"], "primed")
        self.assertEqual(payload["execution"]["status"], "active")
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")


if __name__ == "__main__":
    unittest.main()
