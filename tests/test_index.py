import tempfile
import unittest
from pathlib import Path

from deezlib import index, registry

BASE = """
[meta]
version = 1
default_profile = "full"

[categories]
core = "Always-on essentials"
writing = "Writing and editing"

[profiles]
full = ["*"]
"""

HUMANIZE = """
[skills.humanize]
category = "writing"
runtimes = ["claude"]
"""


class IndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo / "skills").mkdir()

    def make_skill(self, name, description):
        folder = self.repo / "skills" / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n"
        )

    def load(self, extra=""):
        path = self.repo / "registry.toml"
        path.write_text(BASE + extra)
        return registry.load(path)

    def test_empty_registry_renders_a_placeholder(self):
        self.assertIn("No entries yet", index.render(self.load(), self.repo))

    def test_groups_by_category_with_runtime_column(self):
        self.make_skill("humanize", "Rewrites text.")
        rendered = index.render(self.load(HUMANIZE), self.repo)
        self.assertIn("### Writing and editing", rendered)
        self.assertIn("humanize", rendered)
        self.assertIn("Rewrites text.", rendered)
        self.assertIn("claude", rendered)

    def test_pipes_in_a_description_are_escaped(self):
        self.make_skill("humanize", "Does a | b.")
        self.assertIn("a \\| b", index.render(self.load(HUMANIZE), self.repo))

    def test_write_preserves_content_above_the_marker(self):
        readme = self.repo / "README.md"
        readme.write_text(f"# deez-skills\n\nHand-written intro.\n\n{index.MARKER}\nOLD\n")
        index.write(self.load(), self.repo, readme)
        text = readme.read_text()
        self.assertIn("Hand-written intro.", text)
        self.assertNotIn("OLD", text)

    def test_is_stale_is_false_right_after_write(self):
        readme = self.repo / "README.md"
        readme.write_text(f"# x\n\n{index.MARKER}\n")
        reg = self.load()
        index.write(reg, self.repo, readme)
        self.assertFalse(index.is_stale(reg, self.repo, readme))

    def test_is_stale_is_true_when_an_entry_is_added(self):
        readme = self.repo / "README.md"
        readme.write_text(f"# x\n\n{index.MARKER}\n")
        index.write(self.load(), self.repo, readme)
        self.make_skill("humanize", "Rewrites text.")
        self.assertTrue(index.is_stale(self.load(HUMANIZE), self.repo, readme))

    def test_write_returns_false_when_nothing_changed(self):
        readme = self.repo / "README.md"
        readme.write_text(f"# x\n\n{index.MARKER}\n")
        reg = self.load()
        self.assertTrue(index.write(reg, self.repo, readme))
        self.assertFalse(index.write(reg, self.repo, readme))


if __name__ == "__main__":
    unittest.main()
