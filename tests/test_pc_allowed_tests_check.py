import contextlib
import importlib.machinery
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PC_ALLOWED_TESTS_CHECK_PATH = ROOT / "tools" / "pc-allowed-tests-check"


def load_pc_allowed_tests_check():
    loader = importlib.machinery.SourceFileLoader(
        "pc_allowed_tests_check", str(PC_ALLOWED_TESTS_CHECK_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


@contextlib.contextmanager
def pushd(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class TestPcAllowedTestsCheck(unittest.TestCase):
    def setUp(self):
        self.pc_allowed_tests_check = load_pc_allowed_tests_check()

    def test_check_command_accepts_unittest_discover_with_start_dir_and_pattern(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "import unittest\n", encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    'python -m unittest discover -s tests -p "test_*.py"'
                )
            self.assertEqual(missing, [])

    def test_check_command_accepts_unittest_discover_with_positional_start_dir(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "import unittest\n", encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m unittest discover tests"
                )
            self.assertEqual(missing, [])

    def test_check_command_rejects_unittest_discover_when_no_matching_tests(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    'python -m unittest discover -s tests -p "test_*.py"'
                )
            self.assertTrue(
                any("no tests match pattern" in entry for entry in missing), missing
            )

    def test_check_command_accepts_pytest_tests_dir_target(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "def test_ok():\n    assert True\n", encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command("pytest tests -q")
            self.assertEqual(missing, [])

    def test_check_command_rejects_pytest_missing_target(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m pytest tests/test_missing.py -q"
                )
            self.assertEqual(missing, ["tests/test_missing.py"])

    def test_check_command_rejects_make_ci(self):
        missing = self.pc_allowed_tests_check.check_command("make ci")
        self.assertEqual(missing, ["forbidden command: make ci"])


if __name__ == "__main__":
    unittest.main()
