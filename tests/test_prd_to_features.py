import importlib.util
from importlib.machinery import SourceFileLoader
import json
import tempfile
import unittest
from pathlib import Path


TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "prd-to-features"


def load_tool():
    loader = SourceFileLoader("prd_to_features", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def write_template(root: Path) -> None:
    template_dir = root / "docs" / "02-features" / "feature-template"
    template_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "feature-spec.md",
        "tech-design.md",
        "dev-tasks.md",
        "test-plan.md",
        "planner-log.md",
        "reporter-log.md",
        "validation-log.md",
    ]:
        if name == "dev-tasks.md":
            content = (
                "# Development Tasks: [Feature Name]\n\n"
                "## Overview\n\n"
                "Status: Not Started\n\n"
                "## Execution Log\n"
            )
        else:
            content = f"# {name}\n"
        (template_dir / name).write_text(content, encoding="utf-8")


def write_prd(root: Path, content: str) -> None:
    prd_path = root / "docs" / "01-product"
    prd_path.mkdir(parents=True, exist_ok=True)
    (prd_path / "prd.md").write_text(content, encoding="utf-8")


def write_logs(root: Path, implementation: str = "", decision: str = "") -> None:
    logs_dir = root / "docs" / "03-logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "implementation-log.md").write_text(implementation, encoding="utf-8")
    (logs_dir / "decision-log.md").write_text(decision, encoding="utf-8")


def write_order_plan(root: Path, ordered_feature_slugs: list[str]) -> None:
    features_dir = root / "docs" / "02-features"
    features_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "generated_at": "2026-02-16T00:00:00Z",
        "ordered_feature_slugs": ordered_feature_slugs,
        "dependencies": {},
        "ordered_features": [],
        "decisions": [],
    }
    (features_dir / "feature-order.json").write_text(
        json.dumps(payload, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )


class PrdToFeaturesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_template(self.root)
        self.tool = load_tool()

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_missing_features_from_prd(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
| P1       | Beta Feature | X | Y |

## Process Features

- [ ] Gamma Feature (P1): Details
- [ ] Delta Feature (P2): Details
"""
        write_prd(self.root, prd)
        summary = self.tool.apply_prd_to_features(self.root)
        created = {item.name for item in summary["created"]}
        self.assertEqual(
            created,
            {"01-alpha-feature", "02-beta-feature"},
        )
        for name in created:
            self.assertTrue((self.root / "docs/02-features" / name).exists())

    def test_process_features_are_included_only_when_opted_in(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |

## Process Features

- [ ] Gamma Feature (P1): Details
"""
        write_prd(self.root, prd)

        summary_default = self.tool.apply_prd_to_features(self.root)
        created_default = {item.name for item in summary_default["created"]}
        self.assertEqual(created_default, {"01-alpha-feature"})

        with tempfile.TemporaryDirectory() as tmp_dir:
            second_root = Path(tmp_dir)
            write_template(second_root)
            write_prd(second_root, prd)
            summary_opt_in = self.tool.apply_prd_to_features(
                second_root, include_process_features=True
            )
            created_opt_in = {item.name for item in summary_opt_in["created"]}
            self.assertEqual(created_opt_in, {"01-alpha-feature", "02-gamma-feature"})

    def test_create_hydrates_core_docs(self):
        prd = """## Prioritized Feature List

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | Deliver alpha workflow | Key path |
"""
        write_prd(self.root, prd)
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["created"]), 1)

        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_spec = (feature_dir / "feature-spec.md").read_text(encoding="utf-8")
        dev_tasks = (feature_dir / "dev-tasks.md").read_text(encoding="utf-8")

        self.assertIn("Feature Specification: Alpha Feature", feature_spec)
        self.assertNotIn("[Feature Name]", feature_spec)
        self.assertIn("Status: Not Started", dev_tasks)
        self.assertIn("Product Surfaces: CLI", dev_tasks)

    def test_feature_order_plan_reorders_feature_indexes_for_creation(self):
        prd = """## Prioritized Feature List

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | Deliver alpha workflow | Key path |
| P1       | Beta Feature | Deliver beta workflow | Depends on alpha |
"""
        write_prd(self.root, prd)
        write_order_plan(self.root, ["beta-feature", "alpha-feature"])

        summary = self.tool.apply_prd_to_features(self.root)
        created_names = [item.name for item in summary["created"]]
        self.assertEqual(created_names, ["01-beta-feature", "02-alpha-feature"])

    def test_generated_dev_tasks_starts_with_no_runs_placeholder(self):
        prd = """## Prioritized Feature List

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | Deliver alpha workflow | Key path |
"""
        write_prd(self.root, prd)
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["created"]), 1)

        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        dev_tasks = (feature_dir / "dev-tasks.md").read_text(encoding="utf-8")
        self.assertIn("## Execution Log", dev_tasks)
        self.assertIn("- No runs yet.", dev_tasks)
        self.assertNotIn("### WI-YYYYMMDD-01 - Work item execution", dev_tasks)

    def test_skip_done_feature(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: Done\n", encoding="utf-8"
        )
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["created"]), 0)
        self.assertTrue(
            any("Status: Done" in item.reason for item in summary["skipped"])
        )

    def test_done_feature_slug_is_frozen_even_when_index_collides(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        drift_dir = self.root / "docs/02-features/01-old-slug"
        drift_dir.mkdir(parents=True)
        (drift_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: In Progress\n", encoding="utf-8"
        )
        done_dir = self.root / "docs/02-features/03-alpha-feature"
        done_dir.mkdir(parents=True)
        (done_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: Done\n", encoding="utf-8"
        )
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["created"]), 0)
        self.assertTrue(
            any(item.name == "03-alpha-feature" for item in summary["skipped"])
        )
        self.assertTrue(
            any("Status: Done" in item.reason for item in summary["skipped"])
        )

    def test_update_missing_files_for_existing_not_done(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: In Progress\n", encoding="utf-8"
        )
        (feature_dir / "feature-spec.md").write_text(
            "# feature-spec\n", encoding="utf-8"
        )
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["updated"]), 1)
        self.assertTrue((feature_dir / "test-plan.md").exists())

    def test_existing_placeholder_docs_are_hydrated(self):
        prd = """## Prioritized Feature List

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | Deliver alpha workflow | Key path |
"""
        write_prd(self.root, prd)
        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "dev-tasks.md").write_text(
            "# Development Tasks: [Feature Name]\n\nStatus: In Progress\n\n## Execution Log\n",
            encoding="utf-8",
        )
        (feature_dir / "feature-spec.md").write_text(
            "# Feature Specification: [Feature Name]\n", encoding="utf-8"
        )

        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["updated"]), 1)
        self.assertIn("hydrated", summary["updated"][0].reason)
        hydrated_spec = (feature_dir / "feature-spec.md").read_text(encoding="utf-8")
        self.assertIn("Feature Specification: Alpha Feature", hydrated_spec)
        self.assertNotIn("[Feature Name]", hydrated_spec)

    def test_missing_status_line_treated_as_not_done(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "dev-tasks.md").write_text(
            "## Overview\n\nNo status here\n", encoding="utf-8"
        )
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["updated"]), 1)
        self.assertTrue(
            any("Status line not found" in item.reason for item in summary["updated"])
        )

    def test_autofixes_missing_execution_log_for_existing_feature(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: In Progress\n\n## Task Breakdown\n",
            encoding="utf-8",
        )
        for name in ["feature-spec.md", "tech-design.md", "test-plan.md"]:
            (feature_dir / name).write_text(f"# {name}\n", encoding="utf-8")

        summary = self.tool.apply_prd_to_features(self.root)
        content = (feature_dir / "dev-tasks.md").read_text(encoding="utf-8")

        self.assertIn("## Execution Log", content)
        self.assertEqual(len(summary["updated"]), 1)
        self.assertTrue(
            "Execution Log" in summary["updated"][0].reason
            or "hydrated" in summary["updated"][0].reason
        )

    def test_slug_drift_by_index_creates_next_free_feature(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        drift_dir = self.root / "docs/02-features/01-old-slug"
        drift_dir.mkdir(parents=True)
        (drift_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: In Progress\n", encoding="utf-8"
        )
        summary = self.tool.apply_prd_to_features(self.root)
        created = [item.name for item in summary["created"]]
        self.assertIn("02-alpha-feature", created)
        drift_reasons = [item.reason for item in summary["created"]]
        self.assertTrue(
            any("created at index 02" in reason for reason in drift_reasons)
        )

    def test_slug_drift_append_creation_is_idempotent(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        drift_dir = self.root / "docs/02-features/01-old-slug"
        drift_dir.mkdir(parents=True)
        (drift_dir / "dev-tasks.md").write_text(
            "## Overview\n\nStatus: In Progress\n", encoding="utf-8"
        )
        first = self.tool.apply_prd_to_features(self.root)
        self.assertEqual([item.name for item in first["created"]], ["02-alpha-feature"])
        second = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(second["created"]), 0)
        feature_dirs = sorted(
            path.name
            for path in (self.root / "docs/02-features").iterdir()
            if path.is_dir() and "alpha-feature" in path.name
        )
        self.assertEqual(feature_dirs, ["02-alpha-feature"])

    def test_skip_features_marked_deferred_in_logs(self):
        prd = """## Prioritized Feature List

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        write_logs(
            self.root,
            implementation="### 2026-02-14\n- Alpha Feature deferred pending PO approval.\n",
            decision="",
        )
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["created"]), 0)
        self.assertTrue(
            any("deferred marker" in item.reason for item in summary["skipped"])
        )

    def test_bold_status_done_is_skipped(self):
        prd = """## Prioritized Feature List

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        feature_dir = self.root / "docs/02-features/01-alpha-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "dev-tasks.md").write_text(
            "## Overview\n\n**Status:** Done\n\n## Execution Log\n",
            encoding="utf-8",
        )
        summary = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(summary["created"]), 0)
        self.assertTrue(
            any("Status: Done" in item.reason for item in summary["skipped"])
        )

    def test_idempotent_rerun_produces_no_changes(self):
        prd = """## Prioritized Feature List (Template)

| Priority | Feature | Outcome | Notes |
| -------- | ------- | ------- | ----- |
| P0       | Alpha Feature | X | Y |
"""
        write_prd(self.root, prd)
        first = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(first["created"]), 1)
        second = self.tool.apply_prd_to_features(self.root)
        self.assertEqual(len(second["created"]), 0)
        self.assertEqual(len(second["updated"]), 0)


if __name__ == "__main__":
    unittest.main()
