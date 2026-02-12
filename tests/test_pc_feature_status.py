import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PC_FEATURE_STATUS_PATH = ROOT / "tools" / "pc-feature-status"


def load_pc_feature_status():
    loader = importlib.machinery.SourceFileLoader(
        "pc_feature_status", str(PC_FEATURE_STATUS_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class TestPcFeatureStatus(unittest.TestCase):
    def setUp(self):
        self.pc_feature_status = load_pc_feature_status()

    def test_format_summary_lines_includes_current_and_slowest_steps(self):
        status = {
            "state": "RUNNING",
            "feature_slug": "18-commit-gated-by-completed-ticket-docs",
            "feature_id": "18",
            "mode": "auto",
            "started_at": "2026-02-12T12:00:00Z",
            "updated_at": "2026-02-12T12:05:00Z",
            "current_step": "tester",
            "current_attempt": 2,
            "last_event": {
                "timestamp": "2026-02-12T12:05:00Z",
                "step": "tester",
                "event": "START",
                "attempt": 2,
            },
            "steps": {
                "planner": {"last_event": "DONE", "last_duration_ms": 2000, "runs": 2},
                "tester": {"last_event": "START", "runs": 2},
            },
        }
        history = [
            {
                "timestamp": "2026-02-12T12:03:00Z",
                "step": "planner",
                "event": "DONE",
                "duration_ms": 2000,
            },
            {
                "timestamp": "2026-02-12T12:04:50Z",
                "step": "tester",
                "event": "DONE",
                "duration_ms": 8000,
            },
        ]
        lines = self.pc_feature_status.format_summary_lines(
            "WI-20260212-11", status, history
        )
        text = "\n".join(lines)
        self.assertIn("current step: tester (attempt 2)", text)
        self.assertIn("slowest steps:", text)
        self.assertIn("1. tester - 8.00s", text)

    def test_format_history_lines_applies_limit(self):
        events = [
            {"timestamp": "2026-02-12T12:00:00Z", "step": "planner", "event": "START"},
            {"timestamp": "2026-02-12T12:01:00Z", "step": "planner", "event": "DONE"},
            {"timestamp": "2026-02-12T12:02:00Z", "step": "tester", "event": "START"},
        ]
        lines = self.pc_feature_status.format_history_lines(events, limit=2)
        text = "\n".join(lines)
        self.assertIn("history: showing 2 of 3 event(s)", text)
        self.assertNotIn("2026-02-12T12:00:00Z", text)
        self.assertIn("2026-02-12T12:01:00Z", text)
        self.assertIn("2026-02-12T12:02:00Z", text)

    def test_resolve_work_item_uses_latest_when_not_provided(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            logs_root = Path(tmp_dir) / "logs"
            first = logs_root / "WI-20260212-01"
            second = logs_root / "WI-20260212-02"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            first.touch()
            second.touch()
            # Make second newer deterministically.
            first_ts = 1000
            second_ts = 2000
            os.utime(first, (first_ts, first_ts))
            os.utime(second, (second_ts, second_ts))
            resolved = self.pc_feature_status.resolve_work_item(logs_root, None)
            self.assertEqual(resolved, "WI-20260212-02")

    def test_read_history_ignores_invalid_lines(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_path = Path(tmp_dir) / "workflow-history.ndjson"
            history_path.write_text(
                '{"timestamp":"2026-02-12T12:00:00Z","step":"planner","event":"START"}\n'
                "not-json\n",
                encoding="utf-8",
            )
            events = self.pc_feature_status.read_history(history_path)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["step"], "planner")

    def test_parse_git_worktree_list_extracts_worktree_paths(self):
        output = (
            "worktree /tmp/repo\n"
            "HEAD 1111111111111111111111111111111111111111\n"
            "branch refs/heads/main\n"
            "\n"
            "worktree /tmp/repo-feature-patcher\n"
            "HEAD 2222222222222222222222222222222222222222\n"
            "branch refs/heads/repo-feature-patcher\n"
        )
        paths = self.pc_feature_status.parse_git_worktree_list(output)
        self.assertEqual(paths, [Path("/tmp/repo"), Path("/tmp/repo-feature-patcher")])

    def test_discover_logs_roots_includes_worktrees(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "repo"
            patcher = Path(tmp_dir) / "repo-feature-patcher"
            root.mkdir()
            patcher.mkdir()
            stdout = f"worktree {root}\n\nworktree {patcher}\n"
            completed = self.pc_feature_status.subprocess.CompletedProcess(
                args=["git"], returncode=0, stdout=stdout, stderr=""
            )
            with mock.patch.object(
                self.pc_feature_status.subprocess, "run", return_value=completed
            ):
                roots = self.pc_feature_status.discover_logs_roots(root)
            self.assertEqual(roots[0], root.resolve() / "logs")
            self.assertIn(patcher.resolve() / "logs", roots)

    def test_resolve_work_item_location_prefers_newest_across_logs_roots(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            root_logs = base / "root" / "logs"
            patcher_logs = base / "patcher" / "logs"
            wi_root = root_logs / "WI-20260212-05"
            wi_patcher = patcher_logs / "WI-20260212-06"
            wi_root.mkdir(parents=True)
            wi_patcher.mkdir(parents=True)
            os.utime(wi_root, (1000, 1000))
            os.utime(wi_patcher, (2000, 2000))

            work_item, logs_root = self.pc_feature_status.resolve_work_item_location(
                [root_logs, patcher_logs], None
            )
            self.assertEqual(work_item, "WI-20260212-06")
            self.assertEqual(logs_root, patcher_logs)

    def test_main_prints_summary_and_history(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            work_item = "WI-20260212-99"
            work_dir = root / "logs" / work_item
            work_dir.mkdir(parents=True)
            status_path = work_dir / "workflow-status.json"
            status_path.write_text(
                json.dumps(
                    {
                        "state": "RUNNING",
                        "current_step": "planner",
                        "current_attempt": 1,
                        "steps": {"planner": {"last_event": "START", "runs": 1}},
                    }
                ),
                encoding="utf-8",
            )
            history_path = work_dir / "workflow-history.ndjson"
            history_path.write_text(
                '{"timestamp":"2026-02-12T12:00:00Z","step":"planner","event":"START"}\n'
                '{"timestamp":"2026-02-12T12:00:03Z","step":"planner","event":"DONE","duration_ms":3000}\n',
                encoding="utf-8",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = self.pc_feature_status.main(
                    [
                        "--root",
                        str(root),
                        "--wi",
                        work_item,
                        "--history",
                        "--limit",
                        "1",
                    ]
                )
            self.assertEqual(code, 0)
            output = stdout.getvalue()
            self.assertIn(f"work item: {work_item}", output)
            self.assertIn(f"logs root: {(root / 'logs').resolve()}", output)
            self.assertIn("history: showing 1 of 2 event(s)", output)
            self.assertIn("2026-02-12T12:00:03Z", output)
            self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
