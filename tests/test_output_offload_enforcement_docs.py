import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestOutputOffloadEnforcementDocs(unittest.TestCase):
    def test_feature_spec_describes_workflow_steps_and_gates(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "04-output-offload-enforcement"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrases = [
            "workflow steps",
            "approval gate",
            "noisy command handling",
            "offload id reference",
        ]
        for phrase in expected_phrases:
            self.assertIn(phrase, content)

    def test_tech_design_details_gating_outputs(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "04-output-offload-enforcement"
            / "tech-design.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrases = [
            "noisy command handling gate",
            "workflow gate",
            "gate output artifacts",
            "offload id artifacts",
        ]
        for phrase in expected_phrases:
            self.assertIn(phrase, content)

    def test_test_plan_describes_tc_d004_offload_id_gating(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "04-output-offload-enforcement"
            / "test-plan.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrase = "tc-d004: offload id gating behavior when missing or skipped"
        self.assertIn(expected_phrase, content)

    def test_test_plan_captures_tc_d002_offload_id_missing_gate(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "04-output-offload-enforcement"
            / "test-plan.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrase = (
            "tc-d002:** docs capture behavior when an offload id is missing or an "
            "offload is skipped, and the gate/approval decision that follows."
        )
        self.assertIn(expected_phrase, content)

    def test_test_plan_captures_tc_d003_artifact_list(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "04-output-offload-enforcement"
            / "test-plan.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrase = (
            "tc-d003:** the description of noisy-command handling clearly lists the "
            "output artifacts (offload identifiers, log references) required by "
            "later steps."
        )
        self.assertIn(expected_phrase, content)

    def test_execute_ticket_feature_spec_mentions_offload_ids(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "02-execute-ticket-workflow"
            / "feature-spec.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrase = "offload ids and prompt review"
        self.assertIn(expected_phrase, content)

    def test_execute_ticket_tech_design_outputs_include_offload_ids(self):
        path = (
            ROOT
            / "docs"
            / "02-features"
            / "02-execute-ticket-workflow"
            / "tech-design.md"
        )
        content = path.read_text(encoding="utf-8").lower()
        expected_phrase = "stdout/stderr with offload ids if noisy"
        self.assertIn(expected_phrase, content)


if __name__ == "__main__":
    unittest.main()
