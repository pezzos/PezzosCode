import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestExecuteWorkItemDocumentation(unittest.TestCase):
    def test_execution_protocol_mentions_log_sync(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Record a gating summary in docs/03-logs/implementation-log.md and validation findings in docs/03-logs/validation-log.md for the Execute work item workflow so the logs mirror the implemented sequence.",
            content,
        )

    def test_implementation_log_documents_execute_work_item_workflow_summary(self):
        path = ROOT / "docs" / "03-logs" / "implementation-log.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Documented the Execute work item workflow gating summary",
            content,
        )

    def test_validation_log_records_execute_work_item_workflow_gating_steps(self):
        path = ROOT / "docs" / "03-logs" / "validation-log.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Recorded the validation findings for the Execute work item workflow gating steps",
            content,
        )

    def test_execution_protocol_mentions_enforced_offload(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Enforce the output offload workflow with tools/offload-proxy/pp at each gate and capture compliance decisions in docs/03-logs/decision-log.md.",
            content,
        )

    def test_execution_protocol_mentions_shared_worktree_review(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Planner/Tester/Reporter run in the patcher worktree so they review shared content; separate worktrees are not created for those roles.",
            content,
        )

    def test_human_orchestration_workflow_calls_out_offload_decision_logging(self):
        path = ROOT / "docs" / "04-process" / "human-orchestration-workflow.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "The PO loop now routes offload violations through docs/03-logs/decision-log.md so the enforced workflow is recorded before progressing.",
            content,
        )

    def test_decision_log_records_offload_enforcement_choice(self):
        path = ROOT / "docs" / "03-logs" / "decision-log.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Documented the decision to enforce output offload via tools/offload-proxy/pp and link it to work item execution workflow gates.",
            content,
        )


if __name__ == "__main__":
    unittest.main()
