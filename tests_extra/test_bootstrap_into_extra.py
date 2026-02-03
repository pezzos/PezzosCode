import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_INTO = ROOT / "tools" / "bootstrap-into"
LOG_FILES = (
    Path("docs/03-logs/implementation-log.md"),
    Path("docs/03-logs/validation-log.md"),
)
LOG_MARKER = "<!-- PezzosCode bootstrap sha256:"
SCRIPT_MARKER = "# PezzosCode bootstrap sha256:"


def run_bootstrap_into(args, input_text=None):
    return subprocess.run(
        ["bash", str(BOOTSTRAP_INTO), *args],
        text=True,
        capture_output=True,
        check=False,
        input=input_text,
    )


def init_git_repo(path):
    subprocess.run(
        ["git", "init"],
        cwd=path,
        text=True,
        capture_output=True,
        check=True,
    )


class BootstrapIntoLogTests(unittest.TestCase):
    def test_copies_docs_readme_and_reports_it(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            readme = Path(tmp_dir) / "docs" / "README.md"
            self.assertTrue(readme.exists(), "docs/README.md should be created")
            content = readme.read_text(encoding="utf-8")
            self.assertEqual(
                content.count(LOG_MARKER), 1, "README should have one marker"
            )
            self.assertIn("docs/README.md", result.stdout, "CLI should mention README")

    def test_copies_protocol_doc_and_tooling(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            protocol = (
                Path(tmp_dir) / "docs" / "04-process" / "ticket-execution-protocol.md"
            )
            self.assertTrue(protocol.exists(), "protocol doc should exist")
            self.assertIn(LOG_MARKER, protocol.read_text(encoding="utf-8"))
            self.assertIn(
                "docs/04-process/ticket-execution-protocol.md",
                result.stdout,
                "CLI should list the protocol doc",
            )

            tool = Path(tmp_dir) / "tools" / "pc-ticket"
            self.assertTrue(tool.exists(), "pc-ticket should be copied")
            tool_content = tool.read_text(encoding="utf-8")
            self.assertIn(SCRIPT_MARKER, tool_content)
            self.assertEqual(
                tool_content.count(SCRIPT_MARKER),
                1,
                "Tooling script should show only one marker",
            )
            self.assertIn("tools/pc-ticket", result.stdout)

    def test_logs_are_copied_and_reported_once(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            updated_lines = [
                line.strip()
                for line in result.stdout.splitlines()
                if line.startswith("Updated:")
            ]
            self.assertTrue(updated_lines, "Updated lines should exist")

            counts = {rel_path: 0 for rel_path in LOG_FILES}
            for line in updated_lines:
                path = Path(line.split("Updated:", 1)[1].strip())
                try:
                    rel = path.relative_to(tmp_dir)
                except ValueError:
                    continue
                for target in LOG_FILES:
                    if rel == target:
                        counts[target] += 1
            for rel_path, occurrences in counts.items():
                self.assertEqual(
                    occurrences,
                    1,
                    f"{rel_path.name} should be listed exactly once",
                )

    def test_root_templates_and_skills_receive_markers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            for name in ("AGENTS.md", "pp.yml"):
                target = Path(tmp_dir) / name
                self.assertTrue(target.exists(), f"{name} should exist")
                self.assertIn(
                    "PezzosCode bootstrap",
                    target.read_text(encoding="utf-8"),
                    f"{name} should include a bootstrap marker",
                )

            skill_path = (
                Path(tmp_dir) / ".codex" / "skills" / "context-to-product" / "SKILL.md"
            )
            self.assertTrue(skill_path.exists(), "skill should be present")
            self.assertIn(
                "PezzosCode bootstrap",
                skill_path.read_text(encoding="utf-8"),
                "Skill files should include bootstrap marker",
            )

    def test_logs_keep_headers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            headers = {
                LOG_FILES[0]: "# Implementation Log",
                LOG_FILES[1]: "# Validation Log",
            }
            for rel_path, expected in headers.items():
                target = Path(tmp_dir) / rel_path
                self.assertTrue(target.exists(), f"{rel_path} should exist")
                lines = [
                    line
                    for line in target.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
                self.assertEqual(
                    lines[0],
                    expected,
                    f"{rel_path.name} should keep its heading",
                )

    def test_verbose_rerun_reports_skipping_logs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            run_bootstrap_into([tmp_dir])

            rerun = run_bootstrap_into(["--verbose", tmp_dir])
            self.assertEqual(rerun.returncode, 0)
            rerun_stdout = rerun.stdout or ""

            for rel_path in LOG_FILES:
                abs_path = str(Path(tmp_dir) / rel_path)
                self.assertIn(
                    abs_path,
                    rerun_stdout,
                    f"verbose rerun should mention {rel_path.name}",
                )
                content = (Path(tmp_dir) / rel_path).read_text(encoding="utf-8")
                self.assertEqual(
                    content.count(LOG_MARKER),
                    1,
                    f"{rel_path.name} should retain one marker",
                )


if __name__ == "__main__":
    unittest.main()
