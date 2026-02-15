import importlib.machinery
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools" / "pc-devtasks-schema-check"


def load_checker_module():
    loader = importlib.machinery.SourceFileLoader(
        "pc_devtasks_schema_check", str(CHECKER_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcDevtasksSchemaCheck(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker_module()

    def _seed_feature(self, root: Path, feature_name: str, content: str) -> None:
        feature_dir = root / "docs" / "02-features" / feature_name
        feature_dir.mkdir(parents=True, exist_ok=True)
        (feature_dir / "dev-tasks.md").write_text(content, encoding="utf-8")

    def _seed_template(self, root: Path, content: str) -> None:
        template_dir = root / "docs" / "02-features" / "feature-template"
        template_dir.mkdir(parents=True, exist_ok=True)
        (template_dir / "dev-tasks.md").write_text(content, encoding="utf-8")

    @staticmethod
    def _valid_template_content() -> str:
        return (
            "## Execution Log\n\n"
            "#### Allowed Tests\n\n"
            "- (list exact commands; each command must resolve via `tools/pc-allowed-tests-check`)\n"
        )

    @staticmethod
    def _valid_feature_content() -> str:
        return "## Execution Log\n"

    @staticmethod
    def _work_item_with_required_sections(
        *, test_results: str = "- (pending)", tester_feedback: str = "- (pending)"
    ) -> str:
        return (
            "## Execution Log\n\n"
            "### WI-20260214-01 - Work item execution\n\n"
            "- Date: 2026-02-14\n"
            "- Outcome: needs replan\n\n"
            "#### Preflight Report\n\n- (pending)\n\n"
            "#### TDD Plan\n\n- (pending)\n\n"
            "#### Allowed Tests\n\n- (pending)\n\n"
            "#### Files to Change\n\n- (pending)\n\n"
            "#### Docs Updated\n\n- (pending)\n\n"
            "#### Plan\n\n- (pending)\n\n"
            "#### Patch\n\n- (pending)\n\n"
            f"#### Test Results\n\n{test_results}\n\n"
            "#### Reporter Review\n\n- (pending)\n\n"
            "#### Gates\n\n- (pending)\n\n"
            "#### Autofix Attempts\n\n- (none)\n\n"
            f"#### Tester Feedback\n\n{tester_feedback}\n\n"
            "#### Reporter Feedback\n\n- (pending)\n\n"
            "#### Iteration Log\n\n- (pending)\n\n"
            "#### Commit\n\n- (pending)\n\n"
            "#### Final Report\n\n- (pending)\n"
        )

    def test_missing_execution_log_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            missing_exec = "## Task Breakdown\n"
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(root, "01-sample", missing_exec)

            errors = self.checker.run_check(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("01-sample", errors[0])
            self.assertIn("## Execution Log", errors[0])

    def test_missing_template_execution_log_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = self._valid_feature_content()
            missing_exec = "## Task Breakdown\n"
            self._seed_template(root, missing_exec)
            self._seed_feature(root, "01-sample", valid)

            errors = self.checker.run_check(root)

            self.assertTrue(
                any(
                    "feature-template" in item and "## Execution Log" in item
                    for item in errors
                )
            )

    def test_valid_files_pass(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = self._valid_feature_content()
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(root, "01-sample", valid)
            self._seed_feature(root, "02-other", valid)

            errors = self.checker.run_check(root)

            self.assertEqual(errors, [])

    def test_missing_template_allowed_tests_guidance_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            invalid_template = (
                "## Execution Log\n\n"
                "#### Allowed Tests\n\n"
                "- (list exact commands)\n"
            )
            self._seed_template(root, invalid_template)
            self._seed_feature(root, "01-sample", self._valid_feature_content())

            errors = self.checker.run_check(root)

            self.assertTrue(
                any("tools/pc-allowed-tests-check" in item for item in errors)
            )

    def test_feature_with_numeric_work_item_missing_sections_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(
                root,
                "01-sample",
                (
                    "## Execution Log\n\n"
                    "### WI-20260214-01 - Work item execution\n\n"
                    "- Date: 2026-02-14\n"
                    "- Outcome: needs replan\n"
                ),
            )

            errors = self.checker.run_check(root)

            self.assertTrue(
                any(
                    "missing required work-item section(s)" in item
                    and "01-sample" in item
                    for item in errors
                )
            )

    def test_feature_with_numeric_work_item_and_required_sections_passes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(
                root,
                "01-sample",
                self._work_item_with_required_sections(),
            )

            errors = self.checker.run_check(root)

            self.assertEqual(errors, [])

    def test_semantic_invariant_missing_tester_outcome_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(
                root,
                "01-sample",
                self._work_item_with_required_sections(
                    test_results="- `tools/pc-devtasks-schema-check` -> pass (exit 0).",
                    tester_feedback="- Notes: Pending.",
                ),
            )

            errors = self.checker.run_check(root)

            self.assertTrue(
                any(
                    "semantic invariant violation" in item
                    and "missing critical artifact" in item
                    for item in errors
                )
            )

    def test_semantic_invariant_passes_when_tester_outcome_exists(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(
                root,
                "01-sample",
                self._work_item_with_required_sections(
                    test_results="- `tools/pc-devtasks-schema-check` -> pass (exit 0).",
                    tester_feedback="Outcome: PASS\n- Notes: clean.",
                ),
            )

            errors = self.checker.run_check(root)

            self.assertEqual(errors, [])

    def test_main_is_quiet_on_success_by_default(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = self._valid_feature_content()
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(root, "01-sample", valid)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = self.checker.main(["--root", str(root)])

            self.assertEqual(status, 0)
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")

    def test_main_verbose_prints_success_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = self._valid_feature_content()
            self._seed_template(root, self._valid_template_content())
            self._seed_feature(root, "01-sample", valid)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = self.checker.main(["--root", str(root), "--verbose"])

            self.assertEqual(status, 0)
            self.assertIn("pc-devtasks-schema-check: ok (2 files)", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
