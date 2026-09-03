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

MODE = """
[skills.router]
layer = "mode"
category = "core"
runtimes = ["claude"]
"""


class PlaybookReferenceTest(unittest.TestCase):
    """A playbook that points at a sibling which does not exist dead-ends."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        (self.repo / "skills").mkdir(parents=True)
        self.playbooks = self.repo / "skills" / "router" / "playbooks"
        self.playbooks.mkdir(parents=True)
        folder = self.repo / "skills" / "router"
        (folder / "SKILL.md").write_text(
            "---\nname: router\ndescription: A router.\n"
            "disable-model-invocation: true\n---\n\nBody\n"
        )

    def load(self):
        path = self.repo / "registry.toml"
        path.write_text(BASE + MODE)
        return registry.load(path)

    def playbook(self, name, body):
        (self.playbooks / f"{name}.md").write_text(body)

    def codes(self):
        return sorted(f.code for f in doctor.check_playbook_links(self.load(), self.repo))

    def details(self):
        return [f.detail for f in doctor.check_playbook_links(self.load(), self.repo)]

    def test_a_reference_to_a_missing_playbook_fails(self):
        self.playbook("feature", "Then run `playbooks/opening-a-review.md`.")
        self.assertIn("dangling-playbook", self.codes())

    def test_the_message_names_the_missing_file(self):
        self.playbook("feature", "Then run `playbooks/opening-a-review.md`.")
        self.assertTrue(any("opening-a-review.md" in d for d in self.details()))

    def test_a_reference_to_a_present_playbook_passes(self):
        self.playbook("feature", "Then run `playbooks/opening-a-review.md`.")
        self.playbook("opening-a-review", "Rebase, then open it.")
        self.assertEqual(self.codes(), [])

    def test_a_playbook_referencing_itself_passes(self):
        self.playbook("feature", "Re-enter `playbooks/feature.md` at the first unproven step.")
        self.assertEqual(self.codes(), [])

    def test_the_mode_skill_body_is_checked_too(self):
        folder = self.repo / "skills" / "router"
        (folder / "SKILL.md").write_text(
            "---\nname: router\ndescription: A router.\n"
            "disable-model-invocation: true\n---\n\n"
            "| `playbooks/ghost.md` | never written |\n"
        )
        self.assertIn("dangling-playbook", self.codes())

    def test_a_skill_with_no_playbooks_directory_is_skipped(self):
        import shutil

        shutil.rmtree(self.playbooks)
        self.assertEqual(self.codes(), [])


class RoleCheckTest(unittest.TestCase):
    """check_roles existed but nothing called it, so a bogus role never failed."""

    def test_doctor_runs_the_role_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            (repo / "skills" / "router" / "playbooks").mkdir(parents=True)
            (repo / "skills" / "router" / "SKILL.md").write_text(
                "---\nname: router\ndescription: A router.\n"
                "disable-model-invocation: true\n---\n\nBody\n"
            )
            (repo / "skills" / "router" / "playbooks" / "feature.md").write_text(
                "Hand it to the **implementor** role.\n"
            )
            path = repo / "registry.toml"
            path.write_text(BASE + MODE)
            reg = registry.load(path)
            roots = {
                "claude": {"skill": root / "c" / "skills"},
                "codex": {"skill": root / "x" / "skills"},
            }
            for r in roots.values():
                r["skill"].mkdir(parents=True)
            codes = [f.code for f in doctor.check(reg, repo, roots, "full")]
            self.assertIn("unknown-role", codes)

    def test_a_known_role_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            (repo / "skills" / "router" / "playbooks").mkdir(parents=True)
            (repo / "skills" / "router" / "SKILL.md").write_text(
                "---\nname: router\ndescription: A router.\n"
                "disable-model-invocation: true\n---\n\nBody\n"
            )
            (repo / "skills" / "router" / "playbooks" / "feature.md").write_text(
                "Hand it to the **executor** role.\n"
            )
            path = repo / "registry.toml"
            path.write_text(BASE + MODE)
            reg = registry.load(path)
            roots = {
                "claude": {"skill": root / "c" / "skills"},
                "codex": {"skill": root / "x" / "skills"},
            }
            for r in roots.values():
                r["skill"].mkdir(parents=True)
            codes = [f.code for f in doctor.check(reg, repo, roots, "full")]
            self.assertNotIn("unknown-role", codes)

    def test_the_five_roles_are_named_in_one_place(self):
        self.assertEqual(
            doctor.ROLES,
            ("explore", "executor", "test-engineer", "code-reviewer", "verifier"),
        )


if __name__ == "__main__":
    unittest.main()
