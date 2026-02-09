import random
import unittest


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
    if not entry["source_path"].startswith("docs/03-logs/"):
        raise AssertionError("source_path must reference docs/03-logs")
    if not isinstance(entry["evidence_refs"], list) or not entry["evidence_refs"]:
        raise AssertionError("evidence_refs must be a non-empty list")
    if not entry["outcome_rationale"].strip():
        raise AssertionError("outcome_rationale must be non-empty")
    if not entry["summary"].strip():
        raise AssertionError("summary must be non-empty")
    if not entry["source_section"].strip():
        raise AssertionError("source_section must be non-empty")


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


if __name__ == "__main__":
    unittest.main()
