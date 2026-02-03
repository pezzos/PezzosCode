import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PP_SCRIPT = ROOT / "tools" / "offload-proxy" / "pp"


class TestOffloadProxyCLI(unittest.TestCase):
    POINTER_PREFIX = "[pp] offloaded output id:"

    def run_pp(self, command_args, cwd, env=None):
        cmd = [sys.executable, str(PP_SCRIPT), *command_args]
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=True,
            cwd=cwd,
            env=merged_env,
        )

    def extract_pointer_id(self, output: str):
        for line in output.splitlines():
            if line.startswith(self.POINTER_PREFIX):
                return line.split(":", 1)[1].strip()
        return None

    def test_pp_offloads_large_output_and_records_pointer_id(self):
        code = """for i in range(300):
    print(f'line {i}')
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.run_pp([sys.executable, "-c", code], tmp_dir)
            stdout = result.stdout or ""

            self.assertIn(self.POINTER_PREFIX, stdout, "pp should log the pointer id")
            self.assertIn("line 0", stdout)
            self.assertIn("line 299", stdout)
            self.assertIn("...", stdout)

            pointer_id = self.extract_pointer_id(stdout)
            self.assertIsNotNone(pointer_id, "Pointer id should be emitted")
            pointer_id = pointer_id or ""
            self.assertRegex(pointer_id, r"^[0-9a-f]{64}$")

            offload_path = Path(tmp_dir) / ".offload" / f"{pointer_id}.txt"
            self.assertTrue(offload_path.exists(), "offload file must be created")
            content = offload_path.read_text(encoding="utf-8")
            self.assertIn("line 0", content)
            self.assertIn("line 299", content)

    def test_pp_honors_always_offload_config_for_any_output(self):
        custom_prefix = f"{sys.executable} -c"
        config_path = Path(tempfile.mkdtemp()) / "pp_custom.yml"
        config_path.write_text(
            f"always_offload:\n- {custom_prefix}\n", encoding="utf-8"
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.run_pp(
                [sys.executable, "-c", "print('short output')"],
                tmp_dir,
                env={"PP_CONFIG": str(config_path)},
            )
            stdout = result.stdout or ""
            pointer_id = self.extract_pointer_id(stdout)
            self.assertIsNotNone(
                pointer_id, "always_offload commands should still emit an id"
            )
            pointer_id = pointer_id or ""
            offload_path = Path(tmp_dir) / ".offload" / f"{pointer_id}.txt"
            self.assertTrue(offload_path.exists())
            self.assertEqual(
                offload_path.read_text(encoding="utf-8").strip(), "short output"
            )


if __name__ == "__main__":
    unittest.main()
