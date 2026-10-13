import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lib import codex_exec


class TestCodexExec(unittest.TestCase):
    def test_prepare_codex_env_sanitizes_and_copies_chatgpt_auth(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            auth_src = root / "auth-source.json"
            auth_src.write_text(
                json.dumps(
                    {
                        "auth_mode": "chatgpt",
                        "last_refresh": "2026-03-05T10:00:00.000000Z",
                    }
                ),
                encoding="utf-8",
            )
            base_env = {
                "OPENAI_API_KEY": "secret",
                "OPENAI_BILLING_API_KEY": "billing",
                "OPENAI_BASE_URL": "https://api.openai.com/v1",
                "OPENAI_ORG_ID": "org",
                "OPENAI_ORGANIZATION": "org-name",
                "OPENAI_PROJECT": "proj",
                "KEEP": "value",
            }
            with mock.patch.object(
                codex_exec, "auth_source_path", return_value=auth_src
            ):
                prepared = codex_exec.prepare_codex_env(
                    root,
                    ".codex_precommit",
                    error_prefix="test-wrapper",
                    base_env=base_env,
                )
                self.assertEqual(prepared.env["KEEP"], "value")
                self.assertEqual(
                    prepared.env["CODEX_HOME"], str(root / ".codex_precommit")
                )
                self.assertTrue(prepared.auth_dst.exists())
                copied = json.loads(prepared.auth_dst.read_text(encoding="utf-8"))
                self.assertEqual(copied["auth_mode"], "chatgpt")
                for var_name in codex_exec.OPENAI_ENV_VARS:
                    self.assertNotIn(var_name, prepared.env)

    def test_prepare_codex_env_requires_auth_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            missing_auth = root / "missing-auth.json"
            with mock.patch.object(
                codex_exec, "auth_source_path", return_value=missing_auth
            ):
                with self.assertRaises(codex_exec.CodexEnvError) as raised:
                    codex_exec.prepare_codex_env(
                        root,
                        ".codex_precommit",
                        error_prefix="test-wrapper",
                    )
        self.assertIn("required ChatGPT auth file missing", str(raised.exception))

    def test_prepare_codex_env_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            auth_src = root / "auth-source.json"
            auth_src.write_text("{invalid", encoding="utf-8")
            with mock.patch.object(
                codex_exec, "auth_source_path", return_value=auth_src
            ):
                with self.assertRaises(codex_exec.CodexEnvError) as raised:
                    codex_exec.prepare_codex_env(
                        root,
                        ".codex_precommit",
                        error_prefix="test-wrapper",
                    )
        self.assertIn("invalid auth.json", str(raised.exception))

    def test_prepare_codex_env_rejects_non_chatgpt_auth_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            auth_src = root / "auth-source.json"
            auth_src.write_text(
                json.dumps({"auth_mode": "api_key"}),
                encoding="utf-8",
            )
            with mock.patch.object(
                codex_exec, "auth_source_path", return_value=auth_src
            ):
                with self.assertRaises(codex_exec.CodexEnvError) as raised:
                    codex_exec.prepare_codex_env(
                        root,
                        ".codex_precommit",
                        error_prefix="test-wrapper",
                    )
        self.assertIn('must use auth_mode "chatgpt"', str(raised.exception))


if __name__ == "__main__":
    unittest.main()
