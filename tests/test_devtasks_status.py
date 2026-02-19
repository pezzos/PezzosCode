import unittest

from lib.devtasks_status import (
    ALLOWED_STATUS_VALUES,
    is_completed_status,
    parse_status_from_content,
    status_format_errors,
)


class TestDevtasksStatus(unittest.TestCase):
    def test_parse_status_from_content_reads_canonical_line(self):
        status, note = parse_status_from_content("Status: In Progress\n")
        self.assertEqual(status, "In Progress")
        self.assertIsNone(note)

    def test_parse_status_from_content_rejects_legacy_bold_line(self):
        status, note = parse_status_from_content("**Status:** Done\n")
        self.assertIsNone(status)
        self.assertEqual(note, "legacy '**Status:**' format is not allowed")

    def test_status_format_errors_reports_missing_canonical_line(self):
        errors = status_format_errors("## Execution Log\n")
        self.assertIn("missing canonical 'Status:' line", errors)

    def test_status_format_errors_rejects_non_enum_values(self):
        errors = status_format_errors("Status: Completed\n")
        self.assertTrue(any("invalid status value" in item for item in errors))

    def test_is_completed_status_matches_done_only(self):
        self.assertTrue(is_completed_status("Done"))
        self.assertFalse(is_completed_status("Completed"))
        self.assertFalse(is_completed_status("Complete"))
        self.assertFalse(is_completed_status("In Progress"))

    def test_allowed_values_constant(self):
        self.assertEqual(ALLOWED_STATUS_VALUES, ("Not Started", "In Progress", "Done"))


if __name__ == "__main__":
    unittest.main()
