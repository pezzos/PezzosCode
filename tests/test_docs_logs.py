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

    def test_execution_protocol_defines_resume_modes_and_mandatory_reruns(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("`auto` (default): resume in-progress work", content)
        self.assertIn(
            "`prompt`: ask before continuing/recreating an existing feature worktree.",
            content,
        )
        self.assertIn(
            "`fresh`: recreate the feature patcher worktree and start from a clean baseline.",
            content,
        )
        self.assertIn("Tests and CI are always re-run on resume.", content)

    def test_execution_protocol_mentions_devtasks_schema_check(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Validate feature doc schema with `tools/pc-devtasks-schema-check` when creating/updating feature folders.",
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


class TestCompactedPatcherEvidence(unittest.TestCase):
    WI_ID = "WI-20260212-04"

    def _compacted_path(self) -> Path:
        return (
            ROOT
            / "docs"
            / "03-logs"
            / "compacted"
            / f"{self.WI_ID}-patcher-evidence.md"
        )

    def _missing_markers(self, content: str, required_markers) -> list:
        return [marker for marker in required_markers if marker not in content]

    def test_compacted_resume_fixtures_include_required_markers(self):
        path = self._compacted_path()
        content = path.read_text(encoding="utf-8")
        shared_markers = [
            "# WI-20260212-04 Patcher Evidence (Compacted)",
            "## Commands Executed",
            "`python3 -m unittest tests.test_pc_feature.TestPcFeature`",
            "`python3 -m unittest tests.test_docs_logs`",
            "## Ownership Note",
            "Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator",
        ]
        fixture_markers = [
            (
                "gate-pass",
                [
                    "### Fixture: gate-pass",
                    "Expected route: allow",
                    "Commit evidence gate accepts complete required sections.",
                ],
            ),
            (
                "gate-block-missing-empty",
                [
                    "### Fixture: gate-block-missing-empty",
                    "Expected route: block",
                    "Commit evidence gate rejects missing or empty required sections.",
                ],
            ),
        ]
        for marker in shared_markers:
            self.assertIn(marker, content)
        for fixture_name, markers in fixture_markers:
            with self.subTest(fixture=fixture_name):
                missing = self._missing_markers(content, markers)
                self.assertEqual(missing, [])

    def test_compacted_evidence_contract_boundaries(self):
        path = self._compacted_path()
        relative = path.relative_to(ROOT).as_posix()
        self.assertTrue(relative.startswith("docs/03-logs/compacted/"))
        self.assertFalse(relative.endswith("implementation-log.md"))
        self.assertFalse(relative.endswith("validation-log.md"))
        content = path.read_text(encoding="utf-8")
        self.assertIn("## Contract Boundaries", content)
        self.assertIn(
            "Compacted evidence is accepted only under `docs/03-logs/compacted/`.",
            content,
        )

    def test_compacted_evidence_rejects_missing_required_markers(self):
        required = [
            "### Fixture: gate-pass",
            "Expected route: allow",
            "### Fixture: gate-block-missing-empty",
            "Expected route: block",
        ]
        incomplete_fixture = "\n".join(
            [
                "# WI-20260212-04 Patcher Evidence (Compacted)",
                "### Fixture: gate-pass",
                "Expected route: allow",
            ]
        )
        missing = self._missing_markers(incomplete_fixture, required)
        self.assertIn("### Fixture: gate-block-missing-empty", missing)
        self.assertIn("Expected route: block", missing)


class TestCompactedPatcherEvidenceWI2026021203(unittest.TestCase):
    WI_ID = "WI-20260212-03"

    def _compacted_path(self) -> Path:
        return (
            ROOT
            / "docs"
            / "03-logs"
            / "compacted"
            / f"{self.WI_ID}-patcher-evidence.md"
        )

    def _missing_markers(self, content: str, required_markers) -> list:
        return [marker for marker in required_markers if marker not in content]

    def test_compacted_ticket_status_fixtures_include_required_markers(self):
        path = self._compacted_path()
        content = path.read_text(encoding="utf-8")
        shared_markers = [
            "# WI-20260212-03 Patcher Evidence (Compacted)",
            "## Commands Executed",
            "`python3 -m unittest tests.test_pc_feature.TestPcFeature`",
            "`python3 -m unittest tests.test_docs_logs`",
            "## Ownership Note",
            "Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator",
        ]
        fixture_markers = [
            (
                "completed-pass",
                [
                    "### Fixture: completed-pass",
                    "Expected route: allow",
                    "Outcome status accepted as completed.",
                ],
            ),
            (
                "missing-status",
                [
                    "### Fixture: missing-status",
                    "Expected route: block",
                    "Gate failed closed for missing/invalid status.",
                ],
            ),
        ]
        for marker in shared_markers:
            self.assertIn(marker, content)
        for fixture_name, markers in fixture_markers:
            with self.subTest(fixture=fixture_name):
                missing = self._missing_markers(content, markers)
                self.assertEqual(missing, [])

    def test_compacted_ticket_status_contract_boundaries(self):
        path = self._compacted_path()
        relative = path.relative_to(ROOT).as_posix()
        self.assertTrue(relative.startswith("docs/03-logs/compacted/"))
        self.assertFalse(relative.endswith("implementation-log.md"))
        self.assertFalse(relative.endswith("validation-log.md"))
        content = path.read_text(encoding="utf-8")
        self.assertIn("## Contract Boundaries", content)
        self.assertIn(
            "Only completed ticket statuses are accepted at commit gate.", content
        )


if __name__ == "__main__":
    unittest.main()
