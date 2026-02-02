import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_INTO = ROOT / "tools" / "bootstrap-into"


def run_bootstrap_into(args, input_text=None):
    return subprocess.run(
        ["bash", str(BOOTSTRAP_INTO), *args],
        text=True,
        capture_output=True,
        check=False,
        input=input_text,
    )


class TestBootstrapInto(unittest.TestCase):
    def test_bootstrap_into_requires_git_repo(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_bootstrap_into([tmp_dir])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not a git repository", result.stderr.lower())

    def test_bootstrap_into_dry_run_does_not_write_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            subprocess.run(
                ["git", "init"],
                cwd=tmp_dir,
                text=True,
                capture_output=True,
                check=True,
            )
            result = run_bootstrap_into(["--dry-run", tmp_dir])
            self.assertEqual(result.returncode, 0)
            self.assertIn("Dry-run: would update", result.stdout)
            self.assertFalse((Path(tmp_dir) / "docs").exists())

    def test_bootstrap_into_handles_existing_files_skip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            subprocess.run(
                ["git", "init"],
                cwd=tmp_dir,
                text=True,
                capture_output=True,
                check=True,
            )
            docs_dir = Path(tmp_dir) / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            readme_path = docs_dir / "README.md"
            readme_path.write_text("local readme\n", encoding="utf-8")

            result = run_bootstrap_into([tmp_dir], input_text="s\n")

            self.assertEqual(result.returncode, 0)
            self.assertIn("Choose action:", result.stderr)
            self.assertEqual(readme_path.read_text(encoding="utf-8"), "local readme\n")

    def test_bootstrap_into_marks_bootstrap_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            subprocess.run(
                ["git", "init"],
                cwd=tmp_dir,
                text=True,
                capture_output=True,
                check=True,
            )
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)
            readme_path = Path(tmp_dir) / "docs" / "README.md"
            self.assertTrue(readme_path.exists())
            lines = [
                line
                for line in readme_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertTrue(lines)
            self.assertTrue(lines[-1].startswith("<!-- PezzosCode bootstrap"))


if __name__ == "__main__":
    unittest.main()
