import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PC_ROLE_COMMIT = ROOT / "tools" / "pc-role-commit"


class TestPcRoleCommit(unittest.TestCase):
    def _run(self, args, *, cwd: Path):
        return subprocess.run(
            args,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def _git(self, repo: Path, *args: str):
        return self._run(["git", *args], cwd=repo)

    def _init_repo(self, repo: Path):
        init = self._git(repo, "init")
        self.assertEqual(init.returncode, 0, init.stderr)
        user_name = self._git(repo, "config", "user.name", "Test User")
        self.assertEqual(user_name.returncode, 0, user_name.stderr)
        user_email = self._git(repo, "config", "user.email", "test@example.com")
        self.assertEqual(user_email.returncode, 0, user_email.stderr)

    def test_pc_role_commit_stages_and_commits_allowed_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            self._init_repo(repo)
            reporter_log = (
                repo / "docs" / "02-features" / "01-workflow" / "reporter-log.md"
            )
            reporter_log.parent.mkdir(parents=True, exist_ok=True)
            reporter_log.write_text("seed\n", encoding="utf-8")
            add_seed = self._git(repo, "add", str(reporter_log.relative_to(repo)))
            self.assertEqual(add_seed.returncode, 0, add_seed.stderr)
            seed_commit = self._git(repo, "commit", "-m", "chore(test): seed")
            self.assertEqual(seed_commit.returncode, 0, seed_commit.stderr)

            reporter_log.write_text("updated\n", encoding="utf-8")
            run = self._run(
                [
                    str(PC_ROLE_COMMIT),
                    "--role",
                    "reporter",
                    "--work-item-id",
                    "WI-20260214-20",
                    "--allow",
                    str(reporter_log.relative_to(repo)),
                ],
                cwd=repo,
            )
            output = f"{run.stdout}\n{run.stderr}"
            self.assertEqual(run.returncode, 0, output)

            head_message = self._git(repo, "log", "-1", "--pretty=%s")
            self.assertEqual(head_message.returncode, 0, head_message.stderr)
            self.assertEqual(
                head_message.stdout.strip(),
                "reporter: updates for WI-20260214-20",
            )

    def test_pc_role_commit_noop_when_no_staged_changes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            self._init_repo(repo)
            reporter_log = (
                repo / "docs" / "02-features" / "01-workflow" / "reporter-log.md"
            )
            reporter_log.parent.mkdir(parents=True, exist_ok=True)
            reporter_log.write_text("seed\n", encoding="utf-8")
            add_seed = self._git(repo, "add", str(reporter_log.relative_to(repo)))
            self.assertEqual(add_seed.returncode, 0, add_seed.stderr)
            seed_commit = self._git(repo, "commit", "-m", "chore(test): seed")
            self.assertEqual(seed_commit.returncode, 0, seed_commit.stderr)

            run = self._run(
                [
                    str(PC_ROLE_COMMIT),
                    "--role",
                    "reporter",
                    "--work-item-id",
                    "WI-20260214-21",
                    "--allow",
                    str(reporter_log.relative_to(repo)),
                ],
                cwd=repo,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("no staged changes to commit", run.stdout)
