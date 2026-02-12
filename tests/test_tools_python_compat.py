import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"


def python_tool_scripts() -> list[Path]:
    scripts: list[Path] = []
    for path in sorted(TOOLS_DIR.iterdir()):
        if not path.is_file():
            continue
        first_line = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        if first_line and "python3" in first_line[0]:
            scripts.append(path)
    return scripts


def has_future_annotations_import(content: str) -> bool:
    return bool(
        re.search(
            r"^\s*from\s+__future__\s+import\s+annotations\s*$",
            content,
            flags=re.MULTILINE,
        )
    )


class TestToolsPythonCompat(unittest.TestCase):
    def test_union_annotations_require_future_import(self):
        offenders = []
        for script in python_tool_scripts():
            content = script.read_text(encoding="utf-8", errors="replace")
            if "| None" not in content:
                continue
            if has_future_annotations_import(content):
                continue
            offenders.append(str(script.relative_to(ROOT)))
        self.assertEqual(
            offenders,
            [],
            "Python tool scripts using '| None' must import __future__.annotations: "
            + ", ".join(offenders),
        )

    def test_markdown_lint_runs_on_system_python39(self):
        system_python = Path("/usr/bin/python3")
        if not system_python.exists():
            self.skipTest("/usr/bin/python3 is not available on this host")

        version_output = subprocess.check_output(
            [str(system_python), "--version"],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_output)
        if not match:
            self.skipTest(f"Unable to parse system python version: {version_output}")
        major, minor, _patch = (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )
        if (major, minor) != (3, 9):
            self.skipTest(f"System python is {major}.{minor}; test is specific to 3.9")

        markdown_lint = ROOT / "tools" / "markdown-lint"
        with tempfile.TemporaryDirectory() as tmp_dir:
            md_path = Path(tmp_dir) / "ok.md"
            md_path.write_text("# Title\n", encoding="utf-8")
            completed = subprocess.run(
                [str(system_python), str(markdown_lint), str(md_path)],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(
            completed.returncode,
            0,
            f"markdown-lint should run under system Python 3.9. stderr:\n{completed.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
