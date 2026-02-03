import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestExecuteTicketDocumentation(unittest.TestCase):
    def test_ticket_execution_protocol_mentions_log_sync(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Record a gating summary in docs/03-logs/implementation-log.md and validation findings in docs/03-logs/validation-log.md for the Execute ticket workflow so the logs mirror the implemented sequence.",
            content,
        )

    def test_implementation_log_documents_execute_ticket_workflow_summary(self):
        path = ROOT / "docs" / "03-logs" / "implementation-log.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Documented the Execute ticket workflow gating summary",
            content,
        )

    def test_validation_log_records_execute_ticket_workflow_gating_steps(self):
        path = ROOT / "docs" / "03-logs" / "validation-log.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Recorded the validation findings for the Execute ticket workflow gating steps",
            content,
        )


if __name__ == "__main__":
    unittest.main()
