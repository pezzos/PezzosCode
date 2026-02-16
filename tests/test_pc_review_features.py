import importlib.util
from importlib.machinery import SourceFileLoader
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "pc-review-features"


def load_tool_module():
    loader = SourceFileLoader("pc_review_features", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class TestPcReviewFeatures(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool_module()

    def test_build_security_findings_reports_missing_controls(self):
        findings = self.tool.build_security_findings("01", "bare feature content")
        self.assertEqual(len(findings), 5)
        self.assertTrue(all(item.finding_id.startswith("SEC-01-") for item in findings))

    def test_review_command_injects_machine_managed_sections(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            feature_dir = root / "docs/02-features/01-alpha-feature"
            feature_dir.mkdir(parents=True, exist_ok=True)
            (root / "docs/01-product").mkdir(parents=True, exist_ok=True)

            (root / "docs/01-product/ux-ui.md").write_text(
                "# Global UX / UI Blueprint\n\n## User journeys\n\n", encoding="utf-8"
            )
            (feature_dir / "feature-spec.md").write_text(
                "# Feature Specification: Alpha Feature\n\n## Functional Requirements\n\n- Minimal\n",
                encoding="utf-8",
            )
            (feature_dir / "dev-tasks.md").write_text(
                "# Development Tasks: Alpha Feature\n\n## Execution Log\n\n- No runs yet.\n\n## Task Breakdown\n\n- [ ] placeholder\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--skip-schema-check",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(
                    f"pc-review-features failed: {result.stderr}\n{result.stdout}"
                )

            spec_content = (feature_dir / "feature-spec.md").read_text(encoding="utf-8")
            dev_tasks_content = (feature_dir / "dev-tasks.md").read_text(
                encoding="utf-8"
            )
            report_payload = json.loads(
                (root / "docs/03-logs/review-features-report.json").read_text(
                    encoding="utf-8"
                )
            )

            self.assertIn("## Automated Review Findings", spec_content)
            self.assertIn("<!-- review-findings:start -->", spec_content)
            self.assertIn("SEC-01-", spec_content)
            self.assertIn("PROD-01-", spec_content)

            self.assertIn("## Review Findings Backlog", dev_tasks_content)
            self.assertIn("<!-- review-backlog:start -->", dev_tasks_content)
            self.assertIn("SEC-01-", dev_tasks_content)
            self.assertIn("PROD-01-", dev_tasks_content)
            self.assertEqual(report_payload["totals"]["features_reviewed"], 1)
            self.assertGreater(report_payload["totals"]["security_findings"], 0)
            self.assertGreater(report_payload["totals"]["product_findings"], 0)
            self.assertEqual(
                report_payload["features"][0]["feature_id"], "01-alpha-feature"
            )

    def test_review_command_is_idempotent_for_markers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            feature_dir = root / "docs/02-features/01-alpha-feature"
            feature_dir.mkdir(parents=True, exist_ok=True)
            (root / "docs/01-product").mkdir(parents=True, exist_ok=True)

            (root / "docs/01-product/ux-ui.md").write_text(
                "# Global UX / UI Blueprint\n\n## User journeys\n\n", encoding="utf-8"
            )
            (feature_dir / "feature-spec.md").write_text(
                "# Feature Specification: Alpha Feature\n\n## Functional Requirements\n\n- Minimal\n",
                encoding="utf-8",
            )
            (feature_dir / "dev-tasks.md").write_text(
                "# Development Tasks: Alpha Feature\n\n## Execution Log\n\n- No runs yet.\n\n## Task Breakdown\n\n- [ ] placeholder\n",
                encoding="utf-8",
            )

            command = [
                "python3",
                str(TOOL_PATH),
                f"--root={root}",
                "--skip-schema-check",
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
                    f"pc-review-features failed across reruns:\n"
                    f"first stderr={first.stderr}\nsecond stderr={second.stderr}"
                )

            spec_content = (feature_dir / "feature-spec.md").read_text(encoding="utf-8")
            dev_tasks_content = (feature_dir / "dev-tasks.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(spec_content.count("<!-- review-findings:start -->"), 1)
            self.assertEqual(
                dev_tasks_content.count("<!-- review-backlog:start -->"), 1
            )


if __name__ == "__main__":
    unittest.main()
