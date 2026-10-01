import tempfile
import unittest
from pathlib import Path

from deezlib import registry


def write(tmp, text):
    path = Path(tmp) / "registry.toml"
    path.write_text(text)
    return path


BASE = """
[meta]
version = 1
default_profile = "full"

[categories]
core = "Always-on essentials"
om-chat = "OM Chat feature delivery"

[profiles]
full = ["*"]
lean = ["core"]
"""


class LoadTest(unittest.TestCase):
    def test_loads_empty_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = registry.load(write(tmp, BASE))
            self.assertEqual(reg.version, 1)
            self.assertEqual(reg.default_profile, "full")
            self.assertEqual(reg.entries, ())
            self.assertIn("core", reg.categories)

    def test_reads_a_skill_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = registry.load(write(tmp, BASE + """
[skills.om-chat-feature]
category = "om-chat"
runtimes = ["claude", "codex"]
"""))
            entry = reg.entries[0]
            self.assertEqual(entry.kind, "skill")
            self.assertEqual(entry.name, "om-chat-feature")
            self.assertEqual(entry.runtimes, ("claude", "codex"))

    def test_rejects_unknown_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError) as ctx:
                registry.load(write(tmp, BASE + """
[skills.stray]
category = "nope"
runtimes = ["claude"]
"""))
            self.assertIn("nope", str(ctx.exception))

    def test_rejects_unknown_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError):
                registry.load(write(tmp, BASE + """
[skills.stray]
category = "core"
runtimes = ["cursor"]
"""))

    def test_rejects_command_on_codex(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError) as ctx:
                registry.load(write(tmp, BASE + """
[commands.mr-markdown]
category = "core"
runtimes = ["codex"]
"""))
            self.assertIn("codex", str(ctx.exception))

    def test_rejects_duplicate_install_name_within_a_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError) as ctx:
                registry.load(write(tmp, BASE + """
[skills.loop]
category = "core"
runtimes = ["codex"]

[skills.loop-stub]
category = "core"
runtimes = ["codex"]
install_as = { codex = "loop" }
"""))
            self.assertIn("loop", str(ctx.exception))

    def test_rejects_profile_naming_unknown_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError):
                registry.load(write(tmp, """
[meta]
version = 1
default_profile = "broken"

[categories]
core = "Always-on essentials"

[profiles]
broken = ["ghost"]
"""))

    def test_rejects_unsupported_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError):
                registry.load(write(tmp, BASE.replace("version = 1", "version = 99")))

    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(registry.RegistryError):
                registry.load(Path(tmp) / "absent.toml")


class ResolveTest(unittest.TestCase):
    def load(self, extra):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        return registry.load(write(self.tmp.name, BASE + extra))

    def test_install_name_uses_alias_for_that_runtime_only(self):
        reg = self.load("""
[skills.loop-stub]
category = "core"
runtimes = ["claude", "codex"]
install_as = { codex = "loop" }
""")
        entry = reg.entries[0]
        self.assertEqual(registry.install_name(entry, "codex"), "loop")
        self.assertEqual(registry.install_name(entry, "claude"), "loop-stub")

    def test_source_dir_uses_variant_for_that_runtime_only(self):
        reg = self.load("""
[skills.graphify]
category = "core"
runtimes = ["claude", "codex"]
variant = { codex = "skills/graphify-codex" }
""")
        entry = reg.entries[0]
        self.assertEqual(registry.source_dir(entry, "codex"), "skills/graphify-codex")
        self.assertEqual(registry.source_dir(entry, "claude"), "skills/graphify")

    def test_entries_for_filters_by_profile_and_runtime(self):
        reg = self.load("""
[skills.alpha]
category = "core"
runtimes = ["claude", "codex"]

[skills.beta]
category = "om-chat"
runtimes = ["claude"]
""")
        lean_claude = [e.name for e in registry.entries_for(reg, "lean", "claude")]
        full_codex = [e.name for e in registry.entries_for(reg, "full", "codex")]
        full_claude = [e.name for e in registry.entries_for(reg, "full", "claude")]
        self.assertEqual(lean_claude, ["alpha"])
        self.assertEqual(full_codex, ["alpha"])
        self.assertEqual(sorted(full_claude), ["alpha", "beta"])

    def test_unknown_profile_raises(self):
        reg = self.load("")
        with self.assertRaises(registry.RegistryError):
            registry.entries_for(reg, "ghost", "claude")


if __name__ == "__main__":
    unittest.main()


class KindPathTest(unittest.TestCase):
    """Skills are directories; commands and agents are single .md files."""

    def load(self, extra):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        return registry.load(write(self.tmp.name, BASE + extra))

    def test_skill_resolves_to_a_directory(self):
        reg = self.load("""
[skills.alpha]
category = "core"
runtimes = ["claude"]
""")
        self.assertEqual(registry.source_dir(reg.entries[0], "claude"), "skills/alpha")

    def test_command_resolves_to_a_markdown_file(self):
        reg = self.load("""
[commands.mr-markdown]
category = "core"
runtimes = ["claude"]
""")
        self.assertEqual(
            registry.source_dir(reg.entries[0], "claude"), "commands/mr-markdown.md"
        )

    def test_agent_resolves_to_a_markdown_file(self):
        reg = self.load("""
[agents.om-agent]
category = "core"
runtimes = ["claude"]
""")
        self.assertEqual(
            registry.source_dir(reg.entries[0], "claude"), "agents/om-agent.md"
        )

    def test_install_name_keeps_the_extension_for_files(self):
        reg = self.load("""
[agents.om-agent]
category = "core"
runtimes = ["claude"]
""")
        self.assertEqual(
            registry.install_filename(reg.entries[0], "claude"), "om-agent.md"
        )
