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

    def test_check_command_prepatch_allows_unittest_discover_before_tests_exist(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n")
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    'python -m unittest discover -s tests -p "test_*.py"',
                    phase="prepatch",
                )
            self.assertEqual(missing, [])

    def test_check_command_accepts_unittest_dotted_class_target(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "import unittest\n\n"
                "class SampleTests(unittest.TestCase):\n"
                "    def test_ok(self):\n"
                "        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m unittest tests.test_sample.SampleTests"
                )
            self.assertEqual(missing, [])

    def test_check_command_accepts_unittest_dotted_method_target(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "import unittest\n\n"
                "class SampleTests(unittest.TestCase):\n"
                "    def test_ok(self):\n"
                "        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m unittest tests.test_sample.SampleTests.test_ok"
                )
            self.assertEqual(missing, [])

    def test_check_command_rejects_unittest_missing_dotted_target_prefix(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m unittest tests.test_missing.SampleTests"
                )
            self.assertEqual(missing, ["tests.test_missing.SampleTests"])

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
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n")
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m pytest tests/test_missing.py -q"
                )
            self.assertEqual(missing, ["tests/test_missing.py"])

    def test_check_command_rejects_bare_unittest_command(self):
        missing = self.pc_allowed_tests_check.check_command("python -m unittest")
        self.assertEqual(missing, ["unittest requires explicit test target"])

    def test_check_command_rejects_discover_without_explicit_start_dir(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "import unittest\n", encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m unittest discover"
                )
        self.assertEqual(missing, ["discover requires explicit start directory"])

    def test_check_command_rejects_pytest_without_explicit_target(self):
        missing = self.pc_allowed_tests_check.check_command("python -m pytest -q")
        self.assertEqual(missing, ["pytest requires explicit test target"])

    def test_check_command_rejects_make_ci(self):
        missing = self.pc_allowed_tests_check.check_command("make ci")
        self.assertEqual(missing, ["forbidden command: make ci"])

    def test_check_command_accepts_make_target_when_present(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "Makefile").write_text("test:\n\t@echo ok\n", encoding="utf-8")
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command("make test")
            self.assertEqual(missing, [])

    def test_check_command_rejects_make_target_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "Makefile").write_text("lint:\n\t@echo ok\n", encoding="utf-8")
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command("make test")
            self.assertEqual(missing, ["missing make target: test"])

    def test_check_command_prepatch_allows_make_target_to_be_added_by_patch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "Makefile").write_text("lint:\n\t@echo ok\n", encoding="utf-8")
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "make test", phase="prepatch"
                )
            self.assertEqual(missing, [])

    def test_check_command_accepts_node_package_script(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "package.json").write_text(
                '{"name":"demo","scripts":{"test":"vitest run"}}', encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command("npm test")
            self.assertEqual(missing, [])

    def test_check_command_rejects_node_package_missing_script(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "package.json").write_text(
                '{"name":"demo","scripts":{"lint":"eslint ."}}', encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command("npm test")
            self.assertEqual(missing, ["missing package.json script: test"])

    def test_check_command_prepatch_allows_node_script_to_be_added_by_patch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "package.json").write_text(
                '{"name":"demo","scripts":{"lint":"eslint ."}}', encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "npm test", phase="prepatch"
                )
            self.assertEqual(missing, [])

    def test_check_command_rejects_python_when_repo_is_not_python_capable(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "package.json").write_text(
                '{"name":"demo","scripts":{"test":"vitest run"}}', encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "python -m pytest tests/test_missing.py -q",
                    phase="prepatch",
                )
            self.assertEqual(
                missing,
                [
                    "repo does not advertise Python test capability: python -m pytest tests/test_missing.py -q"
                ],
            )

    def test_check_command_accepts_tools_script_for_docs_only_repo(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tools_dir = root / "tools"
            tools_dir.mkdir()
            (tools_dir / "pc-devtasks-schema-check").write_text(
                "#!/bin/sh\nexit 0\n",
                encoding="utf-8",
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "tools/pc-devtasks-schema-check",
                    phase="prepatch",
                )
            self.assertEqual(missing, [])

    def test_check_command_rejects_unsupported_commands(self):
        missing = self.pc_allowed_tests_check.check_command("bash -lc 'echo hi'")
        self.assertEqual(missing, ["unsupported test command: bash -lc 'echo hi'"])

    def test_check_command_accepts_pp_wrapped_pytest(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "def test_ok():\n    assert True\n", encoding="utf-8"
            )
            with pushd(root):
                missing = self.pc_allowed_tests_check.check_command(
                    "tools/offload-proxy/pp pytest tests -q"
                )
            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
