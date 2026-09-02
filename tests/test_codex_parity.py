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


class LayerRuntimeTest(unittest.TestCase):
    """Codex gates invocation via agents/openai.yaml, so mode and playbook-host
    are no longer Claude-only. Verified 2026-09-02 with two probe skills."""

    def load(self, extra):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = Path(self.tmp.name) / "registry.toml"
        p.write_text(BASE + extra)
        return registry.load(p)

    def test_mode_may_install_on_both(self):
        reg = self.load("""
[skills.clanker-mode]
layer = "mode"
category = "core"
runtimes = ["claude", "codex"]
""")
        self.assertEqual(reg.entries[0].runtimes, ("claude", "codex"))

    def test_playbook_host_may_install_on_both(self):
        reg = self.load("""
[skills.om-thing]
layer = "playbook-host"
category = "core"
runtimes = ["claude", "codex"]
""")
        self.assertEqual(reg.entries[0].runtimes, ("claude", "codex"))

    def test_principle_still_requires_both(self):
        with self.assertRaises(registry.RegistryError):
            self.load("""
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude"]
""")


class BothGatesTest(unittest.TestCase):
    """A gated layer needs the Claude gate AND the Codex gate. Half-gated looks
    correct on one runtime and leaks on the other."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills").mkdir(parents=True)

    def build(self, frontmatter_gate, codex_gate, runtimes='["claude", "codex"]'):
        d = self.repo / "skills" / "principle-x"
        (d / "agents").mkdir(parents=True, exist_ok=True)
        flag = "disable-model-invocation: true\n" if frontmatter_gate else ""
        (d / "SKILL.md").write_text(
            f"---\nname: principle-x\ndescription: d\n{flag}---\n\nBody\n")
        if codex_gate is not None:
            policy = "policy:\n  allow_implicit_invocation: false\n" if codex_gate else ""
            (d / "agents" / "openai.yaml").write_text(
                'interface:\n  display_name: "X"\n' + policy)
        (self.repo / "registry.toml").write_text(BASE + f"""
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = {runtimes}
""")
        return registry.load(self.repo / "registry.toml")

    def codes(self, reg):
        return [f.code for f in doctor.check_gates(reg, self.repo)]

    def test_both_gates_pass(self):
        self.assertEqual(self.codes(self.build(True, True)), [])

    def test_missing_codex_gate_fails(self):
        self.assertIn("missing-codex-gate", self.codes(self.build(True, False)))

    def test_no_openai_yaml_at_all_fails(self):
        self.assertIn("missing-codex-gate", self.codes(self.build(True, None)))

    def test_missing_claude_gate_fails(self):
        self.assertIn("missing-flag", self.codes(self.build(False, True)))

    def test_claude_only_skill_needs_no_codex_gate(self):
        """A principle must be on both runtimes, so use a mode for this case."""
        d = self.repo / "skills" / "solo-mode"
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(
            "---\nname: solo-mode\ndescription: d\n"
            "disable-model-invocation: true\n---\n\nBody\n")
        (self.repo / "registry.toml").write_text(BASE + """
[skills.solo-mode]
layer = "mode"
category = "core"
runtimes = ["claude"]
""")
        reg = registry.load(self.repo / "registry.toml")
        self.assertEqual(doctor.check_gates(reg, self.repo), [])


class GateIntentTest(unittest.TestCase):
    """Gating is an author's decision, not a layer's. A skill gated on Claude
    that installs to Codex must be gated there too, whatever its layer."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills" / "helper" / "agents").mkdir(parents=True)

    def build(self, claude_gate, codex_gate):
        d = self.repo / "skills" / "helper"
        flag = "disable-model-invocation: true\n" if claude_gate else ""
        (d / "SKILL.md").write_text(f"---\nname: helper\ndescription: d\n{flag}---\n\nB\n")
        y = d / "agents" / "openai.yaml"
        if codex_gate:
            y.write_text('interface:\n  display_name: "H"\npolicy:\n  allow_implicit_invocation: false\n')
        elif y.exists():
            y.unlink()
        (self.repo / "registry.toml").write_text(BASE + """
[skills.helper]
layer = "workflow"
category = "core"
runtimes = ["claude", "codex"]
""")
        return registry.load(self.repo / "registry.toml")

    def test_workflow_gated_on_claude_only_fails(self):
        codes = [f.code for f in doctor.check_gates(self.build(True, False), self.repo)]
        self.assertIn("missing-codex-gate", codes)

    def test_workflow_gated_on_both_passes(self):
        self.assertEqual(doctor.check_gates(self.build(True, True), self.repo), [])

    def test_ungated_workflow_needs_neither(self):
        self.assertEqual(doctor.check_gates(self.build(False, False), self.repo), [])


class RuntimeNeutralityTest(unittest.TestCase):
    """A playbook naming one runtime's dispatch mechanism breaks on the other."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "skills" / "the-mode" / "playbooks").mkdir(parents=True)
        (self.repo / "skills" / "the-mode" / "agents").mkdir(parents=True)

    def build(self, playbook_body):
        d = self.repo / "skills" / "the-mode"
        (d / "SKILL.md").write_text(
            "---\nname: the-mode\ndescription: d\n"
            "disable-model-invocation: true\n---\n\nBody\n")
        (d / "agents" / "openai.yaml").write_text(
            'interface:\n  display_name: "M"\npolicy:\n  allow_implicit_invocation: false\n')
        (d / "playbooks" / "thing.md").write_text(playbook_body)
        (self.repo / "registry.toml").write_text(BASE + """
[skills.the-mode]
layer = "mode"
category = "core"
runtimes = ["claude", "codex"]
""")
        return registry.load(self.repo / "registry.toml")

    def test_naming_a_claude_mechanism_fails(self):
        reg = self.build('Delegate via `Agent(subagent_type: "codex:codex-rescue")`.')
        codes = [f.code for f in doctor.check_runtime_neutrality(reg, self.repo)]
        self.assertIn("runtime-specific-dispatch", codes)

    def test_naming_a_codex_mechanism_fails(self):
        reg = self.build("Delegate with `agent_type: executor` directly.")
        codes = [f.code for f in doctor.check_runtime_neutrality(reg, self.repo)]
        self.assertIn("runtime-specific-dispatch", codes)

    def test_naming_a_role_passes(self):
        reg = self.build("Delegate to the **executor** role with a specific scope.")
        self.assertEqual(doctor.check_runtime_neutrality(reg, self.repo), [])
