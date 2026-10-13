import importlib.util
import subprocess
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


def load_module(path: Path, name: str):
    loader = SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCodexAutofix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.mod = load_module(root / "tools" / "codex-autofix", "codex_autofix")

    def test_run_codex_uses_sanitized_env(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            message_path = Path(tmpdir) / "message.txt"
            jsonl_path = Path(tmpdir) / "output.jsonl"
            prepared = SimpleNamespace(
                env={"KEEP": "ok", "CODEX_HOME": str(Path(tmpdir) / ".codex_precommit")}
            )
            with mock.patch.object(
                self.mod.shutil, "which", return_value="/usr/bin/codex"
            ), mock.patch.object(
                self.mod.codex_exec, "prepare_codex_env", return_value=prepared
            ) as prepare_mock, mock.patch.object(
                self.mod.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(
                    args=["codex"],
                    returncode=0,
                    stdout="ok\n",
                ),
            ) as run_mock:
                completed = self.mod.run_codex("fix things", message_path, jsonl_path)

        self.assertEqual(completed.returncode, 0)
        prepare_mock.assert_called_once()
        self.assertEqual(run_mock.call_args.kwargs["env"], prepared.env)

    def test_run_codex_surfaces_auth_guard_failures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            message_path = Path(tmpdir) / "message.txt"
            jsonl_path = Path(tmpdir) / "output.jsonl"
            with mock.patch.object(
                self.mod.shutil, "which", return_value="/usr/bin/codex"
            ), mock.patch.object(
                self.mod.codex_exec,
                "prepare_codex_env",
                side_effect=self.mod.codex_exec.CodexEnvError("auth failure"),
            ):
                with self.assertRaises(self.mod.codex_exec.CodexEnvError) as raised:
                    self.mod.run_codex("fix things", message_path, jsonl_path)
        self.assertIn("auth failure", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
