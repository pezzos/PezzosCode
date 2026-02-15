import importlib.util
import json
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


def load_module(path: Path, name: str):
    loader = SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PcAutofixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.mod = load_module(root / "tools" / "pc-autofix", "pc_autofix")

    def test_build_prompt_precommit_is_scoped(self):
        prompt = self.mod.build_prompt(
            "pre-commit",
            "ruff failed",
            ["tools/pc-precommit", "tools/pc-autofix"],
        )
        self.assertIn("Allowed files (edit only these paths)", prompt)
        self.assertIn("tools/pc-precommit", prompt)
        self.assertIn("tools/pc-autofix", prompt)
        self.assertIn("docs/03-logs/*", prompt)
        self.assertIn("Do not add features", prompt)

    def test_build_prompt_stash_conflict_mode(self):
        prompt = self.mod.build_prompt("stash-conflict", "conflicts", ["x"])
        self.assertIn("Resolve the git stash pop conflicts", prompt)
        self.assertNotIn("Allowed files", prompt)

    def test_compute_scope_violations(self):
        changed = {
            "tools/pc-autofix",
            "docs/03-logs/implementation-log.md",
            "README.md",
        }
        allowed = {"tools/pc-autofix"}
        violations = self.mod.compute_scope_violations(changed, allowed)
        self.assertEqual(
            violations,
            ["README.md", "docs/03-logs/implementation-log.md"],
        )

    def test_build_prompt_precommit_sorts_and_deduplicates_allowed_paths(self):
        prompt = self.mod.build_prompt(
            "pre-commit", "ruff failed", ["b.py", "a.py", "b.py"]
        )
        self.assertLess(prompt.index("- a.py"), prompt.index("- b.py"))
        self.assertEqual(prompt.count("- b.py"), 1)

    def test_validate_scope_requires_allowed_paths_for_precommit(self):
        with self.assertRaises(SystemExit) as raised:
            self.mod.validate_scope("pre-commit", [], Path("."))
        self.assertEqual(raised.exception.code, 1)

    def test_source_auth_is_newer_uses_last_refresh(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "src-auth.json"
            dst = Path(tmpdir) / "dst-auth.json"
            src.write_text(
                json.dumps(
                    {
                        "last_refresh": "2026-02-15T08:00:00.000000Z",
                        "tokens": {"refresh_token": "src"},
                    }
                ),
                encoding="utf-8",
            )
            dst.write_text(
                json.dumps(
                    {
                        "last_refresh": "2026-02-10T08:00:00.000000Z",
                        "tokens": {"refresh_token": "dst"},
                    }
                ),
                encoding="utf-8",
            )
            self.assertTrue(self.mod.source_auth_is_newer(src, dst))

    def test_sync_auth_file_copies_when_source_is_newer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "src-auth.json"
            dst = Path(tmpdir) / "dst-auth.json"
            source_payload = {
                "last_refresh": "2026-02-15T08:00:00.000000Z",
                "tokens": {"refresh_token": "src"},
            }
            dst.write_text(
                json.dumps(
                    {
                        "last_refresh": "2026-02-10T08:00:00.000000Z",
                        "tokens": {"refresh_token": "dst"},
                    }
                ),
                encoding="utf-8",
            )
            src.write_text(json.dumps(source_payload), encoding="utf-8")

            copied = self.mod.sync_auth_file(src, dst)

            self.assertTrue(copied)
            self.assertEqual(
                json.loads(dst.read_text(encoding="utf-8")), source_payload
            )

    def test_is_auth_refresh_error_detects_reuse_errors(self):
        self.assertTrue(
            self.mod.is_auth_refresh_error(
                "ERROR: Your access token could not be refreshed because your refresh token was already used."
            )
        )
        self.assertFalse(self.mod.is_auth_refresh_error("some unrelated codex failure"))


if __name__ == "__main__":
    unittest.main()
