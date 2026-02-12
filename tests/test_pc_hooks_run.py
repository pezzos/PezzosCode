import importlib.machinery
import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PC_HOOKS_RUN_PATH = ROOT / "tools" / "pc-hooks-run"


def load_pc_hooks_module():
    loader = importlib.machinery.SourceFileLoader(
        "pc_hooks_run", str(PC_HOOKS_RUN_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcHooksRun(unittest.TestCase):
    def setUp(self):
        self.pc_hooks = load_pc_hooks_module()

    def test_summarize_output_filters_passed_and_skipped_lines(self):
        output = "\n".join(
            [
                "check json.................................................Passed",
                "ruff................................................................Failed",
                "- hook id: ruff",
                "- exit code: 1",
                "a.py:1:1: F401 unused import",
                "black...........................................(no files to check)Skipped",
            ]
        )

        summary_lines, omitted = self.pc_hooks.summarize_output(output, max_lines=20)

        self.assertEqual(omitted, 0)
        self.assertIn(
            "ruff................................................................Failed",
            summary_lines,
        )
        self.assertIn("- hook id: ruff", summary_lines)
        self.assertIn("a.py:1:1: F401 unused import", summary_lines)
        self.assertNotIn(
            "check json.................................................Passed",
            summary_lines,
        )
        self.assertNotIn(
            "black...........................................(no files to check)Skipped",
            summary_lines,
        )

    def test_write_offload_log_writes_payload_and_index_entry(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            pointer_id, log_path, index_path = self.pc_hooks.write_offload_log(
                "sample output\n", "pre-commit run --all-files", root
            )

            self.assertRegex(pointer_id, r"^[0-9a-f]{64}$")
            self.assertTrue(log_path.exists())
            self.assertEqual(log_path.read_text(encoding="utf-8"), "sample output\n")
            self.assertTrue(index_path.exists())

            entries = [
                json.loads(line)
                for line in index_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["id"], pointer_id)
            self.assertEqual(entries[0]["command"], "pre-commit run --all-files")
            self.assertEqual(entries[0]["path"], f".offload/{pointer_id}.txt")
            self.assertIn("timestamp", entries[0])
            self.assertIn("size_bytes", entries[0])

    def test_main_is_quiet_when_precommit_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            fake_precommit = root / "fake-pre-commit"
            fake_precommit.write_text(
                "#!/usr/bin/env bash\n"
                "printf 'ruff............................................................Passed\\n'\n"
                "exit 0\n",
                encoding="utf-8",
            )
            fake_precommit.chmod(0o755)

            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    status = self.pc_hooks.main(
                        [
                            "--hook-stage",
                            "pre-commit",
                            "--all-files",
                            "--pre-commit-bin",
                            str(fake_precommit),
                        ]
                    )
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(status, 0)
            self.assertEqual(stderr.getvalue(), "")
            self.assertFalse((root / ".offload").exists())

    def test_main_prints_concise_failure_and_offload_reference(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            fake_precommit = root / "fake-pre-commit"
            fake_precommit.write_text(
                "#!/usr/bin/env bash\n"
                "printf 'check json.................................................Passed\\n'\n"
                "printf 'ruff................................................................Failed\\n'\n"
                "printf -- '- hook id: ruff\\n'\n"
                "printf -- '- exit code: 1\\n'\n"
                "printf 'a.py:1:1: F401 unused import\\n'\n"
                "printf 'black...........................................(no files to check)Skipped\\n'\n"
                "exit 1\n",
                encoding="utf-8",
            )
            fake_precommit.chmod(0o755)

            previous_cwd = Path.cwd()
            try:
                os.chdir(root)
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    status = self.pc_hooks.main(
                        [
                            "--hook-stage",
                            "pre-commit",
                            "--all-files",
                            "--pre-commit-bin",
                            str(fake_precommit),
                        ]
                    )
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(status, 1)
            err = stderr.getvalue()
            self.assertIn("pre-commit: checks failed.", err)
            self.assertIn(
                "ruff................................................................Failed",
                err,
            )
            self.assertIn("- hook id: ruff", err)
            self.assertIn("a.py:1:1: F401 unused import", err)
            self.assertNotIn(
                "check json.................................................Passed", err
            )
            self.assertNotIn(
                "black...........................................(no files to check)Skipped",
                err,
            )
            self.assertIn("pre-commit: offload id:", err)

            pointer_line = next(
                line
                for line in err.splitlines()
                if line.startswith("pre-commit: offload id:")
            )
            pointer_id = pointer_line.rsplit(":", 1)[1].strip()
            log_path = root / ".offload" / f"{pointer_id}.txt"
            self.assertTrue(log_path.exists())
            raw_log = log_path.read_text(encoding="utf-8")
            self.assertIn("Passed", raw_log)
            self.assertIn("Skipped", raw_log)
            self.assertIn("Failed", raw_log)


if __name__ == "__main__":
    unittest.main()
