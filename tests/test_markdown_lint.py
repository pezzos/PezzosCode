import importlib.machinery
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINT_PATH = ROOT / "tools" / "markdown-lint"


def load_markdown_lint_module():
    loader = importlib.machinery.SourceFileLoader(
        "markdown_lint", str(MARKDOWN_LINT_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestMarkdownLint(unittest.TestCase):
    def setUp(self):
        self.markdown_lint = load_markdown_lint_module()

    def test_main_is_quiet_on_success_by_default(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "ok.md"
            file_path.write_text("# Title\n", encoding="utf-8")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = self.markdown_lint.main([str(file_path)])

            self.assertEqual(status, 0)
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")

    def test_main_verbose_prints_success_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "ok.md"
            file_path.write_text("# Title\n", encoding="utf-8")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = self.markdown_lint.main([str(file_path), "--verbose"])

            self.assertEqual(status, 0)
            self.assertIn("Markdown lint OK (1 files).", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")

    def test_main_reports_issues_on_stderr(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "bad.md"
            file_path.write_bytes(b"# Title  ")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = self.markdown_lint.main([str(file_path)])

            self.assertEqual(status, 1)
            self.assertEqual(stdout.getvalue(), "")
            err = stderr.getvalue()
            self.assertIn("Markdown lint issues found:", err)
            self.assertIn("trailing whitespace", err)
            self.assertIn("missing trailing newline", err)


if __name__ == "__main__":
    unittest.main()
