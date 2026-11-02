import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


class ClankerCliTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = {
            **os.environ,
            "DEEZ_CLANKER_STATE": str(self.root / "state"),
            "DEEZ_CLAUDE_HOME": str(self.root / "claude"),
            "DEEZ_CODEX_HOME": str(self.root / "codex"),
        }

    def run_deez(self, *args, payload=None):
        return subprocess.run(
            [str(REPO / "bin/deez"), *args], input=payload,
            capture_output=True, text=True, env=self.env,
        )

    def test_separate_hook_processes_restore_after_compaction_and_stop(self):
        def hook(event, **fields):
            result = self.run_deez(
                "clanker-hook", "--runtime", "codex",
                payload=json.dumps({"session_id": "session-a",
                                    "hook_event_name": event, **fields}),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout) if result.stdout else None

        self.assertIsNotNone(hook("UserPromptSubmit", prompt="$clanker-mode build a feature"))
        result = hook("SessionStart", source="compact")
        self.assertEqual(result["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("SKILL.md", result["hookSpecificOutput"]["additionalContext"])
        self.assertIsNotNone(hook("UserPromptSubmit", prompt="keep going"))
        hook("UserPromptSubmit", prompt="stop clanker mode")
        self.assertIsNone(hook("SessionStart", source="resume"))

    def test_installer_plan_is_read_only_then_apply_preserves_existing_hook(self):
        self.root.joinpath("codex").mkdir()
        path = self.root / "codex/hooks.json"
        existing = {"hooks": {"SessionStart": [{"hooks": [
            {"type": "command", "command": "existing-hook"}
        ]}]}, "description": "keep me"}
        path.write_text(json.dumps(existing))
        before = path.read_bytes()
        result = self.run_deez("clanker-hooks")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse(self.root.joinpath("claude").exists())

        result = self.run_deez("clanker-hooks", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = json.loads(path.read_text())
        self.assertEqual(installed["description"], "keep me")
        self.assertEqual(installed["hooks"]["SessionStart"][0],
                         existing["hooks"]["SessionStart"][0])
        self.assertIn("UserPromptSubmit", installed["hooks"])
        self.assertIn("SessionStart", installed["hooks"])
        self.assertIn("PreToolUse", installed["hooks"])

    def test_invalid_hook_input_does_not_block_a_turn(self):
        for payload in ("not JSON", "[]", '{"hook_event_name":"UserPromptSubmit"}'):
            with self.subTest(payload=payload):
                result = self.run_deez("clanker-hook", "--runtime", "claude", payload=payload)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(result.stdout)
