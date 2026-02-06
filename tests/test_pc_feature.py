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

from lib.pc_runner import build_metadata

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
        feature_dir = root / "docs" / "02-features" / "01-workflow-hardening"
        feature_dir.mkdir(parents=True, exist_ok=True)
        (feature_dir / "dev-tasks.md").write_text(dev_tasks_content, encoding="utf-8")
        (feature_dir / "feature-spec.md").write_text(
            "# feature spec\n", encoding="utf-8"
        )
        (feature_dir / "tech-design.md").write_text("# tech design\n", encoding="utf-8")
        (feature_dir / "test-plan.md").write_text("# test plan\n", encoding="utf-8")
        logs_dir = root / "docs" / "03-logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        (logs_dir / "implementation-log.md").write_text("# impl\n", encoding="utf-8")
        (logs_dir / "validation-log.md").write_text("# validation\n", encoding="utf-8")
        (logs_dir / "decision-log.md").write_text("# decision\n", encoding="utf-8")
        return feature_dir

    def _patch_main_base(self, root: Path, feature_dir: Path, patcher_path: Path):
        return [
            mock.patch.object(
                self.pc_feature, "parse_args", return_value=("01", False)
            ),
            mock.patch.object(self.pc_feature.os, "getcwd", return_value=str(root)),
            mock.patch.object(
                self.pc_feature, "git_current_branch", return_value="main"
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
            mock.patch.object(self.pc_feature, "worktree_is_dirty", return_value=False),
            mock.patch.object(self.pc_feature, "branch_ahead_count", return_value=0),
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
            mock.patch.object(self.pc_feature, "cleanup_worktrees", return_value=None),
            mock.patch.object(
                self.pc_feature, "check_allowed_tests_exist", return_value=[]
            ),
            mock.patch.object(
                self.pc_feature, "process_docs_changed", return_value=False
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
            {"max_files": 1, "max_new_modules": 0},
            "LOW",
            [],
        )
        self.assertIn("Systematic review:", block)

    def test_build_preflight_block_includes_review_summary(self):
        summary = "make feature F=01: ok"
        block = self.pc_feature.build_preflight_block(
            {},
            "WI-20260204-01",
            {"max_files": 1, "max_new_modules": 0},
            "LOW",
            [],
            summary,
        )
        self.assertIn(f"Systematic review: {summary}", block)

    def test_classify_risk_flags_restore_touch(self):
        data = {"touches_restore": True, "files_to_change": []}
        risk, triggers = self.pc_feature.classify_risk(
            data, {"max_files": 5, "max_new_modules": 0}
        )
        self.assertEqual(risk, "HIGH")
        self.assertIn("affects restore apply semantics or permissions", triggers)

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
        self.assertIn("missing prompt template", stderr_capture.getvalue())
        self.assertIn("role=planner task=create", stderr_capture.getvalue())

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

    def test_main_dirty_existing_worktree_continue_preserves_state(self):
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
            prompt_yes_no_mock = mock.Mock(return_value=True)
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
                        "worktree_is_dirty",
                        return_value=True,
                    )
                )
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
                        "prompt_yes_no",
                        prompt_yes_no_mock,
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
            prompt_yes_no_mock.assert_called_once()
            self.assertTrue(
                any(
                    "existing patcher worktree is not pristine" in str(call.args[0])
                    for call in print_mock.call_args_list
                )
            )

    def test_main_dirty_existing_worktree_abort_exits_without_cleanup(self):
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

            stderr_capture = io.StringIO()
            with contextlib.ExitStack() as stack:
                for patcher in self._patch_main_base(root, feature_dir, patcher_path):
                    stack.enter_context(patcher)
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "worktree_is_dirty",
                        return_value=True,
                    )
                )
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
                        "prompt_yes_no",
                        return_value=False,
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
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stderr(stderr_capture):
                        self.pc_feature.main()

            self.assertIn(
                "aborted by user; existing patcher worktree preserved",
                stderr_capture.getvalue(),
            )
            remove_worktree_mock.assert_not_called()
            prepare_worktree_mock.assert_not_called()

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
                        return_value=[str(feature_dir / "dev-tasks.md")],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        self.pc_feature,
                        "stage_scoped_final_paths",
                        return_value=[str(feature_dir / "dev-tasks.md")],
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
            dev_tasks = (feature_dir / "dev-tasks.md").read_text(encoding="utf-8")
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
            dev_tasks = (feature_dir / "dev-tasks.md").read_text(encoding="utf-8")
            self.assertIn("revised plan from failure feedback", dev_tasks)
            self.assertIn("patcher feedback task executed", dev_tasks)


if __name__ == "__main__":
    unittest.main()
