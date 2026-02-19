import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "pc-write-prd"


class TestPcWritePrd(unittest.TestCase):
    def test_deterministic_mode_keeps_existing_prd_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            prd_path = root / "docs/01-product/prd.md"
            prd_path.parent.mkdir(parents=True, exist_ok=True)
            original = (
                "# Product Requirements Document (PRD)\n\n## Overview\n\nStable.\n"
            )
            prd_path.write_text(original, encoding="utf-8")

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(f"pc-write-prd failed: {result.stderr}\n{result.stdout}")

            self.assertEqual(prd_path.read_text(encoding="utf-8"), original)
            report = json.loads(
                (root / "docs/03-logs/write-prd-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["decision"], "NO_CHANGE")
            self.assertFalse(report["prd_updated"])
            self.assertTrue((root / "docs/03-logs/write-prd-state.json").exists())

    def test_deterministic_mode_creates_prd_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "docs/01-product").mkdir(parents=True, exist_ok=True)

            result = subprocess.run(
                [
                    "python3",
                    str(TOOL_PATH),
                    f"--root={root}",
                    "--role-mode=deterministic",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode != 0:
                self.fail(f"pc-write-prd failed: {result.stderr}\n{result.stdout}")

            prd_path = root / "docs/01-product/prd.md"
            self.assertTrue(prd_path.exists())
            prd_content = prd_path.read_text(encoding="utf-8")
            self.assertIn("Product Requirements Document", prd_content)
            self.assertIn(f"**Product Name:** {root.name}", prd_content)

            report = json.loads(
                (root / "docs/03-logs/write-prd-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["decision"], "UPDATE")
            self.assertTrue(report["prd_updated"])

    def test_state_cache_marks_second_run_as_cached(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            prd_path = root / "docs/01-product/prd.md"
            prd_path.parent.mkdir(parents=True, exist_ok=True)
            prd_path.write_text(
                "# Product Requirements Document (PRD)\n\n## Overview\n\nCached.\n",
                encoding="utf-8",
            )

            command = [
                "python3",
                str(TOOL_PATH),
                f"--root={root}",
                "--role-mode=deterministic",
            ]
            first = subprocess.run(
                command,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            second = subprocess.run(
                command,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if first.returncode != 0 or second.returncode != 0:
                self.fail(
                    f"pc-write-prd failed across reruns:\n"
                    f"first stderr={first.stderr}\nsecond stderr={second.stderr}"
                )

            report = json.loads(
                (root / "docs/03-logs/write-prd-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertTrue(report["from_cache"])
            self.assertEqual(report["decision"], "NO_CHANGE")


if __name__ == "__main__":
    unittest.main()
