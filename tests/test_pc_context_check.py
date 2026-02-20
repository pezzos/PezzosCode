import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "pc-context-check"


def write_context_files(root: Path) -> None:
    files = {
        "docs/00-context/vision.md": "# Vision\n\nClear product direction.\n",
        "docs/00-context/users.md": "# Users\n\nPrimary user: Developer/PO.\n",
        "docs/00-context/system-map.md": "# System Map\n\nCLI -> tooling.\n",
        "docs/00-context/assumptions.md": "# Assumptions\n\n- Local execution.\n",
        "docs/00-context/context-boundaries-operating-model.md": (
            "# Context Boundaries\n\n## Scope Boundaries\n\n- Local CLI.\n"
        ),
        "docs/00-context/expected-features.md": (
            "# Expected Features\n\n## Feature Candidates\n\n"
            "- Feature: Core workflow hardening\n"
            "  - Owner: Product Owner\n"
            "  - Problem: Drift and ambiguity.\n"
            "  - Outcome: Deterministic gates and docs.\n"
            "  - Priority: P0\n"
            "  - Notes: Keep fail-closed behavior.\n"
        ),
    }
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class TestPcContextCheck(unittest.TestCase):
    def test_passes_with_complete_context(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_context_files(root)

            result = subprocess.run(
                ["python3", str(TOOL_PATH), f"--root={root}"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(
                    f"pc-context-check failed unexpectedly: {result.stderr}\n{result.stdout}"
                )

            report = json.loads(
                (root / "docs/03-logs/context-clarity-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["decision"], "PASS")
            self.assertEqual(report["issue_count"], 0)

    def test_blocks_when_open_questions_are_unresolved(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_context_files(root)
            boundaries_path = (
                root / "docs/00-context/context-boundaries-operating-model.md"
            )
            boundaries_path.write_text(
                (
                    "# Context Boundaries\n\n## Scope Boundaries\n\n- Local CLI.\n\n"
                    "## Open Questions\n\n- [ ] Should background execution be enabled?\n"
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(TOOL_PATH), f"--root={root}"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertNotEqual(result.returncode, 0)

            report = json.loads(
                (root / "docs/03-logs/context-clarity-report.json").read_text(
                    encoding="utf-8"
                )
            )
            issue_checks = {item["check"] for item in report["issues"]}
            self.assertIn("open-question-unresolved", issue_checks)

    def test_blocks_when_expected_feature_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_context_files(root)
            expected_path = root / "docs/00-context/expected-features.md"
            expected_path.write_text(
                (
                    "# Expected Features\n\n## Feature Candidates\n\n"
                    "- Feature: Missing outcome\n"
                    "  - Owner: Product Owner\n"
                    "  - Problem: Missing details\n"
                    "  - Priority: P0\n"
                    "  - Notes: Add later\n"
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(TOOL_PATH), f"--root={root}"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertNotEqual(result.returncode, 0)
            report = json.loads(
                (root / "docs/03-logs/context-clarity-report.json").read_text(
                    encoding="utf-8"
                )
            )
            issue_checks = {item["check"] for item in report["issues"]}
            self.assertIn("expected-feature-missing-outcome", issue_checks)


if __name__ == "__main__":
    unittest.main()
