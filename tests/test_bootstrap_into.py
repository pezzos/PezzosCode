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
SKIP_PROMPT_RESPONSE = "s\n"


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


class TestBootstrapInto(unittest.TestCase):
    def test_bootstrap_into_requires_git_repo(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_bootstrap_into([tmp_dir])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not a git repository", result.stderr.lower())

    def test_bootstrap_into_dry_run_does_not_write_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into(["--dry-run", tmp_dir])
            self.assertEqual(result.returncode, 0)
            self.assertIn("Dry-run: would update", result.stdout)
            self.assertFalse((Path(tmp_dir) / "docs").exists())

    def test_bootstrap_into_handles_existing_files_skip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            docs_dir = Path(tmp_dir) / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            readme_path = docs_dir / "README.md"
            readme_path.write_text("local readme\n", encoding="utf-8")

            result = run_bootstrap_into([tmp_dir], input_text=SKIP_PROMPT_RESPONSE)

            self.assertEqual(result.returncode, 0)
            self.assertIn("Choose action:", result.stderr)
            self.assertEqual(readme_path.read_text(encoding="utf-8"), "local readme\n")

    def test_bootstrap_into_marks_bootstrap_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
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

    def test_bootstrap_into_copies_docs_readme(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            readme_path = Path(tmp_dir) / "docs" / "README.md"
            self.assertTrue(readme_path.exists(), "README.md should be copied")
            readme_content = readme_path.read_text(encoding="utf-8")
            self.assertEqual(
                readme_content.count(LOG_MARKER),
                1,
                "README.md should only receive one bootstrap marker",
            )
            self.assertIn("docs/README.md", result.stdout)

    def test_bootstrap_into_copies_protocol_doc(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            protocol_path = (
                Path(tmp_dir) / "docs" / "04-process" / "ticket-execution-protocol.md"
            )
            self.assertTrue(
                protocol_path.exists(),
                "ticket-execution-protocol.md should land in the target repo",
            )
            protocol_content = protocol_path.read_text(encoding="utf-8")
            self.assertIn("Ticket Execution Protocol", protocol_content)
            self.assertEqual(
                protocol_content.count(LOG_MARKER),
                1,
                "Protocol doc should retain exactly one bootstrap marker",
            )
            self.assertIn(
                "docs/04-process/ticket-execution-protocol.md",
                result.stdout,
            )

    def test_bootstrap_into_copies_tooling_scripts(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            tool_path = Path(tmp_dir) / "tools" / "pc-ticket"
            self.assertTrue(
                tool_path.exists(),
                "Annotated tooling scripts should land in tools/",
            )
            tool_content = tool_path.read_text(encoding="utf-8")
            self.assertIn(SCRIPT_MARKER, tool_content)
            self.assertEqual(
                tool_content.count(SCRIPT_MARKER),
                1,
                "Tooling scripts should only have one bootstrap marker",
            )
            self.assertIn("tools/pc-ticket", result.stdout)

    def test_bootstrap_into_copies_log_assets(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            for rel_path in LOG_FILES:
                dest = Path(tmp_dir) / rel_path
                self.assertTrue(dest.exists(), f"{rel_path} should be copied")
                content = dest.read_text(encoding="utf-8")
                self.assertEqual(
                    content.count(LOG_MARKER),
                    1,
                    f"{rel_path.name} should retain exactly one bootstrap marker",
                )

            stdout = result.stdout or ""
            for rel_path in LOG_FILES:
                self.assertIn(
                    rel_path.name,
                    stdout,
                    f"Bootstrap output should mention {rel_path.name}",
                )

    def test_bootstrap_into_reports_each_log_update_once(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            updated_lines = [
                line.strip()
                for line in (result.stdout or "").splitlines()
                if line.startswith("Updated:")
            ]
            self.assertTrue(updated_lines, "Updated output should not be empty")

            counts = {rel_path: 0 for rel_path in LOG_FILES}
            for line in updated_lines:
                dest_str = line.split("Updated:", 1)[1].strip()
                dest_path = Path(dest_str)
                try:
                    relative = dest_path.relative_to(tmp_dir)
                except ValueError:
                    continue
                for rel_path in LOG_FILES:
                    if relative == rel_path:
                        counts[rel_path] += 1

            for rel_path, occurrences in counts.items():
                self.assertEqual(
                    occurrences,
                    1,
                    f"Updated output should mention {rel_path.name} exactly once",
                )

    def test_bootstrap_into_preserves_existing_log_marker(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)

            for rel_path in LOG_FILES:
                target = Path(tmp_dir) / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"# {rel_path.name}\\n{LOG_MARKER}seeded\\n")

            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            for rel_path in LOG_FILES:
                content = (Path(tmp_dir) / rel_path).read_text(encoding="utf-8")
                self.assertEqual(
                    content.count(LOG_MARKER),
                    1,
                    f"{rel_path.name} should keep a single marker when it already existed",
                )

    def test_root_templates_in_primary_flow_receive_markers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            template_headers = {
                "AGENTS.md": "# AGENTS.md",
                "pp.yml": "threshold_lines: 200",
            }
            for rel_path, expected_header in template_headers.items():
                file_path = Path(tmp_dir) / rel_path
                self.assertTrue(
                    file_path.exists(),
                    f"{rel_path} should exist after bootstrapping",
                )
                content = file_path.read_text(encoding="utf-8")
                self.assertIn("PezzosCode bootstrap", content)
                first_non_empty = next(
                    (line for line in content.splitlines() if line.strip()),
                    "",
                )
                self.assertEqual(
                    first_non_empty,
                    expected_header,
                    f"{rel_path} should keep its canonical header",
                )

    def test_bootstrap_into_copies_root_templates_and_skills(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            expectations = [
                {
                    "rel": Path("AGENTS.md"),
                    "header": "# AGENTS.md",
                    "marker": LOG_MARKER,
                },
                {
                    "rel": Path("pp.yml"),
                    "header": "threshold_lines: 200",
                    "marker": SCRIPT_MARKER,
                },
                {
                    "rel": Path(".codex/skills/context-to-product/SKILL.md"),
                    "header_contains": "name: context-to-product",
                    "marker": LOG_MARKER,
                },
            ]

            stdout = result.stdout or ""
            for expectation in expectations:
                rel_path = expectation["rel"]
                dest = Path(tmp_dir) / rel_path
                self.assertTrue(
                    dest.exists(),
                    f"{rel_path} should land in the target repo",
                )

                content = dest.read_text(encoding="utf-8")
                self.assertIn(
                    "PezzosCode bootstrap",
                    content,
                    f"{rel_path} should receive a bootstrap marker",
                )

                if "header" in expectation:
                    first_non_empty = next(
                        (line for line in content.splitlines() if line.strip()),
                        "",
                    )
                    self.assertEqual(
                        first_non_empty,
                        expectation["header"],
                        f"{rel_path} should keep its canonical header",
                    )

                if "header_contains" in expectation:
                    self.assertIn(
                        expectation["header_contains"],
                        content,
                        f"{rel_path} should retain its identifying signature",
                    )

                marker = expectation["marker"]
                self.assertEqual(
                    content.count(marker),
                    1,
                    f"{rel_path} should keep exactly one bootstrap marker",
                )

            for snippet in (
                "AGENTS.md",
                "pp.yml",
                "context-to-product/SKILL.md",
            ):
                self.assertIn(
                    snippet,
                    stdout,
                    f"Bootstrap output should mention {snippet}",
                )

    def test_bootstrap_into_logs_marker_output_consistently(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            updated_lines = [
                line.strip()
                for line in (result.stdout or "").splitlines()
                if line.startswith("Updated:")
            ]
            self.assertTrue(updated_lines, "Updated output should not be empty")

            for rel_path in LOG_FILES:
                dest = Path(tmp_dir) / rel_path
                self.assertTrue(
                    dest.exists(),
                    f"{rel_path.name} should exist after bootstrapping",
                )

                content = dest.read_text(encoding="utf-8")
                self.assertEqual(
                    content.count(LOG_MARKER),
                    1,
                    f"{rel_path.name} should retain a single bootstrap marker",
                )

                occurrences = sum(1 for line in updated_lines if str(dest) in line)
                self.assertEqual(
                    occurrences,
                    1,
                    f"Updated output should mention {rel_path.name} exactly once",
                )

    def test_log_headers_survive_copy(self):
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
                first_non_empty = next(
                    (
                        line
                        for line in target.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ),
                    "",
                )
                self.assertEqual(
                    first_non_empty,
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
