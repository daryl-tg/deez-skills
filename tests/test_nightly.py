import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills/maintain-verification-skill/scripts"
NIGHTLY = SCRIPTS / "nightly.zsh"


class NightlyTest(unittest.TestCase):
    def run_nightly(self, claude_body, *skills, **env_extra):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        home = root / "home"
        (home / "github/openmarket-internal").mkdir(parents=True)
        claude = root / "claude"
        claude.write_text("#!/bin/sh\n" + claude_body)
        claude.chmod(0o755)
        state = {name: root / name for name in ("logs", "reports", "state", "art", "hub")}
        env = {
            "PATH": os.environ["PATH"],
            "HOME": str(home),
            "VM_CLAUDE_BIN": str(claude),
            "VM_LOGS": str(state["logs"]),
            "VM_REPORTS": str(state["reports"]),
            "VM_STATE": str(state["state"]),
            "VM_ART": str(state["art"]),
            "VM_HUB": str(state["hub"]),
            "VM_PRODUCT_REPOS": str(home / "github/openmarket-internal"),
            "VM_POLL_S": "1",
            "PROMPT_CAPTURE": str(root / "prompt.txt"),
            **env_extra,
        }
        result = subprocess.run(["/bin/zsh", str(NIGHTLY), *skills],
                                capture_output=True, text=True, env=env, timeout=60)
        return result, state, root

    def test_a_pass_logs_start_exit_and_done_and_leaves_a_report(self):
        result, state, _ = self.run_nightly('exit 0\n', "verify-om")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"verify-om: start \(session [0-9a-f-]{36}, cwd ")
        self.assertIn("verify-om: exit 0", result.stdout)
        self.assertRegex(result.stdout, r"nightly done \d{4}-\d\d-\d\d: verify-om\n")
        reports = list(state["reports"].glob("*-verify-om.md"))
        self.assertEqual(len(reports), 1)
        self.assertIn("No report written. Exit 0", reports[0].read_text())

    def test_the_prompt_runs_the_skill_unattended_and_asks_for_a_changelog(self):
        result, _, root = self.run_nightly('printf "%s" "$2" > "$PROMPT_CAPTURE"\n', "verify-om")
        self.assertEqual(result.returncode, 0, result.stderr)
        prompt = (root / "prompt.txt").read_text()
        self.assertTrue(prompt.startswith("/maintain-verification-skill verify-om\n"))
        self.assertIn("Never ask a question", prompt)
        self.assertIn("'## Changelog'", prompt)
        self.assertIn("File | Change | Proof", prompt)

    def test_a_failed_pass_records_its_exit_code(self):
        result, _, _ = self.run_nightly('exit 3\n', "verify-om")
        self.assertIn("verify-om: exit 3", result.stdout)

    def test_a_silent_pass_is_killed_at_the_idle_timeout(self):
        result, _, _ = self.run_nightly('sleep 30\n', "verify-om", VM_IDLE_TIMEOUT_S="2")
        self.assertRegex(result.stdout, r"verify-om: killing, log silent for \d+ min")

    def test_an_unmapped_skill_is_skipped(self):
        result, _, _ = self.run_nightly('exit 0\n', "verify-nothing")
        self.assertIn("verify-nothing: no repo mapped or missing", result.stdout)
        self.assertNotIn("verify-nothing: start", result.stdout)

    def test_the_launchd_template_runs_the_hub_script_at_3_17(self):
        plist = (SCRIPTS / "com.dboon.verify-maintenance.plist.template").read_text()
        self.assertIn("<string>HOME_DIR/github/deez-skills/skills/maintain-verification-skill/scripts/nightly.zsh</string>", plist)
        self.assertIn("<key>Hour</key>\n    <integer>3</integer>", plist)
        self.assertIn("<key>Minute</key>\n    <integer>17</integer>", plist)
        self.assertIn("HOME_DIR/Library/Logs/verify-maintenance/launchd.log", plist)


if __name__ == "__main__":
    unittest.main()
