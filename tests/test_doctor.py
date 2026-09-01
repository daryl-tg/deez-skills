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
"""

ENTRY = """
[skills.alpha]
category = "core"
runtimes = ["claude"]
"""


class DoctorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        (self.repo / "skills").mkdir(parents=True)
        (self.repo / "commands").mkdir()
        (self.repo / "agents").mkdir()
        self.skills_root = self.root / "claude" / "skills"
        self.skills_root.mkdir(parents=True)
        self.roots = {"claude": {"skill": self.skills_root}}

    def make_skill(self, name, description="A short description."):
        folder = self.repo / "skills" / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\nBody\n"
        )
        return folder

    def load(self, extra=""):
        path = self.repo / "registry.toml"
        path.write_text(BASE + extra)
        return registry.load(path)

    def codes(self, findings):
        return sorted(f.code for f in findings)

    def check(self, reg):
        return doctor.check(reg, self.repo, self.roots, "full")

    def test_empty_registry_is_clean(self):
        self.assertEqual(self.check(self.load()), [])

    def test_registry_entry_without_a_folder_fails(self):
        self.assertIn("missing-source", self.codes(self.check(self.load(ENTRY))))

    def test_folder_without_a_registry_entry_fails(self):
        self.make_skill("stray")
        self.assertIn("unregistered", self.codes(self.check(self.load())))

    def test_frontmatter_name_mismatch_fails(self):
        folder = self.make_skill("alpha")
        (folder / "SKILL.md").write_text("---\nname: WRONG\ndescription: d\n---\n")
        self.assertIn("name-mismatch", self.codes(self.check(self.load(ENTRY))))

    def test_alias_install_name_is_what_frontmatter_must_match(self):
        folder = self.repo / "skills" / "alpha"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("---\nname: renamed\ndescription: d\n---\n")
        reg = self.load("""
[skills.alpha]
category = "core"
runtimes = ["claude"]
install_as = { claude = "renamed" }
""")
        self.assertNotIn("name-mismatch", self.codes(self.check(reg)))

    def test_description_over_300_chars_fails(self):
        self.make_skill("alpha", "x" * 301)
        self.assertIn("description-too-long", self.codes(self.check(self.load(ENTRY))))

    def test_description_over_200_chars_warns(self):
        self.make_skill("alpha", "x" * 250)
        warn = [f for f in self.check(self.load(ENTRY)) if f.code == "description-long"]
        self.assertEqual([f.level for f in warn], ["warn"])

    def test_wholly_unlinked_is_the_pre_migration_state_not_drift(self):
        self.make_skill("alpha")
        findings = self.check(self.load(ENTRY))
        self.assertIn("unlinked", [f.code for f in findings])
        self.assertEqual([f for f in findings if f.level == "fail"], [])

    def test_correctly_linked_entry_is_clean(self):
        source = self.make_skill("alpha")
        (self.skills_root / "alpha").symlink_to(source)
        self.assertEqual(self.check(self.load(ENTRY)), [])

    def _install_a_correct_link(self):
        """Drift codes only apply once the hub is actually installed."""
        anchor = self.make_skill("anchor")
        (self.skills_root / "anchor").symlink_to(anchor)
        return ENTRY + """
[skills.anchor]
category = "core"
runtimes = ["claude"]
"""

    def test_real_directory_at_destination_is_not_symlink(self):
        entry = self._install_a_correct_link()
        self.make_skill("alpha")
        (self.skills_root / "alpha").mkdir()
        self.assertIn("not-symlink", self.codes(self.check(self.load(entry))))

    def test_symlink_to_the_wrong_place_is_wrong_target(self):
        entry = self._install_a_correct_link()
        self.make_skill("alpha")
        other = self.root / "elsewhere"
        other.mkdir()
        (self.skills_root / "alpha").symlink_to(other)
        self.assertIn("wrong-target", self.codes(self.check(self.load(entry))))

    def test_orphans_are_warnings_only(self):
        orphan = self.skills_root / "ancient-go-style"
        orphan.mkdir()
        (orphan / "SKILL.md").write_text("---\nname: ancient-go-style\ndescription: d\n---\n")
        findings = doctor.orphans(self.roots, self.load())
        self.assertEqual([f.level for f in findings], ["warn"])
        self.assertIn("ancient-go-style", findings[0].detail)

    def test_managed_symlinks_are_not_orphans(self):
        source = self.make_skill("alpha")
        (self.skills_root / "alpha").symlink_to(source)
        self.assertEqual(doctor.orphans(self.roots, self.load(ENTRY)), [])


if __name__ == "__main__":
    unittest.main()
