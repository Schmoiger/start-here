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
from context.scripts.generators.adapters.core.models import (
    CanonicalAgent,
    CanonicalRule,
    CanonicalSkill,
)


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
            "rules": {
                "bash-environment": CanonicalRule(
                    name="bash-environment",
                    description="Bash invocation safety",
                    globs=[],
                    alwaysApply=True,
                    body=(
                        "# Bash Environment\n\n"
                        "**Applies to**: All bash commands and file operations\n\n"
                        "---\n\n"
                        "| Action | Correct | Wrong |\n"
                        "|--------|---------|-------|\n"
                        "| Create file | Write tool | `echo` > file, heredoc |"
                    ),
                ),
                "secrets": CanonicalRule(
                    name="secrets",
                    description="Secrets handling",
                    globs=["**/.env"],
                    alwaysApply=False,
                    body="# Secrets\n\nNever commit secrets.",
                ),
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
        # The agent-sandbox routing bullet lives in the always-on .clinerules.
        self.assertNotIn("consult the **agent-sandbox**", content)

    def test_generate_cline_rules(self):
        generate_cline_rules(self.context, self.output_dir)

        rules_file = self.output_dir / ".clinerules" / "00-core.md"
        self.assertTrue(rules_file.exists())

        content = rules_file.read_text()
        # Always-on rule: must NOT carry YAML frontmatter.
        self.assertFalse(content.startswith("---\n"))
        self.assertIn("yarn", content)
        self.assertIn("unknown", content)
        # Routing bullet directs terminal work to the agent-sandbox skill.
        self.assertIn("agent-sandbox", content)

        # alwaysApply: true rules are projected as frontmatter-less always-on files.
        bash_rule = self.output_dir / ".clinerules" / "bash-environment.md"
        self.assertTrue(bash_rule.exists())
        bash_content = bash_rule.read_text()
        self.assertFalse(bash_content.startswith("---\n"))
        self.assertIn("heredoc", bash_content)
        self.assertIn("Auto-generated", bash_content)

        # Non-alwaysApply rules are NOT projected into always-on rules.
        self.assertFalse((self.output_dir / ".clinerules" / "secrets.md").exists())

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
