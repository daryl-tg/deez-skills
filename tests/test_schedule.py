import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


class ScheduleTest(unittest.TestCase):
    def test_installed_symlink_finds_the_project_skill_and_hub_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hub = root / "hub"
            hub.mkdir()
            for item in ("bin", "deezlib"):
                shutil.copytree(REPO / item, hub / item,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (hub / "registry.toml").write_text('''
[meta]
version = 1
default_profile = "full"
[categories]
core = "Core"
[profiles]
full = ["*"]
[skills.verify-example]
category = "core"
runtimes = ["claude", "codex"]
project = "example-app"
''')
            skill = hub / "projects/example-app/skills/verify-example"
            (skill / "features").mkdir(parents=True)
            (skill / "bin").mkdir()
            (skill / "SKILL.md").write_text("control-example doctor\n")
            wrapper = skill / "bin/control-example"
            wrapper.write_text("#!/bin/sh\nexit 0\n")
            wrapper.chmod(0o755)
            scheduler = hub / "skills/maintain-verification-skill/scripts"
            scheduler.mkdir(parents=True)
            shutil.copy2(REPO / "skills/maintain-verification-skill/scripts/scheduled-run.sh",
                         scheduler / "scheduled-run.sh")
            installed = root / "runtime/skills/maintain-verification-skill"
            installed.parent.mkdir(parents=True)
            installed.symlink_to(scheduler.parent)
            harness = root / "harness-bin"
            harness.mkdir()
            claude = harness / "claude"
            claude.write_text(
                '#!/bin/sh\npwd > "$DEEZ_CWD_CAPTURE"\n'
                'printf "%s" "$2" > "$DEEZ_PROMPT_CAPTURE"\n'
                'printf "VERDICT: clean\\n"\n'
                'exit "${DEEZ_CLAUDE_RC:-0}"\n')
            claude.chmod(0o755)
            product = root / "product-worktree"
            product.mkdir()
            capture = root / "prompt.txt"
            cwd_capture = root / "cwd.txt"
            env = {**os.environ, "PATH": f"{harness}:{os.environ['PATH']}",
                   "DEEZ_MAINTAIN_STATE": str(root / "state"),
                   "DEEZ_CWD_CAPTURE": str(cwd_capture),
                   "DEEZ_PROMPT_CAPTURE": str(capture)}
            result = subprocess.run(
                [str(installed / "scripts/scheduled-run.sh"), str(product), "verify-example"],
                capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(capture.is_file(), result.stdout + result.stderr)
            prompt = capture.read_text()
            self.assertIn(str(skill.resolve()), prompt)
            self.assertIn(
                str(hub.resolve() / "skills/maintain-verification-skill/SKILL.md"),
                prompt)
            self.assertIn(str(hub.resolve() / "docs/project-verification.md"), prompt)
            self.assertIn(f"Initial ownership lookup: {skill.resolve()}", prompt)
            self.assertIn("initial ownership lookup only", prompt)
            self.assertIn("fetch current origin/main", prompt)
            self.assertIn("worktree status, upstream ancestry, and outgoing history", prompt)
            self.assertIn("detached isolated hub worktree", prompt)
            self.assertIn("actual isolated skill path", prompt)
            self.assertIn("Leave the operator hub untouched", prompt)
            self.assertIn("Honor .sync-hold from the original hub", prompt)
            self.assertIn("full user-facing source surface", prompt)
            self.assertIn("source-supported inventory gaps", prompt)
            self.assertIn("explicitly pending", prompt)
            self.assertIn("map-only automatic publisher", prompt)
            self.assertIn("publisher receipt", prompt)
            self.assertEqual(
                Path(cwd_capture.read_text().strip()).resolve(), product.resolve())
            self.assertFalse((root / "state/verify-example.lock.d").exists())

            failed_env = {**env, "DEEZ_CLAUDE_RC": "7"}
            failed = subprocess.run(
                [str(installed / "scripts/scheduled-run.sh"), str(product), "verify-example"],
                capture_output=True, text=True, env=failed_env)
            self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
            self.assertIn("VERDICT: clean", failed.stderr)
            self.assertFalse((root / "state/verify-example.lock.d").exists())
