import importlib.util
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "pc-skills-metadata-check"


def load_tool():
    loader = SourceFileLoader("pc_skills_metadata_check", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def seed_skill(
    root: Path,
    name: str = "demo-skill",
    *,
    description: str = "Do useful work. Use when the user asks for deterministic docs updates.",
    short_description: str = "Deterministic workflow helper skill",
    default_prompt: str = "Use $demo-skill to run deterministic workflow updates.",
) -> None:
    skill_dir = root / ".codex" / "skills" / name
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                f"description: {description}",
                "---",
                "",
                "# Demo",
                "",
                "Sample body.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (agents_dir / "openai.yaml").write_text(
        "\n".join(
            [
                "interface:",
                '  display_name: "Demo Skill"',
                f'  short_description: "{short_description}"',
                f'  default_prompt: "{default_prompt}"',
                "",
            ]
        ),
        encoding="utf-8",
    )


class TestPcSkillsMetadataCheck(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()

    def test_valid_skill_passes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            seed_skill(root)

            errors, count = self.tool.run_check(root)

            self.assertEqual(count, 1)
            self.assertEqual(errors, [])

    def test_default_prompt_requires_skill_token(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            seed_skill(
                root,
                default_prompt="Use this helper to run deterministic workflow updates.",
            )

            errors, _ = self.tool.run_check(root)

            self.assertTrue(
                any(
                    "default_prompt must mention $demo-skill" in item for item in errors
                )
            )

    def test_short_description_length_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            seed_skill(root, short_description="too short")

            errors, _ = self.tool.run_check(root)

            self.assertTrue(any("short_description length" in item for item in errors))

    def test_absolute_local_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            seed_skill(root)
            skill_md = root / ".codex" / "skills" / "demo-skill" / "SKILL.md"
            skill_md.write_text(
                skill_md.read_text(encoding="utf-8")
                + "\nUse /Users/example/local/path for manual testing.\n",
                encoding="utf-8",
            )

            errors, _ = self.tool.run_check(root)

            self.assertTrue(any("absolute local path found" in item for item in errors))

    def test_policy_allow_implicit_invocation_must_be_boolean(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            seed_skill(root)
            openai = (
                root / ".codex" / "skills" / "demo-skill" / "agents" / "openai.yaml"
            )
            openai.write_text(
                openai.read_text(encoding="utf-8")
                + "policy:\n"
                + '  allow_implicit_invocation: "false"\n',
                encoding="utf-8",
            )

            errors, _ = self.tool.run_check(root)

            self.assertTrue(
                any(
                    "allow_implicit_invocation must be boolean" in item
                    for item in errors
                )
            )


if __name__ == "__main__":
    unittest.main()
