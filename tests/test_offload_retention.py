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

random.seed(1337)


class TestOffloadRetention(unittest.TestCase):
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

    def write_index(self, root: Path, entries: list[dict]):
        index_path = root / ".offload" / "index.jsonl"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(
            "\n".join(json.dumps(entry, sort_keys=True) for entry in entries) + "\n",
            encoding="utf-8",
        )
        return index_path

    def test_purge_respects_max_age_and_protected_work_items(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            old_path = root / ".offload" / "old.txt"
            old_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.write_text("old", encoding="utf-8")

            entries = [
                {
                    "id": "old",
                    "command": "rg old",
                    "work_item_id": "WI-KEEP",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-01T00:00:00Z",
                    "size_bytes": 3,
                    "path": str(old_path),
                },
                {
                    "id": "new",
                    "command": "rg new",
                    "work_item_id": "WI-DROP",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-02T00:00:00Z",
                    "size_bytes": 0,
                    "path": str(root / ".offload" / "new.txt"),
                },
            ]
            index_path = self.write_index(root, entries)
            env = {"PP_NOW": "2026-02-09T00:00:00Z"}
            result = self.run_pp(
                [
                    "purge",
                    "--max-age-days",
                    "3",
                    "--protect-work-item",
                    "WI-KEEP",
                    "--index",
                    str(index_path),
                ],
                tmp_dir,
                env=env,
            )
            lines = [json.loads(line) for line in result.stdout.strip().splitlines()]
            summary = lines[-1]["summary"]
            self.assertEqual(summary["removed"], 1)
            self.assertEqual(summary["kept"], 1)

            remaining_ids = {
                json.loads(line)["id"]
                for line in index_path.read_text(encoding="utf-8").splitlines()
            }
            self.assertEqual(remaining_ids, {"old"})

    def test_purge_enforces_max_count_and_handles_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            newest_path = root / ".offload" / "newest.txt"
            newest_path.parent.mkdir(parents=True, exist_ok=True)
            newest_path.write_text("newest", encoding="utf-8")

            entries = [
                {
                    "id": "first",
                    "command": "rg first",
                    "work_item_id": "WI-1",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-06T00:00:00Z",
                    "size_bytes": 0,
                    "path": str(root / ".offload" / "first.txt"),
                },
                {
                    "id": "second",
                    "command": "rg second",
                    "work_item_id": "WI-2",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-07T00:00:00Z",
                    "size_bytes": 0,
                    "path": str(root / ".offload" / "second.txt"),
                },
                {
                    "id": "newest",
                    "command": "rg newest",
                    "work_item_id": "WI-3",
                    "agent_name": "Codex",
                    "timestamp": "2026-02-08T00:00:00Z",
                    "size_bytes": 6,
                    "path": str(newest_path),
                },
            ]
            index_path = self.write_index(root, entries)
            env = {"PP_NOW": "2026-02-09T00:00:00Z"}
            result = self.run_pp(
                ["purge", "--max-count", "1", "--index", str(index_path)],
                tmp_dir,
                env=env,
            )
            lines = [json.loads(line) for line in result.stdout.strip().splitlines()]
            summary = lines[-1]["summary"]
            self.assertEqual(summary["removed"], 2)
            self.assertEqual(summary["kept"], 1)
            self.assertEqual(
                [item["id"] for item in lines[:-1]], ["newest", "second", "first"]
            )

            remaining_ids = {
                json.loads(line)["id"]
                for line in index_path.read_text(encoding="utf-8").splitlines()
            }
            self.assertEqual(remaining_ids, {"newest"})


if __name__ == "__main__":
    unittest.main()
