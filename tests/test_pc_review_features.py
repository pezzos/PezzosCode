import importlib.util
from importlib.machinery import SourceFileLoader
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
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

    def test_deterministic_security_keys_are_stable(self):
        keys = self.tool.deterministic_security_keys(
            "Feature accepts input parameter and writes logs to offload path."
        )
        self.assertIn("SEC-INPUT-VALIDATION", keys)
        self.assertIn("SEC-LOG-REDACTION", keys)
        self.assertTrue(all(item.startswith("SEC-") for item in keys))

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
                (
                    "# Feature Specification: Alpha Feature\n\n"
                    "## Functional Requirements\n\n"
                    "- Input parameter drives output path behavior.\n"
                ),
                encoding="utf-8",
            )
            (feature_dir / "dev-tasks.md").write_text(
                (
                    "# Development Tasks: Alpha Feature\n\n"
                    "Status: Not Started\n\n"
                    "## Execution Log\n\n- No runs yet.\n\n"
                    "## Task Breakdown\n\n- [ ] placeholder\n"
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
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

            self.assertIn("## Automated Review Summary", spec_content)
            self.assertIn("<!-- review-findings:start -->", spec_content)
            self.assertIn("### Security Constraints", spec_content)
            self.assertIn("### Product Constraints", spec_content)
            self.assertIn("SEC-01-", spec_content)
            self.assertIn("PROD-01-", spec_content)
            self.assertNotIn("Action:", spec_content)

            self.assertIn("## Review Findings Backlog", dev_tasks_content)
            self.assertIn("<!-- review-backlog:start -->", dev_tasks_content)
            self.assertIn("### Patcher Tasks", dev_tasks_content)
            self.assertIn("### Human Validation Requests", dev_tasks_content)
            self.assertIn("SEC-01-", dev_tasks_content)
            self.assertIn("PROD-01-", dev_tasks_content)
            self.assertIn("Action:", dev_tasks_content)
            self.assertIn("Acceptance:", dev_tasks_content)
            self.assertNotIn("Reviewer:", dev_tasks_content)
            self.assertEqual(report_payload["version"], 3)
            self.assertEqual(report_payload["totals"]["features_reviewed"], 1)
            self.assertGreater(report_payload["totals"]["security_findings"], 0)
            self.assertGreater(report_payload["totals"]["product_findings"], 0)
            self.assertIn("human_validation_requests", report_payload["totals"])
            self.assertEqual(
                report_payload["features"][0]["feature_id"], "01-alpha-feature"
            )
            first_security = report_payload["features"][0]["security_findings"][0]
            self.assertIn("blocking", first_security)
            self.assertNotIn("owner", first_security)
            self.assertNotIn("phase", first_security)
            self.assertNotIn("reviewer", first_security)

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
                (
                    "# Feature Specification: Alpha Feature\n\n"
                    "## Functional Requirements\n\n"
                    "- Input parameter drives output path behavior.\n"
                ),
                encoding="utf-8",
            )
            (feature_dir / "dev-tasks.md").write_text(
                (
                    "# Development Tasks: Alpha Feature\n\n"
                    "Status: Not Started\n\n"
                    "## Execution Log\n\n- No runs yet.\n\n"
                    "## Task Breakdown\n\n- [ ] placeholder\n"
                ),
                encoding="utf-8",
            )

            command = [
                "python3",
                str(TOOL_PATH),
                f"--root={root}",
                "--role-mode=deterministic",
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

    def test_review_command_skips_completed_by_default(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            feature_dir = root / "docs/02-features/01-alpha-feature"
            feature_dir.mkdir(parents=True, exist_ok=True)
            (root / "docs/01-product").mkdir(parents=True, exist_ok=True)

            original_spec = (
                "# Feature Specification: Alpha Feature\n\n"
                "## Functional Requirements\n\n- Input parameter drives output path behavior.\n"
            )
            original_tasks = (
                "# Development Tasks: Alpha Feature\n\n"
                "Status: Done\n\n"
                "## Execution Log\n\n- No runs yet.\n\n"
                "## Task Breakdown\n\n- [ ] placeholder\n"
            )
            (root / "docs/01-product/ux-ui.md").write_text(
                "# Global UX / UI Blueprint\n\n## User journeys\n\n", encoding="utf-8"
            )
            (feature_dir / "feature-spec.md").write_text(
                original_spec, encoding="utf-8"
            )
            (feature_dir / "dev-tasks.md").write_text(original_tasks, encoding="utf-8")

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
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

            self.assertEqual(
                (feature_dir / "feature-spec.md").read_text(encoding="utf-8"),
                original_spec,
            )
            self.assertEqual(
                (feature_dir / "dev-tasks.md").read_text(encoding="utf-8"),
                original_tasks,
            )
            report_payload = json.loads(
                (root / "docs/03-logs/review-features-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                report_payload["features"][0]["status"], "skipped-completed"
            )
            self.assertEqual(report_payload["totals"]["features_reviewed"], 0)
            self.assertEqual(report_payload["totals"]["features_skipped_completed"], 1)

    def test_review_command_defaults_to_ordered_features(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            features_root = root / "docs/02-features"
            ordered_feature = features_root / "22-target-feature"
            legacy_feature = features_root / "01-legacy-feature"
            ordered_feature.mkdir(parents=True, exist_ok=True)
            legacy_feature.mkdir(parents=True, exist_ok=True)
            (root / "docs/01-product").mkdir(parents=True, exist_ok=True)

            (root / "docs/01-product/ux-ui.md").write_text(
                "# Global UX / UI Blueprint\n\n## User journeys\n\n", encoding="utf-8"
            )
            (features_root / "feature-order.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "ordered_feature_slugs": ["target-feature"],
                    },
                    ensure_ascii=True,
                    indent=2,
                ),
                encoding="utf-8",
            )

            for feature_dir, title in (
                (ordered_feature, "Target Feature"),
                (legacy_feature, "Legacy Feature"),
            ):
                (feature_dir / "feature-spec.md").write_text(
                    (
                        f"# Feature Specification: {title}\n\n"
                        "## Functional Requirements\n\n"
                        "- Input parameter drives output path behavior.\n"
                    ),
                    encoding="utf-8",
                )
                (feature_dir / "dev-tasks.md").write_text(
                    (
                        f"# Development Tasks: {title}\n\n"
                        "Status: Not Started\n\n"
                        "## Execution Log\n\n- No runs yet.\n\n"
                        "## Task Breakdown\n\n- [ ] placeholder\n"
                    ),
                    encoding="utf-8",
                )

            legacy_spec_before = (legacy_feature / "feature-spec.md").read_text(
                encoding="utf-8"
            )
            legacy_tasks_before = (legacy_feature / "dev-tasks.md").read_text(
                encoding="utf-8"
            )

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
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

            report_payload = json.loads(
                (root / "docs/03-logs/review-features-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report_payload["totals"]["features_selected"], 1)
            self.assertEqual(report_payload["totals"]["features_reviewed"], 1)
            self.assertEqual(
                [item["feature_id"] for item in report_payload["features"]],
                ["22-target-feature"],
            )
            self.assertEqual(
                (legacy_feature / "feature-spec.md").read_text(encoding="utf-8"),
                legacy_spec_before,
            )
            self.assertEqual(
                (legacy_feature / "dev-tasks.md").read_text(encoding="utf-8"),
                legacy_tasks_before,
            )

    def test_run_security_role_uses_security_expert_profile_by_default(self):
        captured = {"profile": None}

        def fake_codex_exec_json(**kwargs):
            captured["profile"] = kwargs.get("profile")
            return {"decision": "APPROVE", "selected_keys": [], "evidence": {}}

        with mock.patch.dict(self.tool.os.environ, {}, clear=False):
            self.tool.os.environ.pop("REVIEW_SECURITY_PROFILE", None)
            with mock.patch.object(
                self.tool,
                "codex_exec_json",
                side_effect=fake_codex_exec_json,
            ):
                findings = self.tool.run_security_role(
                    root=ROOT,
                    role_mode=self.tool.ROLE_MODE_CODEX,
                    feature_id="01-alpha-feature",
                    feature_key="01",
                    feature_title="Alpha Feature",
                    feature_spec_content="## Feature Requirements\n- x",
                    dev_tasks_content="## Task Breakdown\n- [ ] x",
                    ux_content="## User journeys",
                )

        self.assertEqual(captured["profile"], "SecurityExpert")
        self.assertEqual(findings, [])

    def test_run_product_role_uses_product_manager_profile_by_default(self):
        captured = {"profile": None}

        def fake_codex_exec_json(**kwargs):
            captured["profile"] = kwargs.get("profile")
            return {"decision": "APPROVE", "selected_keys": [], "evidence": {}}

        with mock.patch.dict(self.tool.os.environ, {}, clear=False):
            self.tool.os.environ.pop("REVIEW_PM_PROFILE", None)
            with mock.patch.object(
                self.tool,
                "codex_exec_json",
                side_effect=fake_codex_exec_json,
            ):
                findings = self.tool.run_product_role(
                    root=ROOT,
                    role_mode=self.tool.ROLE_MODE_CODEX,
                    feature_id="01-alpha-feature",
                    feature_key="01",
                    feature_title="Alpha Feature",
                    feature_spec_content="## Feature Requirements\n- x",
                    dev_tasks_content="## Task Breakdown\n- [ ] x",
                    ux_content="## User journeys",
                    security_findings=[],
                )

        self.assertEqual(captured["profile"], "ProductManager")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
