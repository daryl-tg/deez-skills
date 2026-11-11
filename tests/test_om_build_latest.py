import http.server
import json
import os
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
LATEST = REPO / "skills/om-build/scripts/latest.sh"

HOSTED_OK = """\
BUILD -- daemon 0.1.0, source 0.2.0
installed:             {install_root}/0.2.0/bin/om
waiting for daemon..
mcp singleton:         0.2.0
stale stdio mcp:       3 (live agent sessions; they exec current on restart)
daemon:                0.2.0 pid 4242
GUI:                   real, rooms.js?v=abc123
auth:                  "type":"AUTH_SUCCESS" "username":"someone"
listener:              127.0.0.1:31337
"""


def git(cwd, *args):
    return subprocess.run(
        ["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


class HealthServer:
    def __init__(self, version):
        body = json.dumps({"pid": 1, "version": version}).encode()

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/healthz"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class OmBuildLatestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.mono = self.make_repo("mono", "packages/cli/package.json", '{"version": "0.2.0"}\n')
        self.gui = self.make_repo("gui", "src/app.ts", "// one\n")
        self.state = self.root / "state"
        self.install_root = self.root / "opt"
        (self.install_root / "0.1.0/bin").mkdir(parents=True)
        (self.install_root / "0.2.0/bin").mkdir(parents=True)
        self.record = self.root / "hosted-record"
        self.hosted = self.root / "hosted.sh"
        self.hosted_output = self.root / "hosted-output"
        self.hosted_output.write_text(HOSTED_OK.format(install_root=self.install_root))
        self.hosted.write_text(
            "#!/bin/sh\n"
            '{ printf "args=%s\\n" "$*"; printf "mono=%s\\n" "$OM_MONO"; '
            'printf "gui=%s\\n" "$OM_GUI"; '
            'printf "mono_head=%s\\n" "$(git -C "$OM_MONO" rev-parse HEAD)"; '
            'printf "gui_head=%s\\n" "$(git -C "$OM_GUI" rev-parse HEAD)"; } > "$RECORD"\n'
            'cat "$HOSTED_OUTPUT"\n'
            'exit "${HOSTED_EXIT:-0}"\n'
        )
        self.hosted.chmod(0o755)

    def make_repo(self, name, path, content):
        remote = self.root / f"{name}-remote.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
        work = self.root / name
        subprocess.run(["git", "clone", "-q", str(remote), str(work)], check=True, capture_output=True)
        git(work, "config", "user.email", "t@example.com")
        git(work, "config", "user.name", "t")
        (work / path).parent.mkdir(parents=True, exist_ok=True)
        (work / path).write_text(content)
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", f"{name} first")
        git(work, "push", "-q", "origin", "HEAD:main")
        git(work, "branch", "-q", "--set-upstream-to=origin/main")
        return work

    def push_commit(self, repo, path, content, message):
        other = self.root / f"pusher-{repo.name}"
        if not other.exists():
            subprocess.run(
                ["git", "clone", "-q", git(repo, "remote", "get-url", "origin"), str(other)],
                check=True,
                capture_output=True,
            )
            git(other, "config", "user.email", "t@example.com")
            git(other, "config", "user.name", "t")
        git(other, "pull", "-q", "origin", "main")
        (other / path).write_text(content)
        git(other, "commit", "-q", "-am", message)
        git(other, "push", "-q", "origin", "HEAD:main")
        return git(other, "rev-parse", "HEAD")

    def run_latest(self, *args, health_url="http://127.0.0.1:9/healthz", hosted_exit=0):
        return subprocess.run(
            [str(LATEST), *args],
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "OM_MONO_REPO": str(self.mono),
                "OM_GUI_REPO": str(self.gui),
                "OM_HOSTED_SH": str(self.hosted),
                "OM_HEALTH_URL": health_url,
                "OM_BUILD_STATE_DIR": str(self.state),
                "OM_INSTALL_ROOT": str(self.install_root),
                "RECORD": str(self.record),
                "HOSTED_OUTPUT": str(self.hosted_output),
                "HOSTED_EXIT": str(hosted_exit),
            },
        )

    def recorded(self):
        return dict(
            line.split("=", 1) for line in self.record.read_text().splitlines() if "=" in line
        )

    def worktrees(self, repo):
        return [
            line for line in git(repo, "worktree", "list", "--porcelain").splitlines()
            if line.startswith("worktree ")
        ]

    def test_builds_origin_main_of_both_repos_in_temp_worktrees_and_cleans_up(self):
        mono_head = self.push_commit(self.mono, "packages/cli/package.json", '{"version": "0.2.1"}\n', "mono second")
        result = self.run_latest()
        self.assertEqual(result.returncode, 0, result.stderr)
        rec = self.recorded()
        self.assertEqual(rec["mono_head"], mono_head)
        self.assertNotEqual(Path(rec["mono"]), self.mono)
        self.assertIn("--force", rec["args"])
        self.assertEqual(len(self.worktrees(self.mono)), 1)
        self.assertFalse(Path(rec["mono"]).exists())

    def test_fast_forwards_a_clean_gui_main_and_builds_from_it(self):
        gui_head = self.push_commit(self.gui, "src/app.ts", "// two\n", "gui second")
        result = self.run_latest()
        self.assertEqual(result.returncode, 0, result.stderr)
        rec = self.recorded()
        self.assertEqual(Path(rec["gui"]), self.gui)
        self.assertEqual(git(self.gui, "rev-parse", "HEAD"), gui_head)
        self.assertIn("main fast-forwarded", result.stdout)

    def test_leaves_a_gui_feature_branch_alone_and_builds_origin_main_in_a_worktree(self):
        git(self.gui, "checkout", "-q", "-b", "feat/x")
        gui_head = self.push_commit(self.gui, "src/app.ts", "// two\n", "gui second")
        result = self.run_latest()
        self.assertEqual(result.returncode, 0, result.stderr)
        rec = self.recorded()
        self.assertNotEqual(Path(rec["gui"]), self.gui)
        self.assertEqual(rec["gui_head"], gui_head)
        self.assertEqual(git(self.gui, "rev-parse", "--abbrev-ref", "HEAD"), "feat/x")
        self.assertIn("feat/x", result.stdout)
        self.assertEqual(len(self.worktrees(self.gui)), 1)

    def test_leaves_a_dirty_gui_main_alone(self):
        (self.gui / "src/app.ts").write_text("// local edit\n")
        self.push_commit(self.gui, "src/app.ts", "// two\n", "gui second")
        result = self.run_latest()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(Path(self.recorded()["gui"]), self.gui)
        self.assertEqual((self.gui / "src/app.ts").read_text(), "// local edit\n")
        self.assertIn("uncommitted", result.stdout)

    def test_prints_a_compact_summary(self):
        result = self.run_latest()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        self.assertIn("om        0.2.0 running, pid 4242", out)
        self.assertIn("daemon was down before the build", out)
        self.assertIn("rooms.js?v=abc123", out)
        self.assertIn("AUTH_SUCCESS someone", out)
        self.assertIn("127.0.0.1:31337", out)
        self.assertIn("rollback  0.1.0 kept", out)
        self.assertNotIn("waiting for daemon", out)

    def test_reports_an_in_place_overwrite_and_names_the_previous_install(self):
        self.hosted_output.write_text(
            "NOTE: overwriting 0.2.0 in place -- the outgoing binary is gone\n"
            + HOSTED_OK.format(install_root=self.install_root)
        )
        result = self.run_latest()
        self.assertIn("rollback  0.2.0 overwritten in place; previous install is 0.1.0", result.stdout)

    def test_counts_commits_since_the_last_build(self):
        self.assertEqual(self.run_latest().returncode, 0)
        self.push_commit(self.mono, "packages/cli/package.json", '{"version": "0.2.1"}\n', "mono second")
        self.push_commit(self.mono, "packages/cli/package.json", '{"version": "0.2.2"}\n', "mono third")
        result = self.run_latest()
        self.assertIn("mono third (+2 since last build)", result.stdout)

    def test_skips_when_nothing_moved_and_the_daemon_answers(self):
        health = HealthServer("0.2.0")
        self.addCleanup(health.close)
        self.assertEqual(self.run_latest(health_url=health.url).returncode, 0)
        self.record.unlink()
        result = self.run_latest(health_url=health.url)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("om        0.2.0, up to date", result.stdout)
        self.assertFalse(self.record.exists())

    def test_builds_when_nothing_moved_but_the_daemon_is_down(self):
        self.assertEqual(self.run_latest().returncode, 0)
        self.record.unlink()
        result = self.run_latest()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.record.exists())

    def test_force_rebuilds_when_nothing_moved(self):
        health = HealthServer("0.2.0")
        self.addCleanup(health.close)
        self.assertEqual(self.run_latest(health_url=health.url).returncode, 0)
        self.record.unlink()
        result = self.run_latest("--force", health_url=health.url)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.record.exists())

    def test_failure_prints_the_cause_and_the_log_and_still_cleans_up(self):
        git(self.gui, "checkout", "-q", "-b", "feat/x")
        self.hosted_output.write_text("== build ==\nsomething\nFAIL: monorepo compile\n")
        result = self.run_latest(hosted_exit=1)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: monorepo compile", result.stdout)
        self.assertIn("log", result.stdout)
        self.assertEqual(len(self.worktrees(self.mono)), 1)
        self.assertEqual(len(self.worktrees(self.gui)), 1)
        self.assertFalse((self.state / "last-build").exists())


if __name__ == "__main__":
    unittest.main()
