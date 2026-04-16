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
        service.activate_session("Ship the first workspace flow")
        status = service.status()
        self.assertTrue(status["ok"])
        self.assertEqual(status["durable_store"], "postgres")
        self.assertEqual(status["workspace_status"], "active")

    def test_runtime_composes_workspace_status(self) -> None:
        boundary = RuntimeBoundary(
            authority_owner="nexus",
            durable_store="postgres",
            control_plane_enabled=True,
            execution_graph_enabled=True,
        )
        service = RuntimeService(boundary=boundary, state=RuntimeState())
        service.activate_session("Surface state")
        workspace = service.workspace_status(
            {"control_status": "stable", "checkpoint_status": "primed"},
            {"status": "active", "task_count": 2},
        )
        self.assertTrue(workspace["ok"])
        self.assertEqual(workspace["control"]["control_status"], "stable")
        self.assertEqual(workspace["execution"]["status"], "active")

    def test_runtime_composes_session_status(self) -> None:
        boundary = RuntimeBoundary(
            authority_owner="nexus",
            durable_store="postgres",
            control_plane_enabled=True,
            execution_graph_enabled=True,
        )
        service = RuntimeService(boundary=boundary, state=RuntimeState())
        service.activate_session("Session flow")
        session = service.session_status(
            {"approval_status": "clear", "checkpoint_status": "primed"},
            {"status": "active", "phase": "execution", "task_count": 2},
        )
        self.assertTrue(session["ok"])
        self.assertEqual(session["control"]["approval_status"], "clear")
        self.assertEqual(session["execution"]["phase"], "execution")

    def test_runtime_submit_command(self) -> None:
        boundary = RuntimeBoundary(
            authority_owner="nexus",
            durable_store="postgres",
            control_plane_enabled=True,
            execution_graph_enabled=True,
        )
        service = RuntimeService(boundary=boundary, state=RuntimeState())
        payload = service.submit_command(
            "Run checks",
            {"command_id": "cmd-0001", "command_status": "accepted"},
            {"run_id": "run-run-checks", "task_id": "task-cmd-0001", "status": "queued"},
        )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["request"]["command_id"], "cmd-0001")
        self.assertEqual(payload["session"]["command_count"], 1)
        self.assertEqual(payload["session"]["last_command"], "Run checks")

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

    def test_control_plane_status_model_loads(self) -> None:
        root = Path(__file__).resolve().parents[1]
        module_path = root / "packages" / "control-plane" / "status.py"
        spec = util.spec_from_file_location("control_plane_status", module_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        state = module.ControlPlaneState(approvals_pending=1, approvals_required=True)
        snapshot = state.snapshot()
        self.assertEqual(snapshot["approvals_pending"], 1)
        self.assertTrue(snapshot["approvals_required"])
        session_snapshot = module.session_control_snapshot(state)
        self.assertEqual(session_snapshot["approval_status"], "waiting")
        command_snapshot = module.command_control_snapshot("cmd-0001")
        self.assertEqual(command_snapshot["command_id"], "cmd-0001")
        self.assertEqual(command_snapshot["command_status"], "accepted")

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
        run_state = run_plan.to_run_state(status="active")
        self.assertEqual(run_state.snapshot()["status"], "active")
        run_session = module.build_run_session_state(run_state)
        self.assertEqual(run_session.snapshot()["phase"], "execution")
        command_run = module.build_command_run_state("cmd-0001", "Run checks")
        self.assertEqual(command_run.snapshot()["task_id"], "task-cmd-0001")


if __name__ == "__main__":
    unittest.main()
