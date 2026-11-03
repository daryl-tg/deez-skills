import tempfile
import unittest
from pathlib import Path

from deezlib import doctor, registry

BASE = """
[meta]
version = 1
default_profile = "full"

[categories]
core = "Always-on essentials"

[profiles]
full = ["*"]

[skills.verify-app]
project = "app"
category = "core"
runtimes = ["claude"]
"""

FRONTMATTER = "---\nname: verify-app\ndescription: Drive the app.\n---\n\n"


class MapPublishRuleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo / "registry.toml").write_text(BASE)
        self.skill = self.repo / "projects" / "app" / "skills" / "verify-app"
        self.skill.mkdir(parents=True)

    def findings(self, body, with_map=True):
        (self.skill / "SKILL.md").write_text(FRONTMATTER + body)
        if with_map:
            (self.skill / "features").mkdir(exist_ok=True)
            (self.skill / "features" / "README.md").write_text("# Map\n")
        reg = registry.load(self.repo / "registry.toml")
        return doctor.check_map_publish_rule(reg, self.repo)

    def test_a_mapped_skill_that_never_says_how_to_publish_fails(self):
        found = self.findings("Drive the app.\n")
        self.assertEqual(["map-publish-rule"], [f.code for f in found])
        self.assertEqual("fail", found[0].level)
        self.assertIn("bin/deez sync-feature-maps", found[0].detail)
        self.assertIn("projects/app/skills/verify-app/SKILL.md", found[0].detail)

    def test_naming_the_publish_command_passes(self):
        body = "Push changed maps with `bin/deez sync-feature-maps app verify-app`.\n"
        self.assertEqual([], self.findings(body))

    def test_a_skill_without_a_map_is_not_checked(self):
        self.assertEqual([], self.findings("Drive the app.\n", with_map=False))


if __name__ == "__main__":
    unittest.main()
