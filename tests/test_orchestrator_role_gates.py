import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_PLAN_PATH = (
    ROOT / "docs" / "02-features" / "05-orchestrator-sub-agent-roles" / "test-plan.md"
)


class TestOrchestratorRoleGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = TEST_PLAN_PATH.read_text(encoding="utf-8").lower()

    def test_orchestrator_plan_gate_emits_artifact_before_release(self):
        expected = "verify the orchestrator command produces the documented workflow steps, records the plan/patch/test/report gate states, and emits the expected handoff artifact (e.g., a manifest or worklog update) before releasing control to a sub-agent."
        self.assertIn(expected, self.content)

    def test_sub_agent_requires_plan_artifact(self):
        expected = (
            "run the sub-agent command without the orchestrator artifact/gate record and verify it fails fast with a clear error referencing the missing gate, "
            "then rerun with the artifact present to ensure the gate is marked satisfied and execution continues."
        )
        self.assertIn(expected, self.content)

    def test_role_output_traceability_logs_artifacts(self):
        expected = "confirm each role writes its expected outputs (summary, gate log, or artifact) to the docs/logs targets defined in the feature spec so auditors can trace the workflow from plan through report."
        self.assertIn(expected, self.content)

    def test_gate_artifact_audit_blocks_skipped_handoffs(self):
        expected = "- tc-wf004: gate artifact audit ensures the orchestrator inspects each sub-agent artifact before approving the next gate."
        self.assertIn(expected, self.content)


if __name__ == "__main__":
    unittest.main()
