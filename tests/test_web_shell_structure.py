from pathlib import Path
import unittest


class WebShellStructureTests(unittest.TestCase):
    def test_shell_foundation_files_exist(self) -> None:
        root = Path(__file__).resolve().parents[1]
        shell = root / "apps" / "web" / "shell"
        expected = [
            shell / "index.html",
            shell / "shell.css",
            shell / "shell.js",
            shell / "tokens.css",
            shell / "adaptive" / "adaptive-shell.js",
            shell / "adaptive" / "layout-engine.js",
        ]
        for path in expected:
            self.assertTrue(path.is_file(), f"missing shell file: {path}")

    def test_index_contains_workspace_first_shell_markers(self) -> None:
        root = Path(__file__).resolve().parents[1]
        index_html = (root / "apps" / "web" / "shell" / "index.html").read_text(encoding="utf-8")
        self.assertIn("composerInput", index_html)
        self.assertIn("surface-layer", index_html)
        self.assertIn("Nexus Dock", index_html)
        self.assertIn("workspaceStatusPanel", index_html)
        self.assertIn("systemStatusPanel", index_html)
        self.assertIn("activityFeed", index_html)

    def test_shell_wires_api_surfaces(self) -> None:
        root = Path(__file__).resolve().parents[1]
        shell_js = (root / "apps" / "web" / "shell" / "shell.js").read_text(encoding="utf-8")
        self.assertIn("http://127.0.0.1:8085", shell_js)
        self.assertIn('"/health"', shell_js)
        self.assertIn('"/readiness"', shell_js)
        self.assertIn('"/version"', shell_js)
        self.assertIn('"/session/status"', shell_js)
        self.assertIn('"/workspace/status', shell_js)


if __name__ == "__main__":
    unittest.main()
