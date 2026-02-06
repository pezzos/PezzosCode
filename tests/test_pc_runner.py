import tempfile
import unittest
from pathlib import Path

from lib.pc_runner import RunMetadata, format_log_line, log_message


class TestPcRunner(unittest.TestCase):
    def test_log_prefix_formatting(self):
        metadata = RunMetadata("WI-20260205-01", "pc-feature", "run123")
        line = format_log_line(
            metadata,
            "feature",
            "hello world",
            timestamp="2026-02-05T12:00:00",
        )
        self.assertEqual(
            line,
            "2026-02-05T12:00:00 [WI-20260205-01][pc-feature][feature] "
            "hello world\n",
        )

    def test_log_path_creation(self):
        metadata = RunMetadata("WI-20260205-01", "pc-precommit", "run456")
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            log_path = log_message(
                metadata,
                "precommit",
                "started",
                root=root,
                timestamp="2026-02-05T12:01:00",
            )
            expected = root / "logs" / "WI-20260205-01" / "precommit.log"
            self.assertEqual(log_path, expected)
            self.assertTrue(expected.exists())
            content = expected.read_text(encoding="utf-8")
            self.assertIn("[WI-20260205-01][pc-precommit][precommit]", content)


if __name__ == "__main__":
    unittest.main()
