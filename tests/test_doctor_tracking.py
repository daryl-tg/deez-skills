import subprocess
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

PRINCIPLE = """
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]
"""

GATE = """interface:
  display_name: "Principle X"
policy:
  allow_implicit_invocation: false
"""


class GateTrackingTest(unittest.TestCase):
    """A generated gate that never got committed breaks the next clone.

    The file is hidden in review by .gitattributes, which is exactly why an
    untracked one is easy to miss locally.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills" / "principle-x" / "agents").mkdir(parents=True)
        (self.repo / "skills" / "principle-x" / "SKILL.md").write_text(
            "---\nname: principle-x\ndescription: One rule.\n"
            "disable-model-invocation: true\n---\n\nBody\n"
        )
        (self.repo / "skills" / "principle-x" / "agents" / "openai.yaml").write_text(GATE)
        (self.repo / "registry.toml").write_text(BASE + PRINCIPLE)

    def git(self, *args):
        subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True, capture_output=True,
        )

    def init(self):
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")

    def codes(self):
        reg = registry.load(self.repo / "registry.toml")
        return [f.code for f in doctor.check_gate_tracking(reg, self.repo)]

    def test_an_untracked_gate_fails(self):
        self.init()
        self.assertIn("untracked-gate", self.codes())

    def test_the_message_names_the_file(self):
        self.init()
        details = [f.detail for f in doctor.check_gate_tracking(
            registry.load(self.repo / "registry.toml"), self.repo)]
        self.assertTrue(any("agents/openai.yaml" in d for d in details))

    def test_a_staged_gate_passes(self):
        self.init()
        self.git("add", "skills/principle-x/agents/openai.yaml")
        self.assertEqual(self.codes(), [])

    def test_a_committed_gate_passes(self):
        self.init()
        self.git("add", "-A")
        self.git("commit", "-qm", "add the gate")
        self.assertEqual(self.codes(), [])

    def test_outside_a_git_repository_the_check_is_silent(self):
        self.assertEqual(self.codes(), [])

    def test_doctor_runs_it(self):
        self.init()
        roots = {
            "claude": {"skill": self.repo.parent / "c" / "skills"},
            "codex": {"skill": self.repo.parent / "x" / "skills"},
        }
        for r in roots.values():
            r["skill"].mkdir(parents=True)
        reg = registry.load(self.repo / "registry.toml")
        codes = [f.code for f in doctor.check(reg, self.repo, roots, "full")]
        self.assertIn("untracked-gate", codes)


class GitattributesTest(unittest.TestCase):
    def test_the_hub_hides_its_gates_in_review(self):
        repo = Path(__file__).resolve().parents[1]
        text = (repo / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn("agents/openai.yaml", text)
        self.assertIn("linguist-generated=true", text)


if __name__ == "__main__":
    unittest.main()
