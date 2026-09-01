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


class BudgetTest(unittest.TestCase):
    """No per-skill limit. The aggregate is what a runtime truncates on."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills").mkdir(parents=True)

    def skill(self, name, desc, routed=False):
        f = self.repo / "skills" / name
        f.mkdir(parents=True, exist_ok=True)
        flag = "disable-model-invocation: true\n" if routed else ""
        (f / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {desc}\n{flag}---\n"
        )

    def load(self, names):
        p = self.repo / "registry.toml"
        p.write_text(BASE + "".join(
            f'\n[skills.{n}]\ncategory = "core"\nruntimes = ["claude", "codex"]\n'
            for n in names))
        return registry.load(p)

    def test_a_long_description_no_longer_fails(self):
        self.skill("alpha", "x" * 600)
        findings = doctor.check(self.load(["alpha"]), self.repo, {}, "full")
        self.assertEqual([f for f in findings if f.level == "fail"], [])

    def test_the_aggregate_is_reported_per_runtime(self):
        self.skill("alpha", "x" * 100)
        self.skill("beta", "y" * 100)
        findings = doctor.budget(self.load(["alpha", "beta"]), self.repo)
        codes = [f.code for f in findings]
        self.assertIn("budget", codes)
        detail = " ".join(f.detail for f in findings)
        self.assertIn("claude", detail)
        self.assertIn("codex", detail)

    def test_the_report_separates_visible_from_routed(self):
        self.skill("alpha", "x" * 100, routed=True)
        findings = doctor.budget(self.load(["alpha"]), self.repo)
        claude = next(f.detail for f in findings if f.detail.startswith("claude"))
        codex = next(f.detail for f in findings if f.detail.startswith("codex"))
        self.assertIn("routed", claude)
        # Codex ignores the flag, so the same skill is visible there.
        self.assertIn("1 visible", codex)
        self.assertNotIn("routed", codex)

    def test_it_is_informational_not_a_failure(self):
        self.skill("alpha", "x" * 5000)
        findings = doctor.budget(self.load(["alpha"]), self.repo)
        levels = {f.level for f in findings if f.code == "budget"}
        self.assertEqual(levels, {"info"})


if __name__ == "__main__":
    unittest.main()
