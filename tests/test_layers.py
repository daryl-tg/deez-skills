import tempfile
import unittest
from pathlib import Path

from deezlib import registry

BASE = """
[meta]
version = 1
default_profile = "full"

[categories]
core = "Always-on essentials"

[profiles]
full = ["*"]
"""


def load(tmp, extra):
    path = Path(tmp) / "registry.toml"
    path.write_text(BASE + extra)
    return registry.load(path)


class LayerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_layer_defaults_to_workflow(self):
        reg = load(self.tmp.name, """
[skills.alpha]
category = "core"
runtimes = ["claude"]
""")
        self.assertEqual(reg.entries[0].layer, "workflow")

    def test_layer_is_read(self):
        reg = load(self.tmp.name, """
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]
""")
        self.assertEqual(reg.entries[0].layer, "principle")

    def test_unknown_layer_rejected(self):
        with self.assertRaises(registry.RegistryError):
            load(self.tmp.name, """
[skills.alpha]
layer = "nonsense"
category = "core"
runtimes = ["claude"]
""")

    def test_mode_may_install_on_both_runtimes(self):
        """Codex gates via agents/openai.yaml, so the router is not Claude-only.
        Superseded the earlier rule on 2026-09-02."""
        reg = load(self.tmp.name, """
[skills.clanker-mode]
layer = "mode"
category = "core"
runtimes = ["claude", "codex"]
""")
        self.assertEqual(reg.entries[0].runtimes, ("claude", "codex"))

    def test_playbook_host_may_install_on_both_runtimes(self):
        reg = load(self.tmp.name, """
[skills.om-chat-feature]
layer = "playbook-host"
category = "core"
runtimes = ["claude", "codex"]
""")
        self.assertEqual(reg.entries[0].runtimes, ("claude", "codex"))

    def test_principle_must_be_on_both_runtimes(self):
        with self.assertRaises(registry.RegistryError) as ctx:
            load(self.tmp.name, """
[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude"]
""")
        self.assertIn("both", str(ctx.exception))

    def test_valid_layers_pass(self):
        reg = load(self.tmp.name, """
[skills.om-mode]
layer = "mode"
category = "core"
runtimes = ["claude"]

[skills.principle-x]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]

[skills.om-chat-feature]
layer = "playbook-host"
category = "core"
runtimes = ["claude"]

[skills.helper]
layer = "workflow"
category = "core"
runtimes = ["claude", "codex"]
""")
        self.assertEqual(len(reg.entries), 4)

    def test_requires_flag_helper(self):
        self.assertTrue(registry.requires_flag("mode"))
        self.assertTrue(registry.requires_flag("principle"))
        self.assertTrue(registry.requires_flag("playbook-host"))
        self.assertFalse(registry.requires_flag("workflow"))


class RoutingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_routing_defaults_when_absent(self):
        reg = load(self.tmp.name, "")
        self.assertEqual(reg.routing["default_lane"], "codex")
        self.assertEqual(reg.routing["review"], "claude")

    def test_routing_is_read(self):
        reg = load(self.tmp.name, """
[routing]
default_lane = "claude"
""")
        self.assertEqual(reg.routing["default_lane"], "claude")

    def test_reserved_lanes_cannot_be_dispatched(self):
        with self.assertRaises(registry.RegistryError) as ctx:
            load(self.tmp.name, """
[routing]
git_mutations = "codex"
""")
        self.assertIn("git_mutations", str(ctx.exception))

    def test_unknown_lane_value_rejected(self):
        with self.assertRaises(registry.RegistryError):
            load(self.tmp.name, """
[routing]
default_lane = "gemini"
""")


if __name__ == "__main__":
    unittest.main()
