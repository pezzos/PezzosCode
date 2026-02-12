import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "pc-template-sync"


def run(
    repo: Path, cmd: list[str], check: bool = False
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(cmd)}\n{result.stderr}"
        )
    return result


class TestPcTemplateSync(unittest.TestCase):
    def _init_repo(self, mismatch_initial: bool = False) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name)
        run(repo, ["git", "init"], check=True)
        run(repo, ["git", "config", "user.email", "test@example.com"], check=True)
        run(repo, ["git", "config", "user.name", "Test User"], check=True)

        live = repo / "docs" / "AGENTS.md"
        template = repo / "tools" / "templates" / "docs" / "AGENTS.md"
        live.parent.mkdir(parents=True, exist_ok=True)
        template.parent.mkdir(parents=True, exist_ok=True)
        live.write_text("live-v1\n", encoding="utf-8")
        template.write_text(
            "template-v0\n" if mismatch_initial else "live-v1\n", encoding="utf-8"
        )

        run(repo, ["git", "add", "."], check=True)
        run(repo, ["git", "commit", "-m", "init"], check=True)
        return repo

    def _run_sync(self, repo: Path) -> subprocess.CompletedProcess[str]:
        return run(repo, ["python3", str(SCRIPT), "--apply", "--stage"])

    def test_one_side_changed_copies_staged_source_and_stages_target(self):
        repo = self._init_repo()
        live = repo / "docs" / "AGENTS.md"
        template = repo / "tools" / "templates" / "docs" / "AGENTS.md"

        live.write_text("live-v2\n", encoding="utf-8")
        run(repo, ["git", "add", "docs/AGENTS.md"], check=True)

        result = self._run_sync(repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(template.read_text(encoding="utf-8"), "live-v2\n")
        staged = run(
            repo, ["git", "diff", "--cached", "--name-only"], check=True
        ).stdout
        self.assertIn("tools/templates/docs/AGENTS.md", staged.splitlines())

    def test_neither_side_changed_drift_copies_live_to_template(self):
        repo = self._init_repo(mismatch_initial=True)
        live = repo / "docs" / "AGENTS.md"
        template = repo / "tools" / "templates" / "docs" / "AGENTS.md"

        result = self._run_sync(repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            template.read_text(encoding="utf-8"), live.read_text(encoding="utf-8")
        )
        staged = run(
            repo, ["git", "diff", "--cached", "--name-only"], check=True
        ).stdout
        self.assertIn("tools/templates/docs/AGENTS.md", staged.splitlines())

    def test_both_sides_changed_fails_for_codex_merge(self):
        repo = self._init_repo()
        live = repo / "docs" / "AGENTS.md"
        template = repo / "tools" / "templates" / "docs" / "AGENTS.md"

        live.write_text("live-branch\n", encoding="utf-8")
        template.write_text("template-branch\n", encoding="utf-8")
        run(
            repo,
            ["git", "add", "docs/AGENTS.md", "tools/templates/docs/AGENTS.md"],
            check=True,
        )

        result = self._run_sync(repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("both sides changed", result.stderr)
        self.assertEqual(live.read_text(encoding="utf-8"), "live-branch\n")
        self.assertEqual(template.read_text(encoding="utf-8"), "template-branch\n")


if __name__ == "__main__":
    unittest.main()
