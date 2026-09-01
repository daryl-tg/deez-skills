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


class UnlinkedStateTest(unittest.TestCase):
    """Pre-migration the hub is deliberately unlinked. That is not drift."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        (self.repo / "skills").mkdir(parents=True)
        self.claude = self.root / "c" / "skills"
        self.claude.mkdir(parents=True)
        self.roots = {"claude": {"skill": self.claude}}

    def skill(self, name):
        f = self.repo / "skills" / name
        f.mkdir(parents=True, exist_ok=True)
        (f / "SKILL.md").write_text(f"---\nname: {name}\ndescription: d\n---\n")
        return f

    def load(self, extra):
        path = self.repo / "registry.toml"
        path.write_text(BASE + extra)
        return registry.load(path)

    TWO = """
[skills.alpha]
category = "core"
runtimes = ["claude"]

[skills.beta]
category = "core"
runtimes = ["claude"]
"""

    def test_nothing_linked_is_reported_not_failed(self):
        self.skill("alpha"); self.skill("beta")
        findings = doctor.check(self.load(self.TWO), self.repo, self.roots, "full")
        self.assertEqual([f for f in findings if f.level == "fail"], [])
        self.assertIn("unlinked", [f.code for f in findings])

    def test_partially_linked_is_drift_and_fails(self):
        a = self.skill("alpha"); self.skill("beta")
        (self.claude / "alpha").symlink_to(a)
        findings = doctor.check(self.load(self.TWO), self.repo, self.roots, "full")
        self.assertIn("not-linked", [f.code for f in findings if f.level == "fail"])

    def test_fully_linked_is_clean(self):
        a = self.skill("alpha"); b = self.skill("beta")
        (self.claude / "alpha").symlink_to(a)
        (self.claude / "beta").symlink_to(b)
        findings = doctor.check(self.load(self.TWO), self.repo, self.roots, "full")
        self.assertEqual([f for f in findings if f.level == "fail"], [])


class CitationTest(unittest.TestCase):
    """A skill citing **principle-x** where no such entry exists is a dead route."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills").mkdir(parents=True)

    def skill(self, name, body):
        f = self.repo / "skills" / name
        f.mkdir(parents=True, exist_ok=True)
        (f / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: d\ndisable-model-invocation: true\n---\n\n{body}\n"
        )

    def load(self, extra):
        path = self.repo / "registry.toml"
        path.write_text(BASE + extra)
        return registry.load(path)

    PRINCIPLE = """
[skills.principle-real]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]
"""

    def test_citing_a_missing_principle_fails(self):
        self.skill("principle-real", "See **principle-ghost** for the rest.")
        findings = doctor.check_citations(self.load(self.PRINCIPLE), self.repo)
        self.assertEqual([f.code for f in findings], ["dangling-citation"])
        self.assertIn("principle-ghost", findings[0].detail)

    def test_citing_a_registered_principle_passes(self):
        self.skill("principle-real", "It cites **principle-real** recursively.")
        self.assertEqual(doctor.check_citations(self.load(self.PRINCIPLE), self.repo), [])


class LocalMergeProhibitionTest(unittest.TestCase):
    """The check must tell 'do this' from 'never do this'."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills").mkdir(parents=True)

    def codes_for(self, body):
        f = self.repo / "skills" / "principle-x"
        f.mkdir(parents=True, exist_ok=True)
        (f / "SKILL.md").write_text(
            f"---\nname: principle-x\ndescription: d\n"
            f"disable-model-invocation: true\n---\n\n{body}\n"
        )
        path = self.repo / "registry.toml"
        path.write_text(BASE + """
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]
""")
        reg = registry.load(path)
        return [f.code for f in doctor.check(reg, self.repo, {}, "full")]

    def test_instructing_a_local_merge_fails(self):
        self.assertIn("local-merge", self.codes_for("Run `git merge --ff-only` onto main."))

    def test_inline_negation_passes(self):
        self.assertNotIn("local-merge", self.codes_for("Never run `git merge` onto main."))

    def test_prohibition_bullet_list_passes(self):
        self.assertNotIn("local-merge", self.codes_for(
            "**Never:**\n\n- `git merge` onto main from a worktree.\n- `git push` to main.\n"))

    def test_prohibition_block_ends_at_prose(self):
        self.assertIn("local-merge", self.codes_for(
            "**Never:**\n\n- `git push` to main.\n\nNow run `git merge` onto main.\n"))

    def test_git_pull_rebase_is_fine(self):
        self.assertNotIn("local-merge", self.codes_for("Run `git pull --rebase` first."))


class MixedPreMigrationTest(unittest.TestCase):
    """Old symlinks pointing elsewhere are still the unlinked state, not drift."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        (self.repo / "skills").mkdir(parents=True)
        self.old = self.root / "old-source"
        self.old.mkdir()
        self.claude = self.root / "c" / "skills"
        self.claude.mkdir(parents=True)
        self.roots = {"claude": {"skill": self.claude}}

    def skill(self, name):
        f = self.repo / "skills" / name
        f.mkdir(parents=True, exist_ok=True)
        (f / "SKILL.md").write_text(f"---\nname: {name}\ndescription: d\n---\n")
        return f

    def load(self):
        p = self.repo / "registry.toml"
        p.write_text(BASE + """
[skills.alpha]
category = "core"
runtimes = ["claude"]

[skills.beta]
category = "core"
runtimes = ["claude"]
""")
        return registry.load(p)

    def test_old_symlinks_elsewhere_are_still_unlinked_not_drift(self):
        self.skill("alpha"); self.skill("beta")
        stale = self.old / "alpha"; stale.mkdir()
        (self.claude / "alpha").symlink_to(stale)   # points at the old source
        findings = doctor.check(self.load(), self.repo, self.roots, "full")
        self.assertIn("unlinked", [f.code for f in findings])
        self.assertEqual([f for f in findings if f.level == "fail"], [])

    def test_one_pointing_into_the_hub_makes_the_rest_drift(self):
        a = self.skill("alpha"); self.skill("beta")
        (self.claude / "alpha").symlink_to(a)       # points into the hub
        findings = doctor.check(self.load(), self.repo, self.roots, "full")
        self.assertIn("not-linked", [f.code for f in findings if f.level == "fail"])
