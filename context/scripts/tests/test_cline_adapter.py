import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from context.scripts.generators.adapters.cline.generator import (
    generate_cline_md,
    generate_cline_rules,
    generate_cline_skills,
)
from context.scripts.generators.adapters.core.models import CanonicalAgent, CanonicalSkill


class TestClineAdapter(unittest.TestCase):
    """Tests for the Cline runtime adapter generator (TDD red)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.context = {
            "agents": {
                "test-agent": CanonicalAgent(
                    name="test-agent",
                    description="A test agent",
                    model="cline-test",
                )
            },
            "workflows": {},
            "skills": {
                "demo-skill": CanonicalSkill(
                    name="demo-skill",
                    description="Run this when executing demo tasks.",
                    globs=["**/demo/**"],
                    body="# Demo Skill\n\nDemo instructions.",
                )
            },
        }
        self.output_dir = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_generate_cline_md(self):
        generate_cline_md(self.context, self.output_dir)

        cline_md_path = self.output_dir / "CLINE.md"
        self.assertTrue(cline_md_path.exists())

        content = cline_md_path.read_text()
        self.assertIn("Auto-generated", content)
        self.assertIn("@AGENTS.md", content)
        self.assertIn("execute_command", content)

    def test_generate_cline_rules(self):
        generate_cline_rules(self.context, self.output_dir)

        rules_file = self.output_dir / ".clinerules" / "00-core.md"
        self.assertTrue(rules_file.exists())

        content = rules_file.read_text()
        # Always-on rule: must NOT carry YAML frontmatter.
        self.assertFalse(content.startswith("---\n"))
        self.assertIn("yarn", content)
        self.assertIn("unknown", content)

    def test_generate_cline_skills(self):
        generate_cline_skills(self.context, self.output_dir)

        skill_file = self.output_dir / ".cline" / "skills" / "demo-skill" / "SKILL.md"
        self.assertTrue(skill_file.exists())

        content = skill_file.read_text()
        self.assertTrue(content.startswith("---\n"))

        frontmatter = yaml.safe_load(content.split("---", 2)[1])
        self.assertEqual(frontmatter["name"], "demo-skill")
        self.assertEqual(frontmatter["description"], "Run this when executing demo tasks.")
        self.assertIn("Auto-generated", content)


if __name__ == "__main__":
    unittest.main()
