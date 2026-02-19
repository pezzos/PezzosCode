import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "pc-release-readiness"


def write_expected_features(root: Path) -> None:
    path = root / "docs/00-context/expected-features.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        (
            "# Expected Features\n\n"
            "## Current Expected Features\n\n"
            "- Feature: Existing baseline\n"
            "  - Owner: Product Manager\n"
            "  - Problem: Baseline\n"
            "  - Outcome: Baseline\n"
            "  - Priority: P1\n"
            "  - Notes: Baseline\n"
        ),
        encoding="utf-8",
    )


def write_feature(root: Path, feature_id: str, title: str, status: str) -> None:
    feature_dir = root / "docs/02-features" / feature_id
    feature_dir.mkdir(parents=True, exist_ok=True)
    (feature_dir / "feature-spec.md").write_text(
        f"# Feature Specification: {title}\n",
        encoding="utf-8",
    )
    (feature_dir / "dev-tasks.md").write_text(
        (
            f"# Development Tasks: {title}\n\n"
            f"Status: {status}\n\n"
            "## Task Breakdown\n\n- [ ] Placeholder\n"
        ),
        encoding="utf-8",
    )


class TestPcReleaseReadiness(unittest.TestCase):
    def test_deterministic_mode_writes_report_and_expected_features_followups(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_expected_features(root)
            write_feature(root, "01-alpha-feature", "Alpha Feature", "In Progress")
            write_feature(root, "02-beta-feature", "Beta Feature", "Done")

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(
                    f"pc-release-readiness failed: {result.stderr}\n{result.stdout}"
                )

            report = json.loads(
                (root / "docs/03-logs/release-readiness-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["decision"], "NOT_READY")
            self.assertEqual(report["totals"]["actionable_release_tasks"], 1)
            self.assertEqual(report["totals"]["release_tasks"], 1)

            expected = (root / "docs/00-context/expected-features.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("<!-- release-readiness:start -->", expected)
            self.assertIn("<!-- release-readiness:end -->", expected)
            self.assertIn("Release readiness RR-001", expected)
            self.assertIn("01-alpha-feature", expected)

    def test_release_readiness_block_is_idempotent_across_reruns(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_expected_features(root)
            write_feature(root, "01-alpha-feature", "Alpha Feature", "In Progress")

            command = [
                "python3",
                str(TOOL_PATH),
                f"--root={root}",
                "--role-mode=deterministic",
            ]
            first = subprocess.run(
                command,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            second = subprocess.run(
                command,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if first.returncode != 0 or second.returncode != 0:
                self.fail(
                    "pc-release-readiness failed across reruns:\n"
                    f"first stderr={first.stderr}\nsecond stderr={second.stderr}"
                )

            expected_first = (root / "docs/00-context/expected-features.md").read_text(
                encoding="utf-8"
            )
            report_first = (
                root / "docs/03-logs/release-readiness-report.json"
            ).read_text(encoding="utf-8")

            third = subprocess.run(
                command,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if third.returncode != 0:
                self.fail(f"pc-release-readiness failed on third run: {third.stderr}")

            expected_second = (root / "docs/00-context/expected-features.md").read_text(
                encoding="utf-8"
            )
            report_second = (
                root / "docs/03-logs/release-readiness-report.json"
            ).read_text(encoding="utf-8")
            self.assertEqual(expected_second, expected_first)
            self.assertEqual(report_second, report_first)

    def test_existing_release_readiness_entry_is_continued_not_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            path = root / "docs/00-context/expected-features.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                (
                    "# Expected Features\n\n"
                    "## Current Expected Features\n\n"
                    "- Feature: Existing baseline\n"
                    "  - Owner: Product Manager\n"
                    "  - Problem: Baseline\n"
                    "  - Outcome: Baseline\n"
                    "  - Priority: P1\n"
                    "  - Notes: Baseline\n\n"
                    "## Release Readiness Follow-up Features (Auto-managed)\n\n"
                    "<!-- release-readiness:start -->\n\n"
                    "- Generated at: 2026-02-19T12:00:00Z\n"
                    "- Decision: NOT_READY\n"
                    "- Summary: Existing summary to preserve.\n"
                    "- Actionable follow-up features: 1\n\n"
                    "- Feature: Release readiness RR-007 - Existing wording\n"
                    "  - Owner: Product Manager\n"
                    "  - Problem: Existing problem to preserve.\n"
                    "  - Outcome: Existing outcome to preserve.\n"
                    "  - Priority: P0\n"
                    "  - Notes: Existing notes to preserve.\n"
                    "  - Source: release-readiness (RR-007)\n"
                    "  - Existing Feature Refs: 01-alpha-feature\n\n"
                    "<!-- release-readiness:end -->\n"
                ),
                encoding="utf-8",
            )
            write_feature(root, "01-alpha-feature", "Alpha Feature", "In Progress")

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(
                    f"pc-release-readiness failed: {result.stderr}\n{result.stdout}"
                )

            expected = path.read_text(encoding="utf-8")
            self.assertIn(
                "- Generated at: 2026-02-19T12:00:00Z",
                expected,
            )
            self.assertIn("- Summary: Existing summary to preserve.", expected)
            self.assertIn("Release readiness RR-007 - Existing wording", expected)
            self.assertIn("- Problem: Existing problem to preserve.", expected)
            self.assertIn("- Outcome: Existing outcome to preserve.", expected)
            self.assertIn("- Notes: Existing notes to preserve.", expected)

    def test_ready_decision_when_all_features_are_completed(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_expected_features(root)
            write_feature(root, "01-alpha-feature", "Alpha Feature", "Done")

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(
                    f"pc-release-readiness failed: {result.stderr}\n{result.stdout}"
                )

            report = json.loads(
                (root / "docs/03-logs/release-readiness-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["decision"], "READY")
            self.assertEqual(report["totals"]["release_tasks"], 0)
            self.assertEqual(report["totals"]["actionable_release_tasks"], 0)

            expected = (root / "docs/00-context/expected-features.md").read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "No release-readiness follow-up features required.",
                expected,
            )


if __name__ == "__main__":
    unittest.main()
