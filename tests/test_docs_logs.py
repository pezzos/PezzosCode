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

    def test_serena_gitignore_template_matches_live_memory_policy(self):
        live = (ROOT / ".serena" / ".gitignore").read_text(encoding="utf-8")
        template = (
            ROOT / "tools" / "templates" / "root" / ".serena" / ".gitignore"
        ).read_text(encoding="utf-8")
        self.assertIn("/memories", live)
        self.assertIn("/memories", template)

    def test_execution_protocol_excludes_runtime_shell_snapshots_from_scope(self):
        path = ROOT / "docs" / "04-process" / "ticket-execution-protocol.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "Runtime shell snapshots under `.codex_subagent/shell_snapshots/` are excluded from feature scope and must not be staged/committed as work-item output.",
            content,
        )
        self.assertIn(
            "Runtime artifact paths under `.codex_subagent/shell_snapshots/`, `.codex_subagent/sessions/`, and `.codex_subagent/tmp/` are blocked from branch scope unless explicitly allowlisted.",
            content,
        )
        self.assertIn(
            "Allowlisted `.codex_subagent` paths are limited to deterministic tool metadata (currently `.codex_subagent/config.toml`).",
            content,
        )
        self.assertIn(
            "Scope enforcement provides recommendation-only remediation output and must not auto-mutate tracked files.",
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

    def test_human_orchestration_workflow_mentions_prepare_and_review_features(self):
        path = ROOT / "docs" / "04-process" / "human-orchestration-workflow.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("make context-check", content)
        self.assertIn("docs/03-logs/context-clarity-report.json", content)
        self.assertIn("make write-prd", content)
        self.assertIn("make prepare-features", content)
        self.assertIn("make review-features", content)
        self.assertIn("make release-readiness", content)
        self.assertIn("docs/01-product/design.md", content)
        self.assertIn("docs/01-product/ux-ui.md", content)
        self.assertIn("docs/01-product/security.md", content)
        self.assertIn("docs/03-logs/write-prd-report.json", content)
        self.assertIn("docs/03-logs/write-prd-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-pm-todo.md", content)
        self.assertIn("docs/03-logs/review-features-report.json", content)
        self.assertIn("docs/03-logs/release-readiness-report.json", content)

    def test_human_orchestration_workflow_mentions_semantic_pm_gate(self):
        path = ROOT / "docs" / "04-process" / "human-orchestration-workflow.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("semantic quality criteria", content)
        self.assertIn("feature-specific architecture", content)
        self.assertIn("project-specific user journeys", content)

    def test_tools_readme_mentions_process_feature_opt_in(self):
        path = ROOT / "tools" / "README.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("--include-process-features", content)

    def test_tools_readme_mentions_prepare_pm_todo_artifact(self):
        path = ROOT / "tools" / "README.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("docs/03-logs/prepare-features-pm-todo.md", content)
        self.assertIn("docs/01-product/security.md", content)
        self.assertIn("--snapshot-runs", content)

    def test_docs_readme_mentions_prepare_and_review_artifacts(self):
        path = ROOT / "docs" / "README.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("make context-check", content)
        self.assertIn("docs/03-logs/context-clarity-report.json", content)
        self.assertIn("security.md", content)
        self.assertIn("docs/03-logs/write-prd-report.json", content)
        self.assertIn("docs/03-logs/write-prd-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-pm-todo.md", content)
        self.assertIn("SNAPSHOT_RUNS=1", content)
        self.assertIn("docs/03-logs/review-features-report.json", content)
        self.assertIn("docs/03-logs/release-readiness-report.json", content)

    def test_template_docs_workflow_mentions_prepare_and_review_artifacts(self):
        path = (
            ROOT
            / "tools"
            / "templates"
            / "docs"
            / "04-process"
            / "human-orchestration-workflow.md"
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn("make context-check", content)
        self.assertIn("docs/03-logs/context-clarity-report.json", content)
        self.assertIn("docs/03-logs/write-prd-report.json", content)
        self.assertIn("docs/03-logs/write-prd-state.json", content)
        self.assertIn("docs/01-product/security.md", content)
        self.assertIn("docs/03-logs/prepare-features-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-pm-todo.md", content)
        self.assertIn("docs/03-logs/review-features-report.json", content)
        self.assertIn("docs/03-logs/release-readiness-report.json", content)

    def test_template_docs_readme_mentions_prepare_pm_todo_artifact(self):
        path = ROOT / "tools" / "templates" / "docs" / "README.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn("make context-check", content)
        self.assertIn("docs/03-logs/context-clarity-report.json", content)
        self.assertIn("security.md", content)
        self.assertIn("docs/03-logs/write-prd-report.json", content)
        self.assertIn("docs/03-logs/write-prd-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-state.json", content)
        self.assertIn("docs/03-logs/prepare-features-pm-todo.md", content)
        self.assertIn("SNAPSHOT_RUNS=1", content)
        self.assertIn("docs/03-logs/release-readiness-report.json", content)

    def test_root_agents_mentions_conditional_unittest_discovery(self):
        path = ROOT / "AGENTS.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "run Python unittest discovery only when a local `tests/` directory exists",
            content,
        )

    def test_template_root_agents_mentions_conditional_unittest_discovery(self):
        path = ROOT / "tools" / "templates" / "root" / "AGENTS.md"
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            "run Python unittest discovery only when a local `tests/` directory exists",
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


class TestCompactedPatcherEvidenceWI2026021305(unittest.TestCase):
    WI_ID = "WI-20260213-05"

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

    def test_compacted_completed_only_gate_fixtures_include_required_markers(self):
        path = self._compacted_path()
        content = path.read_text(encoding="utf-8")
        shared_markers = [
            "# WI-20260213-05 Patcher Evidence (Compacted)",
            "## Commands Executed",
            "`python3 -m unittest tests.test_pc_feature.TestPcFeature`",
            "`python3 -m unittest tests.test_docs_logs`",
            "## Ownership Note",
            "Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator",
        ]
        fixture_markers = [
            (
                "completed-allow",
                [
                    "### Fixture: completed-allow",
                    "Expected route: allow",
                    "Commit evidence gate accepts completed ticket docs with required evidence.",
                ],
            ),
            (
                "non-completed-block",
                [
                    "### Fixture: non-completed-block",
                    "Expected route: block",
                    "Gate failed closed for non-completed ticket status.",
                ],
            ),
            (
                "malformed-evidence-block",
                [
                    "### Fixture: malformed-evidence-block",
                    "Expected route: block",
                    "Commit evidence gate rejects malformed or missing required evidence.",
                ],
            ),
            (
                "snapshot-clean-allow",
                [
                    "### Fixture: snapshot-clean-allow",
                    "Expected route: allow",
                    "Scope check passes when no tracked shell snapshot artifacts exist in `refs/heads/main..HEAD`.",
                ],
            ),
            (
                "snapshot-contaminated-block",
                [
                    "### Fixture: snapshot-contaminated-block",
                    "Expected route: block",
                    "Scope check fails closed when tracked shell snapshot artifacts are present in branch diff.",
                ],
            ),
        ]
        for marker in shared_markers:
            self.assertIn(marker, content)
        for fixture_name, markers in fixture_markers:
            with self.subTest(fixture=fixture_name):
                missing = self._missing_markers(content, markers)
                self.assertEqual(missing, [])

    def test_compacted_completed_only_gate_contract_boundaries(self):
        path = self._compacted_path()
        relative = path.relative_to(ROOT).as_posix()
        self.assertTrue(relative.startswith("docs/03-logs/compacted/"))
        self.assertFalse(relative.endswith("implementation-log.md"))
        self.assertFalse(relative.endswith("validation-log.md"))
        content = path.read_text(encoding="utf-8")
        self.assertIn("## Contract Boundaries", content)
        self.assertIn(
            "Commit is blocked unless normalized top-level `Outcome` is exactly `completed`.",
            content,
        )
        self.assertIn(
            "Required fixture markers are deterministic and validated by `tests/test_docs_logs.py`.",
            content,
        )
        self.assertIn(
            "Runtime shell snapshots under `.codex_subagent/shell_snapshots/` are excluded from feature scope and must be removed before reporter/commit revalidation.",
            content,
        )


if __name__ == "__main__":
    unittest.main()
