import importlib.machinery
import importlib.util
import tempfile
import unittest
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

    def test_missing_execution_log_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = "## Execution Log\n"
            missing_exec = "## Task Breakdown\n"
            self._seed_template(root, valid)
            self._seed_feature(root, "01-sample", missing_exec)

            errors = self.checker.run_check(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("01-sample", errors[0])
            self.assertIn("## Execution Log", errors[0])

    def test_missing_template_execution_log_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = "## Execution Log\n"
            missing_exec = "## Task Breakdown\n"
            self._seed_template(root, missing_exec)
            self._seed_feature(root, "01-sample", valid)

            errors = self.checker.run_check(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("feature-template", errors[0])
            self.assertIn("## Execution Log", errors[0])

    def test_valid_files_pass(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            valid = "## Execution Log\n"
            self._seed_template(root, valid)
            self._seed_feature(root, "01-sample", valid)
            self._seed_feature(root, "02-other", valid)

            errors = self.checker.run_check(root)

            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
