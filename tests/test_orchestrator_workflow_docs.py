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

    def test_test_plan_lists_workflow_gate_tests(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "05-orchestrator-sub-agent-roles"
            / "test-plan.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn("- **TC-WF001:** Orchestrator Plan gate enforcement", content)
        self.assertIn("- **TC-WF002:** Sub-agent input gate validation", content)
        self.assertIn("- **TC-WF003:** Role output traceability", content)

    def test_execution_protocol_references_orchestrator_gate_logs(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "docs/03-logs/decision-log.md or docs/03-logs/validation-log.md",
            content,
        )

    def test_human_orchestration_workflow_records_gate_hand_offs(self):
        path = ROOT / "docs" / "04-process" / "human-orchestration-workflow.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "The orchestrator logs each gate handoff in docs/03-logs/decision-log.md and docs/03-logs/validation-log.md before the PO loop continues.",
            content,
        )

    def test_execution_protocol_defines_explicit_role_order_and_restarts(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Orchestrator → Planner → Plan Reviewer → Patcher → Tester → Reporter → Orchestrator",
            content,
        )
        self.assertIn(
            "Plan Reviewer `BLOCK` restarts from **Planner**",
            content,
        )
        self.assertIn("Tester `FAIL` restarts from **Planner**", content)
        self.assertIn("Reporter `FAIL` restarts from **Planner**", content)

    def test_execution_protocol_requires_noop_logging_and_artifact_reuse(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "append an explicit no-op note to the iteration log",
            content,
        )
        self.assertIn(
            "reuse existing work-item artifacts when safe",
            content,
        )

    def test_decision_log_records_orchestrator_gate_entry(self):
        path = ROOT / "docs" / "03-logs" / "decision-log.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "[DEC-006] - Orchestrator gating traceability",
            content,
        )


if __name__ == "__main__":
    unittest.main()
