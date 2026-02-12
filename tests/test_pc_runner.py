import json
import tempfile
import unittest
from pathlib import Path

from lib.pc_runner import (
    RunMetadata,
    format_log_line,
    init_workflow_tracking,
    log_message,
    record_workflow_event,
)


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

    def test_init_workflow_tracking_creates_status_and_history(self):
        metadata = RunMetadata("WI-20260212-01", "pc-feature", "run789")
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            status_path, history_path = init_workflow_tracking(
                metadata,
                root=root,
                feature_id="18",
                feature_slug="18-commit-gated-by-completed-ticket-docs",
                mode="auto",
                timestamp="2026-02-12T12:00:00Z",
            )
            self.assertTrue(status_path.exists())
            self.assertTrue(history_path.exists())
            payload = json.loads(status_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["work_item_id"], "WI-20260212-01")
            self.assertEqual(payload["feature_id"], "18")
            self.assertEqual(payload["mode"], "auto")
            self.assertEqual(payload["state"], "RUNNING")
            self.assertEqual(payload["current_step"], None)

    def test_record_workflow_event_updates_duration_and_history(self):
        metadata = RunMetadata("WI-20260212-01", "pc-feature", "run999")
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            status_path, history_path = init_workflow_tracking(
                metadata,
                root=root,
                timestamp="2026-02-12T12:00:00Z",
            )
            record_workflow_event(
                metadata,
                step="planner",
                event="START",
                attempt=1,
                root=root,
                timestamp="2026-02-12T12:00:05Z",
            )
            done_event = record_workflow_event(
                metadata,
                step="planner",
                event="DONE",
                attempt=1,
                outcome="UPDATED",
                root=root,
                timestamp="2026-02-12T12:00:15Z",
            )
            self.assertEqual(done_event["duration_ms"], 10000)
            status_payload = json.loads(status_path.read_text(encoding="utf-8"))
            planner_state = status_payload["steps"]["planner"]
            self.assertEqual(planner_state["last_event"], "DONE")
            self.assertEqual(planner_state["last_duration_ms"], 10000)
            self.assertEqual(status_payload["current_step"], None)
            history_lines = [
                line
                for line in history_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(history_lines), 2)
            last = json.loads(history_lines[-1])
            self.assertEqual(last["event"], "DONE")
            self.assertEqual(last["step"], "planner")


if __name__ == "__main__":
    unittest.main()
