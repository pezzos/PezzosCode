import contextlib
import importlib.machinery
import importlib.util
import io
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PC_FEATURE_PATH = ROOT / "tools" / "pc-feature"


def load_pc_feature():
    loader = importlib.machinery.SourceFileLoader("pc_feature", str(PC_FEATURE_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcFeature(unittest.TestCase):
    def setUp(self):
        self.pc_feature = load_pc_feature()

    def test_build_preflight_block_accepts_missing_review_summary(self):
        block = self.pc_feature.build_preflight_block(
            {},
            "WI-20260204-01",
            {"max_files": 1, "max_new_modules": 0},
            "LOW",
            [],
        )
        self.assertIn("Systematic review:", block)

    def test_build_preflight_block_includes_review_summary(self):
        summary = "make feature F=01: ok"
        block = self.pc_feature.build_preflight_block(
            {},
            "WI-20260204-01",
            {"max_files": 1, "max_new_modules": 0},
            "LOW",
            [],
            summary,
        )
        self.assertIn(f"Systematic review: {summary}", block)

    def test_classify_risk_flags_restore_touch(self):
        data = {"touches_restore": True, "files_to_change": []}
        risk, triggers = self.pc_feature.classify_risk(
            data, {"max_files": 5, "max_new_modules": 0}
        )
        self.assertEqual(risk, "HIGH")
        self.assertIn("affects restore apply semantics or permissions", triggers)

    def test_normalize_work_item_id_accepts_format(self):
        self.assertEqual(
            self.pc_feature.normalize_work_item_id("WI-20260204-01"),
            "WI-20260204-01",
        )

    def test_normalize_work_item_id_rejects_invalid(self):
        stderr_capture = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(stderr_capture):
                self.pc_feature.normalize_work_item_id("BAD")
        self.assertIn("invalid work item id", stderr_capture.getvalue())

    def test_format_review_item_marks_failure(self):
        line = self.pc_feature.format_review_item("make feature F=01", 2)
        self.assertEqual(line, "make feature F=01: FAIL")

    def test_build_gates_block_uses_command(self):
        line = self.pc_feature.build_gates_block("make ci", "PASS")
        self.assertEqual(line, "- make ci: PASS")


if __name__ == "__main__":
    unittest.main()
