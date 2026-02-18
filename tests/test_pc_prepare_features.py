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
TOOL_PATH = ROOT / "tools" / "pc-prepare-features"


def load_tool_module():
    loader = SourceFileLoader("pc_prepare_features", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class TestPcPrepareFeatures(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool_module()

    def test_resolve_dependency_graph_uses_override_for_unknown_dependency(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=(),
            ),
            self.tool.Feature(
                title="Beta Feature",
                priority="P1",
                slug="beta-feature",
                dependencies=("alpha",),
            ),
        ]

        graph, decisions = self.tool.resolve_dependency_graph(
            features,
            overrides={"AMB-001": 1},
        )

        self.assertIn("alpha-feature", graph["beta-feature"])
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["issue_id"], "AMB-001")
        self.assertEqual(decisions[0]["selected"], "map:alpha-feature")

    def test_cycle_resolution_uses_override_and_returns_acyclic_graph(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=("beta-feature",),
            ),
            self.tool.Feature(
                title="Beta Feature",
                priority="P1",
                slug="beta-feature",
                dependencies=("alpha-feature",),
            ),
        ]

        graph, decisions = self.tool.resolve_dependency_graph(
            features,
            overrides={"CYCLE-001": 1},
        )
        ordered = self.tool.topo_order([feature.slug for feature in features], graph)

        self.assertEqual(len(ordered), 2)
        self.assertEqual({item["type"] for item in decisions}, {"cycle"})

    def test_skip_generation_writes_design_ux_and_order_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "docs/01-product").mkdir(parents=True, exist_ok=True)
            (root / "docs/00-context").mkdir(parents=True, exist_ok=True)
            (root / "docs/02-features").mkdir(parents=True, exist_ok=True)
            (root / "tools").mkdir(parents=True, exist_ok=True)

            (root / "docs/01-product/prd.md").write_text(
                """## Prioritized Feature List

| Priority | Feature | Outcome | Notes | Dependencies |
| -------- | ------- | ------- | ----- | ------------ |
| P0       | Alpha Feature | Deliver alpha flow | Core path | - |
| P1       | Beta Feature | Deliver beta flow | Depends on alpha | Alpha Feature |
""",
                encoding="utf-8",
            )
            (root / "docs/00-context/context-boundaries-operating-model.md").write_text(
                """## Scope Boundaries
- Local CLI only
## Non-Goals
- No cloud runtime
## Operating Model
- Human executes explicit commands
""",
                encoding="utf-8",
            )
            (root / "tools/prd-to-features").write_text(
                """#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass(frozen=True)
class FeatureRecord:
    index: int
    title: str
    priority: str
    slug: str
    dependencies: tuple[str, ...]
    source: str
    outcome: str
    notes: str


def parse_prd_features(_text: str):
    return [
        FeatureRecord(1, \"Alpha Feature\", \"P0\", \"alpha-feature\", tuple(), \"table\", \"x\", \"\"),
        FeatureRecord(2, \"Beta Feature\", \"P1\", \"beta-feature\", (\"alpha-feature\",), \"table\", \"x\", \"\"),
    ]
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--skip-generation",
                    "--skip-schema-check",
                    "--role-mode=deterministic",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(
                    f"pc-prepare-features failed: {result.stderr}\n{result.stdout}"
                )

            design_path = root / "docs/01-product/design.md"
            ux_path = root / "docs/01-product/ux-ui.md"
            order_path = root / "docs/02-features/feature-order.json"
            state_path = root / "docs/03-logs/prepare-features-state.json"
            pm_todo_path = root / "docs/03-logs/prepare-features-pm-todo.md"
            self.assertTrue(design_path.exists())
            self.assertTrue(ux_path.exists())
            self.assertTrue(order_path.exists())
            self.assertTrue(state_path.exists())
            self.assertTrue(pm_todo_path.exists())

            order_payload = json.loads(order_path.read_text(encoding="utf-8"))
            self.assertEqual(
                order_payload["ordered_feature_slugs"],
                ["alpha-feature", "beta-feature"],
            )
            state_payload = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state_payload["pm_gate"]["final_decision"], "approve")
            self.assertEqual(
                state_payload["execution"]["feature_generation_status"], "skipped"
            )
            self.assertIn("pm_todos", state_payload)
            self.assertIn("items", state_payload["pm_todos"])

    def test_choose_option_supports_prefix_override_alias(self):
        options = [
            self.tool.DecisionOption(
                key="retry",
                label="Retry (Recommended)",
                explanation="Retry once.",
                risk="May still fail.",
            ),
            self.tool.DecisionOption(
                key="waive",
                label="Waive",
                explanation="Continue with waiver.",
                risk="May ship drift.",
            ),
        ]
        selected = self.tool.choose_option(
            issue_id="PM-BLOCK-001",
            title="blocked",
            options=options,
            overrides={"PM-BLOCK": 2},
        )
        self.assertEqual(selected.key, "waive")

    def test_parse_features_respects_process_feature_opt_in(self):
        class DummyModule:
            @staticmethod
            def parse_prd_features(_text: str, include_process_features: bool = False):
                base = [
                    type(
                        "Record",
                        (),
                        {
                            "title": "Alpha Feature",
                            "priority": "P0",
                            "slug": "alpha-feature",
                            "dependencies": tuple(),
                            "source": "table",
                            "outcome": "Alpha outcome.",
                            "notes": "",
                        },
                    )()
                ]
                if include_process_features:
                    base.append(
                        type(
                            "Record",
                            (),
                            {
                                "title": "Process Checklist",
                                "priority": "P1",
                                "slug": "process-checklist",
                                "dependencies": tuple(),
                                "source": "process",
                                "outcome": "Checklist outcome.",
                                "notes": "",
                            },
                        )()
                    )
                return base

        without_process = self.tool.parse_features(
            DummyModule(), "ignored", include_process_features=False
        )
        with_process = self.tool.parse_features(
            DummyModule(), "ignored", include_process_features=True
        )

        self.assertEqual([item.slug for item in without_process], ["alpha-feature"])
        self.assertEqual(
            [item.slug for item in with_process],
            ["alpha-feature", "process-checklist"],
        )

    def test_product_manager_review_blocks_generic_markers(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        order_payload = {"ordered_feature_slugs": ["alpha-feature"]}
        design_text = "\n".join(
            [
                "## System architecture",
                "Alpha Feature architecture.",
                "## Module boundaries",
                "Boundaries for Alpha Feature.",
                "## Infra considerations",
                "Local-only CLI execution on macOS with git-backed repository state.",
                "## Design constraints",
                "- Keep scope focused.",
                "## Build strategy",
                "- Deliver Alpha Feature.",
            ]
        )
        ux_text = "\n".join(
            [
                "## User journeys",
                "Primary persona: Developer/PO running local CLI workflows with explicit gates.",
                "Journey includes Alpha Feature details.",
                "## Workflows",
                "Alpha Feature workflow.",
            ]
        )

        issues = self.tool.product_manager_review(
            features=features,
            ordered_slugs=["alpha-feature"],
            graph={"alpha-feature": set()},
            design_text=design_text,
            ux_text=ux_text,
            order_payload=order_payload,
            pm_role_payload={"decision": "APPROVE", "issues": [], "criteria": {}},
            seed_issues=[],
            enforce_semantic_gate=True,
        )

        self.assertTrue(
            any("generic template markers" in issue.summary for issue in issues)
        )

    def test_product_manager_review_rejects_conflicting_pm_decision(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        order_payload = {"ordered_feature_slugs": ["alpha-feature"]}
        design_text = "\n".join(
            [
                "## System architecture",
                "Alpha Feature system design.",
                "## Module boundaries",
                "Alpha boundaries.",
                "## Infra considerations",
                "Project-specific infrastructure text.",
                "## Design constraints",
                "- Constraint for Alpha.",
                "## Build strategy",
                "- Strategy for Alpha Feature.",
            ]
        )
        ux_text = "\n".join(
            [
                "## User journeys",
                "Alpha Feature journey.",
                "## Workflows",
                "Alpha Feature workflow.",
            ]
        )
        pm_payload = {
            "decision": "APPROVE",
            "issues": [
                {
                    "step": "product-manager",
                    "summary": "Semantic mismatch.",
                    "risk": "Mismatch risk.",
                    "remediation": "Fix mismatch.",
                }
            ],
            "criteria": {},
        }

        issues = self.tool.product_manager_review(
            features=features,
            ordered_slugs=["alpha-feature"],
            graph={"alpha-feature": set()},
            design_text=design_text,
            ux_text=ux_text,
            order_payload=order_payload,
            pm_role_payload=pm_payload,
            seed_issues=[],
            enforce_semantic_gate=False,
        )

        self.assertTrue(
            any(
                "returned APPROVE while listing issues" in issue.summary
                for issue in issues
            )
        )

    def test_prompt_templates_render_literal_issue_schema_in_codex_mode(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
                outcome="Deliver alpha flow.",
                notes="Core CLI path.",
            )
        ]
        ordered_slugs = ["alpha-feature"]
        graph = {"alpha-feature": set()}
        base_values = self.tool.prompt_values(
            features=features,
            ordered_slugs=ordered_slugs,
            graph=graph,
            prd_text="## Prioritized Feature List\n- Alpha Feature",
            context_boundaries="## Scope Boundaries\n- Local CLI only",
            dependency_decisions=[],
            prepare_iteration=2,
            previous_design_markdown="## Previous Design\nPREV DESIGN MARKER",
            previous_ux_markdown="## Previous UX\nPREV UX MARKER",
            pm_feedback=[
                {
                    "issue_id": "PM-001",
                    "step": "architect",
                    "summary": "Address PM issue marker.",
                    "risk": "Drift.",
                    "remediation": "Fix marker.",
                }
            ],
        )
        template_paths = [
            Path("prompts/architect-prepare.md"),
            Path("prompts/ux-prepare.md"),
            Path("prompts/product-manager-prepare-gate.md"),
            Path("tools/templates/prompts/architect-prepare.md"),
            Path("tools/templates/prompts/ux-prepare.md"),
            Path("tools/templates/prompts/product-manager-prepare-gate.md"),
        ]

        for template_path in template_paths:
            with self.subTest(template=str(template_path)):
                template = self.tool.load_prompt_template(ROOT, template_path)
                values = dict(base_values)
                if template_path.name == "product-manager-prepare-gate.md":
                    values.update(
                        {
                            "design_markdown": "## System architecture\nAlpha design.",
                            "ux_markdown": "## User journeys\nAlpha journey.",
                            "order_payload_json": json.dumps(
                                {"ordered_feature_slugs": ordered_slugs},
                                ensure_ascii=True,
                                indent=2,
                                sort_keys=True,
                            ),
                        }
                    )
                rendered = self.tool.render_prompt_template(template, values)
                self.assertIn("{step, summary, risk, remediation}", rendered)
                template_name = template_path.name
                if template_name in {"architect-prepare.md", "ux-prepare.md"}:
                    self.assertIn("PREV DESIGN MARKER", rendered)
                    self.assertIn("PREV UX MARKER", rendered)
                    self.assertIn("Address PM issue marker.", rendered)

    def test_prompt_values_include_retry_context_payload(self):
        values = self.tool.prompt_values(
            features=[],
            ordered_slugs=[],
            graph={},
            prd_text="PRD",
            context_boundaries="Context",
            dependency_decisions=[],
            prepare_iteration=3,
            previous_design_markdown="design retry baseline",
            previous_ux_markdown="ux retry baseline",
            pm_feedback=[
                {
                    "issue_id": "PM-009",
                    "step": "ux",
                    "summary": "Improve specificity.",
                    "risk": "Generic UX.",
                    "remediation": "Add feature outcomes.",
                }
            ],
        )

        self.assertEqual(values["prepare_iteration"], "3")
        self.assertEqual(values["previous_design_markdown"], "design retry baseline")
        self.assertEqual(values["previous_ux_markdown"], "ux retry baseline")
        feedback_payload = json.loads(values["pm_feedback_json"])
        self.assertEqual(feedback_payload[0]["issue_id"], "PM-009")
        self.assertEqual(feedback_payload[0]["step"], "ux")
        self.assertIn("pm_todos_json", values)
        self.assertIn("architect_open_todos_json", values)
        self.assertIn("ux_open_todos_json", values)
        self.assertIn("previous_loop_change_summary", values)

    def test_apply_pm_todo_updates_auto_creates_owner_tasks_from_issues(self):
        review_issues = [
            self.tool.ReviewIssue(
                issue_id="PM-001",
                step="architect",
                summary="Architect must add module boundary details.",
                risk="Boundary drift.",
                remediation="Update module boundaries section.",
            ),
            self.tool.ReviewIssue(
                issue_id="PM-002",
                step="ux",
                summary="UX must map journeys to feature outcomes.",
                risk="Generic flows.",
                remediation="Add feature-specific journey details.",
            ),
        ]
        todos, updates = self.tool.apply_pm_todo_updates(
            pm_todos=[],
            raw_todo_updates=[],
            review_issues=review_issues,
            pm_role_decision="BLOCK",
            loop_iteration=1,
        )

        self.assertEqual(len(todos), 2)
        self.assertEqual({item["owner"] for item in todos}, {"architect", "ux"})
        self.assertTrue(all(item["status"] == "open" for item in todos))
        self.assertEqual({item["action"] for item in updates}, {"auto_create"})

    def test_apply_pm_todo_updates_auto_marks_open_tasks_done_on_approve(self):
        initial_todos = [
            {
                "task_id": "PM-TODO-001",
                "created_loop": 1,
                "updated_loop": 1,
                "owner": "architect",
                "status": "open",
                "description": "Architect task.",
                "source_issue_id": "PM-001",
            },
            {
                "task_id": "PM-TODO-002",
                "created_loop": 1,
                "updated_loop": 1,
                "owner": "ux",
                "status": "carry",
                "description": "UX task.",
                "source_issue_id": "PM-002",
            },
        ]
        todos, updates = self.tool.apply_pm_todo_updates(
            pm_todos=initial_todos,
            raw_todo_updates=[],
            review_issues=[],
            pm_role_decision="APPROVE",
            loop_iteration=2,
        )

        self.assertTrue(all(item["status"] == "done" for item in todos))
        self.assertEqual({item["action"] for item in updates}, {"auto_done"})

    def test_run_architect_role_uses_architect_profile_by_default(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        captured = {"profile": None}

        def fake_codex_exec_json(**kwargs):
            captured["profile"] = kwargs.get("profile")
            return {
                "decision": "APPROVE",
                "design_markdown": "## System architecture\nAlpha architecture.",
                "issues": [],
            }

        with mock.patch.dict(self.tool.os.environ, {}, clear=False):
            self.tool.os.environ.pop("PREPARE_ARCHITECT_PROFILE", None)
            with mock.patch.object(
                self.tool,
                "codex_exec_json",
                side_effect=fake_codex_exec_json,
            ):
                self.tool.run_architect_role(
                    root=ROOT,
                    role_mode=self.tool.ROLE_MODE_CODEX,
                    prd_text="PRD",
                    context_boundaries="Context boundaries",
                    features=features,
                    ordered_slugs=["alpha-feature"],
                    graph={"alpha-feature": set()},
                    dependency_decisions=[],
                )

        self.assertEqual(captured["profile"], "Architect")

    def test_run_ux_role_uses_uxui_profile_by_default(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        captured = {"profile": None}

        def fake_codex_exec_json(**kwargs):
            captured["profile"] = kwargs.get("profile")
            return {
                "decision": "APPROVE",
                "ux_markdown": "## User journeys\nAlpha journey.\n## Workflows\nAlpha flow.",
                "issues": [],
            }

        with mock.patch.dict(self.tool.os.environ, {}, clear=False):
            self.tool.os.environ.pop("PREPARE_UX_PROFILE", None)
            with mock.patch.object(
                self.tool,
                "codex_exec_json",
                side_effect=fake_codex_exec_json,
            ):
                self.tool.run_ux_role(
                    root=ROOT,
                    role_mode=self.tool.ROLE_MODE_CODEX,
                    prd_text="PRD",
                    context_boundaries="Context boundaries",
                    features=features,
                    ordered_slugs=["alpha-feature"],
                    graph={"alpha-feature": set()},
                    dependency_decisions=[],
                )

        self.assertEqual(captured["profile"], "UXUI")

    def test_run_pm_role_uses_product_manager_profile_by_default(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        captured = {"profile": None}

        def fake_codex_exec_json(**kwargs):
            captured["profile"] = kwargs.get("profile")
            return {"decision": "APPROVE", "issues": [], "criteria": {}}

        with mock.patch.dict(self.tool.os.environ, {}, clear=False):
            self.tool.os.environ.pop("PREPARE_PM_PROFILE", None)
            with mock.patch.object(
                self.tool,
                "codex_exec_json",
                side_effect=fake_codex_exec_json,
            ):
                self.tool.run_pm_role(
                    root=ROOT,
                    role_mode=self.tool.ROLE_MODE_CODEX,
                    prd_text="PRD",
                    context_boundaries="Context boundaries",
                    design_text="## System architecture\nAlpha design.",
                    ux_text="## User journeys\nAlpha journey.\n## Workflows\nAlpha flow.",
                    order_payload={"ordered_feature_slugs": ["alpha-feature"]},
                    features=features,
                    ordered_slugs=["alpha-feature"],
                    graph={"alpha-feature": set()},
                    dependency_decisions=[],
                )

        self.assertEqual(captured["profile"], "ProductManager")


if __name__ == "__main__":
    unittest.main()
