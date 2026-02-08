import importlib.util
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


if __name__ == "__main__":
    unittest.main()
