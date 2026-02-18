import io
import importlib.util
from importlib.machinery import SourceFileLoader
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock
from pathlib import Path
from types import SimpleNamespace


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

    def _write_minimal_prepare_fixture(self, root: Path) -> None:
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
            self._write_minimal_prepare_fixture(root)

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

    def test_promotes_candidate_artifacts_on_approve(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_minimal_prepare_fixture(root)

            args = SimpleNamespace(
                root=str(root),
                skip_generation=True,
                skip_schema_check=True,
                role_mode=self.tool.ROLE_MODE_DETERMINISTIC,
                include_process_features=False,
                snapshot_runs=False,
            )
            result = self.tool.run_prepare(args)
            self.assertEqual(result, 0)

            pairs = [
                ("docs/01-product/design.md", "docs/01-product/design.candidate.md"),
                ("docs/01-product/ux-ui.md", "docs/01-product/ux-ui.candidate.md"),
                (
                    "docs/02-features/feature-order.json",
                    "docs/02-features/feature-order.candidate.json",
                ),
                (
                    "docs/03-logs/prepare-features-state.json",
                    "docs/03-logs/prepare-features-state.candidate.json",
                ),
                (
                    "docs/03-logs/prepare-features-pm-todo.md",
                    "docs/03-logs/prepare-features-pm-todo.candidate.md",
                ),
            ]
            for canonical_rel, candidate_rel in pairs:
                canonical = root / canonical_rel
                candidate = root / candidate_rel
                self.assertTrue(canonical.exists(), canonical_rel)
                self.assertTrue(candidate.exists(), candidate_rel)
                self.assertEqual(
                    canonical.read_text(encoding="utf-8"),
                    candidate.read_text(encoding="utf-8"),
                )
            self.assertTrue(
                (root / "docs/03-logs/prepare-features-candidate-summary.md").exists()
            )

    def test_blocked_run_preserves_canonical_and_updates_candidates(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_minimal_prepare_fixture(root)
            (root / "docs/03-logs").mkdir(parents=True, exist_ok=True)

            canonical_design = "## System architecture\nCanonical design baseline.\n"
            canonical_ux = (
                "## User journeys\nCanonical ux baseline.\n## Workflows\nX.\n"
            )
            canonical_order = {
                "ordered_feature_slugs": ["alpha-feature", "beta-feature"],
                "decisions": [],
                "dependencies": {
                    "alpha-feature": [],
                    "beta-feature": ["alpha-feature"],
                },
                "ordered_features": [
                    {"index": 1, "slug": "alpha-feature", "dependencies": []},
                    {
                        "index": 2,
                        "slug": "beta-feature",
                        "dependencies": ["alpha-feature"],
                    },
                ],
            }
            canonical_state = {
                "version": 3,
                "pm_gate": {"history": [], "final_decision": "approve"},
                "pm_todos": {"items": []},
                "execution": {
                    "feature_generation_status": "completed",
                    "schema_check_status": "completed",
                },
            }
            canonical_pm_todo = (
                "# Prepare Features PM TODO\n\n## Open + Carry\n\n- (none)\n"
            )

            (root / "docs/01-product/design.md").write_text(
                canonical_design, encoding="utf-8"
            )
            (root / "docs/01-product/ux-ui.md").write_text(
                canonical_ux, encoding="utf-8"
            )
            (root / "docs/02-features/feature-order.json").write_text(
                json.dumps(
                    canonical_order, ensure_ascii=True, indent=2, sort_keys=True
                ),
                encoding="utf-8",
            )
            (root / "docs/03-logs/prepare-features-state.json").write_text(
                json.dumps(
                    canonical_state, ensure_ascii=True, indent=2, sort_keys=True
                ),
                encoding="utf-8",
            )
            (root / "docs/03-logs/prepare-features-pm-todo.md").write_text(
                canonical_pm_todo, encoding="utf-8"
            )

            args = SimpleNamespace(
                root=str(root),
                skip_generation=True,
                skip_schema_check=True,
                role_mode=self.tool.ROLE_MODE_DETERMINISTIC,
                include_process_features=False,
                snapshot_runs=False,
            )

            with mock.patch.object(
                self.tool,
                "run_pm_role",
                return_value={
                    "decision": "BLOCK",
                    "issues": [
                        {
                            "step": "architect",
                            "summary": "Architecture still needs one targeted fix.",
                            "risk": "PM gate blocked.",
                            "remediation": "Update design.md section and retry.",
                        }
                    ],
                    "criteria": {"feature_specificity": "fail"},
                },
            ):
                with mock.patch.dict(
                    self.tool.os.environ,
                    {"PREPARE_DECISIONS": "PM-BLOCK:3"},
                    clear=False,
                ):
                    with self.assertRaises(SystemExit):
                        self.tool.run_prepare(args)

            self.assertEqual(
                (root / "docs/01-product/design.md").read_text(encoding="utf-8"),
                canonical_design,
            )
            self.assertEqual(
                (root / "docs/01-product/ux-ui.md").read_text(encoding="utf-8"),
                canonical_ux,
            )
            self.assertEqual(
                (root / "docs/03-logs/prepare-features-pm-todo.md").read_text(
                    encoding="utf-8"
                ),
                canonical_pm_todo,
            )
            self.assertEqual(
                json.loads(
                    (root / "docs/03-logs/prepare-features-state.json").read_text(
                        encoding="utf-8"
                    )
                ),
                canonical_state,
            )
            self.assertTrue((root / "docs/01-product/design.candidate.md").exists())
            self.assertTrue((root / "docs/01-product/ux-ui.candidate.md").exists())
            self.assertTrue(
                (root / "docs/03-logs/prepare-features-state.candidate.json").exists()
            )

    def test_build_order_payload_normalizes_stringified_dependency_arrays(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            ),
            self.tool.Feature(
                title="Beta Feature",
                priority="P1",
                slug="beta-feature",
                dependencies=("alpha-feature",),
            ),
        ]
        payload = self.tool.build_order_payload(
            ordered_slugs=["alpha-feature", "beta-feature"],
            features=features,
            graph={"alpha-feature": set(), "beta-feature": {"alpha-feature"}},
            decisions=[
                {
                    "feature_slug": "alpha-feature",
                    "depends_on": "[]",
                    "reason_codes": "['root']",
                },
                {
                    "feature_slug": "beta-feature",
                    "depends_on": "['alpha-feature']",
                    "reason_codes": "['dependency_fix']",
                },
            ],
        )

        self.assertEqual(
            payload["dependencies"]["beta-feature"],
            ["alpha-feature"],
        )
        beta_decision = next(
            item
            for item in payload["decisions"]
            if item["feature_slug"] == "beta-feature"
        )
        self.assertEqual(beta_decision["depends_on"], ["alpha-feature"])
        self.assertEqual(
            beta_decision["reason_codes"],
            ["DEPENDENCY_FIX"],
        )
        beta_row = next(
            item
            for item in payload["ordered_features"]
            if item["slug"] == "beta-feature"
        )
        self.assertEqual(beta_row["dependencies"], ["alpha-feature"])

    def test_retry_path_persists_prepare_state_before_next_iteration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_minimal_prepare_fixture(root)

            args = SimpleNamespace(
                root=str(root),
                skip_generation=True,
                skip_schema_check=True,
                role_mode=self.tool.ROLE_MODE_DETERMINISTIC,
                include_process_features=False,
                snapshot_runs=False,
            )
            pm_payloads = [
                {
                    "decision": "BLOCK",
                    "issues": [
                        {
                            "step": "architect",
                            "summary": "Architect iteration needs one more pass.",
                            "risk": "PM gate cannot approve yet.",
                            "remediation": "Revise architecture details.",
                        }
                    ],
                    "criteria": {},
                },
                {"decision": "APPROVE", "issues": [], "criteria": {}},
            ]

            def fake_run_pm_role(**_kwargs):
                if not pm_payloads:
                    return {"decision": "APPROVE", "issues": [], "criteria": {}}
                return pm_payloads.pop(0)

            with mock.patch.object(
                self.tool,
                "run_pm_role",
                side_effect=fake_run_pm_role,
            ):
                with mock.patch.dict(
                    self.tool.os.environ,
                    {"PREPARE_DECISIONS": "PM-BLOCK:1"},
                    clear=False,
                ):
                    stdout_buffer = io.StringIO()
                    with redirect_stdout(stdout_buffer):
                        result = self.tool.run_prepare(args)

            self.assertEqual(result, 0)
            output = stdout_buffer.getvalue()
            self.assertGreaterEqual(
                output.count(
                    "wrote candidate artifacts -> docs/01-product/design.candidate.md"
                ),
                2,
            )
            state_payload = json.loads(
                (root / "docs/03-logs/prepare-features-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                state_payload["pm_gate"]["history"][0]["decision"], "retry"
            )
            self.assertGreaterEqual(
                state_payload["pm_gate"]["history"][0]["issue_count"], 1
            )

    def test_run_prepare_calls_dependency_autofix_for_raw_order_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_minimal_prepare_fixture(root)

            args = SimpleNamespace(
                root=str(root),
                skip_generation=True,
                skip_schema_check=True,
                role_mode=self.tool.ROLE_MODE_CODEX,
                include_process_features=False,
                snapshot_runs=False,
            )

            design_md = "\n".join(
                [
                    "## System architecture",
                    "Alpha Feature and Beta Feature architecture mapping.",
                    "## Module boundaries",
                    "Boundaries.",
                    "## Infra considerations",
                    "Infra.",
                    "## Design constraints",
                    "- Constraint.",
                    "## Build strategy",
                    "- Strategy.",
                    "## Feature alignment map",
                    "- Alpha Feature",
                    "- Beta Feature",
                ]
            )
            ux_md = "\n".join(
                [
                    "## User journeys",
                    "Alpha Feature and Beta Feature journeys.",
                    "## Workflows",
                    "Alpha Feature workflow then Beta Feature workflow.",
                    "## UX constraints",
                    "- Keep deterministic.",
                ]
            )
            inconsistent_order_payload = {
                "ordered_feature_slugs": ["alpha-feature", "beta-feature"],
                "decisions": [
                    {"feature_slug": "alpha-feature", "depends_on": "[]"},
                    {
                        "feature_slug": "beta-feature",
                        "depends_on": "['alpha-feature']",
                    },
                ],
                "dependencies": {
                    "alpha-feature": [],
                    "beta-feature": [],
                },
                "ordered_features": [
                    {
                        "index": 1,
                        "slug": "alpha-feature",
                        "title": "Alpha Feature",
                        "priority": "P0",
                        "dependencies": [],
                    },
                    {
                        "index": 2,
                        "slug": "beta-feature",
                        "title": "Beta Feature",
                        "priority": "P1",
                        "dependencies": [],
                    },
                ],
            }

            with mock.patch.object(
                self.tool,
                "run_architect_role",
                return_value=(design_md, []),
            ), mock.patch.object(
                self.tool,
                "run_ux_role",
                return_value=(ux_md, []),
            ), mock.patch.object(
                self.tool,
                "run_orderer_role",
                return_value=(inconsistent_order_payload, []),
            ), mock.patch.object(
                self.tool,
                "run_pm_role",
                return_value={
                    "decision": "APPROVE",
                    "issues": [],
                    "criteria": {
                        "feature_specificity": "pass",
                        "journey_specificity": "pass",
                        "dependency_alignment": "pass",
                    },
                    "todo_updates": [],
                },
            ), mock.patch.object(
                self.tool,
                "run_order_payload_autofix_session",
                side_effect=lambda **kwargs: dict(kwargs["order_payload"]),
            ) as autofix_mock:
                result = self.tool.run_prepare(args)

            self.assertEqual(result, 0)
            self.assertEqual(autofix_mock.call_count, 1)
            order_payload = json.loads(
                (root / "docs/02-features/feature-order.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                order_payload["dependencies"]["beta-feature"],
                ["alpha-feature"],
            )

    def test_snapshot_runs_write_per_run_prepare_snapshots(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_minimal_prepare_fixture(root)

            args = SimpleNamespace(
                root=str(root),
                skip_generation=True,
                skip_schema_check=True,
                role_mode=self.tool.ROLE_MODE_DETERMINISTIC,
                include_process_features=False,
                snapshot_runs=True,
            )
            stdout_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer):
                result = self.tool.run_prepare(args)

            self.assertEqual(result, 0)
            runs_root = root / "docs/03-logs/prepare-features-runs"
            run_dirs = [item for item in runs_root.iterdir() if item.is_dir()]
            self.assertEqual(len(run_dirs), 1)
            run_dir = run_dirs[0]
            index_path = run_dir / "index.json"
            self.assertTrue(index_path.exists())

            index_payload = json.loads(index_path.read_text(encoding="utf-8"))
            self.assertEqual(index_payload["run_id"], run_dir.name)
            self.assertGreaterEqual(len(index_payload["snapshots"]), 1)
            snapshot_entry = index_payload["snapshots"][0]
            self.assertEqual(snapshot_entry["label"], "post-gate")
            self.assertTrue((run_dir / snapshot_entry["state_file"]).exists())
            self.assertTrue((run_dir / snapshot_entry["pm_todo_file"]).exists())

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

    def test_normalize_prepare_step_aliases_dependency_planner_terms(self):
        samples = [
            "feature-order.json ordering",
            "dependency decision records",
            "orderer",
            "dependency-planner",
        ]
        normalized = {
            self.tool.normalize_prepare_step(sample, default="product-manager")
            for sample in samples
        }
        self.assertEqual(normalized, {"dependency-planner"})

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
            Path("prompts/orderer-prepare.md"),
            Path("prompts/product-manager-prepare-gate.md"),
            Path("tools/templates/prompts/architect-prepare.md"),
            Path("tools/templates/prompts/ux-prepare.md"),
            Path("tools/templates/prompts/orderer-prepare.md"),
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
                if template_path.name == "orderer-prepare.md":
                    values.update(
                        {
                            "baseline_order_payload_json": json.dumps(
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
                if template_name in {
                    "architect-prepare.md",
                    "ux-prepare.md",
                    "orderer-prepare.md",
                }:
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
        self.assertIn("orderer_open_todos_json", values)
        self.assertIn("previous_order_payload_json", values)
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
            self.tool.ReviewIssue(
                issue_id="PM-003",
                step="feature-order.json ordering",
                summary="Dependency order must place pipeline first.",
                risk="Sequencing regression.",
                remediation="Reorder feature-order payload to satisfy dependencies.",
            ),
        ]
        todos, updates = self.tool.apply_pm_todo_updates(
            pm_todos=[],
            raw_todo_updates=[],
            review_issues=review_issues,
            pm_role_decision="BLOCK",
            loop_iteration=1,
        )

        self.assertEqual(len(todos), 3)
        self.assertEqual(
            {item["owner"] for item in todos},
            {"architect", "ux", "dependency-planner"},
        )
        self.assertTrue(all(item["status"] == "open" for item in todos))
        self.assertEqual({item["action"] for item in updates}, {"auto_create"})

    def test_apply_pm_todo_updates_marks_resolved_tasks_done_on_block(self):
        initial_todos = [
            {
                "task_id": "PM-TODO-001",
                "created_loop": 1,
                "updated_loop": 1,
                "owner": "architect",
                "status": "open",
                "description": "Architect must add module boundary details.",
                "source_issue_id": "PM-001",
            },
            {
                "task_id": "PM-TODO-002",
                "created_loop": 1,
                "updated_loop": 1,
                "owner": "ux",
                "status": "carry",
                "description": "UX must map journeys to feature outcomes.",
                "source_issue_id": "PM-002",
            },
        ]
        review_issues = [
            self.tool.ReviewIssue(
                issue_id="PM-101",
                step="architect",
                summary="Architect must add module boundary details.",
                risk="Boundary drift.",
                remediation="Update module boundaries section.",
            )
        ]

        todos, updates = self.tool.apply_pm_todo_updates(
            pm_todos=initial_todos,
            raw_todo_updates=[],
            review_issues=review_issues,
            pm_role_decision="BLOCK",
            loop_iteration=2,
        )

        by_description = {item["description"]: item for item in todos}
        self.assertEqual(
            by_description["Architect must add module boundary details."]["status"],
            "open",
        )
        self.assertEqual(
            by_description["UX must map journeys to feature outcomes."]["status"],
            "done",
        )
        self.assertTrue(
            any(
                update["action"] == "auto_done_resolved"
                and update["task_id"] == "PM-TODO-002"
                for update in updates
            )
        )

    def test_apply_pm_todo_updates_tracks_review_issues_when_raw_updates_are_sparse(
        self,
    ):
        review_issues = [
            self.tool.ReviewIssue(
                issue_id="PM-201",
                step="architect",
                summary="design.md does not mention feature 'Alpha'.",
                risk="Missing architecture alignment.",
                remediation="Update feature alignment map in design.md.",
            ),
            self.tool.ReviewIssue(
                issue_id="PM-202",
                step="ux",
                summary="ux-ui.md does not mention feature 'Alpha'.",
                risk="Missing journey alignment.",
                remediation="Update workflows in ux-ui.md.",
            ),
        ]
        raw_todo_updates = [
            {
                "owner": "architect",
                "status": "open",
                "description": "Align design map to canonical order.",
                "source_issue_id": "PM-ISSUE-ARCH-001",
            },
            {
                "owner": "ux",
                "status": "open",
                "description": "Align ux workflows to canonical order.",
                "source_issue_id": "PM-ISSUE-UX-001",
            },
        ]

        todos, _ = self.tool.apply_pm_todo_updates(
            pm_todos=[],
            raw_todo_updates=raw_todo_updates,
            review_issues=review_issues,
            pm_role_decision="BLOCK",
            loop_iteration=1,
        )

        active_descriptions = {
            item["description"] for item in todos if item["status"] in {"open", "carry"}
        }
        self.assertEqual(
            active_descriptions,
            {
                "design.md does not mention feature 'Alpha'.",
                "ux-ui.md does not mention feature 'Alpha'.",
            },
        )
        stale_done_descriptions = {
            item["description"] for item in todos if item["status"] == "done"
        }
        self.assertIn("Align design map to canonical order.", stale_done_descriptions)
        self.assertIn(
            "Align ux workflows to canonical order.",
            stale_done_descriptions,
        )

    def test_product_manager_review_rejects_unknown_pm_issue_step(self):
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
                "Alpha boundaries.",
                "## Infra considerations",
                "Infra text.",
                "## Design constraints",
                "- Constraint.",
                "## Build strategy",
                "- Strategy.",
            ]
        )
        ux_text = "\n".join(
            [
                "## User journeys",
                "Alpha journey.",
                "## Workflows",
                "Alpha workflow.",
            ]
        )
        pm_payload = {
            "decision": "BLOCK",
            "issues": [
                {
                    "step": "non-existent-step",
                    "summary": "Bad step field.",
                    "risk": "Routing mismatch.",
                    "remediation": "Use an allowed step.",
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
            any("is not allowed; use one of" in issue.summary for issue in issues)
        )

    def test_product_manager_review_maps_failed_dependency_criterion_to_owner_issue(
        self,
    ):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
                outcome="Deliver alpha dependency-safe flow.",
                notes="Dependency order must be deterministic.",
            )
        ]
        order_payload = {"ordered_feature_slugs": ["alpha-feature"]}
        design_text = "\n".join(
            [
                "## System architecture",
                "Alpha Feature architecture.",
                "## Module boundaries",
                "Alpha boundaries.",
                "## Infra considerations",
                "Project-specific infra.",
                "## Design constraints",
                "- Constraint.",
                "## Build strategy",
                "- Strategy.",
            ]
        )
        ux_text = "\n".join(
            [
                "## User journeys",
                "Alpha journey references outcome details.",
                "## Workflows",
                "Alpha workflow references deterministic sequence.",
            ]
        )
        pm_payload = {
            "decision": "BLOCK",
            "issues": [],
            "criteria": {"dependency_alignment": "fail"},
            "todo_updates": [
                {
                    "owner": "dependency-planner",
                    "status": "open",
                    "description": "Fix order payload dependency sequencing.",
                }
            ],
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
            enforce_semantic_gate=True,
        )

        self.assertTrue(
            any(
                issue.step == "dependency-planner"
                and "dependency_alignment" in issue.summary
                for issue in issues
            )
        )

    def test_product_manager_review_blocks_when_todo_updates_missing_for_block(self):
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
                "Alpha boundaries.",
                "## Infra considerations",
                "Project-specific infra.",
                "## Design constraints",
                "- Constraint.",
                "## Build strategy",
                "- Strategy.",
            ]
        )
        ux_text = "\n".join(
            [
                "## User journeys",
                "Alpha journey.",
                "## Workflows",
                "Alpha workflow.",
            ]
        )
        pm_payload = {
            "decision": "BLOCK",
            "issues": [
                {
                    "step": "architect",
                    "summary": "Architecture remains generic.",
                    "risk": "Low confidence.",
                    "remediation": "Update design.md in Feature alignment map; acceptance: feature-specific semantics present.",
                }
            ],
            "criteria": {},
            "todo_updates": [],
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
            any("missing actionable todo_updates" in issue.summary for issue in issues)
        )

    def test_product_manager_review_flags_ambiguous_pm_issue_remediation(self):
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
                "Alpha boundaries.",
                "## Infra considerations",
                "Project-specific infra.",
                "## Design constraints",
                "- Constraint.",
                "## Build strategy",
                "- Strategy.",
            ]
        )
        ux_text = "\n".join(
            [
                "## User journeys",
                "Alpha journey.",
                "## Workflows",
                "Alpha workflow.",
            ]
        )
        pm_payload = {
            "decision": "BLOCK",
            "issues": [
                {
                    "step": "ux",
                    "summary": "Needs better UX.",
                    "risk": "Generic UX.",
                    "remediation": "Fix it.",
                }
            ],
            "criteria": {},
            "todo_updates": [
                {
                    "owner": "ux",
                    "status": "open",
                    "description": "Improve UX details",
                }
            ],
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
            any("is ambiguous; missing" in issue.summary for issue in issues)
        )

    def test_retry_owner_scope_includes_dependency_planner_for_pm_dependency_feedback(
        self,
    ):
        issues = [
            self.tool.ReviewIssue(
                issue_id="PM-001",
                step="product-manager",
                summary="PM semantic criterion 'dependency_alignment' failed.",
                risk="Semantic gate failed.",
                remediation="Update feature-order sequencing and dependency decisions.",
            )
        ]
        scope = self.tool.retry_owner_scope_from_issues(issues)
        self.assertIn("dependency-planner", scope)

    def test_run_orderer_role_uses_orderer_profile_by_default(self):
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
                "ordered_feature_slugs": ["alpha-feature"],
                "decisions": [],
                "issues": [],
            }

        with mock.patch.dict(self.tool.os.environ, {}, clear=False):
            self.tool.os.environ.pop("PREPARE_ORDERER_PROFILE", None)
            with mock.patch.object(
                self.tool,
                "codex_exec_json",
                side_effect=fake_codex_exec_json,
            ):
                payload, issues = self.tool.run_orderer_role(
                    root=ROOT,
                    role_mode=self.tool.ROLE_MODE_CODEX,
                    prd_text="PRD",
                    context_boundaries="Context boundaries",
                    features=features,
                    ordered_slugs=["alpha-feature"],
                    graph={"alpha-feature": set()},
                    dependency_decisions=[],
                    baseline_order_payload={"ordered_feature_slugs": ["alpha-feature"]},
                )

        self.assertEqual(captured["profile"], "Orderer")
        self.assertEqual(payload["ordered_feature_slugs"], ["alpha-feature"])
        self.assertEqual(issues, [])

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

    def test_run_architect_role_flags_retry_rewrite_without_actionable_inputs(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        previous_design = "\n".join(
            [
                "## System architecture",
                "Prospect client: discovery to qualified contact or audit booking",
                "## Module boundaries",
                "Alpha boundaries.",
            ]
        )

        def fake_codex_exec_json(**_kwargs):
            return {
                "decision": "APPROVE",
                "design_markdown": "\n".join(
                    [
                        "## System architecture",
                        "Prospect client to qualified contact or audit booking",
                        "## Module boundaries",
                        "Alpha boundaries.",
                    ]
                ),
                "changed_sections": ["System architecture"],
                "change_rationale": "PM-001 wording refresh only.",
                "issues": [],
            }

        with mock.patch.object(
            self.tool,
            "codex_exec_json",
            side_effect=fake_codex_exec_json,
        ):
            _markdown, issues = self.tool.run_architect_role(
                root=ROOT,
                role_mode=self.tool.ROLE_MODE_CODEX,
                prd_text="PRD",
                context_boundaries="Context boundaries",
                features=features,
                ordered_slugs=["alpha-feature"],
                graph={"alpha-feature": set()},
                dependency_decisions=[],
                prepare_iteration=2,
                previous_design_markdown=previous_design,
                previous_ux_markdown="## User journeys\nAlpha journey.",
                pm_feedback=[],
                pm_todos=[],
                previous_loop_change_summary="No actionable changes requested.",
            )

        self.assertTrue(
            any(
                "without actionable PM TODO/feedback" in issue["summary"]
                for issue in issues
            )
        )

    def test_run_architect_role_requires_change_metadata_when_actionable(self):
        features = [
            self.tool.Feature(
                title="Alpha Feature",
                priority="P0",
                slug="alpha-feature",
                dependencies=tuple(),
            )
        ]
        previous_design = "\n".join(
            [
                "## System architecture",
                "Original architecture text.",
                "## Module boundaries",
                "Original boundaries.",
            ]
        )

        def fake_codex_exec_json(**_kwargs):
            return {
                "decision": "APPROVE",
                "design_markdown": "\n".join(
                    [
                        "## System architecture",
                        "Updated architecture text for PM-TODO-001.",
                        "## Module boundaries",
                        "Original boundaries.",
                    ]
                ),
                "issues": [],
            }

        with mock.patch.object(
            self.tool,
            "codex_exec_json",
            side_effect=fake_codex_exec_json,
        ):
            _markdown, issues = self.tool.run_architect_role(
                root=ROOT,
                role_mode=self.tool.ROLE_MODE_CODEX,
                prd_text="PRD",
                context_boundaries="Context boundaries",
                features=features,
                ordered_slugs=["alpha-feature"],
                graph={"alpha-feature": set()},
                dependency_decisions=[],
                prepare_iteration=2,
                previous_design_markdown=previous_design,
                previous_ux_markdown="## User journeys\nAlpha journey.",
                pm_feedback=[],
                pm_todos=[
                    {
                        "task_id": "PM-TODO-001",
                        "owner": "architect",
                        "status": "open",
                        "description": "Update architecture details.",
                    }
                ],
                previous_loop_change_summary="PM-TODO-001 open.",
            )

        self.assertTrue(
            any("omitted change_rationale" in issue["summary"] for issue in issues)
        )

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
