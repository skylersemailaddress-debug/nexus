import json
import threading
import unittest
from http.client import HTTPConnection

from apps.api.app import ApiState, create_server


class ApiEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server("127.0.0.1", 0, ApiState(version="0.0.1-test", ready=True))
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def _get(self, path: str) -> tuple[int, dict]:
        conn = HTTPConnection("127.0.0.1", self.port, timeout=2)
        conn.request("GET", path)
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        conn.close()
        return response.status, payload

    def test_health(self) -> None:
        status, payload = self._get("/health")
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "healthy")

    def test_readiness(self) -> None:
        status, payload = self._get("/readiness")
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "ready")

    def test_version(self) -> None:
        status, payload = self._get("/version")
        self.assertEqual(status, 200)
        self.assertEqual(payload["version"], "0.0.1-test")


if __name__ == "__main__":
    unittest.main()
