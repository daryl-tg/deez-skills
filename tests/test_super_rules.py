import re
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import rules
from deezlib.superclanker.domain import Trigger, trigger_id
from deezlib.superclanker.sources import terminal
from deezlib.superclanker.store import Store, SuperError

SOURCES = """
[sources.github]
enabled = true
mode = "candidates"
senders = ["daryl-tg"]
"""


class RulesTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "state"
        patcher = mock.patch.dict(
            os.environ, {"USER": "daryl", "DEEZ_SUPER_STATE": str(self.root)}
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        (self.root / "sources.toml").write_text(SOURCES, encoding="utf-8")
        self.rules_dir = self.root / "policy" / "rules"
        self.rules_dir.mkdir(parents=True)

    def rule(self, name, text):
        path = self.rules_dir / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        return path

    def deez(self, *argv):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", *argv])
        return code, out.getvalue(), err.getvalue()

    def overheard(self, event_id, text):
        trigger = Trigger(
            trigger_id("github", event_id), "github", event_id,
            f"github:daryl-tg/deez-skills#{event_id}", "someone", False, text, None,
            "2026-11-02T10:00:00+00:00", {},
        )
        self.store.receive(trigger)
        return trigger

    def test_load_reads_title_mode_and_text(self):
        self.rule("red-builds", "# Red builds on my repos\n\nmode: auto\n\nAccept a red CI build.\nOnly on main.\n")

        self.assertEqual(rules.load(self.root), {
            "red-builds": rules.Rule(
                "red-builds", "Red builds on my repos", "auto",
                "Accept a red CI build.\nOnly on main.",
            ),
        })

    def test_missing_mode_defaults_to_observe(self):
        self.rule("typos", "# Typos in docs\nFix obvious typos.\n")

        loaded = rules.load(self.root)["typos"]

        self.assertEqual((loaded.mode, loaded.text), ("observe", "Fix obvious typos."))
        self.assertEqual(rules.load(Path(self.root) / "elsewhere"), {})

    def test_set_mode_rewrites_only_that_line(self):
        moded = self.rule("red-builds", "# Red builds\n\nAccept red CI.\nmode: observe\nOnly main.\n")
        bare = self.rule("typos", "# Typos\nFix typos.\n")

        rules.set_mode(self.root, "red-builds", "auto")
        rules.set_mode(self.root, "typos", "off")
        rules.set_mode(self.root, "typos", "off")

        self.assertEqual(
            moded.read_text(encoding="utf-8"), "# Red builds\n\nAccept red CI.\nmode: auto\nOnly main.\n"
        )
        self.assertEqual(bare.read_text(encoding="utf-8"), "# Typos\nmode: off\nFix typos.\n")
        with self.assertRaisesRegex(SuperError, "no rule missing"):
            rules.set_mode(self.root, "missing", "auto")
        with self.assertRaisesRegex(SuperError, "mode loud"):
            rules.set_mode(self.root, "typos", "loud")
        self.assertEqual(bare.read_text(encoding="utf-8"), "# Typos\nmode: off\nFix typos.\n")

    def test_rules_and_policy_verbs_print_and_set_modes(self):
        self.rule("red-builds", "# Red builds\nmode: auto\nAccept red CI.\n")
        self.rule("typos", "# Typos in docs\nFix typos.\n")

        listed = self.deez("rules")
        one = self.deez("rules", "typos")
        changed = self.deez("policy", "set", "typos", "--mode", "off")
        unknown = self.deez("rules", "missing")

        self.assertEqual(listed, (0, "red-builds  auto  Red builds\ntypos  observe  Typos in docs\n", ""))
        self.assertEqual(one, (0, "# Typos in docs\nmode: observe\n\nFix typos.\n", ""))
        self.assertEqual(changed, (0, "rule typos mode off\n", ""))
        self.assertEqual(rules.load(self.root)["typos"].mode, "off")
        self.assertEqual(unknown, (2, "", "deez: no rule missing\n"))

    def test_dispatch_refuses_off_rule_and_accepts_on_auto_rule(self):
        self.rule("red-builds", "# Red builds\nmode: off\nAccept red CI.\n")
        red = self.overheard("evt-1", "the build is red")
        dispatch = ("--slug", "fix-red-build", "--playbook", "bug-fix", "--rule", "red-builds")

        refused = self.deez("dispatch", red.id, *dispatch)
        unknown = self.deez("dispatch", red.id, "--slug", "x", "--playbook", "bug-fix", "--rule", "nope")

        self.assertEqual(refused, (2, "", "deez: rule red-builds is off\n"))
        self.assertEqual(unknown, (2, "", "deez: no rule nope\n"))
        self.assertEqual([t.id for t in self.store.queued()], [red.id])
        self.assertEqual(self.store.status(), [])

        self.deez("policy", "set", "red-builds", "--mode", "auto")
        code, out, err = self.deez("dispatch", red.id, *dispatch)

        self.assertEqual((code, err), (0, ""))
        self.assertIn(f"accept {red.id} → ticket", out)
        self.assertEqual([row["slug"] for row in self.store.status()], ["fix-red-build"])

        self.deez("policy", "set", "red-builds", "--mode", "observe")
        watched = self.overheard("evt-2", "the build is red again")
        observed = self.deez("dispatch", watched.id, "--slug", "fix-red-again", *dispatch[2:])
        self.assertEqual(
            observed[1],
            f"would accept {watched.id} as fix-red-again (observe mode, nothing started)\n",
        )

        self.deez("policy", "set", "red-builds", "--mode", "off")
        asked, _receipt = terminal.ask(self.store, "fix the red build")
        explicit = self.deez("dispatch", asked.id, "--slug", "fix-red-asked", *dispatch[2:])
        self.assertEqual(explicit[0], 0, explicit[2])
        self.assertIn(f"accept {asked.id} → ticket", explicit[1])
        ticket = re.search(r"ticket (k_[0-9a-f]{10})", explicit[1]).group(1)
        mandate = self.store.show(self.store.show(ticket)["mandate_id"])
        self.assertEqual(tuple(mandate["rules"]), ())


if __name__ == "__main__":
    unittest.main()
