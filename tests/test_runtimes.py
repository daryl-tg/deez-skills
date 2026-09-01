import tempfile
import unittest
from pathlib import Path

from deezlib import runtimes


class RootsTest(unittest.TestCase):
    def test_defaults_to_dot_claude_and_dot_codex_under_home(self):
        roots = runtimes.roots({}, Path("/home/x"))
        self.assertEqual(roots["claude"]["skill"], Path("/home/x/.claude/skills"))
        self.assertEqual(roots["claude"]["command"], Path("/home/x/.claude/commands"))
        self.assertEqual(roots["claude"]["agent"], Path("/home/x/.claude/agents"))
        self.assertEqual(roots["codex"]["skill"], Path("/home/x/.codex/skills"))

    def test_codex_has_no_command_or_agent_root(self):
        roots = runtimes.roots({}, Path("/home/x"))
        self.assertNotIn("command", roots["codex"])
        self.assertNotIn("agent", roots["codex"])

    def test_env_overrides_win(self):
        with tempfile.TemporaryDirectory() as tmp:
            roots = runtimes.roots(
                {"DEEZ_CLAUDE_HOME": f"{tmp}/c", "DEEZ_CODEX_HOME": f"{tmp}/x"},
                Path("/home/x"),
            )
            self.assertEqual(roots["claude"]["skill"], Path(tmp) / "c" / "skills")
            self.assertEqual(roots["codex"]["skill"], Path(tmp) / "x" / "skills")


if __name__ == "__main__":
    unittest.main()
