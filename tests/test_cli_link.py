import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEEZ = REPO / "bin" / "deez"


class CliLinkTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = {
            **os.environ,
            "DEEZ_CLAUDE_HOME": f"{self.tmp.name}/claude",
            "DEEZ_CODEX_HOME": f"{self.tmp.name}/codex",
        }

    def run_deez(self, *args):
        return subprocess.run(
            [str(DEEZ), *args], capture_output=True, text=True, env=self.env
        )

    def test_link_without_apply_reports_a_plan_and_changes_nothing(self):
        result = self.run_deez("link")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--apply", result.stdout)
        self.assertFalse(Path(self.tmp.name, "claude").exists())

    def test_link_plans_but_never_creates_a_runtime_root(self):
        """Whatever the registry holds, a bare `link` must not touch disk."""
        result = self.run_deez("link")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("plan only", result.stdout)
        self.assertFalse(Path(self.tmp.name, "claude").exists())
        self.assertFalse(Path(self.tmp.name, "codex").exists())

    def test_unknown_profile_exits_nonzero(self):
        result = self.run_deez("link", "--profile", "ghost")
        self.assertNotEqual(result.returncode, 0)

    def test_unknown_runtime_is_rejected_by_argparse(self):
        result = self.run_deez("link", "--runtime", "cursor")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
