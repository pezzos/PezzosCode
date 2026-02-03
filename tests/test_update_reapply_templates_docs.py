import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestUpdateReapplyTemplatesDocs(unittest.TestCase):
    def test_feature_spec_documents_workflow_behavior_steps_gates_outputs(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "03-update-reapply-templates"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrases = [
            "preflight validation gate",
            "template diff review gate",
            "conflict summary output",
        ]
        for phrase in expected_phrases:
            self.assertIn(phrase, content)

    def test_tech_design_outlines_cli_gates_and_outputs(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "03-update-reapply-templates"
            / "tech-design.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrases = [
            "cli preflight validation gate",
            "cli diff review gate",
            "cli conflict summary output",
        ]
        for phrase in expected_phrases:
            self.assertIn(phrase, content)

    def test_test_plan_defines_doc_update_case(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "03-update-reapply-templates"
            / "test-plan.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrase = (
            "tc-d001: docs/logs accurately describe the cli gating workflow"
        )
        self.assertIn(expected_phrase, content)

    def test_implementation_log_mentions_docs_logs_ticket_501(self):
        path = ROOT / "docs" / "03-logs" / "implementation-log.md"
        content = path.read_text(encoding="utf-8").lower()
        expected_phrases = [
            "ticket 501",
            "update/reapply templates workflow docs",
            "update/reapply templates",
        ]
        for phrase in expected_phrases:
            self.assertIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
