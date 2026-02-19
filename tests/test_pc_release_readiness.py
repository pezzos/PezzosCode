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

            expected = (root / "docs/00-context/expected-features.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(expected.count("<!-- release-readiness:start -->"), 1)
            self.assertEqual(expected.count("<!-- release-readiness:end -->"), 1)

    def test_ready_decision_when_all_features_are_completed(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_expected_features(root)
            write_feature(root, "01-alpha-feature", "Alpha Feature", "Completed")

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
