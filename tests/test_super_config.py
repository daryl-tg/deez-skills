import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from deezlib.superclanker import config
from deezlib.superclanker.store import SuperError

EXAMPLE = """\
[accept]
mode = "observe"
policy_version = "2026-11-02.1"

[router]
model = "sonnet"
wake_cap_chars = 12000
inline_chars = 200
im_reply_words = 100

[sources.terminal]
enabled = true
mode = "explicit-only"
senders = ["dboon"]

[sources.github]
enabled = true
mode = "explicit-only"
senders = ["daryl-tg"]
bots = ["dependabot[bot]"]
scopes = ["daryl-tg/deez-skills"]
"""


class SuperConfigTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, text):
        (self.root / "sources.toml").write_text(text, encoding="utf-8")

    def test_missing_file_gives_defaults_and_writes_nothing(self):
        root = self.root / "super"

        with mock.patch.dict(os.environ, {"USER": "dboon"}):
            loaded = config.load(root)

        self.assertFalse(root.exists())
        self.assertEqual((loaded.accept.mode, loaded.accept.policy_version), ("observe", "unset"))
        self.assertEqual(
            (loaded.router.model, loaded.router.wake_cap_chars, loaded.router.inline_chars,
             loaded.router.im_reply_words),
            ("sonnet", 12000, 200, 100),
        )
        terminal = loaded.policy("terminal")
        self.assertEqual(
            (terminal.enabled, terminal.mode, tuple(terminal.senders)),
            (True, "explicit-only", ("dboon",)),
        )
        self.assertFalse(loaded.policy("github").enabled)
        self.assertEqual(loaded.rules, [])

    def test_example_file_reads_every_section(self):
        self.write(EXAMPLE)

        loaded = config.load(self.root)

        self.assertEqual(loaded.accept.policy_version, "2026-11-02.1")
        github = loaded.policy("github")
        self.assertEqual(
            (github.name, github.enabled, github.mode, tuple(github.senders), tuple(github.bots),
             tuple(github.scopes)),
            ("github", True, "explicit-only", ("daryl-tg",), ("dependabot[bot]",),
             ("daryl-tg/deez-skills",)),
        )
        self.assertEqual(tuple(loaded.policy("terminal").senders), ("dboon",))
        self.assertFalse(loaded.policy("gitlab").enabled)

    def test_unknown_mode_names_the_key(self):
        cases = {
            '[sources.github]\nmode = "loud"\n': "sources.github.mode",
            '[accept]\nmode = "sometimes"\n': "accept.mode",
            "[router]\ncolour = 1\n": "router.colour",
            '[router]\ninline_chars = "many"\n': "router.inline_chars",
            "[sources.om]\nenabled = true\nmuted = true\n": "sources.om.muted",
            "[weather]\nsunny = true\n": "weather",
        }
        for text, key in cases.items():
            with self.subTest(key=key):
                self.write(text)
                with self.assertRaises(SuperError) as raised:
                    config.load(self.root)
                self.assertIn(key, str(raised.exception))

    def test_rules_are_sorted_stems(self):
        rules = self.root / "policy" / "rules"
        rules.mkdir(parents=True)
        for name in ("silent-repro.md", "review-reply.md", "notes.txt"):
            (rules / name).write_text("rule\n", encoding="utf-8")

        self.assertEqual(config.load(self.root).rules, ["review-reply", "silent-repro"])


if __name__ == "__main__":
    unittest.main()
