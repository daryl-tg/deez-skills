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


class DoctorLayerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        for d in ("skills", "commands", "agents"):
            (self.repo / d).mkdir(parents=True)
        self.roots = {
            "claude": {"skill": self.root / "c" / "skills"},
            "codex": {"skill": self.root / "x" / "skills"},
        }
        for r in self.roots.values():
            r["skill"].mkdir(parents=True)

    def skill(self, name, body="Body", flag=False, desc="A short description."):
        f = self.repo / "skills" / name
        f.mkdir(parents=True, exist_ok=True)
        fm = f"---\nname: {name}\ndescription: {desc}\n"
        if flag:
            fm += "disable-model-invocation: true\n"
        fm += "---\n\n" + body + "\n"
        (f / "SKILL.md").write_text(fm)
        # link both runtimes so link-state checks stay quiet
        for rt, roots in self.roots.items():
            dest = roots["skill"] / name
            if not dest.exists():
                dest.symlink_to(f)
        return f

    def load(self, extra):
        path = self.repo / "registry.toml"
        path.write_text(BASE + extra)
        return registry.load(path)

    def codes(self, reg):
        return sorted(f.code for f in doctor.check(reg, self.repo, self.roots, "full"))

    PRINCIPLE = """
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]
"""

    def test_principle_without_the_flag_fails(self):
        self.skill("principle-x", flag=False)
        self.assertIn("missing-flag", self.codes(self.load(self.PRINCIPLE)))

    def test_principle_with_the_flag_passes(self):
        self.skill("principle-x", flag=True)
        self.assertNotIn("missing-flag", self.codes(self.load(self.PRINCIPLE)))

    def test_workflow_without_the_flag_is_fine(self):
        self.skill("helper", flag=False)
        codes = self.codes(self.load("""
[skills.helper]
layer = "workflow"
category = "core"
runtimes = ["claude", "codex"]
"""))
        self.assertNotIn("missing-flag", codes)

    def test_local_merge_language_fails(self):
        self.skill("principle-x", flag=True,
                   body="Run `git merge --ff-only` onto main from the worktree.")
        self.assertIn("local-merge", self.codes(self.load(self.PRINCIPLE)))

    def test_describing_the_pr_squash_is_not_a_local_merge(self):
        self.skill("principle-x", flag=True,
                   body="Land through the PR, squashed. Never merge locally.")
        self.assertNotIn("local-merge", self.codes(self.load(self.PRINCIPLE)))

    def test_role_not_in_the_matrix_fails(self):
        self.skill("principle-x", flag=True,
                   body="Delegate to the **nonexistent-role** role.")
        reg = self.load(self.PRINCIPLE)
        findings = doctor.check_roles(reg, self.repo, {"explore", "executor"})
        self.assertEqual([f.code for f in findings], ["unknown-role"])

    def test_known_role_passes(self):
        self.skill("principle-x", flag=True,
                   body="Delegate to the **executor** role.")
        reg = self.load(self.PRINCIPLE)
        self.assertEqual(doctor.check_roles(reg, self.repo, {"explore", "executor"}), [])


if __name__ == "__main__":
    unittest.main()
