import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
PC_COMMIT_PATH = ROOT / "tools" / "pc-commit"


class TestPcCommit(unittest.TestCase):
    def _run(
        self, args: List[str], *, cwd: Path, env: Optional[Dict[str, str]] = None
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            args,
            cwd=cwd,
            env=env,
            check=False,
            text=True,
            capture_output=True,
        )

    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess:
        return self._run(["git", *args], cwd=repo)

    def _init_repo_with_fake_make(self, repo: Path) -> Dict[str, str]:
        init = self._git(repo, "init")
        self.assertEqual(init.returncode, 0, init.stderr)

        user_name = self._git(repo, "config", "user.name", "Test User")
        self.assertEqual(user_name.returncode, 0, user_name.stderr)
        user_email = self._git(repo, "config", "user.email", "test@example.com")
        self.assertEqual(user_email.returncode, 0, user_email.stderr)

        fake_bin = Path(tempfile.mkdtemp(prefix="pc-commit-fake-bin-"))
        self.addCleanup(shutil.rmtree, fake_bin, True)
        fake_make = fake_bin / "make"
        fake_make.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        fake_make.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = f"{fake_bin}{os.pathsep}{env.get('PATH', '')}"
        return env

    def test_missing_allow_path_does_not_break_commit(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)

            docs_path = repo / "docs"
            docs_path.mkdir(parents=True, exist_ok=True)
            tracked_file = docs_path / "notes.md"
            tracked_file.write_text("# Initial\n", encoding="utf-8")
            add = self._git(repo, "add", "docs/notes.md")
            self.assertEqual(add.returncode, 0, add.stderr)
            seed_commit = self._git(repo, "commit", "-m", "chore(test): seed")
            self.assertEqual(seed_commit.returncode, 0, seed_commit.stderr)

            tracked_file.write_text("# Updated\n", encoding="utf-8")
            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--message",
                    "docs(test): update notes",
                    "--allow",
                    "docs/notes.md",
                    "--allow",
                    ".tmp",
                ],
                cwd=repo,
                env=env,
            )
            output = f"{commit.stdout}\n{commit.stderr}"
            self.assertEqual(commit.returncode, 0, output)
            self.assertNotIn("pathspec '.tmp' did not match any files", output)

            head_count = self._git(repo, "rev-list", "--count", "HEAD")
            self.assertEqual(head_count.returncode, 0, head_count.stderr)
            self.assertEqual(head_count.stdout.strip(), "2")

    def test_allow_prefix_stages_nested_changes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)

            logs_dir = repo / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            tracked_file = logs_dir / "run.log"
            tracked_file.write_text("first\n", encoding="utf-8")
            add = self._git(repo, "add", "logs/run.log")
            self.assertEqual(add.returncode, 0, add.stderr)
            seed_commit = self._git(repo, "commit", "-m", "chore(test): seed logs")
            self.assertEqual(seed_commit.returncode, 0, seed_commit.stderr)

            tracked_file.write_text("first\nsecond\n", encoding="utf-8")
            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--message",
                    "chore(test): update logs",
                    "--allow",
                    "logs/",
                ],
                cwd=repo,
                env=env,
            )
            output = f"{commit.stdout}\n{commit.stderr}"
            self.assertEqual(commit.returncode, 0, output)

            changed_files = self._git(
                repo, "show", "--name-only", "--pretty=format:", "HEAD"
            )
            self.assertEqual(changed_files.returncode, 0, changed_files.stderr)
            self.assertIn("logs/run.log", changed_files.stdout.splitlines())


if __name__ == "__main__":
    unittest.main()
