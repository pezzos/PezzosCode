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

    def _completed_work_item_entry(self, work_item_id: str) -> str:
        return f"""### {work_item_id} - Work item execution

- Date: 2026-02-12
- Outcome: completed
- Tests run: `python3 -m unittest`

#### Test Results

- Outcome: PASS

#### Commit

- Commit message: chore(test): complete ticket docs

#### Final Report

What changed (files): docs/02-features/01-workflow-hardening/dev-tasks.md
Tests written (names) + results: none
Docs/logs updated checklist: done
make ci results: PASS
Commands run (use pp for noisy output): python3 -m unittest
Commit message: chore(test): complete ticket docs
"""

    def _incomplete_work_item_entry(self, work_item_id: str) -> str:
        return f"""### {work_item_id} - Work item execution

- Date: 2026-02-12
- Outcome: needs replan
- Tests run:

#### Test Results

- (pending)

#### Commit

- Commit message:

#### Final Report

-
"""

    def _build_dev_tasks(self, entries: List[str]) -> str:
        return (
            "# Development Tasks\n\n"
            "## Execution Log\n\n" + "\n\n".join(entries).rstrip() + "\n"
        )

    def _stage_dev_tasks(self, repo: Path, content: str) -> str:
        rel_path = "docs/02-features/01-workflow-hardening/dev-tasks.md"
        full_path = repo / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(
            self._build_dev_tasks([self._completed_work_item_entry("WI-20260212-00")]),
            encoding="utf-8",
        )
        add_seed = self._git(repo, "add", rel_path)
        self.assertEqual(add_seed.returncode, 0, add_seed.stderr)
        seed_commit = self._git(repo, "commit", "-m", "chore(test): seed dev tasks")
        self.assertEqual(seed_commit.returncode, 0, seed_commit.stderr)

        full_path.write_text(content, encoding="utf-8")
        add = self._git(repo, "add", rel_path)
        self.assertEqual(add.returncode, 0, add.stderr)
        return rel_path

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

    def test_commit_evidence_gate_selects_highest_work_item_when_unsorted(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)
            rel_path = self._stage_dev_tasks(
                repo,
                self._build_dev_tasks(
                    [
                        self._completed_work_item_entry("WI-20260212-10"),
                        self._incomplete_work_item_entry("WI-20260212-01"),
                    ]
                ),
            )

            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--message",
                    "chore(test): validate unsorted work items",
                    "--allow",
                    rel_path,
                ],
                cwd=repo,
                env=env,
            )
            output = f"{commit.stdout}\n{commit.stderr}"
            self.assertEqual(commit.returncode, 0, output)

    def test_commit_evidence_gate_honors_explicit_work_item_id(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)
            rel_path = self._stage_dev_tasks(
                repo,
                self._build_dev_tasks(
                    [
                        self._incomplete_work_item_entry("WI-20260212-11"),
                        self._completed_work_item_entry("WI-20260212-10"),
                    ]
                ),
            )

            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--work-item-id",
                    "WI-20260212-10",
                    "--message",
                    "chore(test): explicit work item override",
                    "--allow",
                    rel_path,
                ],
                cwd=repo,
                env=env,
            )
            output = f"{commit.stdout}\n{commit.stderr}"
            self.assertEqual(commit.returncode, 0, output)

    def test_commit_evidence_gate_fails_when_explicit_work_item_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)
            rel_path = self._stage_dev_tasks(
                repo,
                self._build_dev_tasks(
                    [self._completed_work_item_entry("WI-20260212-10")]
                ),
            )

            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--work-item-id",
                    "WI-20260212-99",
                    "--message",
                    "chore(test): missing explicit work item",
                    "--allow",
                    rel_path,
                ],
                cwd=repo,
                env=env,
            )
            self.assertNotEqual(commit.returncode, 0)
            self.assertIn(
                "requested work-item execution entry not found: WI-20260212-99",
                commit.stderr,
            )

    def test_commit_evidence_gate_remediation_message_is_literal_text(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)
            rel_path = self._stage_dev_tasks(
                repo,
                self._build_dev_tasks(
                    [self._incomplete_work_item_entry("WI-20260212-10")]
                ),
            )

            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--message",
                    "chore(test): remediation quote check",
                    "--allow",
                    rel_path,
                ],
                cwd=repo,
                env=env,
            )
            self.assertNotEqual(commit.returncode, 0)
            self.assertIn(
                'Remediation: complete required "Test Results", "Commit", and "Final Report" evidence before commit.',
                commit.stderr,
            )
            self.assertNotIn("command not found", commit.stderr)

    def test_commit_evidence_gate_does_not_cross_capture_blank_outcome(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)
            rel_path = self._stage_dev_tasks(
                repo,
                self._build_dev_tasks(
                    [
                        self._completed_work_item_entry("WI-20260212-09"),
                        self._completed_work_item_entry("WI-20260212-10").replace(
                            "- Outcome: completed\n- Tests run: `python3 -m unittest`\n",
                            "- Outcome:\n- Tests run:\n",
                        ),
                    ]
                ),
            )

            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--message",
                    "chore(test): verify blank top fields remain blank",
                    "--allow",
                    rel_path,
                ],
                cwd=repo,
                env=env,
            )

            self.assertNotEqual(commit.returncode, 0)
            self.assertIn("missing top execution field: Outcome", commit.stderr)
            self.assertIn("missing top execution field: Tests run", commit.stderr)
            self.assertNotIn("Outcome=- Tests run:", commit.stderr)

    def test_commit_evidence_gate_rejects_legacy_pass_outcome(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            env = self._init_repo_with_fake_make(repo)
            rel_path = self._stage_dev_tasks(
                repo,
                self._build_dev_tasks(
                    [
                        self._completed_work_item_entry("WI-20260212-10").replace(
                            "- Outcome: completed\n",
                            "- Outcome: pass\n",
                        ),
                    ]
                ),
            )

            commit = self._run(
                [
                    str(PC_COMMIT_PATH),
                    "--yes",
                    "--message",
                    "chore(test): reject legacy pass outcome",
                    "--allow",
                    rel_path,
                ],
                cwd=repo,
                env=env,
            )

            self.assertNotEqual(commit.returncode, 0)
            self.assertIn(
                "active ticket status is not completed: Outcome=pass",
                commit.stderr,
            )


if __name__ == "__main__":
    unittest.main()
