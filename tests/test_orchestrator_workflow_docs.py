import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestOrchestratorWorkflowDocs(unittest.TestCase):
    def test_feature_spec_describes_role_responsibilities(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Role responsibilities for the orchestrator and sub-agents are detailed below.",
            content,
        )

    def test_feature_spec_highlights_orchestrator_plan_gate(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Orchestrator Plan gate ensures preflight readiness, documents the patch plan, and hands off the task to the implementer.",
            content,
        )

    def test_tech_design_lists_gates_and_outputs_per_role(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "tech-design.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Gates and outputs per role: Plan gate (Orchestrator) outputs the plan summary, Patch gate (Implementer) outputs artifacts/logs, Test gate (Tester) outputs pass/fail proofs, Report gate (Reviewer) outputs recommendations.",
            content,
        )

    def test_feature_spec_sequences_plan_patch_test_report_handoff(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "The orchestrator sequences the workflow through the Plan, Patch, Test, and Report gates, requiring each gate's artifact to be archived before releasing control to the next role.",
            content,
        )

    def test_feature_spec_records_sub_agent_outputs_for_review(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Sub-agent outputs include the implementer patch artifact, the tester pass/fail summary, and the reviewer recommendations, all documented for the orchestrator to verify.",
            content,
        )

    def test_test_plan_requires_gate_artifact_audit(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "test-plan.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "TC-WF004: Gate artifact audit ensures the orchestrator inspects each sub-agent artifact before approving the next gate.",
            content,
        )


if __name__ == "__main__":
    unittest.main()
