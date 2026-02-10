import json
import os
import random
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from lib import log_compaction


random.seed(1337)

REQUIRED_FIELDS = {
    "source_path",
    "source_section",
    "work_item_ref",
    "outcome_rationale",
    "evidence_refs",
    "summary",
}


def validate_compact_entry(entry: dict) -> None:
    missing = REQUIRED_FIELDS - set(entry.keys())
    if missing:
        raise AssertionError(f"missing required fields: {missing}")
    if not entry["source_path"].strip():
        raise AssertionError("source_path must be non-empty")
    if not isinstance(entry["evidence_refs"], list) or not entry["evidence_refs"]:
        raise AssertionError("evidence_refs must be a non-empty list")
    if not entry["outcome_rationale"].strip():
        raise AssertionError("outcome_rationale must be non-empty")
    if not entry["summary"].strip():
        raise AssertionError("summary must be non-empty")
    if not entry["source_section"].strip():
        raise AssertionError("source_section must be non-empty")


def load_log_compaction_tool() -> object:
    tool_path = Path(__file__).resolve().parents[1] / "tools" / "log-compaction"
    module = types.ModuleType("log_compaction_tool")
    module.__dict__["__file__"] = str(tool_path)
    code = tool_path.read_text(encoding="utf-8")
    exec(compile(code, str(tool_path), "exec"), module.__dict__)
    return module


class TestLogCompactionContract(unittest.TestCase):
    def test_decision_log_contract_fixtures(self):
        fixtures = [
            {
                "source_path": "docs/03-logs/decision-log.md",
                "source_section": "2026-02-09",
                "work_item_ref": "WI-20260209-01",
                "outcome_rationale": "Keep compaction output non-destructive.",
                "evidence_refs": ["logs/WI-20260209-01/feature.log"],
                "summary": "Decision preserved with evidence reference.",
            },
            {
                "source_path": "docs/03-logs/decision-log.md",
                "source_section": "missing or moved",
                "work_item_ref": "",
                "outcome_rationale": "Source section missing, note in compact output.",
                "evidence_refs": ["offload:abc123"],
                "summary": "Compact entry flags missing source section.",
            },
        ]
        for entry in fixtures:
            validate_compact_entry(entry)


class TestLogCompactionPaths(unittest.TestCase):
    def test_compacted_log_output_paths_respect_root_override(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_path = root / "tools" / "log-compaction-config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                json.dumps({"compacted_logs_dir": "alt/compacted"}),
                encoding="utf-8",
            )
            outputs = log_compaction.compacted_log_output_paths(root=root)
            expected_dir = os.path.join(str(root), "alt", "compacted")
            self.assertEqual(
                outputs["decision"],
                os.path.join(expected_dir, "decision-log-compact.json"),
            )
            self.assertEqual(
                outputs["implementation"],
                os.path.join(expected_dir, "implementation-log-compact.json"),
            )
            self.assertEqual(
                outputs["validation"],
                os.path.join(expected_dir, "validation-log-compact.json"),
            )

    def test_compacted_log_output_paths_respect_env_override(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with mock.patch.dict(
                os.environ, {"PC_COMPACTED_LOGS_DIR": "alt/compacted"}, clear=False
            ):
                outputs = log_compaction.compacted_log_output_paths(root=root)
            expected_dir = os.path.join(str(root), "alt", "compacted")
            self.assertEqual(
                outputs["decision"],
                os.path.join(expected_dir, "decision-log-compact.json"),
            )

    def test_compacted_log_output_paths_respect_config_override(self):
        root = Path("/tmp/pc-root")
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "log-compaction.json"
            payload = {
                "compacted_logs_dir": "alt/compacted",
                "log_sources": {
                    "decision": "logs/decision.md",
                    "implementation": "logs/implementation.md",
                    "validation": "logs/validation.md",
                },
            }
            config_path.write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch.dict(
                os.environ,
                {"PC_LOG_COMPACTION_CONFIG": str(config_path)},
                clear=False,
            ):
                outputs = log_compaction.compacted_log_output_paths(root=root)
                sources = log_compaction.log_sources(root=root)
        expected_dir = os.path.join("/tmp/pc-root", "alt", "compacted")
        self.assertEqual(
            outputs["implementation"],
            os.path.join(expected_dir, "implementation-log-compact.json"),
        )
        self.assertEqual(sources["decision"], "logs/decision.md")

    def test_compacted_log_output_paths_fallback_when_config_missing(self):
        root = Path("/tmp/pc-root")
        missing_config = Path("/tmp/non-existent-log-compaction-config.json")
        with mock.patch.dict(
            os.environ,
            {
                "PC_LOG_COMPACTION_CONFIG": str(missing_config),
                "PC_COMPACTED_LOGS_DIR": "",
            },
            clear=False,
        ):
            outputs = log_compaction.compacted_log_output_paths(root=root)
        expected_dir = os.path.join("/tmp/pc-root", "docs", "03-logs", "compacted")
        self.assertEqual(
            outputs["validation"],
            os.path.join(expected_dir, "validation-log-compact.json"),
        )

    def test_implementation_log_contract_fixtures(self):
        fixtures = [
            {
                "source_path": "docs/03-logs/implementation-log.md",
                "source_section": "2026-02-09",
                "work_item_ref": "WI-20260209-01",
                "outcome_rationale": "Added index lifecycle commands.",
                "evidence_refs": ["offload:def456"],
                "summary": "List/get/purge implemented with retention support.",
            },
            {
                "source_path": "docs/03-logs/implementation-log.md",
                "source_section": "stale reference",
                "work_item_ref": "WI-20260209-02",
                "outcome_rationale": "Section shifted; mark as stale.",
                "evidence_refs": ["logs/WI-20260209-02/patch.log"],
                "summary": "Compact entry documents stale section.",
            },
        ]
        for entry in fixtures:
            validate_compact_entry(entry)

    def test_validation_log_contract_fixtures(self):
        fixtures = [
            {
                "source_path": "docs/03-logs/validation-log.md",
                "source_section": "2026-02-09",
                "work_item_ref": "WI-20260209-01",
                "outcome_rationale": "Unit tests passed.",
                "evidence_refs": ["logs/WI-20260209-01/test.log"],
                "summary": "Validation evidence recorded.",
            },
            {
                "source_path": "docs/03-logs/validation-log.md",
                "source_section": "missing or moved",
                "work_item_ref": "",
                "outcome_rationale": "Section missing, documented in compact view.",
                "evidence_refs": ["offload:ghi789"],
                "summary": "Compact entry flags missing source section.",
            },
        ]
        for entry in fixtures:
            validate_compact_entry(entry)


class TestLogCompactionEntries(unittest.TestCase):
    def test_missing_sections_marked_with_required_metadata(self):
        tool = load_log_compaction_tool()
        entries = tool.build_entries("decision", "logs/decision.md", "", max_entries=5)
        self.assertEqual(entries[0]["source_section"], "missing or moved")
        for field in REQUIRED_FIELDS:
            self.assertIn(field, entries[0])
        self.assertEqual(entries[0]["source_path"], "logs/decision.md")
        self.assertTrue(entries[0]["evidence_refs"])
        self.assertTrue(entries[0]["outcome_rationale"].strip())

    def test_work_item_and_date_extracted(self):
        tool = load_log_compaction_tool()
        sample = (
            "### 2026-02-09 - Example\n"
            "- Rationale\n"
            "  - Completed WI-20260209-01\n"
            "- Evidence: logs/WI-20260209-01/feature.log\n"
        )
        entries = tool.build_entries(
            "decision", "logs/decision.md", sample, max_entries=5
        )
        self.assertEqual(entries[0]["source_section"], "2026-02-09")
        self.assertEqual(entries[0]["work_item_ref"], "WI-20260209-01")


if __name__ == "__main__":
    unittest.main()
