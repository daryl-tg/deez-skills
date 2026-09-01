import tempfile
import unittest
from pathlib import Path

from deezlib import linkplan, registry

BASE = """
[meta]
version = 1
default_profile = "full"

[categories]
core = "Always-on essentials"

[profiles]
full = ["*"]
"""

ENTRY = """
[skills.alpha]
category = "core"
runtimes = ["claude"]
"""


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.claude = self.root / "claude"
        (self.claude / "skills").mkdir(parents=True)
        self.roots = {"claude": {"skill": self.claude / "skills"}}

    def build(self, extra="", make_source=True):
        path = self.repo / "registry.toml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(BASE + extra)
        if make_source:
            source = self.repo / "skills" / "alpha"
            source.mkdir(parents=True, exist_ok=True)
            (source / "SKILL.md").write_text("---\nname: alpha\ndescription: d\n---\n")
        return registry.load(path)

    def plan(self, reg):
        return linkplan.compute(reg, self.repo, self.roots, "full")

    def test_empty_registry_produces_no_actions(self):
        self.assertEqual(self.plan(self.build()), [])

    def test_absent_destination_is_a_link(self):
        actions = self.plan(self.build(ENTRY))
        self.assertEqual([a.verb for a in actions], ["link"])
        self.assertEqual(actions[0].dest, self.claude / "skills" / "alpha")
        self.assertEqual(actions[0].src, self.repo / "skills" / "alpha")

    def test_correct_symlink_is_ok(self):
        reg = self.build(ENTRY)
        (self.claude / "skills" / "alpha").symlink_to(self.repo / "skills" / "alpha")
        self.assertEqual([a.verb for a in self.plan(reg)], ["ok"])

    def test_symlink_elsewhere_is_relink(self):
        reg = self.build(ENTRY)
        other = self.root / "other"
        other.mkdir()
        (self.claude / "skills" / "alpha").symlink_to(other)
        self.assertEqual([a.verb for a in self.plan(reg)], ["relink"])

    def test_identical_real_directory_is_adopt(self):
        reg = self.build(ENTRY)
        dest = self.claude / "skills" / "alpha"
        dest.mkdir()
        (dest / "SKILL.md").write_text("---\nname: alpha\ndescription: d\n---\n")
        self.assertEqual([a.verb for a in self.plan(reg)], ["adopt"])

    def test_differing_real_directory_is_backup(self):
        reg = self.build(ENTRY)
        dest = self.claude / "skills" / "alpha"
        dest.mkdir()
        (dest / "SKILL.md").write_text("---\nname: alpha\ndescription: DIFFERENT\n---\n")
        self.assertEqual([a.verb for a in self.plan(reg)], ["backup"])

    def test_nested_difference_is_still_backup(self):
        reg = self.build(ENTRY)
        (self.repo / "skills" / "alpha" / "references").mkdir()
        (self.repo / "skills" / "alpha" / "references" / "a.md").write_text("repo\n")
        dest = self.claude / "skills" / "alpha"
        (dest / "references").mkdir(parents=True)
        (dest / "SKILL.md").write_text("---\nname: alpha\ndescription: d\n---\n")
        (dest / "references" / "a.md").write_text("different\n")
        self.assertEqual([a.verb for a in self.plan(reg)], ["backup"])

    def test_absent_source_is_missing_source(self):
        reg = self.build(ENTRY, make_source=False)
        self.assertEqual([a.verb for a in self.plan(reg)], ["missing-source"])

    def test_planning_never_creates_anything(self):
        reg = self.build(ENTRY)
        before = sorted(p.name for p in (self.claude / "skills").iterdir())
        self.plan(reg)
        after = sorted(p.name for p in (self.claude / "skills").iterdir())
        self.assertEqual(before, after)

    def test_codex_only_kinds_are_skipped_without_a_root(self):
        reg = self.build(ENTRY + """
[commands.only-claude]
category = "core"
runtimes = ["claude"]
""")
        self.roots["claude"].pop("command", None)
        self.assertEqual([a.name for a in self.plan(reg)], ["alpha"])


if __name__ == "__main__":
    unittest.main()
