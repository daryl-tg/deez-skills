import os
import stat
import tempfile
import tomllib
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import fields
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import config, rules, sources

EXAMPLE_RULE = cli.REPO_ROOT / "skills" / "super-clanker" / "references" / "rules" / "silent-repro.md"


class InitTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "state"
        patcher = mock.patch.dict(
            os.environ, {**os.environ, "DEEZ_SUPER_STATE": str(self.root), "USER": "daryl"},
            clear=True,
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.sources = self.root / "sources.toml"
        self.rule = self.root / "policy" / "rules" / "silent-repro.md"

    def deez(self, *argv):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super", *argv])
        return code, out.getvalue(), err.getvalue()

    def test_init_writes_config_and_example_rule_and_keeps_existing_without_force(self):
        first = self.deez("init")

        self.assertEqual(first, (0, f"wrote {self.sources}\nwrote {self.rule}\n", ""))
        self.assertEqual(stat.S_IMODE(self.root.stat().st_mode), 0o700)
        self.assertEqual(
            self.rule.read_text(encoding="utf-8"), EXAMPLE_RULE.read_text(encoding="utf-8")
        )
        self.assertEqual(rules.load(self.root)["silent-repro"].mode, config.AcceptMode.observe)
        self.assertFalse((self.root / "super.db").exists())

        written = self.sources.read_text(encoding="utf-8")
        self.sources.write_text('[router]\nmodel = "opus"\n', encoding="utf-8")
        self.rule.write_text("# Edited\nmode: auto\n", encoding="utf-8")
        again = self.deez("init")

        self.assertEqual(again, (0, f"kept {self.sources}\nkept {self.rule}\n", ""))
        self.assertEqual(config.load(self.root).router.model, "opus")
        self.assertEqual(rules.load(self.root)["silent-repro"].mode, config.AcceptMode.auto)

        forced = self.deez("init", "--force")

        self.assertEqual(forced, (0, f"wrote {self.sources}\nwrote {self.rule}\n", ""))
        self.assertEqual(self.sources.read_text(encoding="utf-8"), written)
        self.assertEqual(rules.load(self.root)["silent-repro"].mode, config.AcceptMode.observe)

    def test_init_config_loads_with_every_default(self):
        self.deez("init")

        loaded = config.load(self.root)
        raw = tomllib.loads(self.sources.read_text(encoding="utf-8"))

        self.assertEqual(loaded.accept, config.AcceptPolicy())
        self.assertEqual(loaded.accept.mode, config.AcceptMode.observe)
        self.assertEqual(loaded.router, config.RouterConfig())
        self.assertEqual(loaded.router.model, "sonnet")
        self.assertEqual(loaded.workers, config.WorkersConfig())
        self.assertEqual(loaded.watchdog, config.WatchdogConfig())
        self.assertEqual(loaded.rules, ["silent-repro"])
        named = ["terminal", *sources.POLLERS]
        self.assertEqual(sorted(raw["sources"]), sorted(named))
        self.assertEqual(loaded.policy("terminal").senders, ("daryl",))
        self.assertTrue(loaded.policy("terminal").enabled)
        for name in named:
            self.assertEqual(loaded.policy(name), config.default_policy(name))
            source_keys = {f.name for f in fields(config.SourcePolicy)} - {"name"}
            self.assertEqual(set(raw["sources"][name]), source_keys)
        for name in sources.POLLERS:
            self.assertFalse(raw["sources"][name]["enabled"])
        for section, kind in (
            ("accept", config.AcceptPolicy), ("router", config.RouterConfig),
            ("watchdog", config.WatchdogConfig),
        ):
            self.assertEqual(set(raw[section]), {f.name for f in fields(kind)})
        self.assertEqual(set(raw["workers"]), {"max_running"})


if __name__ == "__main__":
    unittest.main()
