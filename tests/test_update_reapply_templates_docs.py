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


if __name__ == "__main__":
    unittest.main()
