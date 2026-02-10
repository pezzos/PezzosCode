import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PP_SCRIPT = ROOT / "tools" / "offload-proxy" / "pp"

REQUIRED_FIELDS = {
    "id",
    "command",
    "work_item_id",
    "agent_name",
    "timestamp",
    "size_bytes",
    "path",
}

random.seed(1337)


class TestOffloadIndex(unittest.TestCase):
    def run_pp(self, command_args, cwd, env=None, check=True):
        cmd = [sys.executable, str(PP_SCRIPT), *command_args]
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=check,
            cwd=cwd,
            env=merged_env,
        )

    def test_offload_creates_index_entry_with_required_fields(self):
        code = """for i in range(250):
    print(f'line {i}')
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            env = {
                "PC_WORK_ITEM_ID": "WI-20260209-01",
                "PC_AGENT_NAME": "Codex",
            }
            result = self.run_pp([sys.executable, "-c", code], tmp_dir, env=env)
            self.assertEqual(result.returncode, 0)

            index_path = Path(tmp_dir) / ".offload" / "index.jsonl"
            self.assertTrue(index_path.exists(), "index file should be created")
            lines = index_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            entry = json.loads(lines[0])

            self.assertTrue(REQUIRED_FIELDS.issubset(entry.keys()))
            self.assertEqual(entry["work_item_id"], "WI-20260209-01")
            self.assertEqual(entry["agent_name"], "Codex")
            stored_path = Path(entry["path"])
            if not stored_path.is_absolute():
                stored_path = Path(tmp_dir) / stored_path
            self.assertIn("line 0", stored_path.read_text(encoding="utf-8"))
            self.assertGreater(entry["size_bytes"], 0)

    def test_list_orders_entries_by_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / ".offload" / "index.jsonl"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            entries = [
                {
                    "id": "bbb",
                    "command": "rg foo",
                    "work_item_id": "WI-20260209-02",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-08T12:00:00Z",
                    "size_bytes": 10,
                    "path": ".offload/bbb.txt",
                },
                {
                    "id": "aaa",
                    "command": "rg bar",
                    "work_item_id": "WI-20260209-01",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-09T12:00:00Z",
                    "size_bytes": 12,
                    "path": ".offload/aaa.txt",
                },
            ]
            index_path.write_text(
                "\n".join(json.dumps(entry, sort_keys=True) for entry in entries)
                + "\n",
                encoding="utf-8",
            )
            result = self.run_pp(["list", "--index", str(index_path)], tmp_dir)
            lines = [json.loads(line) for line in result.stdout.strip().splitlines()]
            self.assertEqual([item["id"] for item in lines], ["aaa", "bbb"])

    def test_list_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / ".offload" / "index.jsonl"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "id": "missing",
                "command": "rg missing",
                "work_item_id": "WI-20260209-03",
                "agent_name": "Codex",
                "timestamp": "2026-02-09T12:00:00Z",
                "size_bytes": 42,
                "path": ".offload/missing.txt",
            }
            index_path.write_text(json.dumps(entry) + "\n", encoding="utf-8")
            result = self.run_pp(
                ["list", "--missing-only", "--index", str(index_path)], tmp_dir
            )
            lines = [json.loads(line) for line in result.stdout.strip().splitlines()]
            self.assertEqual(len(lines), 1)
            self.assertFalse(lines[0].get("file_exists"))

    def test_get_returns_entry_and_handles_unknown_id(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / ".offload" / "index.jsonl"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "id": "known",
                "command": "rg known",
                "work_item_id": "WI-20260209-04",
                "agent_name": "Codex",
                "timestamp": "2026-02-09T12:00:00Z",
                "size_bytes": 42,
                "path": ".offload/known.txt",
            }
            index_path.write_text(json.dumps(entry) + "\n", encoding="utf-8")

            result = self.run_pp(["get", "known", "--index", str(index_path)], tmp_dir)
            payload = json.loads(result.stdout.strip())
            self.assertTrue(REQUIRED_FIELDS.issubset(payload.keys()))

            missing = self.run_pp(
                ["get", "unknown", "--index", str(index_path)],
                tmp_dir,
                check=False,
            )
            self.assertNotEqual(missing.returncode, 0)


if __name__ == "__main__":
    unittest.main()
