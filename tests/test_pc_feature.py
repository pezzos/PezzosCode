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


def load_pc_feature():
    loader = importlib.machinery.SourceFileLoader("pc_feature", str(PC_FEATURE_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcFeature(unittest.TestCase):
    def setUp(self):
        self.pc_feature = load_pc_feature()

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
                self.pc_feature, "reset_dev_tasks_if_dirty", return_value=None
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
        plan = (
            "- Edit docs/02-features/12-incremental-prd-to-features/dev-tasks.md\n"
            "- Update docs/03-logs/implementation-log.md\n"
            "- Run make feature F=12\n"
        )
        violations = self.pc_feature.plan_policy_violations(plan)
        self.assertTrue(any("dev-tasks.md" in item for item in violations))
        self.assertTrue(any("docs/03-logs" in item for item in violations))
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
        with mock.patch.dict(self.pc_feature.os.environ, {}, clear=False):
            self.assertEqual(self.pc_feature.parse_resume_mode(), "auto")

    def test_parse_resume_mode_invalid_value_exits(self):
        stderr_capture = io.StringIO()
        with mock.patch.dict(
            self.pc_feature.os.environ, {"RESUME_MODE": "invalid"}, clear=False
        ):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(stderr_capture):
                    self.pc_feature.parse_resume_mode()
        self.assertIn("invalid RESUME_MODE value", stderr_capture.getvalue())

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

    def test_run_scoped_autofix_blocks_out_of_scope_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            stderr_capture = io.StringIO()
            with mock.patch.object(self.pc_feature, "run_command", return_value=0):
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
                            self.pc_feature.run_scoped_autofix(
                                str(root),
                                ["docs/02-features/01-workflow-hardening/dev-tasks.md"],
                            )
            self.assertIn(
                "scoped autofix touched out-of-scope files", stderr_capture.getvalue()
            )
            self.assertIn("README.md", stderr_capture.getvalue())

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
                        "run_command_with_step_log",
                        side_effect=fake_run_with_step_log,
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
                "max iteration attempts reached",
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

            def fake_subprocess_run(cmd, **kwargs):
                git_commands.append(list(cmd))
                return SimpleNamespace(returncode=0, stdout="", stderr="")

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
                        self.pc_feature.subprocess,
                        "run",
                        side_effect=fake_subprocess_run,
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
            scoped_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"

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
                    if ci_attempts["count"] == 1:
                        return 1
                    if ci_attempts["count"] == 2:
                        return 1
                    self.fail("ci should not run more than 2 attempts")
                return 0

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
            self.assertEqual(autofix_calls["count"], 1)
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

            def fake_entry_complete(content: str, wi_id: str, section: str) -> bool:
                if section in {"Preflight Report", "Plan"}:
                    return True
                if section == "Patch":
                    return False
                return original_entry_complete(content, wi_id, section)

            def fake_codex_exec(prompt: str, **kwargs) -> str:
                if "You are the Plan Reviewer agent." in prompt:
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
                        1,
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
                with self.assertRaises(SystemExit):
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


class ProposalGenerationTests(unittest.TestCase):
    def _template(self) -> str:
        return (ROOT / "docs" / "possible-improvements.md").read_text(encoding="utf-8")

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
