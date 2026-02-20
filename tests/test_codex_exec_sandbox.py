import importlib.util
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_tool_module(module_name: str, tool_rel_path: str):
    tool_path = ROOT / tool_rel_path
    loader = SourceFileLoader(module_name, str(tool_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class TestCodexExecSandbox(unittest.TestCase):
    def _assert_codex_exec_is_read_only(self, module) -> None:
        with mock.patch.object(module.shutil, "which", return_value="/usr/bin/codex"):
            with mock.patch.object(
                module.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=0, stdout="{}", stderr=""),
            ) as run_mock:
                payload = module.codex_exec_json(
                    root=ROOT,
                    prompt="{}",
                    profile="TestProfile",
                    label="test-role",
                )

        self.assertEqual(payload, {})
        run_mock.assert_called_once()

        cmd = run_mock.call_args[0][0]
        self.assertEqual(cmd[0:4], ["codex", "-C", str(ROOT), "--profile"])
        self.assertIn("--sandbox", cmd)
        sandbox_idx = cmd.index("--sandbox")
        self.assertEqual(cmd[sandbox_idx + 1], "read-only")
        self.assertIn("--ask-for-approval", cmd)
        approval_idx = cmd.index("--ask-for-approval")
        self.assertEqual(cmd[approval_idx + 1], "never")
        self.assertEqual(cmd[-2:], ["exec", "{}"])

        kwargs = run_mock.call_args.kwargs
        self.assertEqual(kwargs["cwd"], str(ROOT))
        self.assertFalse(kwargs["check"])
        self.assertTrue(kwargs["text"])

    def test_pc_review_features_defaults_to_deterministic_role_mode(self):
        module = load_tool_module(
            "pc_review_features_sandbox", "tools/pc-review-features"
        )
        with mock.patch.dict(module.os.environ, {}, clear=False):
            module.os.environ.pop("REVIEW_ROLE_MODE", None)
            self.assertEqual(module.default_role_mode(), module.ROLE_MODE_DETERMINISTIC)
            module.os.environ["REVIEW_ROLE_MODE"] = module.ROLE_MODE_CODEX
            self.assertEqual(module.default_role_mode(), module.ROLE_MODE_CODEX)
            module.os.environ["REVIEW_ROLE_MODE"] = "invalid"
            self.assertEqual(module.default_role_mode(), module.ROLE_MODE_DETERMINISTIC)

    def test_pc_review_features_codex_exec_is_read_only(self):
        module = load_tool_module("pc_review_features_exec", "tools/pc-review-features")
        self._assert_codex_exec_is_read_only(module)

    def test_pc_prepare_features_codex_exec_is_read_only(self):
        module = load_tool_module(
            "pc_prepare_features_exec", "tools/pc-prepare-features"
        )
        self._assert_codex_exec_is_read_only(module)

    def test_pc_write_prd_codex_exec_is_read_only(self):
        module = load_tool_module("pc_write_prd_exec", "tools/pc-write-prd")
        self._assert_codex_exec_is_read_only(module)

    def test_pc_release_readiness_codex_exec_is_read_only(self):
        module = load_tool_module(
            "pc_release_readiness_exec", "tools/pc-release-readiness"
        )
        self._assert_codex_exec_is_read_only(module)


if __name__ == "__main__":
    unittest.main()
