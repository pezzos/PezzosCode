import contextlib
import importlib.machinery
import importlib.util
import io
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from lib.pc_runner import (
    build_metadata,
    build_proposal_from_outcome,
    merge_or_append_proposal,
    record_outcome_proposal,
    render_proposal_entry,
)

ROOT = Path(__file__).resolve().parents[1]
PC_FEATURE_PATH = ROOT / "tools" / "pc-feature"
PC_FEATURE_STATUS_PATH = ROOT / "tools" / "pc-feature-status"


def load_pc_feature():
    loader = importlib.machinery.SourceFileLoader("pc_feature", str(PC_FEATURE_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def load_pc_feature_status():
    loader = importlib.machinery.SourceFileLoader(
        "pc_feature_status", str(PC_FEATURE_STATUS_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcFeature(unittest.TestCase):
    def setUp(self):
        self.pc_feature = load_pc_feature()
        self.pc_feature_status = load_pc_feature_status()

    def _build_entry_content(
        self,
        work_item_id: str,
        *,
        outcome: str = "needs replan",
        commit_message: str = "",
    ) -> str:
        content = "## Execution Log\n\n" + self.pc_feature.build_execution_entry(
            work_item_id
        )
        content = self.pc_feature.update_entry_field(
            content, work_item_id, "Outcome", outcome
        )
        if commit_message:
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Commit",
                f"- Commit message: {commit_message}",
            )
        return content

    def _write_feature_workspace(self, root: Path, dev_tasks_content: str) -> Path:
        def seed_workspace(base: Path) -> Path:
            feature_dir = base / "docs" / "02-features" / "01-workflow-hardening"
            feature_dir.mkdir(parents=True, exist_ok=True)
            (feature_dir / "dev-tasks.md").write_text(
                dev_tasks_content, encoding="utf-8"
            )
            (feature_dir / "feature-spec.md").write_text(
                "# feature spec\n", encoding="utf-8"
            )
            (feature_dir / "tech-design.md").write_text(
                "# tech design\n", encoding="utf-8"
            )
            (feature_dir / "test-plan.md").write_text("# test plan\n", encoding="utf-8")
            logs_dir = base / "docs" / "03-logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            (logs_dir / "implementation-log.md").write_text(
                "# impl\n", encoding="utf-8"
            )
            (logs_dir / "validation-log.md").write_text(
                "# validation\n", encoding="utf-8"
            )
            (logs_dir / "decision-log.md").write_text("# decision\n", encoding="utf-8")
            return feature_dir

        feature_dir = seed_workspace(root)
        patcher_workspace = root / "patcher"
        if patcher_workspace.exists():
            seed_workspace(patcher_workspace)
        return feature_dir

    def _worktree_dev_tasks(self, patcher_path: Path) -> Path:
        return (
            patcher_path
            / "docs"
            / "02-features"
            / "01-workflow-hardening"
            / "dev-tasks.md"
        )

    def _build_commit_gate_ready_content(self, work_item_id: str) -> str:
        content = self._build_entry_content(work_item_id)
        tests_run_cmd = "`python3 -m unittest tests.test_pc_feature.TestPcFeature`"
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Test Results",
            (
                "- Runtime reconciliation: derived from tester feedback.\n"
                "- Outcome: PASS\n"
                f"- Tests run: {tests_run_cmd}\n"
                "- Notes: baseline pass"
            ),
        )
        content = self.pc_feature.update_entry_field(
            content, work_item_id, "Tests run", tests_run_cmd
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Commit",
            "- Commit message: chore(workflow): finalize documentation gate",
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Final Report",
            (
                "What changed (files): docs and tooling updated\n"
                "Tests written (names) + results: TestPcFeature commit gate fixtures pass\n"
                "Docs/logs updated checklist: docs/04-process updated\n"
                "make ci results: PASS\n"
                "Commands run (use pp for noisy output): python3 -m unittest tests.test_pc_feature.TestPcFeature\n"
                "Commit message: chore(workflow): finalize documentation gate"
            ),
        )
        return content

    def _patch_main_base(self, root: Path, feature_dir: Path, patcher_path: Path):
        return [
            mock.patch.object(
                self.pc_feature, "parse_args", return_value=("01", False)
            ),
            mock.patch.object(self.pc_feature.os, "getcwd", return_value=str(root)),
            mock.patch.object(
                self.pc_feature,
                "git_current_branch",
                side_effect=lambda path: (
                    "main" if Path(path) == root else "patcher-branch"
                ),
            ),
            mock.patch.object(
                self.pc_feature, "resolve_feature_dir", return_value=str(feature_dir)
            ),
            mock.patch.object(
                self.pc_feature, "build_worktree_path", return_value=str(patcher_path)
            ),
            mock.patch.object(
                self.pc_feature, "build_worktree_branch", return_value="patcher-branch"
            ),
            mock.patch.object(
                self.pc_feature, "parse_resume_mode", return_value="auto"
            ),
            mock.patch.object(
                self.pc_feature, "enforce_single_active_feature", return_value=None
            ),
            mock.patch.object(self.pc_feature, "worktree_is_dirty", return_value=False),
            mock.patch.object(self.pc_feature, "get_status_paths", return_value=[]),
            mock.patch.object(self.pc_feature, "branch_ahead_count", return_value=0),
            mock.patch.object(self.pc_feature, "branch_behind_count", return_value=0),
            mock.patch.object(
                self.pc_feature,
                "git_ref_sha",
                return_value="a" * 40,
            ),
            mock.patch.object(
                self.pc_feature,
                "prepare_worktree",
                return_value=(str(patcher_path), "patcher-branch"),
            ),
            mock.patch.object(
                self.pc_feature, "cleanup_dirty_role_logs", return_value=None
            ),
            mock.patch.object(
                self.pc_feature, "cleanup_dirty_global_logs", return_value=None
            ),
            mock.patch.object(
                self.pc_feature, "ensure_clean_worktree", return_value=None
            ),
            mock.patch.object(self.pc_feature, "ensure_role_log", return_value=None),
            mock.patch.object(self.pc_feature, "append_role_log", return_value=None),
            mock.patch.object(
                self.pc_feature, "format_role_changes", return_value=None
            ),
            mock.patch.object(self.pc_feature, "enforce_role_scope", return_value=None),
            mock.patch.object(
                self.pc_feature, "commit_worktree_changes", return_value=None
            ),
            mock.patch.object(
                self.pc_feature, "reset_dev_tasks_if_dirty", return_value=False
            ),
            mock.patch.object(
                self.pc_feature, "reset_global_logs_to_head", return_value=None
            ),
            mock.patch.object(
                self.pc_feature, "reset_role_logs_to_head", return_value=None
            ),
            mock.patch.object(self.pc_feature, "remove_worktree", return_value=None),
            mock.patch.object(
                self.pc_feature, "collect_allowed_final_stage_paths", return_value=[]
            ),
            mock.patch.object(
                self.pc_feature, "collect_branch_merge_paths", return_value=[]
            ),
            mock.patch.object(
                self.pc_feature,
                "classify_resume_dirty_paths",
                return_value=([], []),
            ),
            mock.patch.object(
                self.pc_feature, "checkpoint_resume_dev_tasks", return_value=False
            ),
            mock.patch.object(
                self.pc_feature, "ensure_root_start_scope", return_value=None
            ),
            mock.patch.object(
                self.pc_feature,
                "ensure_compacted_policy_bootstrap_ready",
                return_value=None,
            ),
            mock.patch.object(
                self.pc_feature, "check_allowed_tests_exist", return_value=[]
            ),
            mock.patch.object(
                self.pc_feature, "process_docs_changed", return_value=False
            ),
            mock.patch.object(
                self.pc_feature, "anti_hardcode_coverage_issues", return_value=[]
            ),
            mock.patch.object(
                self.pc_feature, "collect_dirty_snapshot", return_value={}
            ),
            mock.patch.object(
                self.pc_feature,
                "ensure_plan_reviewer_read_only",
                return_value=([], []),
            ),
            mock.patch.object(self.pc_feature, "apply_branch_diff", return_value=True),
            mock.patch.object(
                self.pc_feature.pc_runner, "build_metadata", return_value=object()
            ),
            mock.patch.object(
                self.pc_feature.pc_runner, "log_message", return_value=None
            ),
            mock.patch.object(self.pc_feature, "append_log_line", return_value=None),
        ]

    def test_build_preflight_block_accepts_missing_review_summary(self):
        block = self.pc_feature.build_preflight_block(
            {},
            "WI-20260204-01",
            "LOW",
            [],
        )
        self.assertIn("Systematic review:", block)

    def test_build_preflight_block_includes_review_summary(self):
        summary = "make feature F=01: ok"
        block = self.pc_feature.build_preflight_block(
            {},
            "WI-20260204-01",
            "LOW",
            [],
            summary,
        )
        self.assertIn(f"Systematic review: {summary}", block)

    def test_classify_risk_flags_restore_touch(self):
        data = {"touches_restore": True, "files_to_change": []}
        risk, triggers = self.pc_feature.classify_risk(data)
        self.assertEqual(risk, "HIGH")
        self.assertIn("affects restore apply semantics or permissions", triggers)

    def test_classify_risk_flags_protocol_path_triggers_from_planned_files(self):
        path_cases = [
            ("sanitizer/rules.py", "touches sanitizer/ path"),
            ("detectors/scan.py", "touches detectors/ path"),
            ("restore/apply.py", "touches restore/ path"),
            ("git_ops/rebase.py", "touches git_ops/ path"),
            ("metadata/index.py", "touches metadata/ path"),
        ]
        for file_path, expected_trigger in path_cases:
            with self.subTest(file_path=file_path):
                data = {"files_to_change": [file_path]}
                risk, triggers = self.pc_feature.classify_risk(data)
                self.assertEqual(risk, "HIGH")
                self.assertIn(expected_trigger, triggers)

    def test_classify_risk_flags_protocol_path_triggers_from_actual_changed_paths(self):
        data = {"files_to_change": ["docs/notes.md"]}
        risk, triggers = self.pc_feature.classify_risk(
            data,
            actual_changed_paths=["metadata/schema.json", "src/app.py"],
        )
        self.assertEqual(risk, "HIGH")
        self.assertIn("touches metadata/ path", triggers)

    def test_classify_risk_deduplicates_mixed_path_triggers(self):
        data = {"files_to_change": ["restore/plan.md", "restore/apply.py"]}
        risk, triggers = self.pc_feature.classify_risk(
            data,
            actual_changed_paths=["restore/cleanup.py", "detectors/rules.py"],
        )
        self.assertEqual(risk, "HIGH")
        self.assertEqual(triggers.count("touches restore/ path"), 1)
        self.assertIn("touches detectors/ path", triggers)

    def test_escalation_command_allowed_unwraps_pp_and_denies_broad_commands(self):
        self.assertTrue(
            self.pc_feature.escalation_command_allowed(
                ["tools/offload-proxy/pp", "python3", "-m", "unittest", "-h"]
            )
        )
        self.assertFalse(
            self.pc_feature.escalation_command_allowed(
                ["tools/offload-proxy/pp", "bash", "-lc", "echo hi"]
            )
        )

    def test_collect_branch_merge_paths_includes_feature_runtime_docs(self):
        with mock.patch.object(
            self.pc_feature,
            "branch_diff_paths",
            return_value=[
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/planner-log.md",
                "docs/03-logs/decision-log.md",
                "logs/WI-20260206-01/tests.log",
                "tools/pc-feature",
            ],
        ):
            paths = self.pc_feature.collect_branch_merge_paths(
                str(ROOT),
                "HEAD",
                "feature-branch",
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening",
            )
        self.assertEqual(
            paths,
            [
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/planner-log.md",
                "tools/pc-feature",
            ],
        )

    def test_collect_patcher_autofix_paths_skips_role_scoped_docs(self):
        with mock.patch.object(
            self.pc_feature,
            "collect_branch_merge_paths",
            return_value=[
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/planner-log.md",
                "tools/pc-feature",
            ],
        ):
            allowed, skipped = self.pc_feature.collect_patcher_autofix_paths(
                str(ROOT),
                "HEAD",
                "feature-branch",
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening",
            )
        self.assertEqual(allowed, ["tools/pc-feature"])
        self.assertEqual(
            skipped,
            [
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/planner-log.md",
            ],
        )

    def test_collect_patcher_autofix_paths_returns_empty_when_all_forbidden(self):
        with mock.patch.object(
            self.pc_feature,
            "collect_branch_merge_paths",
            return_value=[
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/reporter-log.md",
            ],
        ):
            allowed, skipped = self.pc_feature.collect_patcher_autofix_paths(
                str(ROOT),
                "HEAD",
                "feature-branch",
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening",
            )
        self.assertEqual(allowed, [])
        self.assertEqual(
            skipped,
            [
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/reporter-log.md",
            ],
        )

    def test_collect_branch_into_main_auto_skips_conflicting_paths(self):
        include_paths = ["src/a.py", "src/b.py", "src/c.py"]
        calls = []

        def fake_apply(
            root,
            base_ref,
            branch,
            include_paths=None,
            diagnostics=None,
            precheck=False,
        ):
            normalized = list(include_paths or [])
            calls.append((normalized, precheck))
            if normalized == ["src/a.py", "src/b.py", "src/c.py"]:
                if diagnostics is not None:
                    diagnostics.clear()
                    diagnostics["precheck_conflicts"] = ["src/b.py"]
                    diagnostics["conflicts"] = ["src/b.py"]
                    diagnostics["attempts"] = []
                return False
            if normalized == ["src/a.py", "src/c.py"]:
                if diagnostics is not None:
                    diagnostics.clear()
                    diagnostics["precheck_conflicts"] = []
                    diagnostics["conflicts"] = []
                    diagnostics["attempts"] = []
                return True
            raise AssertionError(f"unexpected include_paths call: {normalized}")

        with mock.patch.object(
            self.pc_feature,
            "apply_branch_diff",
            side_effect=fake_apply,
        ):
            summary = self.pc_feature.collect_branch_into_main(
                str(ROOT),
                "HEAD",
                "patcher-branch",
                include_paths,
            )

        self.assertEqual(summary["applied_paths"], ["src/a.py", "src/c.py"])
        self.assertEqual(summary["skipped_paths"], ["src/b.py"])
        self.assertEqual(summary["conflict_paths"], ["src/b.py"])
        self.assertEqual(
            calls,
            [
                (["src/a.py", "src/b.py", "src/c.py"], True),
                (["src/a.py", "src/c.py"], False),
            ],
        )

    def test_collect_branch_into_main_falls_back_to_per_path_apply(self):
        include_paths = ["src/a.py", "src/b.py", "src/c.py"]

        def fake_apply(
            root,
            base_ref,
            branch,
            include_paths=None,
            diagnostics=None,
            precheck=False,
        ):
            normalized = list(include_paths or [])
            if normalized == ["src/a.py", "src/b.py", "src/c.py"]:
                if diagnostics is not None:
                    diagnostics.clear()
                    diagnostics["precheck_conflicts"] = ["src/b.py"]
                    diagnostics["conflicts"] = ["src/b.py"]
                    diagnostics["attempts"] = []
                return False
            if normalized == ["src/a.py", "src/c.py"]:
                if diagnostics is not None:
                    diagnostics.clear()
                    diagnostics["precheck_conflicts"] = []
                    diagnostics["conflicts"] = []
                    diagnostics["attempts"] = []
                return False
            if normalized == ["src/a.py"]:
                if diagnostics is not None:
                    diagnostics.clear()
                    diagnostics["precheck_conflicts"] = []
                    diagnostics["conflicts"] = []
                    diagnostics["attempts"] = []
                return True
            if normalized == ["src/c.py"]:
                if diagnostics is not None:
                    diagnostics.clear()
                    diagnostics["precheck_conflicts"] = []
                    diagnostics["conflicts"] = []
                    diagnostics["attempts"] = []
                return False
            raise AssertionError(f"unexpected include_paths call: {normalized}")

        with mock.patch.object(
            self.pc_feature,
            "apply_branch_diff",
            side_effect=fake_apply,
        ):
            summary = self.pc_feature.collect_branch_into_main(
                str(ROOT),
                "HEAD",
                "patcher-branch",
                include_paths,
            )

        self.assertEqual(summary["applied_paths"], ["src/a.py"])
        self.assertEqual(summary["skipped_paths"], ["src/b.py", "src/c.py"])
        self.assertEqual(summary["conflict_paths"], ["src/b.py", "src/c.py"])

    def test_normalize_allowed_test_restricts_to_unittest_or_pytest(self):
        self.assertEqual(
            self.pc_feature.normalize_allowed_test(
                "python -m unittest discover -s tests"
            ),
            "python -m unittest discover -s tests",
        )
        self.assertEqual(
            self.pc_feature.normalize_allowed_test("pytest tests -q"),
            "pytest tests -q",
        )
        self.assertIsNone(self.pc_feature.normalize_allowed_test("bash -lc 'echo hi'"))
        self.assertIsNone(
            self.pc_feature.normalize_allowed_test("node scripts/test.js")
        )

    def test_sanitize_allowed_tests_response_keeps_only_commands(self):
        response = (
            "**Allowed Tests**\n"
            "- `python -m unittest tests.test_pc_feature`\n"
            "**Patch**\n"
            "- Updated docs/03-logs/implementation-log.md\n"
            "- `pytest tests/test_pc_feature.py -q`\n"
            "Note: keep only test commands.\n"
        )
        sanitized = self.pc_feature.sanitize_allowed_tests_response(response)
        self.assertEqual(
            sanitized,
            "- `python -m unittest tests.test_pc_feature`\n"
            "- `pytest tests/test_pc_feature.py -q`",
        )

    def test_reconcile_runtime_execution_record_populates_sections_and_fields(self):
        work_item_id = "WI-20260212-10"
        content = self._build_entry_content(work_item_id)
        tester_feedback = (
            "Outcome: PASS\n"
            "Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`\n"
            "Notes: all checks passed\n"
            f"Work Item ID: {work_item_id}\n"
        )
        reporter_feedback = (
            "Outcome: PASS\n"
            "Docs/logs updated: docs/03-logs/implementation-log.md\n"
            "Notes: review approved\n"
            f"Work Item ID: {work_item_id}\n"
        )
        updated, repaired = self.pc_feature.reconcile_runtime_execution_record(
            content,
            work_item_id,
            patch_completed=True,
            tester_feedback=tester_feedback,
            reporter_feedback=reporter_feedback,
            reporter_outcome="PASS",
        )
        self.assertIn("Patch", repaired)
        self.assertIn("Test Results", repaired)
        self.assertIn("Reporter Review", repaired)
        self.assertNotIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Patch"),
        )
        self.assertNotIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Test Results"),
        )
        self.assertNotIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Reporter Review"),
        )
        self.assertEqual(
            self.pc_feature.get_entry_field(updated, work_item_id, "Patcher"), "Codex"
        )
        self.assertEqual(
            self.pc_feature.get_entry_field(updated, work_item_id, "Tester"), "Codex"
        )
        self.assertEqual(
            self.pc_feature.get_entry_field(updated, work_item_id, "Reporter"), "Codex"
        )
        self.assertIn(
            "python -m pytest",
            self.pc_feature.get_entry_field(updated, work_item_id, "Tests run"),
        )
        self.assertIn(
            "implementation-log",
            self.pc_feature.get_entry_field(updated, work_item_id, "Docs/logs updated"),
        )

    def test_execution_handoff_completeness_issues_detects_pending_placeholders(self):
        work_item_id = "WI-20260212-11"
        content = self._build_entry_content(work_item_id)
        issues = self.pc_feature.execution_handoff_completeness_issues(
            content, work_item_id, require_reporter_review=True
        )
        self.assertTrue(
            any(
                "Patch section still contains pending placeholders" in issue
                for issue in issues
            )
        )
        self.assertTrue(
            any("top execution field is blank: Reporter" in issue for issue in issues)
        )

    def test_required_compacted_output_paths_detects_explicit_and_wildcard_contract(
        self,
    ):
        work_item_id = "WI-20260212-12"
        content = self._build_entry_content(work_item_id)
        explicit_path = self.pc_feature.compacted_log_output_paths()["decision"]
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Files to Change", f"- Files: {explicit_path}"
        )
        required = self.pc_feature.required_compacted_output_paths(
            content, work_item_id
        )
        self.assertIn(explicit_path, required)

        legacy_path = "docs/03-logs/compacted/decision-log-compact.md"
        content_legacy = self._build_entry_content(work_item_id)
        content_legacy = self.pc_feature.replace_entry_section(
            content_legacy, work_item_id, "Files to Change", f"- Files: {legacy_path}"
        )
        required_legacy = self.pc_feature.required_compacted_output_paths(
            content_legacy, work_item_id
        )
        self.assertIn(legacy_path, required_legacy)

        content_wildcard = self._build_entry_content(work_item_id)
        content_wildcard = self.pc_feature.replace_entry_section(
            content_wildcard,
            work_item_id,
            "Files to Change",
            "- Files: docs/03-logs/compacted/*",
        )
        required_wildcard = self.pc_feature.required_compacted_output_paths(
            content_wildcard, work_item_id
        )
        self.assertEqual(
            sorted(required_wildcard),
            sorted(self.pc_feature.compacted_log_output_paths().values()),
        )

    def test_replace_entry_section_accepts_legacy_files_section_alias(self):
        work_item_id = "WI-20260204-02"
        content = "## Execution Log\n\n" + self.pc_feature.build_execution_entry(
            work_item_id
        )
        content = content.replace(
            "#### Files to Change", "#### Files to Change + Change Budget"
        )
        updated = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Files to Change",
            "- Files: tools/pc-feature",
        )
        self.assertIn("#### Files to Change + Change Budget", updated)
        section = self.pc_feature.get_entry_section(
            updated, work_item_id, "Files to Change"
        )
        self.assertEqual(section, "- Files: tools/pc-feature")

    def test_restore_dirty_paths_resets_tracked_and_removes_untracked(self):
        run_calls = []
        removed_files = []
        removed_dirs = []

        def fake_run(cmd, **kwargs):
            run_calls.append(list(cmd))
            if cmd[:3] == ["git", "ls-files", "--error-unmatch"]:
                if cmd[3] == "tracked.txt":
                    return SimpleNamespace(returncode=0, stdout="", stderr="")
                return SimpleNamespace(returncode=1, stdout="", stderr="")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        def fake_exists(path):
            return not str(path).endswith("missing")

        def fake_isdir(path):
            return str(path).endswith("new-dir")

        with mock.patch.object(self.pc_feature.subprocess, "run", side_effect=fake_run):
            with mock.patch.object(
                self.pc_feature.os.path, "exists", side_effect=fake_exists
            ):
                with mock.patch.object(
                    self.pc_feature.os.path, "isdir", side_effect=fake_isdir
                ):
                    with mock.patch.object(
                        self.pc_feature.os, "remove", side_effect=removed_files.append
                    ):
                        with mock.patch.object(
                            self.pc_feature.shutil,
                            "rmtree",
                            side_effect=lambda p, ignore_errors: removed_dirs.append(
                                (p, ignore_errors)
                            ),
                        ):
                            self.pc_feature.restore_dirty_paths(
                                "/tmp/worktree",
                                ["tracked.txt", "new-file", "new-dir"],
                            )

        self.assertIn(
            ["git", "checkout", "--", "tracked.txt"],
            run_calls,
        )
        self.assertIn("/tmp/worktree/new-file", removed_files)
        self.assertIn(("/tmp/worktree/new-dir", True), removed_dirs)

    def test_plan_policy_violations_detects_forbidden_paths_and_commands(self):
        compacted_path = self.pc_feature.compacted_log_output_paths()["decision"]
        plan = (
            "- Edit docs/02-features/12-incremental-prd-to-features/dev-tasks.md\n"
            "- Update docs/03-logs/implementation-log.md\n"
            f"- Write {compacted_path}\n"
            "- Run make feature F=12\n"
        )
        violations = self.pc_feature.plan_policy_violations(plan)
        self.assertTrue(any("dev-tasks.md" in item for item in violations))
        self.assertTrue(any("docs/03-logs" in item for item in violations))
        self.assertFalse(any(compacted_path in item for item in violations))
        self.assertTrue(any("make feature" in item for item in violations))

    def test_plan_policy_violations_scans_full_plan_beyond_files_section(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior.\n"
            "Files to change:\n"
            "- tools/prd-to-features\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "Notes:\n"
            "- Also update docs/02-features/12-incremental-prd-to-features/dev-tasks.md\n"
        )
        violations = self.pc_feature.plan_policy_violations(plan)
        self.assertTrue(any("dev-tasks.md" in item for item in violations))

    def test_plan_policy_violations_does_not_treat_files_path_as_command(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior and note that docs/03-logs updates are handled by reporter/orchestrator; patcher will not edit those files.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertFalse(
            any(
                "forbidden command in plan: tools/pc-feature" in item
                for item in violations
            )
        )
        self.assertFalse(
            any("forbidden command in plan: pc-feature" in item for item in violations)
        )

    def test_plan_policy_violations_detects_tools_pc_feature_command_context(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Run tools/pc-feature F=12 and note docs/03-logs updates are owned by reporter/orchestrator; patcher will not edit those files.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertTrue(
            any(
                "forbidden command in plan: tools/pc-feature" in item
                for item in violations
            )
        )
        self.assertTrue(
            any("forbidden command in plan: pc-feature" in item for item in violations)
        )

    def test_plan_policy_violations_requires_global_log_handoff(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "- docs/04-process/ticket-execution-protocol.md\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
        )
        violations = self.pc_feature.plan_policy_violations(plan)
        self.assertTrue(
            any(
                "assign docs/03-logs updates to reporter/orchestrator" in item
                for item in violations
            )
        )

    def test_plan_policy_violations_skips_handoff_for_compacted_outputs_only(self):
        compacted_path = self.pc_feature.compacted_log_output_paths()["decision"]
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Generate compacted outputs from canonical logs.\n"
            "Files to change:\n"
            f"- {compacted_path}\n"
            "- tools/log-compaction\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertFalse(
            any(
                "assign docs/03-logs updates to reporter/orchestrator" in item
                for item in violations
            )
        )
        self.assertFalse(any(compacted_path in item for item in violations))

    def test_plan_policy_violations_allows_docs_logs_wildcard_handoff_note(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior and note required docs/03-logs/* updates are handled by reporter/orchestrator; patcher will not edit those files.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertFalse(
            any("forbidden path in plan: docs/03-logs/*" in item for item in violations)
        )
        self.assertFalse(
            any(
                "forbidden path in plan: docs/03-logs/\\*" in item
                for item in violations
            )
        )

    def test_plan_policy_violations_blocks_docs_logs_wildcard_in_files_section(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "- docs/03-logs/*\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertTrue(
            any("forbidden path in plan: docs/03-logs/*" in item for item in violations)
        )

    def test_plan_policy_violations_blocks_possible_improvements_registry(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "- docs/possible-improvements.md\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertTrue(
            any(
                "forbidden path in plan: docs/possible-improvements.md" in item
                for item in violations
            )
        )

    def test_plan_policy_violations_requires_plan_tests_to_match_allowed_tests(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior and note docs/03-logs updates are handled by reporter/orchestrator; patcher will not edit those files.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_learning_loop_proposals.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertTrue(
            any(
                "plan test commands must be listed in Allowed Tests" in item
                for item in violations
            )
        )

    def test_plan_policy_violations_allows_matching_plan_test_commands(self):
        plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. Implement behavior and note docs/03-logs updates are handled by reporter/orchestrator; patcher will not edit those files.\n"
            "Files to change:\n"
            "- tools/pc-feature\n"
            "Risks:\n"
            "- regression risk\n"
            "Tests (anti-hardcode coverage required):\n"
            "- Fixture coverage: at least 2 fixtures\n"
            "- Deterministic seed strategy: fixed ordering\n"
            "- Invariant checks: no deletes\n"
            "- Contract boundary coverage: parser + output\n"
            "- Allowed test commands: `pytest tests/test_pc_feature.py`\n"
        )
        violations = self.pc_feature.plan_policy_violations(
            plan,
            allowed_tests=["pytest tests/test_pc_feature.py"],
        )
        self.assertFalse(
            any(
                "plan test commands must be listed in Allowed Tests" in item
                for item in violations
            )
        )

    def test_revised_plan_quality_issues_require_contract_when_previous_uses_contract(
        self,
    ):
        previous_plan = (
            "Plan Contract v1\n"
            "Approach:\n"
            "1. A\n"
            "Files to change:\n"
            "- tools/prd-to-features\n"
            "Risks:\n"
            "- B\n"
            "Tests (anti-hardcode coverage required):\n"
            "- C\n"
        )
        revised_plan = "1. quick patch only"
        issues = self.pc_feature.revised_plan_quality_issues(
            revised_plan, previous_plan=previous_plan
        )
        self.assertTrue(any("missing required sections" in item for item in issues))

    def test_merge_revised_plan_replaces_previous_plan(self):
        current = "old plan content\nwith stale path docs/02-features/12/dev-tasks.md"
        revised = "Plan Contract v1\nApproach:\n1. clean"
        merged = self.pc_feature.merge_revised_plan(current, revised)
        self.assertEqual(merged, revised)

    def test_role_scoped_path_forbidden_for_patcher_detects_cross_feature_docs(self):
        compacted_path = self.pc_feature.compacted_log_output_paths()["decision"]
        self.assertTrue(
            self.pc_feature.role_scoped_path_forbidden_for_patcher(
                "docs/02-features/12-incremental-prd-to-features/dev-tasks.md"
            )
        )
        self.assertTrue(
            self.pc_feature.role_scoped_path_forbidden_for_patcher(
                "docs/03-logs/validation-log.md"
            )
        )
        self.assertFalse(
            self.pc_feature.role_scoped_path_forbidden_for_patcher(compacted_path)
        )
        self.assertFalse(
            self.pc_feature.role_scoped_path_forbidden_for_patcher(
                "docs/02-features/12-incremental-prd-to-features/feature-spec.md"
            )
        )

    def test_enforce_role_scope_blocks_patcher_cross_feature_role_docs(self):
        stderr_capture = io.StringIO()
        with mock.patch.object(
            self.pc_feature,
            "get_status_paths",
            return_value=[
                "docs/02-features/12-incremental-prd-to-features/dev-tasks.md"
            ],
        ):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(stderr_capture):
                    self.pc_feature.enforce_role_scope(
                        "/tmp/worktree",
                        "patcher",
                        "docs/02-features/11-simplify-worktree-tracking",
                    )
        self.assertIn("patcher edited role-scoped files", stderr_capture.getvalue())

    def test_commit_role_step_tester_resets_dev_tasks_before_scope_check(self):
        feature_dir = "docs/02-features/01-workflow-hardening"
        dev_tasks_path = f"{feature_dir}/dev-tasks.md"
        validation_log_path = f"{feature_dir}/validation-log.md"
        reset_dev_tasks = mock.Mock(return_value=False)
        with mock.patch.object(
            self.pc_feature,
            "get_status_paths",
            side_effect=[
                [dev_tasks_path, validation_log_path],
                [validation_log_path],
            ],
        ):
            with mock.patch.object(
                self.pc_feature, "format_role_changes", return_value=None
            ):
                with mock.patch.object(
                    self.pc_feature,
                    "reset_possible_improvements_to_head",
                    return_value=None,
                ):
                    with mock.patch.object(
                        self.pc_feature, "reset_global_logs_to_head", return_value=None
                    ):
                        with mock.patch.object(
                            self.pc_feature,
                            "reset_dev_tasks_if_dirty",
                            reset_dev_tasks,
                        ):
                            with mock.patch.object(
                                self.pc_feature,
                                "enforce_role_scope",
                                return_value=None,
                            ):
                                with mock.patch.object(
                                    self.pc_feature,
                                    "commit_worktree_changes",
                                    return_value=None,
                                ):
                                    with mock.patch.object(
                                        self.pc_feature,
                                        "ensure_clean_worktree",
                                        return_value=None,
                                    ):
                                        committed = self.pc_feature.commit_role_step(
                                            "/tmp/root",
                                            "/tmp/worktree",
                                            "patcher-branch",
                                            "tester",
                                            "WI-20260210-01",
                                            feature_dir,
                                        )
        self.assertTrue(committed)
        reset_dev_tasks.assert_called_once_with("/tmp/worktree", dev_tasks_path)

    def test_commit_role_step_tester_logs_auto_reset_of_dev_tasks(self):
        feature_dir = "docs/02-features/01-workflow-hardening"
        dev_tasks_path = f"{feature_dir}/dev-tasks.md"
        validation_log_path = f"{feature_dir}/validation-log.md"
        reset_dev_tasks = mock.Mock(return_value=True)
        with mock.patch.object(
            self.pc_feature,
            "get_status_paths",
            side_effect=[
                [dev_tasks_path, validation_log_path],
                [validation_log_path],
            ],
        ):
            with mock.patch.object(
                self.pc_feature, "format_role_changes", return_value=None
            ):
                with mock.patch.object(
                    self.pc_feature,
                    "reset_possible_improvements_to_head",
                    return_value=None,
                ):
                    with mock.patch.object(
                        self.pc_feature, "reset_global_logs_to_head", return_value=None
                    ):
                        with mock.patch.object(
                            self.pc_feature,
                            "reset_dev_tasks_if_dirty",
                            reset_dev_tasks,
                        ):
                            with mock.patch.object(
                                self.pc_feature,
                                "enforce_role_scope",
                                return_value=None,
                            ):
                                with mock.patch.object(
                                    self.pc_feature,
                                    "commit_worktree_changes",
                                    return_value=None,
                                ):
                                    with mock.patch.object(
                                        self.pc_feature,
                                        "ensure_clean_worktree",
                                        return_value=None,
                                    ):
                                        with mock.patch("builtins.print") as print_mock:
                                            committed = (
                                                self.pc_feature.commit_role_step(
                                                    "/tmp/root",
                                                    "/tmp/worktree",
                                                    "patcher-branch",
                                                    "tester",
                                                    "WI-20260210-01",
                                                    feature_dir,
                                                )
                                            )
        self.assertTrue(committed)
        reset_dev_tasks.assert_called_once_with("/tmp/worktree", dev_tasks_path)
        print_mock.assert_any_call(
            "pc-feature: tester auto-reset planner-owned dev-tasks.md before "
            f"scope check: {dev_tasks_path}"
        )

    def test_compacted_policy_bootstrap_issues_reports_scope_block(self):
        with mock.patch.object(
            self.pc_feature, "role_scoped_path_forbidden_for_patcher", return_value=True
        ):
            issues = self.pc_feature.compacted_policy_bootstrap_issues()
        self.assertTrue(
            any(
                "patcher scope blocks compacted output path" in issue
                for issue in issues
            )
        )

    def test_ensure_compacted_policy_bootstrap_ready_exits_on_policy_mismatch(self):
        stderr_capture = io.StringIO()
        with mock.patch.object(
            self.pc_feature,
            "compacted_policy_bootstrap_issues",
            return_value=["scope mismatch"],
        ):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(stderr_capture):
                    self.pc_feature.ensure_compacted_policy_bootstrap_ready()
        self.assertIn(
            "compacted outputs are blocked by current workflow policy",
            stderr_capture.getvalue(),
        )

    def test_ensure_plan_reviewer_read_only_allows_preexisting_unchanged_dirty(self):
        baseline = {
            "docs/02-features/12-incremental-prd-to-features/dev-tasks.md": "abc"
        }
        with mock.patch.object(
            self.pc_feature,
            "collect_dirty_snapshot",
            return_value=dict(baseline),
        ):
            preexisting, delta = self.pc_feature.ensure_plan_reviewer_read_only(
                "/tmp/worktree", baseline_snapshot=baseline
            )
        self.assertEqual(
            preexisting,
            ["docs/02-features/12-incremental-prd-to-features/dev-tasks.md"],
        )
        self.assertEqual(delta, [])

    def test_ensure_plan_reviewer_read_only_detects_delta_on_changed_dirty(self):
        baseline = {
            "docs/02-features/12-incremental-prd-to-features/dev-tasks.md": "abc"
        }
        with mock.patch.object(
            self.pc_feature,
            "collect_dirty_snapshot",
            return_value={
                "docs/02-features/12-incremental-prd-to-features/dev-tasks.md": "xyz"
            },
        ):
            preexisting, delta = self.pc_feature.ensure_plan_reviewer_read_only(
                "/tmp/worktree", baseline_snapshot=baseline
            )
        self.assertEqual(
            preexisting,
            ["docs/02-features/12-incremental-prd-to-features/dev-tasks.md"],
        )
        self.assertEqual(
            delta, ["docs/02-features/12-incremental-prd-to-features/dev-tasks.md"]
        )

    def test_anti_hardcode_coverage_issues_requires_all_signals(self):
        missing = self.pc_feature.anti_hardcode_coverage_issues(
            "Plan with tests only",
            "TDD without details",
        )
        self.assertTrue(any("fixture coverage" in item for item in missing))
        self.assertTrue(any("seed strategy" in item for item in missing))
        self.assertTrue(any("invariant" in item for item in missing))
        self.assertTrue(any("contract boundary" in item for item in missing))
        complete = self.pc_feature.anti_hardcode_coverage_issues(
            "Use >=2 fixtures per critical path; deterministic seed strategy; invariant checks; contract boundary coverage.",
            "TDD plan includes fixture matrix.",
        )
        self.assertEqual(complete, [])

    def test_with_failure_context_guard_appends_missing_fields_for_fail(self):
        feedback = "Outcome: FAIL\nDocs/logs updated: none\nNotes: not enough details"
        guarded = self.pc_feature.with_failure_context_guard(feedback, role="reporter")
        self.assertIn(
            "Failure context guard (reporter): missing required fields", guarded
        )
        self.assertIn("Expected fix:", guarded)

    def test_build_failure_outcome_payload_uses_feedback_improvement_fields(self):
        payload = self.pc_feature.build_failure_outcome_payload(
            work_item_id="WI-20260209-01",
            tester_outcome="FAIL",
            reporter_outcome="FAIL",
            tester_feedback=(
                "Outcome: FAIL\n"
                "File/Path: logs/WI-20260209-01/tests.log\n"
                "Check: tests exit 0\n"
                "Evidence: command exited 1\n"
                "Expected fix: tighten assertions\n"
                "Proposed Patch Location: tests/test_pc_feature.py\n"
            ),
            reporter_feedback=(
                "Outcome: FAIL\n"
                "File/Path: tools/pc-feature\n"
                "Check: workflow retries\n"
                "Evidence: repeated scope failures\n"
                "Expected fix: route proposals through orchestrator queue\n"
                "Proposed Improvement: collect and dedupe proposals at orchestrator checkpoints\n"
                "Proposed Patch Location: tools/pc-feature\n"
                "Risks / Trade-offs: Slightly more orchestration state\n"
            ),
        )
        self.assertEqual(
            payload.get("proposed_improvement"),
            "collect and dedupe proposals at orchestrator checkpoints",
        )
        self.assertEqual(
            payload.get("proposed_patch_location"),
            "tools/pc-feature, tests/test_pc_feature.py, logs/WI-20260209-01/tests.log",
        )
        self.assertEqual(payload.get("risks"), "Slightly more orchestration state")

    def test_should_enforce_anti_hardcode_only_for_high_risk_or_trigger_paths(self):
        work_item_id = "WI-20260208-01"
        content = "## Execution Log\n\n" + self.pc_feature.build_execution_entry(
            work_item_id
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Preflight Report",
            "- Work Item: WI-20260208-01\n"
            "- PRD ref: F-11\n"
            "- Risk level: LOW\n"
            "- Triggers: (none)\n"
            "- Scope in: docs\n"
            "- Scope out: code\n"
            "- Non-goals reminder: none\n"
            "- Files to change: docs/04-process/ticket-execution-protocol.md\n"
            "- TDD plan: (none)\n"
            "- Systematic review: done",
        )
        self.assertFalse(
            self.pc_feature.should_enforce_anti_hardcode(content, work_item_id)
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Preflight Report",
            "- Work Item: WI-20260208-01\n"
            "- PRD ref: F-11\n"
            "- Risk level: HIGH\n"
            "- Triggers: touches restore/ path\n"
            "- Scope in: restore\n"
            "- Scope out: docs\n"
            "- Non-goals reminder: none\n"
            "- Files to change: restore/apply.py\n"
            "- TDD plan: (none)\n"
            "- Systematic review: done",
        )
        self.assertTrue(
            self.pc_feature.should_enforce_anti_hardcode(content, work_item_id)
        )

    def test_high_risk_preflight_approved_interactively_continues(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-16"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "preparing preflight data for a work item execution" in prompt:
                    return (
                        '{"prd_ref":"F-10","scope_in":"x","scope_out":"y",'
                        '"non_goals_reminder":"z","files_to_change":["restore/apply.py"],'
                        '"planned_new_modules":0,"touches_secret_blocking":false,'
                        '"touches_restore":true,"touches_secret_scanning":false,'
                        '"cross_cutting_refactor_modules":0,"tdd_tests":[],"doc_updates":[]}'
                    )
                if "You are the Planner agent. Provide a concise plan" in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "prompt_yes_no", return_value=True
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature.sys.stdin, "isatty", return_value=True
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "codex_exec", side_effect=fake_codex_exec
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

    def test_high_risk_resume_without_approval_note_reprompts(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-17"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Preflight Report",
                (
                    "- Work Item: WI-20260206-17\n"
                    "- PRD ref: docs/01-product/prd.md\n"
                    "- Risk level: HIGH\n"
                    "- Triggers: touches restore/ path\n"
                    "- Scope in: x\n"
                    "- Scope out: y\n"
                    "- Non-goals reminder: z\n"
                    "- Files to change: restore/apply.py\n"
                    "- TDD plan: test\n"
                    "- Systematic review: done"
                ),
            )
            content = self.pc_feature.update_entry_field(
                content, work_item_id, "Notes", "Awaiting PO Approval"
            )
            feature_dir = self._write_feature_workspace(root, content)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Planner agent. Provide a concise plan" in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "prompt_yes_no",
                        return_value=True,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature.sys.stdin, "isatty", return_value=True
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "codex_exec", side_effect=fake_codex_exec
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            updated = self._worktree_dev_tasks(patcher_path).read_text(encoding="utf-8")
            self.assertIn("High-risk gate approved interactively.", updated)

    def test_normalize_work_item_id_accepts_format(self):
        self.assertEqual(
            self.pc_feature.normalize_work_item_id("WI-20260204-01"),
            "WI-20260204-01",
        )

    def test_normalize_work_item_id_rejects_invalid(self):
        stderr_capture = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(stderr_capture):
                self.pc_feature.normalize_work_item_id("BAD")
        self.assertIn("invalid work item id", stderr_capture.getvalue())

    def test_next_work_item_id_increments_per_feature(self):
        original_datetime = self.pc_feature.datetime

        class FakeDateTime:
            @classmethod
            def now(cls):
                return datetime(2026, 2, 6)

        self.pc_feature.datetime = FakeDateTime
        try:
            content = (
                "### WI-20260204-01 - Work item execution\n"
                "### WI-20260205-02 - Work item execution\n"
            )
            self.assertEqual(
                self.pc_feature.next_work_item_id(content),
                "WI-20260206-03",
            )
        finally:
            self.pc_feature.datetime = original_datetime

    def test_select_resume_work_item_id_resumes_newest_non_pass(self):
        newest = "WI-20260206-03"
        middle = "WI-20260206-02"
        oldest = "WI-20260206-01"
        content = "## Execution Log\n\n"
        content += self.pc_feature.build_execution_entry(newest) + "\n"
        content += self.pc_feature.build_execution_entry(middle) + "\n"
        content += self.pc_feature.build_execution_entry(oldest)
        content = self.pc_feature.update_entry_field(
            content, newest, "Outcome", "needs replan"
        )
        content = self.pc_feature.update_entry_field(content, middle, "Outcome", "pass")
        content = self.pc_feature.update_entry_field(
            content, oldest, "Outcome", "needs replan"
        )
        self.assertEqual(
            self.pc_feature.select_resume_work_item_id(content),
            newest,
        )

    def test_select_resume_work_item_id_returns_none_when_newest_pass(self):
        newest = "WI-20260206-03"
        older = "WI-20260206-02"
        content = "## Execution Log\n\n"
        content += self.pc_feature.build_execution_entry(newest) + "\n"
        content += self.pc_feature.build_execution_entry(older)
        content = self.pc_feature.update_entry_field(content, newest, "Outcome", "pass")
        content = self.pc_feature.update_entry_field(
            content, older, "Outcome", "needs replan"
        )
        self.assertIsNone(self.pc_feature.select_resume_work_item_id(content))

    def test_parse_resume_mode_defaults_to_auto(self):
        with mock.patch.dict(self.pc_feature.os.environ, {}, clear=True):
            self.assertEqual(self.pc_feature.parse_resume_mode(), "auto")

    def test_parse_args_help_flag_exits_zero_and_prints_resume_modes(self):
        stdout_capture = io.StringIO()
        with self.assertRaises(SystemExit) as raised:
            with contextlib.redirect_stdout(stdout_capture):
                self.pc_feature.parse_args(["--help"])
        self.assertEqual(raised.exception.code, 0)
        help_text = stdout_capture.getvalue()
        self.assertIn("Usage:", help_text)
        self.assertIn("RESUME_MODE", help_text)
        self.assertIn("sync", help_text)

    def test_parse_args_short_help_flag_exits_zero(self):
        with self.assertRaises(SystemExit) as raised:
            self.pc_feature.parse_args(["-h"])
        self.assertEqual(raised.exception.code, 0)

    def test_parse_resume_mode_normalizes_supported_values(self):
        cases = [
            ({}, "auto"),
            ({"RESUME_MODE": "  "}, "auto"),
            ({"RESUME_MODE": "AUTO"}, "auto"),
            ({"RESUME_MODE": " Prompt "}, "prompt"),
            ({"RESUME_MODE": "fresh"}, "fresh"),
            ({"RESUME_MODE": "SYNC"}, "sync"),
        ]
        for env_updates, expected in cases:
            with self.subTest(env=env_updates, expected=expected):
                with mock.patch.dict(
                    self.pc_feature.os.environ, env_updates, clear=True
                ):
                    self.assertEqual(self.pc_feature.parse_resume_mode(), expected)

    def test_parse_resume_mode_invalid_value_exits(self):
        stderr_capture = io.StringIO()
        with mock.patch.dict(
            self.pc_feature.os.environ, {"RESUME_MODE": "invalid"}, clear=False
        ):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(stderr_capture):
                    self.pc_feature.parse_resume_mode()
        self.assertIn("invalid RESUME_MODE value", stderr_capture.getvalue())

    def test_parse_resume_contradiction_policy_defaults_to_repair(self):
        with mock.patch.dict(self.pc_feature.os.environ, {}, clear=True):
            self.assertEqual(
                self.pc_feature.parse_resume_contradiction_policy(),
                "repair",
            )

    def test_parse_resume_contradiction_policy_normalizes_supported_values(self):
        cases = [
            ({}, "repair"),
            ({"RESUME_CONTRADICTION_POLICY": "  "}, "repair"),
            ({"RESUME_CONTRADICTION_POLICY": "REPAIR"}, "repair"),
            ({"RESUME_CONTRADICTION_POLICY": " block "}, "block"),
            ({"RESUME_CONTRADICTION_POLICY": "rewind"}, "rewind"),
        ]
        for env_updates, expected in cases:
            with self.subTest(env=env_updates, expected=expected):
                with mock.patch.dict(
                    self.pc_feature.os.environ, env_updates, clear=True
                ):
                    self.assertEqual(
                        self.pc_feature.parse_resume_contradiction_policy(),
                        expected,
                    )

    def test_parse_resume_contradiction_policy_invalid_value_exits(self):
        stderr_capture = io.StringIO()
        with mock.patch.dict(
            self.pc_feature.os.environ,
            {"RESUME_CONTRADICTION_POLICY": "invalid"},
            clear=False,
        ):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(stderr_capture):
                    self.pc_feature.parse_resume_contradiction_policy()
        self.assertIn(
            "invalid RESUME_CONTRADICTION_POLICY value",
            stderr_capture.getvalue(),
        )

    def test_detect_resume_route_planner_and_reviewer_complete_routes_to_patcher(self):
        work_item_id = "WI-20260210-01"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Plan",
            "Plan Contract v1\n\nApproach:\n- resume safely",
        )
        first = self.pc_feature.detect_resume_route(content, work_item_id)
        second = self.pc_feature.detect_resume_route(content, work_item_id)
        self.assertEqual(first, second)
        self.assertEqual(first, ("patcher", None))

    def test_detect_resume_route_tester_failed_routes_to_planner(self):
        work_item_id = "WI-20260210-02"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Plan",
            "Plan Contract v1\n\nApproach:\n- apply patch",
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patched files present"
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Tester Feedback",
            "Outcome: FAIL\nNotes: test failed",
        )
        self.assertEqual(
            self.pc_feature.detect_resume_route(content, work_item_id),
            ("planner", None),
        )

    def test_detect_resume_route_reporter_complete_routes_to_tester(self):
        work_item_id = "WI-20260210-03"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", "- python -m pytest ... -> 0"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Reporter Review", "Outcome: PASS\nNotes: approved"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Tester Feedback", "Outcome: PASS\nNotes: clean"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Reporter Feedback", "Outcome: PASS\nNotes: clean"
        )
        self.assertEqual(
            self.pc_feature.detect_resume_route(content, work_item_id),
            ("tester", None),
        )

    def test_detect_resume_route_blocks_contradictory_state(self):
        work_item_id = "WI-20260210-04"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", "- python -m pytest ... -> 1"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Reporter Review", "Outcome: PASS\nNotes: approved"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Tester Feedback", "Outcome: FAIL\nNotes: failed"
        )
        route, reason = self.pc_feature.detect_resume_route(content, work_item_id)
        self.assertEqual(route, "block")
        self.assertIn("contradictory", reason)

    def test_detect_resume_route_blocks_missing_critical_artifact(self):
        work_item_id = "WI-20260210-05"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Reporter Feedback", "Outcome: PASS\nNotes: approved"
        )
        route, reason = self.pc_feature.detect_resume_route(content, work_item_id)
        self.assertEqual(route, "block")
        self.assertIn("missing critical artifact", reason)

    def test_detect_resume_route_blocks_pending_sections_when_role_artifacts_exist(
        self,
    ):
        work_item_id = "WI-20260210-06"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tester_log = Path(tmpdir) / "validation-log.md"
            reporter_log = Path(tmpdir) / "reporter-log.md"
            tester_log.write_text(
                (
                    "# Validation Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nOutcome: PASS\n"
                ),
                encoding="utf-8",
            )
            reporter_log.write_text(
                (
                    "# Reporter Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nOutcome: FAIL\n"
                ),
                encoding="utf-8",
            )
            route, reason = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                tester_log_path=str(tester_log),
                reporter_log_path=str(reporter_log),
            )
        self.assertEqual(route, "block")
        self.assertIn("contradictory", reason)
        self.assertIn("patch section is pending", reason)
        self.assertIn("test results section is pending", reason)
        self.assertIn("reporter review section is pending", reason)

    def test_detect_resume_route_allows_complete_sections_with_role_artifacts(self):
        work_item_id = "WI-20260210-07"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", "- python -m pytest ... -> 0"
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Tester Feedback",
            "Outcome: PASS\nNotes: clean",
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Reporter Review",
            "Outcome: FAIL\nNotes: traceability",
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Reporter Feedback",
            "Outcome: FAIL\nNotes: traceability",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tester_log = Path(tmpdir) / "validation-log.md"
            reporter_log = Path(tmpdir) / "reporter-log.md"
            tester_log.write_text(
                (
                    "# Validation Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nOutcome: PASS\n"
                ),
                encoding="utf-8",
            )
            reporter_log.write_text(
                (
                    "# Reporter Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nOutcome: FAIL\n"
                ),
                encoding="utf-8",
            )
            first = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                tester_log_path=str(tester_log),
                reporter_log_path=str(reporter_log),
            )
            second = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                tester_log_path=str(tester_log),
                reporter_log_path=str(reporter_log),
            )
        self.assertEqual(first, second)
        self.assertEqual(first, ("tester", None))

    def test_detect_resume_route_blocks_pending_plan_when_planner_artifacts_exist(
        self,
    ):
        work_item_id = "WI-20260210-08"
        content = self._build_entry_content(work_item_id)
        with tempfile.TemporaryDirectory() as tmpdir:
            planner_log = Path(tmpdir) / "planner-log.md"
            reviewer_log = Path(tmpdir) / "plan-reviewer-log.md"
            planner_log.write_text(
                (
                    "# Planner Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nPlan drafted.\n"
                ),
                encoding="utf-8",
            )
            reviewer_log.write_text(
                (
                    "# Plan Reviewer Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nDecision: APPROVE\n"
                ),
                encoding="utf-8",
            )
            route, reason = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                planner_log_path=str(planner_log),
                reviewer_log_path=str(reviewer_log),
            )
        self.assertEqual(route, "block")
        self.assertIn("contradictory", reason)
        self.assertIn("planner artifact exists while plan section is pending", reason)
        self.assertIn(
            "plan-reviewer artifact exists while plan section is pending", reason
        )

    def test_detect_resume_route_blocks_missing_tester_feedback_for_test_results(self):
        work_item_id = "WI-20260210-09"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", "- python -m pytest ... -> 0"
        )
        route, reason = self.pc_feature.detect_resume_route(content, work_item_id)
        self.assertEqual(route, "block")
        self.assertIn("missing critical artifact", reason)
        self.assertIn("tester feedback", reason)

    def test_detect_resume_route_uses_role_artifact_outcomes_when_feedback_missing(
        self,
    ):
        work_item_id = "WI-20260210-10"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", "- pytest -> 1"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tester_log = Path(tmpdir) / "validation-log.md"
            tester_log.write_text(
                (
                    "# Validation Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\n"
                    "Outcome: FAIL\n"
                    "Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`\n"
                ),
                encoding="utf-8",
            )
            route, reason = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                tester_log_path=str(tester_log),
            )
        self.assertEqual(route, "planner")
        self.assertIsNone(reason)

    def test_detect_resume_route_allows_reporter_skipped_without_reporter_review(self):
        work_item_id = "WI-20260210-11"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Patch", "- patch complete"
        )
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", "- pytest -> 1"
        )
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Reporter Feedback",
            "Outcome: SKIPPED\nNotes: deferred",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tester_log = Path(tmpdir) / "validation-log.md"
            reporter_log = Path(tmpdir) / "reporter-log.md"
            tester_log.write_text(
                (
                    "# Validation Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\nOutcome: FAIL\n"
                ),
                encoding="utf-8",
            )
            reporter_log.write_text(
                (
                    "# Reporter Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\nOutcome: SKIPPED\n"
                    "Docs/logs updated: reporter deferred\n"
                    "Notes: Reporter skipped because tester failed.\n"
                ),
                encoding="utf-8",
            )
            route, reason = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                tester_log_path=str(tester_log),
                reporter_log_path=str(reporter_log),
            )
        self.assertEqual(route, "planner")
        self.assertIsNone(reason)

    def test_reconcile_resume_pending_sections_backfills_pending_sections_only(self):
        work_item_id = "WI-20260210-12"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tester_log = Path(tmpdir) / "validation-log.md"
            reporter_log = Path(tmpdir) / "reporter-log.md"
            tester_log.write_text(
                (
                    "# Validation Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\n"
                    "Outcome: PASS\n"
                    "Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`\n"
                    "Notes: all checks passed\n"
                ),
                encoding="utf-8",
            )
            reporter_log.write_text(
                (
                    "# Reporter Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\n"
                    "Outcome: PASS\n"
                    "Docs/logs updated: reporter complete\n"
                    "Notes: scope approved\n"
                ),
                encoding="utf-8",
            )
            updated, repaired_sections = (
                self.pc_feature.reconcile_resume_pending_sections(
                    content,
                    work_item_id,
                    tester_log_path=str(tester_log),
                    reporter_log_path=str(reporter_log),
                )
            )
        self.assertEqual(
            repaired_sections,
            ["Patch", "Test Results", "Reporter Review"],
        )
        self.assertNotIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Patch"),
        )
        self.assertNotIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Test Results"),
        )
        self.assertNotIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Reporter Review"),
        )
        self.assertIn(
            "Startup auto-repair aligned pending sections",
            self.pc_feature.get_entry_section(updated, work_item_id, "Iteration Log"),
        )

    def test_reconcile_resume_pending_sections_skips_reporter_review_for_skipped(self):
        work_item_id = "WI-20260210-13"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tester_log = Path(tmpdir) / "validation-log.md"
            reporter_log = Path(tmpdir) / "reporter-log.md"
            tester_log.write_text(
                (
                    "# Validation Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\nOutcome: FAIL\n"
                    "Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`\n"
                ),
                encoding="utf-8",
            )
            reporter_log.write_text(
                (
                    "# Reporter Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-12\n\nOutcome: SKIPPED\n"
                    "Docs/logs updated: reporter deferred\n"
                ),
                encoding="utf-8",
            )
            updated, repaired_sections = (
                self.pc_feature.reconcile_resume_pending_sections(
                    content,
                    work_item_id,
                    tester_log_path=str(tester_log),
                    reporter_log_path=str(reporter_log),
                )
            )
        self.assertEqual(repaired_sections, ["Patch", "Test Results"])
        self.assertIn(
            "(pending)",
            self.pc_feature.get_entry_section(updated, work_item_id, "Reporter Review"),
        )

    def test_detect_resume_route_planner_and_reviewer_artifacts_route_to_patcher(self):
        work_item_id = "WI-20260210-14"
        content = self._build_entry_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Plan", "Plan Contract v1\n\nApproach:\n- done"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            planner_log = Path(tmpdir) / "planner-log.md"
            reviewer_log = Path(tmpdir) / "plan-reviewer-log.md"
            planner_log.write_text(
                (
                    "# Planner Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nPlan drafted.\n"
                ),
                encoding="utf-8",
            )
            reviewer_log.write_text(
                (
                    "# Plan Reviewer Log\n\n## Entries\n\n"
                    f"### {work_item_id} - 2026-02-11\n\nDecision: APPROVE\n"
                ),
                encoding="utf-8",
            )
            first = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                planner_log_path=str(planner_log),
                reviewer_log_path=str(reviewer_log),
            )
            second = self.pc_feature.detect_resume_route(
                content,
                work_item_id,
                planner_log_path=str(planner_log),
                reviewer_log_path=str(reviewer_log),
            )
        self.assertEqual(first, second)
        self.assertEqual(first, ("patcher", None))

    def test_detect_resume_route_fixture_matrix_is_deterministic(self):
        def with_plan(content: str, work_item_id: str) -> str:
            return self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Plan",
                "Plan Contract v1\n\nApproach:\n- done",
            )

        fixtures = [
            {
                "name": "valid-routes-to-patcher",
                "work_item_id": "WI-20260211-11",
                "path": "valid",
                "critical_path": "planner-reviewer-complete",
                "build": lambda content, work_item_id: with_plan(content, work_item_id),
                "expected_route": "patcher",
                "reason_contains": None,
            },
            {
                "name": "valid-routes-to-tester",
                "work_item_id": "WI-20260211-12",
                "path": "valid",
                "critical_path": "reporter-complete",
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        self.pc_feature.replace_entry_section(
                            self.pc_feature.replace_entry_section(
                                self.pc_feature.replace_entry_section(
                                    with_plan(content, work_item_id),
                                    work_item_id,
                                    "Patch",
                                    "- patch complete",
                                ),
                                work_item_id,
                                "Test Results",
                                "- python -m pytest ... -> 0",
                            ),
                            work_item_id,
                            "Reporter Review",
                            "Outcome: PASS\nNotes: approved",
                        ),
                        work_item_id,
                        "Tester Feedback",
                        "Outcome: PASS\nNotes: clean",
                    ),
                    work_item_id,
                    "Reporter Feedback",
                    "Outcome: PASS\nNotes: approved",
                ),
                "expected_route": "tester",
                "reason_contains": None,
            },
            {
                "name": "missing-critical-test-results-without-tester-feedback",
                "work_item_id": "WI-20260211-18",
                "path": "missing-critical",
                "critical_path": None,
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        with_plan(content, work_item_id),
                        work_item_id,
                        "Patch",
                        "- patch complete",
                    ),
                    work_item_id,
                    "Test Results",
                    "- python -m pytest ... -> 0",
                ),
                "expected_route": "block",
                "reason_contains": "missing critical artifact",
            },
            {
                "name": "contradiction-pending-plan-with-planner-artifacts",
                "work_item_id": "WI-20260211-19",
                "path": "contradictory",
                "critical_path": None,
                "build": lambda content, _work_item_id: content,
                "with_artifacts": "planner-reviewer",
                "expected_route": "block",
                "reason_contains": "plan section is pending",
            },
            {
                "name": "valid-planner-reviewer-artifacts-route-to-patcher",
                "work_item_id": "WI-20260211-20",
                "path": "valid",
                "critical_path": "planner-reviewer-complete",
                "build": lambda content, work_item_id: with_plan(content, work_item_id),
                "with_artifacts": "planner-reviewer",
                "expected_route": "patcher",
                "reason_contains": None,
            },
            {
                "name": "valid-tester-failed-routes-to-planner",
                "work_item_id": "WI-20260211-22",
                "path": "valid",
                "critical_path": "tester-failed",
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        self.pc_feature.replace_entry_section(
                            with_plan(content, work_item_id),
                            work_item_id,
                            "Patch",
                            "- patch complete",
                        ),
                        work_item_id,
                        "Tester Feedback",
                        "Outcome: FAIL\nNotes: failed",
                    ),
                    work_item_id,
                    "Test Results",
                    "- python -m pytest ... -> 1",
                ),
                "expected_route": "planner",
                "reason_contains": None,
            },
            {
                "name": "valid-reporter-complete-via-role-artifacts-routes-to-tester",
                "work_item_id": "WI-20260211-23",
                "path": "valid",
                "critical_path": "reporter-complete",
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        self.pc_feature.replace_entry_section(
                            self.pc_feature.replace_entry_section(
                                with_plan(content, work_item_id),
                                work_item_id,
                                "Patch",
                                "- patch complete",
                            ),
                            work_item_id,
                            "Test Results",
                            "- python -m pytest ... -> 0",
                        ),
                        work_item_id,
                        "Reporter Review",
                        "Outcome: PASS\nNotes: approved",
                    ),
                    work_item_id,
                    "Tester Feedback",
                    "Outcome: PASS\nNotes: clean",
                ),
                "with_artifacts": "tester-reporter-pass",
                "expected_route": "tester",
                "reason_contains": None,
            },
            {
                "name": "valid-tester-failed-via-role-artifacts-routes-to-planner",
                "work_item_id": "WI-20260211-24",
                "path": "valid",
                "critical_path": "tester-failed",
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        with_plan(content, work_item_id),
                        work_item_id,
                        "Patch",
                        "- patch complete",
                    ),
                    work_item_id,
                    "Test Results",
                    "- python -m pytest ... -> 1",
                ),
                "with_artifacts": "tester-fail-reporter-skipped",
                "expected_route": "planner",
                "reason_contains": None,
            },
            {
                "name": "contradiction-tester-fail-vs-reporter-pass",
                "work_item_id": "WI-20260211-13",
                "path": "contradictory",
                "critical_path": None,
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        self.pc_feature.replace_entry_section(
                            self.pc_feature.replace_entry_section(
                                self.pc_feature.replace_entry_section(
                                    with_plan(content, work_item_id),
                                    work_item_id,
                                    "Patch",
                                    "- patch complete",
                                ),
                                work_item_id,
                                "Test Results",
                                "- python -m pytest ... -> 1",
                            ),
                            work_item_id,
                            "Reporter Review",
                            "Outcome: PASS\nNotes: approved",
                        ),
                        work_item_id,
                        "Tester Feedback",
                        "Outcome: FAIL\nNotes: failed",
                    ),
                    work_item_id,
                    "Reporter Feedback",
                    "Outcome: PASS\nNotes: approved",
                ),
                "expected_route": "block",
                "reason_contains": "contradictory",
            },
            {
                "name": "contradiction-reporter-feedback-before-review",
                "work_item_id": "WI-20260211-14",
                "path": "contradictory",
                "critical_path": None,
                "build": lambda content, work_item_id: self.pc_feature.replace_entry_section(
                    self.pc_feature.replace_entry_section(
                        self.pc_feature.replace_entry_section(
                            with_plan(content, work_item_id),
                            work_item_id,
                            "Patch",
                            "- patch complete",
                        ),
                        work_item_id,
                        "Test Results",
                        "- python -m pytest ... -> 0",
                    ),
                    work_item_id,
                    "Reporter Feedback",
                    "Outcome: PASS\nNotes: exists before review",
                ),
                "expected_route": "block",
                "reason_contains": "reporter feedback",
            },
            {
                "name": "baseline-no-plan-routes-to-planner",
                "work_item_id": "WI-20260211-15",
                "path": "baseline",
                "critical_path": None,
                "build": lambda content, _work_item_id: content,
                "expected_route": "planner",
                "reason_contains": None,
            },
            {
                "name": "baseline-plan-and-patchout-routes-to-patcher",
                "work_item_id": "WI-20260211-16",
                "path": "baseline",
                "critical_path": None,
                "build": lambda content, work_item_id: with_plan(content, work_item_id),
                "expected_route": "patcher",
                "reason_contains": None,
            },
        ]

        path_counts = {}
        for fixture in fixtures:
            path_counts[fixture["path"]] = path_counts.get(fixture["path"], 0) + 1
        self.assertGreaterEqual(path_counts.get("valid", 0), 2)
        self.assertGreaterEqual(path_counts.get("contradictory", 0), 2)
        self.assertGreaterEqual(path_counts.get("baseline", 0), 2)
        self.assertGreaterEqual(path_counts.get("missing-critical", 0), 1)
        critical_counts = {}
        for fixture in fixtures:
            critical_path = fixture.get("critical_path")
            if not critical_path:
                continue
            critical_counts[critical_path] = critical_counts.get(critical_path, 0) + 1
        self.assertGreaterEqual(critical_counts.get("planner-reviewer-complete", 0), 2)
        self.assertGreaterEqual(critical_counts.get("tester-failed", 0), 2)
        self.assertGreaterEqual(critical_counts.get("reporter-complete", 0), 2)

        for fixture in fixtures:
            with self.subTest(fixture=fixture["name"]):
                content = self._build_entry_content(fixture["work_item_id"])
                content = fixture["build"](content, fixture["work_item_id"])
                kwargs = {}
                if fixture.get("with_artifacts") == "planner-reviewer":
                    with tempfile.TemporaryDirectory() as tmpdir:
                        planner_log = Path(tmpdir) / "planner-log.md"
                        reviewer_log = Path(tmpdir) / "plan-reviewer-log.md"
                        planner_log.write_text(
                            (
                                "# Planner Log\n\n## Entries\n\n"
                                f"### {fixture['work_item_id']} - 2026-02-11\n\nPlan drafted.\n"
                            ),
                            encoding="utf-8",
                        )
                        reviewer_log.write_text(
                            (
                                "# Plan Reviewer Log\n\n## Entries\n\n"
                                f"### {fixture['work_item_id']} - 2026-02-11\n\nDecision: APPROVE\n"
                            ),
                            encoding="utf-8",
                        )
                        kwargs = {
                            "planner_log_path": str(planner_log),
                            "reviewer_log_path": str(reviewer_log),
                        }
                        first = self.pc_feature.detect_resume_route(
                            content, fixture["work_item_id"], **kwargs
                        )
                        second = self.pc_feature.detect_resume_route(
                            content, fixture["work_item_id"], **kwargs
                        )
                elif fixture.get("with_artifacts") == "tester-reporter-pass":
                    with tempfile.TemporaryDirectory() as tmpdir:
                        tester_log = Path(tmpdir) / "validation-log.md"
                        reporter_log = Path(tmpdir) / "reporter-log.md"
                        tester_log.write_text(
                            (
                                "# Validation Log\n\n## Entries\n\n"
                                f"### {fixture['work_item_id']} - 2026-02-11\n\nOutcome: PASS\n"
                                "Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`\n"
                            ),
                            encoding="utf-8",
                        )
                        reporter_log.write_text(
                            (
                                "# Reporter Log\n\n## Entries\n\n"
                                f"### {fixture['work_item_id']} - 2026-02-11\n\nOutcome: PASS\n"
                                "Docs/logs updated: reporter complete\n"
                            ),
                            encoding="utf-8",
                        )
                        kwargs = {
                            "tester_log_path": str(tester_log),
                            "reporter_log_path": str(reporter_log),
                        }
                        first = self.pc_feature.detect_resume_route(
                            content, fixture["work_item_id"], **kwargs
                        )
                        second = self.pc_feature.detect_resume_route(
                            content, fixture["work_item_id"], **kwargs
                        )
                elif fixture.get("with_artifacts") == "tester-fail-reporter-skipped":
                    with tempfile.TemporaryDirectory() as tmpdir:
                        tester_log = Path(tmpdir) / "validation-log.md"
                        reporter_log = Path(tmpdir) / "reporter-log.md"
                        tester_log.write_text(
                            (
                                "# Validation Log\n\n## Entries\n\n"
                                f"### {fixture['work_item_id']} - 2026-02-11\n\nOutcome: FAIL\n"
                                "Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`\n"
                            ),
                            encoding="utf-8",
                        )
                        reporter_log.write_text(
                            (
                                "# Reporter Log\n\n## Entries\n\n"
                                f"### {fixture['work_item_id']} - 2026-02-11\n\nOutcome: SKIPPED\n"
                                "Docs/logs updated: reporter deferred\n"
                            ),
                            encoding="utf-8",
                        )
                        kwargs = {
                            "tester_log_path": str(tester_log),
                            "reporter_log_path": str(reporter_log),
                        }
                        first = self.pc_feature.detect_resume_route(
                            content, fixture["work_item_id"], **kwargs
                        )
                        second = self.pc_feature.detect_resume_route(
                            content, fixture["work_item_id"], **kwargs
                        )
                else:
                    first = self.pc_feature.detect_resume_route(
                        content, fixture["work_item_id"]
                    )
                    second = self.pc_feature.detect_resume_route(
                        content, fixture["work_item_id"]
                    )
                self.assertEqual(first, second)
                self.assertEqual(first[0], fixture["expected_route"])
                if fixture["reason_contains"]:
                    self.assertIsNotNone(first[1])
                    self.assertIn(fixture["reason_contains"], first[1])
                else:
                    self.assertIsNone(first[1])

    def test_main_resume_consistency_gate_shared_by_auto_and_prompt(self):
        class StopAfterRoute(RuntimeError):
            pass

        for resume_mode in ("auto", "prompt"):
            with self.subTest(resume_mode=resume_mode):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    root = Path(tmp_dir)
                    patcher_path = root / "patcher"
                    patcher_path.mkdir(parents=True, exist_ok=True)
                    (patcher_path / ".git").write_text(
                        "gitdir: /tmp/fake\n", encoding="utf-8"
                    )
                    work_item_id = "WI-20260211-17"
                    content = self._build_entry_content(work_item_id)
                    feature_dir = self._write_feature_workspace(root, content)
                    die_messages = []

                    def capture_die(message: str) -> None:
                        die_messages.append(message)
                        raise StopAfterRoute()

                    with contextlib.ExitStack() as stack:
                        for patcher in self._patch_main_base(
                            root, feature_dir, patcher_path
                        ):
                            stack.enter_context(patcher)
                        stack.enter_context(
                            mock.patch.object(
                                self.pc_feature,
                                "parse_resume_mode",
                                return_value=resume_mode,
                            )
                        )
                        detect_mock = stack.enter_context(
                            mock.patch.object(
                                self.pc_feature,
                                "detect_resume_route",
                                return_value=(
                                    "block",
                                    "contradictory resume state: fixture",
                                ),
                            )
                        )
                        stack.enter_context(
                            mock.patch.object(
                                self.pc_feature,
                                "die",
                                side_effect=capture_die,
                            )
                        )
                        with self.assertRaises(StopAfterRoute):
                            self.pc_feature.main()
                    self.assertEqual(detect_mock.call_count, 1)
                    self.assertEqual(len(die_messages), 1)
                    self.assertIn("contradictory resume state", die_messages[0])
                    self.assertIn(f"mode={resume_mode}", die_messages[0])

    def test_main_passes_all_role_logs_to_resume_route(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260211-21"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)

            def capture_detect(content: str, incoming_work_item_id: str, **kwargs):
                self.assertEqual(incoming_work_item_id, work_item_id)
                self.assertIn("planner_log_path", kwargs)
                self.assertIn("reviewer_log_path", kwargs)
                self.assertIn("tester_log_path", kwargs)
                self.assertIn("reporter_log_path", kwargs)
                raise StopMain()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "detect_resume_route",
                        side_effect=capture_detect,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

    def test_classify_resume_dirty_paths_separates_runtime_and_unexpected(self):
        feature_dir = "docs/02-features/01-workflow-hardening"
        dev_tasks = "docs/02-features/01-workflow-hardening/dev-tasks.md"
        runtime, unexpected = self.pc_feature.classify_resume_dirty_paths(
            [
                dev_tasks,
                "docs/02-features/01-workflow-hardening/planner-log.md",
                "docs/03-logs/implementation-log.md",
                "README.md",
            ],
            feature_dir,
            dev_tasks,
        )
        self.assertEqual(
            runtime,
            [
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening/planner-log.md",
                "docs/03-logs/implementation-log.md",
            ],
        )
        self.assertEqual(unexpected, ["README.md"])

    def test_classify_resume_dirty_paths_allows_possible_improvements_registry(self):
        feature_dir = "docs/02-features/01-workflow-hardening"
        dev_tasks = "docs/02-features/01-workflow-hardening/dev-tasks.md"
        runtime, unexpected = self.pc_feature.classify_resume_dirty_paths(
            [
                "docs/possible-improvements.md",
                "README.md",
            ],
            feature_dir,
            dev_tasks,
        )
        self.assertEqual(runtime, ["docs/possible-improvements.md"])
        self.assertEqual(unexpected, ["README.md"])

    def test_enforce_single_active_feature_blocks_other_active_patcher(self):
        stderr_capture = io.StringIO()
        with mock.patch.object(
            self.pc_feature,
            "list_worktree_entries",
            return_value=[
                (
                    "/tmp/current",
                    "feature-11-simplify-worktree-tracking-patcher",
                ),
                (
                    "/tmp/other",
                    "feature-12-incremental-prd-to-features-patcher",
                ),
            ],
        ):
            with mock.patch.object(
                self.pc_feature,
                "get_status_paths",
                return_value=[
                    "docs/02-features/12-incremental-prd-to-features/dev-tasks.md"
                ],
            ):
                with mock.patch.object(
                    self.pc_feature, "branch_ahead_count", return_value=0
                ):
                    with self.assertRaises(SystemExit):
                        with contextlib.redirect_stderr(stderr_capture):
                            self.pc_feature.enforce_single_active_feature(
                                "/tmp/root",
                                "11-simplify-worktree-tracking",
                                "/tmp/current",
                            )
        self.assertIn(
            "another feature is already in progress", stderr_capture.getvalue()
        )

    def test_enforce_single_active_feature_allows_clean_other_patcher(self):
        with mock.patch.object(
            self.pc_feature,
            "list_worktree_entries",
            return_value=[
                (
                    "/tmp/current",
                    "feature-11-simplify-worktree-tracking-patcher",
                ),
                (
                    "/tmp/other",
                    "feature-12-incremental-prd-to-features-patcher",
                ),
            ],
        ):
            with mock.patch.object(
                self.pc_feature, "get_status_paths", return_value=[]
            ):
                with mock.patch.object(
                    self.pc_feature, "branch_ahead_count", return_value=0
                ):
                    self.pc_feature.enforce_single_active_feature(
                        "/tmp/root",
                        "11-simplify-worktree-tracking",
                        "/tmp/current",
                    )

    def test_parse_plan_reviewer_decision(self):
        self.assertEqual(
            self.pc_feature.parse_plan_reviewer_decision("Decision: Approve"),
            "APPROVE",
        )
        self.assertEqual(
            self.pc_feature.parse_plan_reviewer_decision("Decision: Block"),
            "BLOCK",
        )
        self.assertEqual(
            self.pc_feature.parse_plan_reviewer_decision("Decision: Conflict"),
            "CONFLICT",
        )
        self.assertEqual(
            self.pc_feature.parse_plan_reviewer_decision("Decision: conflict"),
            "CONFLICT",
        )
        self.assertEqual(
            self.pc_feature.parse_plan_reviewer_decision("unexpected output"),
            "BLOCK",
        )

    def test_parse_feedback_plan_decision(self):
        self.assertEqual(
            self.pc_feature.parse_feedback_plan_decision("Decision: PLAN_STILL_VALID"),
            "PLAN_STILL_VALID",
        )
        self.assertEqual(
            self.pc_feature.parse_feedback_plan_decision("Decision: REVISE_PLAN"),
            "REVISE_PLAN",
        )
        self.assertEqual(
            self.pc_feature.parse_feedback_plan_decision(
                "Decision: revised plan required"
            ),
            "REVISE_PLAN",
        )
        self.assertEqual(
            self.pc_feature.parse_feedback_plan_decision("unexpected output"),
            "REVISE_PLAN",
        )

    def test_locked_main_head_note_helpers(self):
        sha1 = "a" * 40
        sha2 = "b" * 40
        note = self.pc_feature.set_locked_main_head_note("", sha1)
        self.assertIn(sha1, note)
        self.assertEqual(self.pc_feature.parse_locked_main_head(note), sha1)
        updated = self.pc_feature.set_locked_main_head_note(note, sha2)
        self.assertIn(sha2, updated)
        self.assertEqual(self.pc_feature.parse_locked_main_head(updated), sha2)
        self.assertNotIn(sha1, updated)

    def test_main_fails_fast_when_locked_main_head_changes_on_resume(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-19"
            content = self._build_entry_content(work_item_id)
            locked = "a" * 40
            content = self.pc_feature.update_entry_field(
                content,
                work_item_id,
                "Notes",
                f"Main head locked: {locked}",
            )
            feature_dir = self._write_feature_workspace(root, content)
            stderr_capture = io.StringIO()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "git_ref_sha",
                        return_value="b" * 40,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "main branch moved during feature execution",
                stderr_capture.getvalue(),
            )

    def test_parse_escalation_request_supports_nested_payload(self):
        request = self.pc_feature.parse_escalation_request(
            '{"escalation_request":{"command":["git","status"],"reason":"need git output"}}'
        )
        self.assertIsNotNone(request)
        self.assertEqual(request["command"], ["git", "status"])

    def test_process_escalation_request_denies_disallowed_command(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.pc_feature.process_escalation_request(
                {"command": ["git", "reset", "--hard"], "reason": "unsafe"},
                root=tmp_dir,
                default_cwd=tmp_dir,
            )
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("not allowed", result["error"])

    def test_process_escalation_request_approves_and_dispatches_allowed_command(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.pc_feature.process_escalation_request(
                {"command": ["python3", "-m", "unittest", "-h"], "reason": "check cli"},
                root=tmp_dir,
                default_cwd=tmp_dir,
            )
        self.assertEqual(result["decision"], "APPROVE")
        self.assertIn("exit_code", result)

    def test_format_review_item_marks_failure(self):
        line = self.pc_feature.format_review_item("make feature F=01", 2)
        self.assertEqual(line, "make feature F=01: FAIL")

    def test_build_gates_block_uses_command(self):
        line = self.pc_feature.build_gates_block("make ci", "PASS")
        self.assertEqual(line, "- make ci: PASS")

    def test_run_command_with_step_log_writes_tests_log(self):
        metadata = build_metadata("WI-20260206-02", "pc-feature", "run-abc123")
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            exit_code = self.pc_feature.run_command_with_step_log(
                ["python3", "-c", "print('ok')"],
                metadata,
                step="tests",
                root=root,
                label="python smoke",
            )
            self.assertEqual(exit_code, 0)
            log_path = root / "logs" / "WI-20260206-02" / "tests.log"
            self.assertTrue(log_path.exists())
            content = log_path.read_text(encoding="utf-8")
            self.assertIn("[WI-20260206-02][pc-feature][tests]", content)
            self.assertIn("start python smoke", content)
            self.assertIn("complete python smoke: exit=0", content)

    def test_load_prompt_template_prefers_task_specific_then_fallback(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompts_dir = Path(tmp_dir)
            (prompts_dir / "planner.md").write_text(
                "fallback {work_item_id}\n", encoding="utf-8"
            )
            original_prompts_dir = self.pc_feature.PROMPTS_DIR
            self.pc_feature.PROMPTS_DIR = prompts_dir
            try:
                fallback = self.pc_feature.load_prompt_template("planner", "create")
                self.assertEqual(fallback, "fallback {work_item_id}\n")
                (prompts_dir / "planner-create.md").write_text(
                    "specific {work_item_id}\n",
                    encoding="utf-8",
                )
                specific = self.pc_feature.load_prompt_template("planner", "create")
                self.assertEqual(specific, "specific {work_item_id}\n")
            finally:
                self.pc_feature.PROMPTS_DIR = original_prompts_dir

    def test_render_prompt_template_substitutes_variables(self):
        rendered = self.pc_feature.render_prompt_template(
            "Work Item ID: {work_item_id}\nPlan:\n{plan}",
            {"work_item_id": "WI-20260206-01", "plan": "- test"},
        )
        self.assertEqual(rendered, "Work Item ID: WI-20260206-01\nPlan:\n- test")

    def test_load_prompt_template_missing_file_has_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            original_prompts_dir = self.pc_feature.PROMPTS_DIR
            self.pc_feature.PROMPTS_DIR = Path(tmp_dir)
            stderr_capture = io.StringIO()
            try:
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.load_prompt_template("planner", "create")
            finally:
                self.pc_feature.PROMPTS_DIR = original_prompts_dir
        message = stderr_capture.getvalue()
        self.assertIn("missing prompt template", message)
        self.assertIn("role=planner task=create", message)
        self.assertIn("prompts", message)
        self.assertIn("templates", message)
        self.assertIn("loads prompts from files only", message)

    def test_load_prompt_template_role_only_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompts_dir = Path(tmp_dir)
            (prompts_dir / "planner.md").write_text(
                "base {work_item_id}\n", encoding="utf-8"
            )
            original_prompts_dir = self.pc_feature.PROMPTS_DIR
            self.pc_feature.PROMPTS_DIR = prompts_dir
            try:
                rendered = self.pc_feature.load_prompt_template("planner")
                self.assertEqual(rendered, "base {work_item_id}\n")
            finally:
                self.pc_feature.PROMPTS_DIR = original_prompts_dir

    def test_load_prompt_template_missing_role_only_has_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            original_prompts_dir = self.pc_feature.PROMPTS_DIR
            self.pc_feature.PROMPTS_DIR = Path(tmp_dir)
            stderr_capture = io.StringIO()
            try:
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.load_prompt_template("planner")
            finally:
                self.pc_feature.PROMPTS_DIR = original_prompts_dir
        message = stderr_capture.getvalue()
        self.assertIn("missing prompt template", message)
        self.assertIn("role=planner", message)
        self.assertIn("remediation", message)

    def test_prompt_templates_match_prompt_inventory(self):
        prompts_dir = ROOT / "prompts"
        templates_dir = ROOT / "tools" / "templates" / "prompts"
        prompt_files = sorted(path.name for path in prompts_dir.glob("*.md"))
        template_files = sorted(path.name for path in templates_dir.glob("*.md"))
        self.assertEqual(prompt_files, template_files)

    def test_required_prompt_templates_exist(self):
        required = {
            "commit-message.md",
            "patcher-apply.md",
            "patcher-update_from_feedback.md",
            "patcher.md",
            "plan-reviewer-gate.md",
            "plan-reviewer.md",
            "planner-create.md",
            "planner-update-allowed-tests.md",
            "planner-update-from-feedback.md",
            "planner-update_from_feedback.md",
            "planner.md",
            "reporter-global-log.md",
            "reporter-review.md",
            "reporter.md",
            "tester.md",
        }
        prompts_dir = ROOT / "prompts"
        templates_dir = ROOT / "tools" / "templates" / "prompts"
        prompt_files = {path.name for path in prompts_dir.glob("*.md")}
        template_files = {path.name for path in templates_dir.glob("*.md")}
        for name in sorted(required):
            with self.subTest(name=name):
                self.assertIn(name, prompt_files)
                self.assertIn(name, template_files)

    def test_stage_scoped_final_paths_blocks_unrelated_dirty_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            stderr_capture = io.StringIO()
            with mock.patch.object(
                self.pc_feature,
                "get_status_paths",
                return_value=[
                    "docs/02-features/01-workflow-hardening/dev-tasks.md",
                    "README.md",
                ],
            ):
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.stage_scoped_final_paths(
                            str(root),
                            ["docs/02-features/01-workflow-hardening/dev-tasks.md"],
                        )
            self.assertIn(
                "unrelated dirty paths block final commit", stderr_capture.getvalue()
            )
            self.assertIn("README.md", stderr_capture.getvalue())

    def test_stage_scoped_final_paths_ignores_runtime_logs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            staged = []

            def fake_subprocess_run(cmd, **kwargs):
                staged.append(list(cmd))
                return SimpleNamespace(returncode=0, stdout="", stderr="")

            with mock.patch.object(
                self.pc_feature,
                "get_status_paths",
                return_value=[
                    "docs/02-features/01-workflow-hardening/dev-tasks.md",
                    "logs/WI-20260206-01/tests.log",
                    "logs/WI-20260206-01/ci.log",
                ],
            ):
                with mock.patch.object(
                    self.pc_feature.subprocess,
                    "run",
                    side_effect=fake_subprocess_run,
                ):
                    paths = self.pc_feature.stage_scoped_final_paths(
                        str(root),
                        ["docs/02-features/01-workflow-hardening/dev-tasks.md"],
                    )

            self.assertEqual(
                paths, ["docs/02-features/01-workflow-hardening/dev-tasks.md"]
            )
            self.assertEqual(
                staged,
                [
                    [
                        "git",
                        "add",
                        "--",
                        "docs/02-features/01-workflow-hardening/dev-tasks.md",
                    ]
                ],
            )

    def test_collect_allowed_final_stage_paths_includes_possible_improvements(self):
        with mock.patch.object(
            self.pc_feature,
            "collect_branch_merge_paths",
            return_value=["tools/pc-feature"],
        ):
            paths = self.pc_feature.collect_allowed_final_stage_paths(
                "/tmp/root",
                "refs/heads/main",
                "feature-branch",
                "docs/02-features/01-workflow-hardening/dev-tasks.md",
                "docs/02-features/01-workflow-hardening",
            )
        self.assertIn("docs/possible-improvements.md", paths)
        self.assertIn("tools/pc-feature", paths)
        self.assertIn(
            "docs/02-features/01-workflow-hardening/dev-tasks.md",
            paths,
        )

    def test_run_scoped_autofix_blocks_new_out_of_scope_touches(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            stderr_capture = io.StringIO()
            with mock.patch.object(self.pc_feature, "run_command", return_value=0):
                with mock.patch.object(
                    self.pc_feature,
                    "collect_dirty_snapshot",
                    side_effect=[
                        {
                            "docs/02-features/01-workflow-hardening/dev-tasks.md": "before"
                        },
                        {
                            "docs/02-features/01-workflow-hardening/dev-tasks.md": "after",
                            "README.md": "new",
                        },
                    ],
                ):
                    with self.assertRaises(SystemExit):
                        with contextlib.redirect_stderr(stderr_capture):
                            self.pc_feature.run_scoped_autofix(
                                str(root),
                                ["docs/02-features/01-workflow-hardening/dev-tasks.md"],
                            )
            self.assertIn(
                "scoped autofix touched out-of-scope files", stderr_capture.getvalue()
            )
            self.assertIn("README.md", stderr_capture.getvalue())

    def test_run_scoped_autofix_allows_preexisting_out_of_scope_dirty_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            scoped_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"
            with mock.patch.object(self.pc_feature, "run_command", return_value=0):
                with mock.patch.object(
                    self.pc_feature,
                    "collect_dirty_snapshot",
                    side_effect=[
                        {scoped_path: "before", "README.md": "steady"},
                        {scoped_path: "after", "README.md": "steady"},
                    ],
                ):
                    with mock.patch.object(
                        self.pc_feature.subprocess,
                        "run",
                        return_value=SimpleNamespace(
                            returncode=0, stdout="", stderr=""
                        ),
                    ) as add_mock:
                        status = self.pc_feature.run_scoped_autofix(
                            str(root), [scoped_path]
                        )
        self.assertEqual(status, 0)
        add_mock.assert_called_once()

    def test_main_manual_mode_prints_feature_status_hints_when_tracking_enabled(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-15"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            stdout_capture = io.StringIO()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "parse_args", return_value=("01", True)
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature.pc_runner,
                        "build_metadata",
                        return_value=self.pc_feature.pc_runner.RunMetadata(
                            work_item_id, "pc-feature", "run123"
                        ),
                    )
                )
                with contextlib.redirect_stdout(stdout_capture):
                    self.pc_feature.main()

            output = stdout_capture.getvalue()
            self.assertIn(
                f"`make feature-status WI={work_item_id} FOLLOW=1`",
                output,
            )
            self.assertIn(
                f"`make feature-status WI={work_item_id} HISTORY=1 LIMIT=30`",
                output,
            )

    def test_main_resumes_newest_in_progress_work_item(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            newest = "WI-20260206-02"
            older = "WI-20260206-01"
            content = "## Execution Log\n\n"
            content += self.pc_feature.build_execution_entry(newest) + "\n"
            content += self.pc_feature.build_execution_entry(older)
            feature_dir = self._write_feature_workspace(root, content)
            selected = {}

            def capture_allowed(content: str, work_item_id: str) -> str:
                selected["work_item_id"] = work_item_id
                raise StopMain()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=capture_allowed,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()
            self.assertEqual(selected.get("work_item_id"), newest)

    def test_main_startup_checkpoints_dirty_dev_tasks_for_in_progress_item(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260209-01"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            dev_tasks_repo_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"
            checkpoint_mock = mock.Mock(return_value=[dev_tasks_repo_path])

            def stop_after_precheck(content: str, work_item_id: str) -> str:
                raise StopMain()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "get_status_paths",
                        side_effect=[
                            [dev_tasks_repo_path],
                            [],
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "checkpoint_resume_state",
                        checkpoint_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=stop_after_precheck,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            checkpoint_mock.assert_called_once_with(
                str(patcher_path),
                work_item_id,
                feature_slug="01-workflow-hardening",
            )

    def test_main_startup_checkpoints_dirty_dev_tasks_without_resume_item(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260209-02"
            content = self._build_entry_content(work_item_id, outcome="pass")
            feature_dir = self._write_feature_workspace(root, content)
            dev_tasks_repo_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"
            checkpoint_mock = mock.Mock(return_value=[dev_tasks_repo_path])

            def stop_after_precheck(content: str, work_item_id: str) -> str:
                raise StopMain()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "get_status_paths",
                        side_effect=[
                            [dev_tasks_repo_path],
                            [],
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "checkpoint_resume_state",
                        checkpoint_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=stop_after_precheck,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            checkpoint_mock.assert_called_once_with(
                str(patcher_path),
                None,
                feature_slug="01-workflow-hardening",
            )

    def test_main_dirty_existing_worktree_auto_resume_preserves_state(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            work_item_id = "WI-20260206-07"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            remove_worktree_mock = mock.Mock()
            prepare_worktree_mock = mock.Mock(
                return_value=(str(patcher_path), "patcher-branch")
            )
            print_mock = mock.Mock()
            reached_after_precheck = {"value": False}

            def stop_after_precheck(content: str, work_item_id: str) -> str:
                reached_after_precheck["value"] = True
                raise StopMain()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "branch_ahead_count",
                        return_value=1,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_resume_mode",
                        return_value="auto",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "prepare_worktree",
                        prepare_worktree_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "remove_worktree",
                        remove_worktree_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=stop_after_precheck,
                    )
                )
                stack.enter_context(mock.patch("builtins.print", print_mock))
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            remove_worktree_mock.assert_not_called()
            self.assertTrue(reached_after_precheck["value"])
            self.assertTrue(
                any(
                    "existing patcher worktree is not pristine" in str(call.args[0])
                    for call in print_mock.call_args_list
                )
            )
            self.assertTrue(
                any(
                    "auto-resume enabled" in str(call.args[0])
                    for call in print_mock.call_args_list
                )
            )

    def test_main_stale_existing_worktree_auto_mode_fails(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            work_item_id = "WI-20260212-01"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            stderr_capture = io.StringIO()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_resume_mode",
                        return_value="auto",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "branch_behind_count",
                        return_value=1,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "existing patcher worktree is stale (behind main)",
                stderr_capture.getvalue(),
            )

    def test_main_stale_existing_worktree_sync_mode_merges_and_continues(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            work_item_id = "WI-20260212-02"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            checkpoint_mock = mock.Mock(
                return_value=[
                    "docs/02-features/01-workflow-hardening/dev-tasks.md",
                ]
            )
            merge_mock = mock.Mock(return_value=(True, "merge ok"))

            behind_values = iter([1, 0])

            def behind_side_effect(*args, **kwargs):
                try:
                    return next(behind_values)
                except StopIteration:
                    return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_resume_mode",
                        return_value="sync",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "branch_behind_count",
                        side_effect=behind_side_effect,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "checkpoint_resume_state",
                        checkpoint_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "merge_main_into_worktree",
                        merge_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=StopMain,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            checkpoint_mock.assert_called_once_with(
                str(patcher_path),
                None,
                feature_slug="01-workflow-hardening",
            )
            merge_mock.assert_called_once_with(str(patcher_path), "refs/heads/main")

    def test_main_stale_existing_worktree_sync_mode_merge_failure_blocks(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            work_item_id = "WI-20260212-04"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            stderr_capture = io.StringIO()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_resume_mode",
                        return_value="sync",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "branch_behind_count",
                        return_value=1,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "merge_main_into_worktree",
                        return_value=(False, "conflict"),
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "failed to sync stale patcher worktree with main",
                stderr_capture.getvalue(),
            )

    def test_main_sync_mode_refreshes_locked_main_head_after_stale_sync(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            work_item_id = "WI-20260212-03"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.update_entry_field(
                content,
                work_item_id,
                "Notes",
                f"Main head locked: {'a' * 40}",
            )
            feature_dir = self._write_feature_workspace(root, content)

            behind_values = iter([1, 0])

            def behind_side_effect(*args, **kwargs):
                try:
                    return next(behind_values)
                except StopIteration:
                    return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_resume_mode",
                        return_value="sync",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "branch_behind_count",
                        side_effect=behind_side_effect,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "merge_main_into_worktree",
                        return_value=(True, "merge ok"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "git_ref_sha",
                        return_value="b" * 40,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_root_start_scope",
                        side_effect=StopMain,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("Main head locked: " + ("b" * 40), dev_tasks)
            self.assertNotIn("Main head locked: " + ("a" * 40), dev_tasks)

    def test_main_existing_worktree_non_runtime_dirty_is_checkpointed(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            work_item_id = "WI-20260206-08"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            remove_worktree_mock = mock.Mock()
            prepare_worktree_mock = mock.Mock(
                return_value=(str(patcher_path), "patcher-branch")
            )
            checkpoint_mock = mock.Mock(return_value=["README.md"])

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "get_status_paths",
                        side_effect=[
                            ["README.md"],
                            ["README.md"],
                            [],
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "prepare_worktree",
                        prepare_worktree_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "remove_worktree",
                        remove_worktree_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "checkpoint_resume_state",
                        checkpoint_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=StopMain,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            remove_worktree_mock.assert_not_called()
            prepare_worktree_mock.assert_called_once()
            checkpoint_mock.assert_called_once_with(
                str(patcher_path),
                work_item_id,
                feature_slug="01-workflow-hardening",
            )

    def test_main_fresh_mode_ignores_resume_item_and_starts_new_work_item(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            (patcher_path / ".git").write_text("gitdir: /tmp/fake\n", encoding="utf-8")
            existing_work_item = "WI-20260211-01"
            content = self._build_entry_content(existing_work_item)
            feature_dir = self._write_feature_workspace(root, content)
            selected = {}
            next_work_item_id = "WI-20990101-01"

            def capture_allowed(content: str, work_item_id: str) -> str:
                selected["work_item_id"] = work_item_id
                raise StopMain()

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_resume_mode",
                        return_value="fresh",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "next_work_item_id",
                        return_value=next_work_item_id,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_allowed_tests_section",
                        side_effect=capture_allowed,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(selected.get("work_item_id"), next_work_item_id)

    def test_allowed_tests_run_in_worktree_cwd(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-03"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            captured = {}
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_run_with_step_log_capture(
                cmd,
                metadata,
                *,
                step,
                root,
                label,
                **kwargs,
            ):
                if step == "tests":
                    captured["cwd"] = kwargs.get("cwd")
                    raise StopMain()
                return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        side_effect=fake_run_with_step_log_capture,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        return_value="Decision: Approve\nReasons:\n- clear",
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()
            self.assertEqual(captured.get("cwd"), str(patcher_path))

    def test_plan_reviewer_uses_plan_reviewer_profile(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-03"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            captured = {"profile": None}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    captured["profile"] = kwargs.get("profile")
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(captured.get("profile"), "PlanReviewer")

    def test_prepatch_smoke_runs_in_worktree_cwd(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-09"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            captured = {}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    raise StopMain()
                return True

            def fake_run_command(cmd, cwd=None):
                if cmd and cmd[0] == "tools/offload-proxy/pp":
                    captured["cwd"] = cwd
                return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command",
                        side_effect=fake_run_command,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        return_value="Decision: Approve\nReasons:\n- clear",
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(captured.get("cwd"), str(patcher_path))

    def test_main_fails_when_allowed_tests_remain_invalid_after_planner_retries(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-15"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section == "Preflight Report":
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Planner agent." in prompt and "Allowed Tests" in prompt:
                    return ""
                if "You are the Planner agent. Provide a concise plan" in prompt:
                    return "- initial plan"
                return "Decision: Approve\nReasons:\n- clear"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "check_allowed_tests_exist",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "codex_exec", side_effect=fake_codex_exec
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "max tester retry attempts reached",
                stderr_capture.getvalue(),
            )
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertNotIn("SMOKE_TEST_REQUIRED", dev_tasks)
            self.assertIn("allowed-tests validation failed", dev_tasks)
            self.assertIn(
                "plan-reviewer no-op; reason=blocked by invalid allowed tests",
                dev_tasks,
            )
            self.assertIn(
                "patcher no-op; reason=blocked by invalid allowed tests", dev_tasks
            )
            self.assertIn(
                "reporter no-op; reason=blocked by invalid allowed tests", dev_tasks
            )

    def test_main_discards_allowed_tests_side_effect_files(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260209-03"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "Allowed Tests must list specific, meaningful" in prompt:
                    return (
                        "- `python -m unittest tests.test_pc_feature`\n"
                        "**Patch**\n"
                        "- Updated docs/03-logs/implementation-log.md\n"
                    )
                if "You are the Plan Reviewer agent." in prompt:
                    raise StopMain()
                return "Decision: Approve\nReasons:\n- clear"

            restore_mock = mock.Mock(return_value=None)
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "ensure_plan_reviewer_read_only",
                        side_effect=[
                            ([], ["docs/03-logs/implementation-log.md"]),
                            ([], []),
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "restore_dirty_paths",
                        restore_mock,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            restore_mock.assert_called_once_with(
                str(patcher_path), ["docs/03-logs/implementation-log.md"]
            )
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("`python -m unittest tests.test_pc_feature`", dev_tasks)
            self.assertNotIn("**Patch**", dev_tasks)

    def test_reporter_is_skipped_when_tester_fails(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-18"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reporter_prompt_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "Review changes for scope and completeness" in prompt:
                    reporter_prompt_calls["count"] += 1
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: should not run on tester fail"
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    raise StopMain()
                return "ok"

            def fake_run_with_step_log(
                cmd,
                metadata,
                *,
                step,
                root,
                label,
                **kwargs,
            ):
                if step == "tests":
                    return 1
                return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        side_effect=fake_run_with_step_log,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reporter_prompt_calls["count"], 0)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("reporter no-op; reason=tester failed", dev_tasks)

    def test_pre_reporter_completeness_gate_blocks_reporter_prompt(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-20"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reporter_prompt_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_handoff_issues(
                content: str, wi_id: str, *, require_reporter_review: bool
            ):
                if require_reporter_review:
                    return []
                return ["Patch section still contains pending placeholders"]

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "Review changes for scope and completeness" in prompt:
                    reporter_prompt_calls["count"] += 1
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: should not run"
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        return_value=(0, "OK"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "execution_handoff_completeness_issues",
                        side_effect=fake_handoff_issues,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reporter_prompt_calls["count"], 0)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "Reporter blocked by pre-handoff completeness gate", dev_tasks
            )

    def test_reporter_commit_happens_before_runtime_reconciliation_write(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-34"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reporter_commit_calls = {"count": 0}
            reporter_review_pending_at_commit = {"value": None}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "Review changes for scope and completeness" in prompt:
                    return (
                        "Outcome: PASS\n"
                        "Docs/logs updated: docs/02-features/01-workflow-hardening/reporter-log.md\n"
                        "Notes: approved\n"
                    )
                return "ok"

            def fake_commit_role_step(
                root_path: str,
                worktree_path: str,
                branch: str,
                role: str,
                work_item: str,
                feature_path: str,
                *,
                allow_empty: bool = False,
            ) -> bool:
                if role == "reporter":
                    reporter_commit_calls["count"] += 1
                    reporter_text = self._worktree_dev_tasks(patcher_path).read_text(
                        encoding="utf-8"
                    )
                    reporter_review_pending_at_commit["value"] = (
                        "#### Reporter Review\n\n- (pending)" in reporter_text
                    )
                    raise StopMain()
                return False

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        return_value=(0, "OK"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "commit_role_step",
                        side_effect=fake_commit_role_step,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reporter_commit_calls["count"], 1)
            self.assertTrue(reporter_review_pending_at_commit["value"])

    def test_finalization_only_reporter_fail_is_normalized_before_retry_loop(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-35"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            planner_feedback_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "Review changes for scope and completeness" in prompt:
                    return (
                        "Outcome: FAIL\n"
                        "Docs/logs updated: docs/02-features/01-workflow-hardening/reporter-log.md\n"
                        "File/Path: docs/02-features/01-workflow-hardening/dev-tasks.md\n"
                        "Check: Final execution summary completeness.\n"
                        "Evidence: Commit message is empty and Final Report still says No runs yet.\n"
                        "Expected fix: Fill Commit message and Final Report after final gates.\n"
                        "Notes: finalization placeholders only.\n"
                    )
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    planner_feedback_calls["count"] += 1
                    return "Decision: PLAN_STILL_VALID\nRationale: should not trigger\n"
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        return_value=(0, "OK"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        side_effect=StopMain(),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(planner_feedback_calls["count"], 0)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "Reporter finalization-only FAIL normalized to PASS",
                dev_tasks,
            )

    def test_is_finalization_only_reporter_failure_classifier(self):
        finalization_only_feedback = (
            "Outcome: FAIL\n"
            "Docs/logs updated: reporter-log.md\n"
            "Check: Final execution summary completeness.\n"
            "Evidence: Commit message is empty and Final Report still says No runs yet.\n"
            "Expected fix: Fill Commit message and Final Report after final gates.\n"
        )
        self.assertTrue(
            self.pc_feature.is_finalization_only_reporter_failure(
                finalization_only_feedback
            )
        )

        handoff_feedback = (
            "Outcome: FAIL\n"
            "Docs/logs updated: reporter-log.md\n"
            "Check: Reporter handoff completeness.\n"
            "Evidence: Reporter Review is still pending.\n"
            "Expected fix: Populate Reporter Review section.\n"
        )
        self.assertFalse(
            self.pc_feature.is_finalization_only_reporter_failure(handoff_feedback)
        )

    def test_post_reporter_gate_blocks_pass_when_compacted_outputs_missing(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-21"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reporter_prompt_calls = {"count": 0}
            missing_path = "docs/03-logs/compacted/decision-log-compact.md"

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "Review changes for scope and completeness" in prompt:
                    reporter_prompt_calls["count"] += 1
                    return "Outcome: PASS\nDocs/logs updated: docs/03-logs/implementation-log.md\nNotes: approved"
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        return_value=(0, "OK"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "execution_handoff_completeness_issues",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "required_compacted_output_paths",
                        return_value=[missing_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "missing_compacted_output_paths",
                        return_value=[missing_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "reporter_traceability_issues",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reporter_prompt_calls["count"], 1)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "Reporter PASS blocked by post-review completeness gate", dev_tasks
            )
            self.assertIn("required compacted output missing", dev_tasks)

    def test_commit_evidence_gate_passes_when_required_evidence_present(self):
        work_item_id = "WI-20260212-40"
        content = self._build_commit_gate_ready_content(work_item_id)
        issues = self.pc_feature.commit_evidence_gate_issues(content, work_item_id)
        self.assertEqual(issues, [])

    def test_commit_evidence_gate_fails_when_tests_run_field_missing(self):
        work_item_id = "WI-20260212-41"
        content = self._build_commit_gate_ready_content(work_item_id)
        content = self.pc_feature.update_entry_field(
            content, work_item_id, "Tests run", ""
        )
        issues = self.pc_feature.commit_evidence_gate_issues(content, work_item_id)
        self.assertIn("missing top execution field: Tests run", issues)

    def test_commit_evidence_gate_fails_when_final_report_fields_missing(self):
        work_item_id = "WI-20260212-42"
        content = self._build_commit_gate_ready_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content,
            work_item_id,
            "Final Report",
            (
                "What changed (files): docs and tooling updated\n"
                "make ci results: PASS\n"
                "Commit message: chore(workflow): finalize documentation gate"
            ),
        )
        issues = self.pc_feature.commit_evidence_gate_issues(content, work_item_id)
        self.assertIn(
            "Final Report is missing required field: Tests written (names) + results",
            issues,
        )
        self.assertIn(
            "Final Report is missing required field: Docs/logs updated checklist",
            issues,
        )
        self.assertIn(
            "Final Report is missing required field: Commands run (use pp for noisy output)",
            issues,
        )

    def test_commit_evidence_gate_fails_on_duplicate_headings(self):
        work_item_id = "WI-20260212-43"
        content = self._build_commit_gate_ready_content(work_item_id)
        content = content.replace(
            "#### Final Report\n\n",
            "#### Final Report\n\n- duplicate body\n\n#### Final Report\n\n",
            1,
        )
        issues = self.pc_feature.commit_evidence_gate_issues(content, work_item_id)
        self.assertIn("duplicate required section heading: Final Report", issues)

    def test_commit_evidence_gate_fails_on_empty_required_body(self):
        work_item_id = "WI-20260212-44"
        content = self._build_commit_gate_ready_content(work_item_id)
        content = self.pc_feature.replace_entry_section(
            content, work_item_id, "Test Results", ""
        )
        issues = self.pc_feature.commit_evidence_gate_issues(content, work_item_id)
        self.assertIn("required section is empty: Test Results", issues)

    def test_ticket_status_completion_matrix_is_deterministic(self):
        fixtures = [
            ("completed-lower", "completed", True),
            ("completed-upper-whitespace", "  COMPLETED  ", True),
            ("pass-mixed-case", " PaSs ", True),
            ("non-completed-ongoing", "Ongoing", False),
            ("non-completed-awaiting-approval", "Awaiting PO Approval", False),
            ("missing", "", False),
            ("whitespace-only", "   ", False),
        ]
        first_pass = []
        second_pass = []
        for fixture_name, raw_status, expected in fixtures:
            with self.subTest(fixture=fixture_name):
                result = self.pc_feature_status.ticket_status_is_completed(raw_status)
                self.assertEqual(result, expected)
                first_pass.append((fixture_name, result))
        for fixture_name, raw_status, expected in fixtures:
            with self.subTest(fixture=f"{fixture_name}-rerun"):
                result = self.pc_feature_status.ticket_status_is_completed(raw_status)
                self.assertEqual(result, expected)
                second_pass.append((fixture_name, result))
        self.assertEqual(first_pass, second_pass)

    def test_ticket_status_normalization_contract_boundaries(self):
        fixtures = [
            (
                "collapsed_whitespace",
                "  Awaiting   PO   Approval ",
                "awaiting po approval",
            ),
            ("simple_completed", "Completed", "completed"),
            ("empty", "", ""),
        ]
        for fixture_name, raw_status, expected in fixtures:
            with self.subTest(fixture=fixture_name):
                self.assertEqual(
                    self.pc_feature_status.normalize_ticket_status(raw_status), expected
                )

    def test_commit_evidence_gate_fails_closed_on_malformed_required_section(self):
        work_item_id = "WI-20260212-45"
        content = self._build_commit_gate_ready_content(work_item_id)
        content = content.replace("#### Final Report", "### Final Report", 1)
        issues = self.pc_feature.commit_evidence_gate_issues(content, work_item_id)
        self.assertIn("missing required section: Final Report", issues)

    def test_main_does_not_write_feature_worktree_manifest(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-04"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            manifest_path = feature_dir / "feature-worktrees.json"

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section == "Preflight Report":
                    return True
                if section == "Plan":
                    raise StopMain()
                return True

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()
            self.assertFalse(manifest_path.exists())

    def test_main_prepares_worktree_before_first_dev_tasks_write(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            feature_dir = self._write_feature_workspace(root, "## Execution Log\n\n")
            events = []
            original_write_file = self.pc_feature.write_file
            dev_tasks_suffix = "docs/02-features/01-workflow-hardening/dev-tasks.md"

            def fake_prepare_worktree(*args, **kwargs):
                events.append("prepare")
                return (str(patcher_path), "patcher-branch")

            def fake_write_file(path: str, content: str):
                if path.endswith(dev_tasks_suffix):
                    events.append("devtasks-write")
                    raise StopMain()
                return original_write_file(path, content)

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "prepare_worktree",
                        side_effect=fake_prepare_worktree,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "write_file", side_effect=fake_write_file
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertIn("prepare", events)
            self.assertIn("devtasks-write", events)
            self.assertLess(events.index("prepare"), events.index("devtasks-write"))

    def test_main_avoids_git_add_all_for_final_staging(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-05"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            git_commands = []

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "Review changes for scope and completeness" in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: ok"
                if "Provide short, single-line summaries for global logs" in prompt:
                    return (
                        '{"implementation_log":"none","validation_log":"none",'
                        '"decision_log":"none"}'
                    )
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "generating a concise, scoped commit message" in prompt:
                    return "workflow: finalize scoped changes"
                return "ok"

            def fake_run_command_with_step_log_capture(*args, **kwargs):
                cmd = args[0] if args else []
                git_commands.append(list(cmd))
                return (0, "")

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        return_value=0,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "codex_exec", side_effect=fake_codex_exec
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_allowed_final_stage_paths",
                        return_value=[
                            "docs/02-features/01-workflow-hardening/dev-tasks.md"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "stage_scoped_final_paths",
                        return_value=[
                            "docs/02-features/01-workflow-hardening/dev-tasks.md"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        side_effect=fake_run_command_with_step_log_capture,
                    )
                )
                self.pc_feature.main()
            self.assertNotIn(["git", "add", "-A"], git_commands)
            self.assertFalse(
                any(cmd[:2] == ["git", "commit"] for cmd in git_commands),
                "pc-feature should not call git commit directly",
            )
            self.assertTrue(
                any(cmd and cmd[0] == "tools/pc-commit" for cmd in git_commands),
                "pc-feature should call tools/pc-commit for final commit",
            )
            pc_commit_cmds = [
                cmd for cmd in git_commands if cmd and cmd[0] == "tools/pc-commit"
            ]
            self.assertTrue(pc_commit_cmds)
            allow_values = [
                pc_commit_cmds[0][idx + 1]
                for idx, token in enumerate(pc_commit_cmds[0][:-1])
                if token == "--allow"
            ]
            self.assertIn("logs", allow_values)
            self.assertIn("--work-item-id", pc_commit_cmds[0])
            wi_idx = pc_commit_cmds[0].index("--work-item-id")
            self.assertEqual(pc_commit_cmds[0][wi_idx + 1], work_item_id)

    def test_main_commit_failure_surfaces_pc_commit_detail(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-05"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "Review changes for scope and completeness" in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: ok"
                if "Provide short, single-line summaries for global logs" in prompt:
                    return (
                        '{"implementation_log":"none","validation_log":"none",'
                        '"decision_log":"none"}'
                    )
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "generating a concise, scoped commit message" in prompt:
                    return "workflow: finalize scoped changes"
                return "ok"

            def fake_run_command_with_step_log_capture(*args, **kwargs):
                cmd = args[0] if args else []
                if cmd and cmd[0] == "tools/pc-commit":
                    return (1, "fatal: pathspec '.tmp' did not match any files\n")
                return (0, "")

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        return_value=0,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "codex_exec", side_effect=fake_codex_exec
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_allowed_final_stage_paths",
                        return_value=[
                            "docs/02-features/01-workflow-hardening/dev-tasks.md"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "stage_scoped_final_paths",
                        return_value=[
                            "docs/02-features/01-workflow-hardening/dev-tasks.md"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        side_effect=fake_run_command_with_step_log_capture,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stdout(stdout_capture):
                        with contextlib.redirect_stderr(stderr_capture):
                            self.pc_feature.main()

            self.assertIn("COMMIT FAIL", stdout_capture.getvalue())
            self.assertIn(
                "detail=fatal: pathspec '.tmp' did not match any files",
                stdout_capture.getvalue(),
            )
            self.assertIn(
                (
                    "pc-feature: failed to commit collected changes via tools/pc-commit; "
                    "detail=fatal: pathspec '.tmp' did not match any files"
                ),
                stderr_capture.getvalue(),
            )

    def test_extract_command_failure_detail_prefers_gate_marker_over_noise(self):
        output = "\n".join(
            [
                "pc-feature: requested feature id=01; resolved feature=01-workflow-hardening",
                "........................................................",
                "Commit evidence gate failed:",
                "docs/.../dev-tasks.md [WI-20260212-01]: active ticket status is not completed",
            ]
        )
        detail = self.pc_feature.extract_command_failure_detail(output)
        self.assertEqual(detail, "Commit evidence gate failed:")

    def test_main_skips_commit_generation_if_commit_section_already_filled(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-06"
            content = self._build_entry_content(
                work_item_id,
                commit_message="existing scoped message",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "Review changes for scope and completeness" in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: ok"
                if "Provide short, single-line summaries for global logs" in prompt:
                    return (
                        '{"implementation_log":"none","validation_log":"none",'
                        '"decision_log":"none"}'
                    )
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "generating a concise, scoped commit message" in prompt:
                    return "unexpected generated message"
                return "ok"

            codex_exec_mock = mock.Mock(side_effect=fake_codex_exec)

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        return_value=0,
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "codex_exec", codex_exec_mock)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature.subprocess,
                        "run",
                        return_value=SimpleNamespace(
                            returncode=0, stdout="", stderr=""
                        ),
                    )
                )
                self.pc_feature.main()

            commit_prompts = [
                call
                for call in codex_exec_mock.call_args_list
                if "generating a concise, scoped commit message" in call.args[0]
            ]
            self.assertEqual(commit_prompts, [])

    def test_main_repairs_reporter_global_json_before_appending_logs(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-11"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            prompt_counts = {"global": 0, "repair": 0}
            append_calls = []

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "Review changes for scope and completeness" in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: ok"
                if "Provide short, single-line summaries for global logs" in prompt:
                    prompt_counts["global"] += 1
                    return "Need a feature id and log scope before I can proceed."
                if "Convert the raw output below into strict JSON." in prompt:
                    prompt_counts["repair"] += 1
                    return (
                        '{"implementation_log":"impl from repair",'
                        '"validation_log":"val from repair","decision_log":"none"}'
                    )
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "generating a concise, scoped commit message" in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        return_value=0,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_allowed_final_stage_paths",
                        return_value=[
                            "docs/02-features/01-workflow-hardening/dev-tasks.md"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "append_log_line",
                        side_effect=lambda path, line: append_calls.append(
                            (path, line)
                        ),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(prompt_counts["global"], 1)
            self.assertEqual(prompt_counts["repair"], 1)
            self.assertIn(
                ("docs/03-logs/implementation-log.md", "impl from repair"),
                append_calls,
            )
            self.assertIn(
                ("docs/03-logs/validation-log.md", "val from repair"),
                append_calls,
            )
            self.assertNotIn(
                ("docs/03-logs/decision-log.md", "none"),
                append_calls,
            )

    def test_main_uses_deterministic_global_logs_when_json_unrecoverable(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-12"
            content = self._build_entry_content(work_item_id)
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            prompt_counts = {"global": 0, "repair": 0}
            append_calls = []

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "Review changes for scope and completeness" in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: ok"
                if "Provide short, single-line summaries for global logs" in prompt:
                    prompt_counts["global"] += 1
                    return "Need a feature id and log scope before I can proceed."
                if "Convert the raw output below into strict JSON." in prompt:
                    prompt_counts["repair"] += 1
                    return "still not valid json"
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "generating a concise, scoped commit message" in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        return_value=0,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_allowed_final_stage_paths",
                        return_value=[
                            "docs/02-features/01-workflow-hardening/dev-tasks.md"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "append_log_line",
                        side_effect=lambda path, line: append_calls.append(
                            (path, line)
                        ),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            fallback = self.pc_feature.deterministic_global_log_payload(
                work_item_id, False
            )
            self.assertEqual(prompt_counts["global"], 1)
            self.assertEqual(prompt_counts["repair"], 1)
            self.assertIn(
                (
                    "docs/03-logs/implementation-log.md",
                    fallback["implementation_log"],
                ),
                append_calls,
            )
            self.assertIn(
                (
                    "docs/03-logs/validation-log.md",
                    fallback["validation_log"],
                ),
                append_calls,
            )
            self.assertFalse(
                any(path == "docs/03-logs/decision-log.md" for path, _ in append_calls)
            )

    def test_deterministic_global_log_payload_uses_requires_global_logs_flag(self):
        false_payload = self.pc_feature.deterministic_global_log_payload(
            "WI-20260206-99", False
        )
        true_payload = self.pc_feature.deterministic_global_log_payload(
            "WI-20260206-99", True
        )

        self.assertEqual(false_payload["decision_log"], "none")
        self.assertNotEqual(
            false_payload["implementation_log"], true_payload["implementation_log"]
        )
        self.assertNotEqual(
            false_payload["validation_log"], true_payload["validation_log"]
        )
        self.assertIn("Process docs changed", true_payload["decision_log"])

    def test_ci_gate_runs_make_ci_once_when_first_attempt_passes(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-13"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            ci_attempts = {"count": 0}
            scoped_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "Provide short, single-line summaries for global logs" in prompt:
                    raise StopMain()
                if "You are the Reporter agent." in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: done"
                return "ok"

            def fake_run_with_step_log(
                cmd,
                metadata,
                *,
                step,
                root,
                label,
                **kwargs,
            ):
                if step == "tests":
                    return 0
                if step == "ci":
                    ci_attempts["count"] += 1
                    return 0
                return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        side_effect=fake_run_with_step_log,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_allowed_final_stage_paths",
                        return_value=[scoped_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(ci_attempts["count"], 1)

    def test_ci_gate_retries_once_after_autofix(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-14"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            ci_attempts = {"count": 0}
            autofix_calls = {"count": 0}
            ci_cwds = []
            scoped_path = "tools/pc-feature"
            forbidden_autofix_path = (
                "docs/02-features/01-workflow-hardening/dev-tasks.md"
            )

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "You are the Reporter agent." in prompt:
                    return "Outcome: PASS\nDocs/logs updated: ok\nNotes: done"
                return "ok"

            def fake_run_command(cmd, cwd=None):
                if cmd[:4] == [
                    "tools/offload-proxy/pp",
                    "pre-commit",
                    "run",
                    "--files",
                ]:
                    self.assertNotIn("--all-files", cmd)
                    self.assertIn(scoped_path, cmd)
                    self.assertNotIn(forbidden_autofix_path, cmd)
                    autofix_calls["count"] += 1
                return 0

            def fake_run_with_step_log(
                cmd,
                metadata,
                *,
                step,
                root,
                label,
                **kwargs,
            ):
                if step == "tests":
                    return 0
                if step == "ci":
                    ci_attempts["count"] += 1
                    ci_cwds.append(kwargs.get("cwd"))
                    if ci_attempts["count"] == 1:
                        return 1
                    if ci_attempts["count"] == 2:
                        return 1
                    self.fail("ci should not run more than 2 attempts")
                return 0

            stderr_capture = io.StringIO()
            collect_mock = mock.Mock(
                return_value={
                    "applied_paths": [scoped_path],
                    "skipped_paths": [],
                    "conflict_paths": [],
                }
            )
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "branch_ahead_count", return_value=1
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command",
                        side_effect=fake_run_command,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        side_effect=fake_run_with_step_log,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_branch_merge_paths",
                        return_value=[forbidden_autofix_path, scoped_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_branch_into_main",
                        collect_mock,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_allowed_final_stage_paths",
                        return_value=[scoped_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "stage_scoped_final_paths",
                        return_value=[scoped_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "get_staged_paths",
                        return_value=[scoped_path],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature.subprocess,
                        "run",
                        return_value=SimpleNamespace(
                            returncode=0, stdout="", stderr=""
                        ),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertEqual(ci_attempts["count"], 2)
            self.assertEqual(ci_cwds, [str(patcher_path), str(patcher_path)])
            self.assertEqual(autofix_calls["count"], 1)
            collect_mock.assert_not_called()
            self.assertIn("max attempts: 2", stderr_capture.getvalue())

    def test_plan_reviewer_block_routes_back_to_planner_before_patch(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-10"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}
            append_role_log_mock = mock.Mock()

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    if reviewer_calls["count"] == 1:
                        return "Decision: Block\nReasons:\n- missing checks"
                    return "Decision: Approve\nReasons:\n- looks good"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return "- revised plan after review feedback"
                if "You are the Patcher agent." in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "append_role_log", append_role_log_mock
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertGreaterEqual(reviewer_calls["count"], 2)
            self.assertEqual(planner_update_calls["count"], 1)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("Plan Reviewer BLOCK; planner updated plan", dev_tasks)
            self.assertTrue(append_role_log_mock.called)

    def test_plan_reviewer_approve_allows_patch(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-11"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    return "Decision: Approve\nReasons:\n- clear"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return "- should not be called"
                if "You are the Patcher agent." in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reviewer_calls["count"], 1)
            self.assertEqual(planner_update_calls["count"], 0)

    def test_plan_reviewer_conflict_halts_before_patch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-12"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return (
                        "Decision: Conflict\n"
                        "Reasons:\n- conflicting requirements\n"
                        "Required changes:\n- reconcile scope"
                    )
                if "You are the Patcher agent." in prompt:
                    raise AssertionError("patcher should not run on conflict")
                return "ok"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn("plan reviewer conflict", stderr_capture.getvalue())
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("Plan reviewer conflict", dev_tasks)

    def test_plan_reviewer_conflict_case_insensitive(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-13"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: conflict\nReasons:\n- unclear"
                return "ok"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn("plan reviewer conflict", stderr_capture.getvalue())

    def test_plan_reviewer_block_high_risk_routes_back_to_planner(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-13"
            content = self._build_entry_content(work_item_id)
            plan_text = (
                "- Approach: fixture coverage >=2 fixtures per critical path; "
                "deterministic seed strategy; invariant checks; contract boundary coverage."
            )
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", plan_text
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            preflight_block = self.pc_feature.build_preflight_block(
                {"files_to_change": []},
                work_item_id,
                "HIGH",
                ["touches secret blocking or fail-close behavior"],
            )
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Preflight Report", preflight_block
            )
            content = self.pc_feature.update_entry_field(
                content,
                work_item_id,
                "Notes",
                self.pc_feature.HIGH_RISK_APPROVAL_NOTE,
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}
            append_role_log_mock = mock.Mock()

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    if reviewer_calls["count"] == 1:
                        return "Decision: Block\nReasons:\n- missing checks"
                    return "Decision: Approve\nReasons:\n- looks good"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return "- revised plan after review feedback"
                if "You are the Patcher agent." in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature, "append_role_log", append_role_log_mock
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertGreaterEqual(reviewer_calls["count"], 2)
            self.assertEqual(planner_update_calls["count"], 1)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("Plan Reviewer BLOCK; planner updated plan", dev_tasks)
            self.assertTrue(append_role_log_mock.called)

    def test_plan_reviewer_approve_high_risk_allows_patch(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-14"
            content = self._build_entry_content(work_item_id)
            plan_text = (
                "- Approach: fixture coverage >=2 fixtures per critical path; "
                "deterministic seed strategy; invariant checks; contract boundary coverage."
            )
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", plan_text
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            preflight_block = self.pc_feature.build_preflight_block(
                {"files_to_change": []},
                work_item_id,
                "HIGH",
                ["touches secret blocking or fail-close behavior"],
            )
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Preflight Report", preflight_block
            )
            content = self.pc_feature.update_entry_field(
                content,
                work_item_id,
                "Notes",
                self.pc_feature.HIGH_RISK_APPROVAL_NOTE,
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    return "Decision: Approve\nReasons:\n- clear"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return "- should not be called"
                if "You are the Patcher agent." in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reviewer_calls["count"], 1)
            self.assertEqual(planner_update_calls["count"], 0)

    def test_plan_reviewer_conflict_high_risk_records_guidance(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-15"
            content = self._build_entry_content(work_item_id)
            plan_text = (
                "- Approach: fixture coverage >=2 fixtures per critical path; "
                "deterministic seed strategy; invariant checks; contract boundary coverage."
            )
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", plan_text
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            preflight_block = self.pc_feature.build_preflight_block(
                {"files_to_change": []},
                work_item_id,
                "HIGH",
                ["touches secret blocking or fail-close behavior"],
            )
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Preflight Report", preflight_block
            )
            content = self.pc_feature.update_entry_field(
                content,
                work_item_id,
                "Notes",
                self.pc_feature.HIGH_RISK_APPROVAL_NOTE,
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return (
                        "Decision: Conflict\n"
                        "Reasons:\n- conflicting requirements\n"
                        "Required changes:\n- reconcile scope"
                    )
                if "You are the Patcher agent." in prompt:
                    raise AssertionError("patcher should not run on conflict")
                return "ok"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn("plan reviewer conflict", stderr_capture.getvalue())
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("Plan reviewer conflict", dev_tasks)
            self.assertIn(
                "Plan reviewer conflict; resolve conflicting instructions and update Plan/Allowed Tests before retrying.",
                dev_tasks,
            )

    def test_plan_policy_block_routes_back_to_planner_before_patcher(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260208-02"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Plan",
                "- update docs/02-features/12-incremental-prd-to-features/dev-tasks.md\n"
                "- run make feature F=12",
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}
            patcher_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    return "Decision: Approve\nReasons:\n- clear"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    raise StopMain()
                if "You are the Patcher agent." in prompt:
                    patcher_calls["count"] += 1
                    return "should not patch"
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reviewer_calls["count"], 0)
            self.assertEqual(planner_update_calls["count"], 1)
            self.assertEqual(patcher_calls["count"], 0)

    def test_preexisting_dirty_before_reviewer_is_not_misattributed(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260208-03"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "You are the Patcher agent." in prompt:
                    raise StopMain()
                return "ok"

            dirty_snapshot = {
                "docs/02-features/01-workflow-hardening/dev-tasks.md": "same-hash"
            }

            def fake_parse_bool_env(name: str):
                if name == "AUTO_REVIEWER_HYGIENE":
                    return False
                return None

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "collect_dirty_snapshot",
                        return_value=dirty_snapshot,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_bool_env",
                        side_effect=fake_parse_bool_env,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("- Plan Reviewer: Codex", dev_tasks)

    def test_plan_reviewer_blocks_do_not_consume_execution_attempt_budget(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-41"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    if reviewer_calls["count"] <= 4:
                        return "Decision: Block\nReasons:\n- formatting mismatch"
                    return "Decision: Approve\nReasons:\n- clear"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return "- revised plan"
                if "You are the Patcher agent." in prompt:
                    raise StopMain()
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(reviewer_calls["count"], 5)
            self.assertEqual(planner_update_calls["count"], 4)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("reviewer_block=4/12", dev_tasks)

    def test_role_retry_counters_reset_after_successful_gate(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260212-09"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            reviewer_calls = {"count": 0}
            planner_update_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    if reviewer_calls["count"] in {1, 2, 4}:
                        return "Decision: Block\nReasons:\n- policy mismatch"
                    if reviewer_calls["count"] == 3:
                        return "Decision: Approve\nReasons:\n- clear"
                    raise StopMain()
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return "- revised plan"
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    return (
                        "Decision: PLAN_STILL_VALID\n"
                        "Rationale: narrow fix and rerun tests\n"
                    )
                if (
                    "Apply the smallest possible patch based on failure feedback"
                    in prompt
                ):
                    return "Patched based on failure feedback."
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "commit_paths",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        return_value=(1, "failed"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(planner_update_calls["count"], 3)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertGreaterEqual(dev_tasks.count("reviewer_block=1/12"), 2)
            self.assertIn("reviewer_block=2/12", dev_tasks)
            self.assertNotIn("reviewer_block=3/12", dev_tasks)
            self.assertIn("tester_retry=1/3", dev_tasks)

    def test_excessive_plan_reviewer_blocks_fail_with_specific_message(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-42"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Block\nReasons:\n- unresolved policy"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    return "- revised plan"
                return "ok"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "MAX_REVIEWER_BLOCKS",
                        2,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "max plan-reviewer block attempts reached",
                stderr_capture.getvalue(),
            )

    def test_planner_revision_limit_reaches_terminal_failure(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-43"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Block\nReasons:\n- unresolved policy"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    return "1. Edit docs/02-features/12-incremental-prd-to-features/dev-tasks.md"
                return "ok"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "MAX_REVIEWER_BLOCKS", 10)
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "MAX_PLANNER_REVISIONS", 2)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "max planner revision attempts reached",
                stderr_capture.getvalue(),
            )

    def test_reviewer_stagnation_guard_stops_repeated_unresolved_policy(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-44"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Block\nReasons:\n- unresolved policy"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    return "1. Edit docs/02-features/12-incremental-prd-to-features/dev-tasks.md"
                return "ok"

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "MAX_REVIEWER_BLOCKS", 10)
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "MAX_PLANNER_REVISIONS", 10)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "MAX_STAGNANT_REVIEWER_BLOCKS",
                        2,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "planner/reviewer loop is stagnant",
                stderr_capture.getvalue(),
            )

    def test_prepatch_policy_recheck_routes_back_to_planner_before_patcher(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-45"
            safe_plan = (
                "Plan Contract v1\n"
                "Approach:\n"
                "1. Keep scope tight.\n"
                "Files to change:\n"
                "- tools/pc-feature\n"
                "Risks:\n"
                "- low\n"
                "Tests (anti-hardcode coverage required):\n"
                "- Fixture coverage: at least 2 fixtures.\n"
                "- Deterministic seed strategy: fixed ordering.\n"
                "- Invariant checks: no role-scoped edits.\n"
                "- Contract boundary coverage: policy guard + reroute.\n"
            )
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", safe_plan
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            patcher_calls = {"count": 0}
            planner_update_calls = {"count": 0}
            reviewer_calls = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    reviewer_calls["count"] += 1
                    if reviewer_calls["count"] >= 2:
                        raise StopMain()
                    return "Decision: Approve\nReasons:\n- clear"
                if "Update the Plan section based on Plan Reviewer feedback" in prompt:
                    planner_update_calls["count"] += 1
                    return (
                        "Plan Contract v1\n"
                        "Approach:\n"
                        "1. Keep scope to implementation files.\n"
                        "Files to change:\n"
                        "- tools/pc-feature\n"
                        "Risks:\n"
                        "- low\n"
                        "Tests (anti-hardcode coverage required):\n"
                        "- Fixture coverage: at least 2 fixtures.\n"
                        "- Deterministic seed strategy: fixed ordering.\n"
                        "- Invariant checks: no role-scoped edits.\n"
                        "- Contract boundary coverage: policy guard + reroute.\n"
                    )
                if "You are the Patcher agent." in prompt:
                    patcher_calls["count"] += 1
                    return "patched"
                return "ok"

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "MAX_LOOPS",
                        2,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "plan_policy_violations",
                        side_effect=[
                            [],
                            [
                                "forbidden path in plan: docs/02-features/01-workflow-hardening/dev-tasks.md"
                            ],
                            [],
                            [],
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(patcher_calls["count"], 0)
            self.assertEqual(planner_update_calls["count"], 1)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("pre-patch policy recheck BLOCK", dev_tasks)

    def test_failure_loop_invokes_planner_and_patcher_feedback_and_logs_iteration(self):
        class StopMain(RuntimeError):
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-12"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            planner_feedback_calls = {"count": 0}
            patcher_feedback_calls = {"count": 0}
            test_runs = {"count": 0}

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if "You are the Reporter agent." in prompt:
                    return (
                        "Outcome: PASS\nDocs/logs updated: ok\n"
                        "Notes: reporter review complete\n"
                    )
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    planner_feedback_calls["count"] += 1
                    return (
                        "Decision: REVISE_PLAN\n"
                        "Rationale: tighten assertions before rerun\n"
                        "Revised Plan:\n"
                        "- revised plan from failure feedback"
                    )
                if (
                    "Apply the smallest possible patch based on failure feedback"
                    in prompt
                ):
                    patcher_feedback_calls["count"] += 1
                    return "Patched based on feedback."
                return "ok"

            def fake_run_with_step_log(
                cmd,
                metadata,
                *,
                step,
                root,
                label,
                **kwargs,
            ):
                if step == "tests":
                    test_runs["count"] += 1
                    if test_runs["count"] == 1:
                        return 1
                    raise StopMain()
                return 0

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log",
                        side_effect=fake_run_with_step_log,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "commit_paths",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(StopMain):
                    self.pc_feature.main()

            self.assertEqual(planner_feedback_calls["count"], 1)
            self.assertEqual(patcher_feedback_calls["count"], 1)
            self.assertGreaterEqual(test_runs["count"], 2)
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("revised plan from failure feedback", dev_tasks)
            self.assertIn("patcher feedback pending", dev_tasks)

    def test_feedback_loop_scope_violation_routes_back_to_planner(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            patcher_path = root / "patcher"
            patcher_path.mkdir(parents=True, exist_ok=True)
            work_item_id = "WI-20260206-13"
            content = self._build_entry_content(work_item_id)
            content = self.pc_feature.replace_entry_section(
                content, work_item_id, "Plan", "- initial plan"
            )
            content = self.pc_feature.replace_entry_section(
                content,
                work_item_id,
                "Allowed Tests",
                "- python -m unittest discover -s tests -p test_pc_feature.py",
            )
            feature_dir = self._write_feature_workspace(root, content)
            original_entry_complete = self.pc_feature.entry_section_complete
            planner_feedback_calls = {"count": 0}
            patcher_feedback_calls = {"count": 0}
            patcher_commit_attempts = {"count": 0}
            patcher_dirty = {"value": False}
            restore_calls = []
            dev_tasks_repo_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan", "Patch"}:
                    return True
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
                    return "Decision: Approve\nReasons:\n- clear"
                if (
                    "Re-evaluate the current plan using tester/reporter failure feedback"
                    in prompt
                ):
                    planner_feedback_calls["count"] += 1
                    return (
                        "Decision: REVISE_PLAN\n"
                        "Rationale: tighten assertions before rerun\n"
                        "Revised Plan:\n"
                        "- revised plan from failure feedback"
                    )
                if (
                    "Apply the smallest possible patch based on failure feedback"
                    in prompt
                ):
                    patcher_feedback_calls["count"] += 1
                    patcher_dirty["value"] = True
                    return "Patched based on feedback."
                return "ok"

            def fake_get_status_paths(path: str):
                if Path(path) == patcher_path and patcher_dirty["value"]:
                    return [dev_tasks_repo_path]
                return []

            def fake_restore_dirty_paths(worktree_path: str, paths):
                restore_calls.append((worktree_path, list(paths)))
                patcher_dirty["value"] = False

            def fake_commit_role_step(
                root_path: str,
                worktree_path: str,
                branch: str,
                role: str,
                work_item: str,
                feature_path: str,
                *,
                allow_empty: bool = False,
            ) -> bool:
                if role == "patcher":
                    patcher_commit_attempts["count"] += 1
                return False

            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "entry_section_complete",
                        side_effect=fake_entry_complete,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "parse_allowed_tests",
                        return_value=[
                            "python -m unittest discover -s tests -p test_pc_feature.py"
                        ],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "run_command_with_step_log_capture",
                        return_value=(1, "failed"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(self.pc_feature, "run_command", return_value=0)
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "commit_role_step",
                        side_effect=fake_commit_role_step,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "get_status_paths",
                        side_effect=fake_get_status_paths,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "restore_dirty_paths",
                        side_effect=fake_restore_dirty_paths,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "MAX_LOOPS",
                        2,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "codex_exec",
                        side_effect=fake_codex_exec,
                    )
                )
                with self.assertRaises(SystemExit):
                    self.pc_feature.main()

            self.assertEqual(planner_feedback_calls["count"], 2)
            self.assertEqual(patcher_feedback_calls["count"], 1)
            self.assertEqual(patcher_commit_attempts["count"], 0)
            self.assertEqual(
                restore_calls,
                [(str(patcher_path), [dev_tasks_repo_path])],
            )
            dev_tasks = self._worktree_dev_tasks(patcher_path).read_text(
                encoding="utf-8"
            )
            self.assertIn("patcher feedback role-scope violation", dev_tasks)


class ProposalGenerationTests(unittest.TestCase):
    PROPOSAL_TEMPLATE = """# Possible Improvements

## Entries

<!-- Add proposals here -->
"""

    def _template(self) -> str:
        return self.PROPOSAL_TEMPLATE

    def _entries_section(self, content: str) -> str:
        marker = "## Entries"
        if marker not in content:
            return ""
        return content.split(marker, 1)[1]

    def test_fail_outcome_generates_proposal_with_template_fields(self):
        outcome = {
            "outcome": "FAIL",
            "work_item_id": "WI-20260209-01",
            "agent_name": "Patcher",
            "step": "Patch",
            "failure_summary": "Unit tests failed on pc_runner",
            "proposed_improvement": "Harden proposal dedup for missing context",
            "proposed_patch_location": "lib/pc_runner.py",
            "risks": "May alter proposal merge behavior",
            "decision_log_ref": "DEC-20260209-01",
        }
        proposal = build_proposal_from_outcome(outcome, date="2026-02-09")
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal.status, "Proposed")
        rendered = render_proposal_entry(proposal)
        required_fields = [
            "**Date:**",
            "**Work Item:**",
            "**Agent:**",
            "**Step:**",
            "**Failure Summary:**",
            "**Proposed Improvement:**",
            "**Proposed Patch Location:**",
            "**Risks / Trade-offs:**",
            "**Status:**",
            "**Decision Log Ref:**",
        ]
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, rendered)

    def test_stall_outcome_missing_context_fills_placeholders(self):
        outcome = {"outcome": "STALL"}
        proposal = build_proposal_from_outcome(outcome, date="2026-02-09")
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal.work_item_id, "Unknown")
        self.assertEqual(proposal.agent, "Unknown")
        self.assertEqual(proposal.step, "Unknown")
        self.assertIn("Missing context:", proposal.failure_summary)

    def test_pass_outcome_returns_none(self):
        self.assertIsNone(build_proposal_from_outcome({"outcome": "PASS"}))

    def test_multi_agent_payload_combines_agents(self):
        outcome = {
            "outcome": "FAIL",
            "work_item_id": "WI-20260209-01",
            "agent_names": ["Reporter", "Tester", "Reporter"],
            "step": "Review",
            "failure_summary": "Missing reviewer feedback",
        }
        proposal = build_proposal_from_outcome(outcome, date="2026-02-09")
        self.assertEqual(proposal.agent, "Reporter, Tester")

    def test_dedup_skips_duplicate_signature(self):
        outcome = {
            "outcome": "FAIL",
            "work_item_id": "WI-20260209-01",
            "agent_name": "Tester",
            "step": "Test",
            "failure_summary": "Integration tests failed",
        }
        proposal = build_proposal_from_outcome(outcome, date="2026-02-09")
        template = self._template()
        updated, action = merge_or_append_proposal(template, proposal)
        self.assertEqual(action, "appended")
        updated_again, action_again = merge_or_append_proposal(updated, proposal)
        self.assertEqual(action_again, "skipped")
        self.assertEqual(self._entries_section(updated_again).count("### Proposal:"), 1)

    def test_dedup_merges_distinct_agents(self):
        seed_outcome = {
            "outcome": "FAIL",
            "work_item_id": "WI-20260209-01",
            "agent_name": "Tester",
            "step": "Test",
            "failure_summary": "Integration tests failed",
        }
        template = self._template()
        initial = build_proposal_from_outcome(seed_outcome, date="2026-02-09")
        updated, action = merge_or_append_proposal(template, initial)
        self.assertEqual(action, "appended")

        follow_outcome = {**seed_outcome, "agent_name": "Reporter"}
        follow = build_proposal_from_outcome(follow_outcome, date="2026-02-09")
        merged, action = merge_or_append_proposal(updated, follow)
        self.assertEqual(action, "merged")
        self.assertIn("**Agent:** Tester, Reporter", merged)

    def test_dedup_merges_placeholder_fields(self):
        seed_outcome = {
            "outcome": "FAIL",
            "work_item_id": "WI-20260209-01",
            "step": "Test",
            "failure_summary": "Timeout contacting service",
        }
        template = self._template()
        initial = build_proposal_from_outcome(seed_outcome, date="2026-02-09")
        updated, action = merge_or_append_proposal(template, initial)
        self.assertEqual(action, "appended")

        enriched_outcome = {
            **seed_outcome,
            "agent_name": "Tester",
            "proposed_improvement": "Add retry with backoff",
            "proposed_patch_location": "lib/pc_runner.py",
        }
        enriched = build_proposal_from_outcome(enriched_outcome, date="2026-02-09")
        merged, action = merge_or_append_proposal(updated, enriched)
        self.assertEqual(action, "merged")
        self.assertIn("**Agent:** Tester", merged)
        self.assertIn("**Proposed Improvement:** Add retry with backoff", merged)
        self.assertEqual(self._entries_section(merged).count("### Proposal:"), 1)

    def test_record_failure_proposal_appends_entry(self):
        pc_feature = load_pc_feature()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_dir = root / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            (docs_dir / "possible-improvements.md").write_text(
                self._template(), encoding="utf-8"
            )
            payload = {
                "outcome": "FAIL",
                "work_item_id": "WI-20260209-01",
                "agent_name": "Tester",
                "step": "Test",
                "failure_summary": "Unit tests failed",
            }
            pc_feature.record_failure_proposal(payload, root=root)
            updated = (docs_dir / "possible-improvements.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("### Proposal:", updated)

    def test_flush_collected_proposals_dedupes_and_merges_queue(self):
        pc_feature = load_pc_feature()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_dir = root / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            registry = docs_dir / "possible-improvements.md"
            registry.write_text(self._template(), encoding="utf-8")
            pending = []
            payload_a = {
                "outcome": "FAIL",
                "work_item_id": "WI-20260209-01",
                "agent_name": "Tester",
                "step": "Test",
                "failure_summary": "Unit tests failed",
                "proposed_patch_location": "tests/test_pc_feature.py",
            }
            payload_b = {
                "outcome": "FAIL",
                "work_item_id": "WI-20260209-01",
                "agent_name": "Reporter",
                "step": "Test",
                "failure_summary": "Unit tests failed",
                "proposed_improvement": "Route proposals through orchestrator queue",
            }
            pc_feature.queue_failure_proposal(payload_a, pending)
            pc_feature.queue_failure_proposal(payload_b, pending)
            self.assertEqual(len(pending), 2)
            pc_feature.flush_collected_proposals(
                pending,
                root=root,
                reason="unit-test",
            )
            self.assertEqual(pending, [])
            updated = registry.read_text(encoding="utf-8")
            self.assertEqual(self._entries_section(updated).count("### Proposal:"), 1)
            self.assertIn("**Agent:** Tester, Reporter", updated)
            self.assertIn(
                "**Proposed Improvement:** Route proposals through orchestrator queue",
                updated,
            )

    def test_record_outcome_proposal_appends_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_dir = root / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            registry = docs_dir / "possible-improvements.md"
            registry.write_text(self._template(), encoding="utf-8")
            payload = {
                "outcome": "FAIL",
                "work_item_id": "WI-20260209-01",
                "agent_name": "Reporter",
                "step": "Report",
                "failure_summary": "Missing log updates",
            }
            action = record_outcome_proposal(payload, root=root)
            self.assertEqual(action, "appended")
            updated = registry.read_text(encoding="utf-8")
            self.assertIn("### Proposal:", updated)

    def test_record_outcome_proposal_noop_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_dir = root / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            registry = docs_dir / "possible-improvements.md"
            registry.write_text(self._template(), encoding="utf-8")
            before = registry.read_text(encoding="utf-8")
            action = record_outcome_proposal({"outcome": "PASS"}, root=root)
            after = registry.read_text(encoding="utf-8")
            self.assertIsNone(action)
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
