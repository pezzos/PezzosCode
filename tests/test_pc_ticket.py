import contextlib
import importlib.machinery
import importlib.util
import io
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PC_TICKET_PATH = ROOT / "tools" / "pc-ticket"


def load_pc_ticket():
    loader = importlib.machinery.SourceFileLoader("pc_ticket", str(PC_TICKET_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcTicket(unittest.TestCase):
    def setUp(self):
        self.pc_ticket = load_pc_ticket()

    def test_build_preflight_block_accepts_missing_review_summary(self):
        block = self.pc_ticket.build_preflight_block(
            {},
            "T-001",
            {"max_files": 1, "max_new_modules": 0},
            "LOW",
            [],
        )
        self.assertIn("Systematic review:", block)

    def test_build_preflight_block_includes_review_summary(self):
        summary = "make ticket T=T-001: ok"
        block = self.pc_ticket.build_preflight_block(
            {},
            "T-001",
            {"max_files": 1, "max_new_modules": 0},
            "LOW",
            [],
            summary,
        )
        self.assertIn(f"Systematic review: {summary}", block)

    def test_classify_risk_flags_restore_touch(self):
        data = {"touches_restore": True, "files_to_change": []}
        risk, triggers = self.pc_ticket.classify_risk(
            data, {"max_files": 5, "max_new_modules": 0}
        )
        self.assertEqual(risk, "HIGH")
        self.assertIn("affects restore apply semantics or permissions", triggers)

    def test_normalize_ticket_id_accepts_common_formats(self):
        self.assertEqual(self.pc_ticket.normalize_ticket_id("001"), "T-001")
        self.assertEqual(self.pc_ticket.normalize_ticket_id("TASK-002"), "T-002")
        self.assertEqual(self.pc_ticket.normalize_ticket_id("T-003"), "T-003")

    def test_normalize_ticket_id_rejects_invalid(self):
        stderr_capture = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(stderr_capture):
                self.pc_ticket.normalize_ticket_id("BAD")
        self.assertIn("invalid task id", stderr_capture.getvalue())

    def test_format_review_item_marks_failure(self):
        line = self.pc_ticket.format_review_item("make ticket T=T-001", 2)
        self.assertEqual(line, "make ticket T=T-001: FAIL")

    def test_build_gates_block_uses_command(self):
        line = self.pc_ticket.build_gates_block("make ci", "PASS")
        self.assertEqual(line, "- make ci: PASS")

    def test_is_approval_granted(self):
        self.assertTrue(self.pc_ticket.is_approval_granted({"approval": "granted"}))
        self.assertTrue(self.pc_ticket.is_approval_granted({"approval": "GRANTED"}))
        self.assertFalse(self.pc_ticket.is_approval_granted({"approval": "pending"}))
        self.assertFalse(self.pc_ticket.is_approval_granted({}))


if __name__ == "__main__":
    unittest.main()
