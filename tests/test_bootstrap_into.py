import json
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
LEGACY_BOOTSTRAP_MARKER = "PezzosCode bootstrap sha256:"
SKIP_PROMPT_RESPONSE = "s\n"
GATE_PHRASES = (
    "preflight validation gate",
    "template diff review gate",
    "conflict summary output",
)


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

    def test_bootstrap_into_stops_writing_legacy_bootstrap_markers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)
            readme_path = Path(tmp_dir) / "docs" / "README.md"
            self.assertTrue(readme_path.exists())
            readme_content = readme_path.read_text(encoding="utf-8")
            self.assertNotIn(LEGACY_BOOTSTRAP_MARKER, readme_content)

    def test_bootstrap_into_copies_docs_readme(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            readme_path = Path(tmp_dir) / "docs" / "README.md"
            self.assertTrue(readme_path.exists(), "README.md should be copied")
            readme_content = readme_path.read_text(encoding="utf-8")
            self.assertNotIn(
                LEGACY_BOOTSTRAP_MARKER,
                readme_content,
                "README.md should not receive a legacy marker footer",
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
            self.assertNotIn(
                LEGACY_BOOTSTRAP_MARKER,
                protocol_content,
                "Protocol doc should not retain legacy markers",
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

            tool_path = Path(tmp_dir) / "tools" / "pc-feature"
            self.assertTrue(
                tool_path.exists(),
                "Annotated tooling scripts should land in tools/",
            )
            tool_content = tool_path.read_text(encoding="utf-8")
            self.assertNotIn(
                LEGACY_BOOTSTRAP_MARKER,
                tool_content,
                "Tooling scripts should not have bootstrap marker footers",
            )
            self.assertIn("tools/pc-feature", result.stdout)

    def test_bootstrap_into_copies_runtime_lib_modules(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            lib_module_path = Path(tmp_dir) / "lib" / "pc_runner.py"
            self.assertTrue(
                lib_module_path.exists(),
                "Runtime lib modules should land in lib/ for tool imports.",
            )
            lib_module_content = lib_module_path.read_text(encoding="utf-8")
            self.assertNotIn(
                LEGACY_BOOTSTRAP_MARKER,
                lib_module_content,
                "Runtime lib modules should not have bootstrap marker footers",
            )
            self.assertIn("lib/pc_runner.py", result.stdout)

    def test_bootstrap_into_keeps_json_configs_valid(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            json_paths = (
                Path(tmp_dir) / "tools" / "pc-ticket-config.json",
                Path(tmp_dir) / "tools" / "log-compaction-config.json",
            )
            for path in json_paths:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsInstance(
                    payload, dict, f"{path.name} should parse as JSON"
                )

    def test_bootstrap_into_deploys_prompts_as_living_files_only(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            source_prompts = sorted(
                path.name
                for path in (ROOT / "tools" / "templates" / "prompts").glob("*.md")
            )
            prompt_dir = Path(tmp_dir) / "prompts"
            self.assertTrue(
                prompt_dir.exists(),
                "prompts/ should be created from template prompt assets",
            )
            target_prompts = sorted(path.name for path in prompt_dir.glob("*.md"))
            self.assertEqual(
                target_prompts,
                source_prompts,
                "Bootstrap should materialize all prompt templates under prompts/",
            )
            self.assertFalse(
                (Path(tmp_dir) / "tools" / "templates").exists(),
                "Bootstrap should deploy template assets as living files, not ship tools/templates/",
            )

    def test_bootstrap_into_copies_log_assets(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            for rel_path in LOG_FILES:
                dest = Path(tmp_dir) / rel_path
                self.assertTrue(dest.exists(), f"{rel_path} should be copied")
                content = dest.read_text(encoding="utf-8")
                self.assertNotIn(
                    LEGACY_BOOTSTRAP_MARKER,
                    content,
                    f"{rel_path.name} should not contain legacy markers",
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

    def test_bootstrap_into_preserves_existing_protected_logs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)

            seeded_content = {}
            for rel_path in LOG_FILES:
                target = Path(tmp_dir) / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                seeded_content[rel_path] = (
                    f"# {rel_path.name}\n<!-- {LEGACY_BOOTSTRAP_MARKER}seeded -->\n"
                )
                target.write_text(seeded_content[rel_path], encoding="utf-8")

            result = run_bootstrap_into([tmp_dir])
            self.assertEqual(result.returncode, 0)

            for rel_path in LOG_FILES:
                content = (Path(tmp_dir) / rel_path).read_text(encoding="utf-8")
                self.assertIn(
                    LEGACY_BOOTSTRAP_MARKER,
                    content,
                    f"{rel_path.name} should remain untouched because logs are protected",
                )
                self.assertEqual(content, seeded_content[rel_path])

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
                self.assertNotIn(LEGACY_BOOTSTRAP_MARKER, content)
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
                },
                {
                    "rel": Path("pp.yml"),
                    "header": "threshold_lines: 200",
                },
                {
                    "rel": Path(".codex/skills/context-to-product/SKILL.md"),
                    "header_contains": "name: context-to-product",
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
                self.assertNotIn(
                    LEGACY_BOOTSTRAP_MARKER,
                    content,
                    f"{rel_path} should not receive legacy marker footers",
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
                self.assertNotIn(
                    LEGACY_BOOTSTRAP_MARKER,
                    content,
                    f"{rel_path.name} should not contain legacy markers",
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
            initial = run_bootstrap_into([tmp_dir])
            self.assertEqual(initial.returncode, 0)

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
                self.assertNotIn(
                    LEGACY_BOOTSTRAP_MARKER,
                    content,
                    f"{rel_path.name} should not contain legacy markers",
                )

    def test_update_reapply_primary_flow_reports_gates(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            initial = run_bootstrap_into([tmp_dir])
            self.assertEqual(initial.returncode, 0)

            readme_path = Path(tmp_dir) / "docs" / "README.md"
            existing = readme_path.read_text(encoding="utf-8")
            readme_path.write_text(existing + "\nlocal change\n", encoding="utf-8")

            result = run_bootstrap_into(
                ["--reapply", "--verbose", tmp_dir],
            )

            self.assertEqual(result.returncode, 0)
            combined_output = f"{result.stdout or ''}\n{result.stderr or ''}".lower()

            for gate in GATE_PHRASES:
                self.assertIn(
                    gate,
                    combined_output,
                    f"Reapply runs should mention the {gate}.",
                )
            self.assertNotIn("choose action", combined_output)

    def test_update_reapply_exit_code_and_log_outputs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            init_git_repo(tmp_dir)
            run_bootstrap_into([tmp_dir])

            readme_path = Path(tmp_dir) / "docs" / "README.md"
            base_content = readme_path.read_text(encoding="utf-8")
            readme_path.write_text(base_content + "\nlocal change\n", encoding="utf-8")

            result = run_bootstrap_into(
                ["--reapply", "--verbose", tmp_dir],
            )

            self.assertEqual(
                result.returncode,
                0,
                "Reapply flow should exit successfully while forcing overwrite.",
            )

            stderr = (result.stderr or "").lower()
            self.assertIn(
                "template diff review gate: reviewing the diff for docs/readme.md before acting.",
                stderr,
                "The diff gate message for README.md should appear in stderr.",
            )
            self.assertIn(
                "conflict summary output: docs/readme.md -> overwrite (reapply).",
                stderr,
                "Conflict summaries should mention reapply overwrite behavior.",
            )
            self.assertNotIn("choose action", stderr)
            self.assertNotIn(
                "local change",
                readme_path.read_text(encoding="utf-8"),
                "Reapply should overwrite README changes without prompting.",
            )

            for rel_path in LOG_FILES:
                dest = Path(tmp_dir) / rel_path
                self.assertTrue(dest.exists(), f"{rel_path.name} should still exist.")
                self.assertNotIn(
                    LEGACY_BOOTSTRAP_MARKER,
                    dest.read_text(encoding="utf-8"),
                    f"{rel_path.name} should not contain legacy marker text.",
                )


if __name__ == "__main__":
    unittest.main()
