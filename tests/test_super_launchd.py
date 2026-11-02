import json
import os
import plistlib
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import launchd

FAKE_LAUNCHCTL = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAKE_LAUNCHCTL_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
sys.exit(3 if sys.argv[1] == "bootout" else 0)
"""


class LaunchdTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.home = self.tmp / "home"
        self.agents = self.tmp / "agents"
        self.hub = Path("/hub")
        self.root = self.tmp / "state"
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "launchctl").write_text(FAKE_LAUNCHCTL, encoding="utf-8")
        (bin_dir / "launchctl").chmod(0o755)
        self.calls = self.tmp / "launchctl.jsonl"
        patcher = mock.patch.dict(os.environ, {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_LAUNCHCTL_LOG": str(self.calls),
            "HOME": str(self.home),
        })
        patcher.start()
        self.addCleanup(patcher.stop)
        self.plist_path = self.agents / "com.dboon.super-clanker.plist"
        self.watchdog_path = self.agents / "com.dboon.super-watchdog.plist"
        self.domain = f"gui/{os.getuid()}"

    def install(self, apply, root=None):
        return launchd.install(self.hub, root or self.root, self.home, self.agents, apply)

    def launchctl_calls(self):
        if not self.calls.exists():
            return []
        return [json.loads(line) for line in self.calls.read_text(encoding="utf-8").splitlines()]

    def test_install_plan_writes_nothing(self):
        planned = self.install(apply=False)
        self.assertFalse(self.agents.exists())
        self.assertEqual(self.launchctl_calls(), [])
        self.assertIn(f"would create {self.plist_path}", planned)
        self.install(apply=True)
        self.assertIn(f"would replace {self.plist_path} (unchanged)", self.install(apply=False))
        moved = self.install(apply=False, root=self.tmp / "proof")
        self.assertIn(f"would replace {self.plist_path} (changed)", moved)

    def test_install_apply_writes_plist_with_keepalive_and_state_env(self):
        self.install(apply=True)
        written = plistlib.loads(self.plist_path.read_bytes())
        self.assertEqual(written, {
            "Label": "com.dboon.super-clanker",
            "ProgramArguments": ["/hub/bin/deez", "super", "daemon"],
            "RunAtLoad": True,
            "KeepAlive": True,
            "WorkingDirectory": str(self.root),
            "StandardOutPath": str(self.root / "log" / "launchd.out.log"),
            "StandardErrorPath": str(self.root / "log" / "launchd.err.log"),
            "EnvironmentVariables": {
                "PATH": f"{self.home}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin",
                "HOME": str(self.home),
                "DEEZ_SUPER_STATE": str(self.root),
            },
        })
        self.assertTrue((self.root / "log").is_dir())

    def test_install_apply_runs_bootout_bootstrap_kickstart_in_order(self):
        lines = self.install(apply=True)
        self.assertEqual(self.launchctl_calls(), [
            ["bootout", f"{self.domain}/com.dboon.super-clanker"],
            ["bootstrap", self.domain, str(self.plist_path)],
            ["kickstart", "-k", f"{self.domain}/com.dboon.super-clanker"],
            ["bootout", f"{self.domain}/com.dboon.super-watchdog"],
            ["bootstrap", self.domain, str(self.watchdog_path)],
        ])
        self.assertEqual(lines, [
            f"wrote {self.plist_path}",
            f"launchctl bootout {self.domain}/com.dboon.super-clanker exit 3",
            f"launchctl bootstrap {self.domain} {self.plist_path} exit 0",
            f"launchctl kickstart -k {self.domain}/com.dboon.super-clanker exit 0",
            f"wrote {self.watchdog_path}",
            f"launchctl bootout {self.domain}/com.dboon.super-watchdog exit 3",
            f"launchctl bootstrap {self.domain} {self.watchdog_path} exit 0",
        ])

    def test_uninstall_removes_plist(self):
        self.install(apply=True)
        planned = launchd.uninstall(self.home, self.agents, apply=False)
        self.assertTrue(self.plist_path.exists())
        removed = launchd.uninstall(self.home, self.agents, apply=True)
        self.assertFalse(self.plist_path.exists())
        self.assertFalse(self.watchdog_path.exists())
        self.assertEqual(self.launchctl_calls()[-2:], [
            ["bootout", f"{self.domain}/com.dboon.super-clanker"],
            ["bootout", f"{self.domain}/com.dboon.super-watchdog"],
        ])
        self.assertEqual(planned, [
            f"would boot out com.dboon.super-clanker and remove {self.plist_path}",
            f"would boot out com.dboon.super-watchdog and remove {self.watchdog_path}",
        ])
        self.assertEqual(removed, [
            f"launchctl bootout {self.domain}/com.dboon.super-clanker exit 3",
            f"removed {self.plist_path}",
            f"launchctl bootout {self.domain}/com.dboon.super-watchdog exit 3",
            f"removed {self.watchdog_path}",
        ])

    def test_install_verb_plans_against_the_given_state_root(self):
        proof = self.tmp / "proof"
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super", "install", "--state", str(proof)])
        target = self.home / "Library" / "LaunchAgents" / "com.dboon.super-clanker.plist"
        self.assertEqual((code, err.getvalue()), (0, ""))
        self.assertIn(f"would create {target}", out.getvalue())
        self.assertIn(f"state {proof}", out.getvalue())
        self.assertFalse(target.exists())
        self.assertFalse(proof.exists())
        self.assertEqual(self.launchctl_calls(), [])


if __name__ == "__main__":
    unittest.main()
