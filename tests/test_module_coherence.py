from importlib import util
from pathlib import Path
import sys
import unittest

from packages.runtime import RuntimeBoundary, RuntimeService, RuntimeState


class ModuleCoherenceTests(unittest.TestCase):
    def test_runtime_package_importability(self) -> None:
        boundary = RuntimeBoundary(
            authority_owner="nexus",
            durable_store="postgres",
            control_plane_enabled=True,
            execution_graph_enabled=True,
        )
        service = RuntimeService(boundary=boundary, state=RuntimeState())
        status = service.status()
        self.assertTrue(status["ok"])
        self.assertEqual(status["durable_store"], "postgres")

    def test_control_plane_module_loads(self) -> None:
        root = Path(__file__).resolve().parents[1]
        module_path = root / "packages" / "control-plane" / "approvals.py"
        spec = util.spec_from_file_location("control_plane_approvals", module_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        self.assertTrue(hasattr(module, "ApprovalRequest"))
        self.assertTrue(hasattr(module, "approve"))

    def test_execution_graph_module_shape(self) -> None:
        root = Path(__file__).resolve().parents[1]
        module_path = root / "packages" / "execution-graph" / "run.py"
        spec = util.spec_from_file_location("execution_graph_run", module_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        run_plan = module.RunPlan(run_id="run-1", objective="ship foundation")
        run_plan.add_task("task-1")
        snapshot = run_plan.snapshot()
        self.assertEqual(snapshot["task_count"], 1)


if __name__ == "__main__":
    unittest.main()
