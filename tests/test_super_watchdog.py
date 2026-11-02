import json
import os
import plistlib
import re
import shutil
import subprocess
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import config, daemon, launchd, router, watchdog, workers
from deezlib.superclanker.domain import utc_now
from deezlib.superclanker.sources import terminal
from deezlib.superclanker.store import Store, SuperError

HUB = cli.REPO_ROOT
FAKE = Path(__file__).with_name("fake_claude.py")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
FAKE_LAUNCHCTL = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAKE_LAUNCHCTL_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
sys.exit(0)
"""
ALLOWLIST = [
    "Bash(deez super *)", "Bash(launchctl list *)", "Bash(launchctl kickstart *)",
    "Bash(claude logs *)",
]


def dead_pid():
    process = subprocess.Popen(["true"])
    process.wait()
    return process.pid


def later(**delta):
    moved = datetime.fromisoformat(utc_now()) + timedelta(**delta)
    return moved.isoformat(timespec="seconds")


def block(digest, kind):
    after = digest.split(f"## {kind}\n", 1)[1]
    return after.split("\n## ", 1)[0]


class WatchdogTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.root = self.tmp / "state"
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        shutil.copy(FAKE, bin_dir / "claude")
        (bin_dir / "claude").chmod(0o755)
        (bin_dir / "launchctl").write_text(FAKE_LAUNCHCTL, encoding="utf-8")
        (bin_dir / "launchctl").chmod(0o755)
        self.log = self.tmp / "argv.jsonl"
        self.launchctl_log = self.tmp / "launchctl.jsonl"
        environ = {
            key: value for key, value in os.environ.items()
            if not key.startswith("FAKE_CLAUDE_")
        }
        environ.update({
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_CLAUDE_LOG": str(self.log),
            "FAKE_LAUNCHCTL_LOG": str(self.launchctl_log),
            "DEEZ_SUPER_STATE": str(self.root),
            "DEEZ_SUPER_DEVNOTES": str(self.tmp / "dev-notes"),
            "HOME": str(self.tmp / "home"),
            "USER": "daryl",
        })
        patcher = mock.patch.dict(os.environ, environ, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)

    def settings(self):
        return config.load(self.root)

    def digest(self, now=utc_now):
        return watchdog.digest(self.store, self.settings(), self.root, now=now)

    def tick(self):
        return watchdog.tick(self.store, self.settings(), self.root, HUB)

    def daemon_alive(self, at=None):
        lock = self.root / "daemon.lock.d"
        lock.mkdir(exist_ok=True)
        (lock / "pid").write_text(str(os.getpid()), encoding="utf-8")
        (self.root / "daemon.heartbeat").write_text((at or utc_now()) + "\n", encoding="utf-8")

    def deez(self, *argv):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super", *argv])
        return code, out.getvalue(), err.getvalue()

    def argvs(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def dispatch(self, text="fix the typo in README", slug="fix-readme-typo"):
        trigger, _receipt = terminal.ask(self.store, text)
        code, out, err = self.deez("dispatch", trigger.id, "--slug", slug, "--playbook", "bug-fix")
        self.assertEqual(code, 0, err)
        ticket_id = re.search(r"ticket (k_[0-9a-f]{10})", out).group(1)
        return ticket_id, self.store.assignment_for(ticket_id).id

    def run_worker(self, assignment_id, result):
        os.environ["FAKE_CLAUDE_RESULT"] = result
        started = workers.launch(self.store, self.settings(), assignment_id, HUB, self.root)
        deadline = time.monotonic() + 2
        while workers.alive(started.pid):
            self.assertLess(time.monotonic(), deadline, "fake worker did not exit")
            time.sleep(0.01)
        del os.environ["FAKE_CLAUDE_RESULT"]
        return started

    def stalled_ticket(self):
        ticket_id, assignment_id = self.dispatch()
        self.run_worker(assignment_id, "tried hard\nREPORT failed boom")
        workers.reap(self.store, self.root)
        return ticket_id, assignment_id

    def test_empty_digest_skips_model_call(self):
        self.daemon_alive()

        self.assertEqual(self.digest(), "")
        self.assertIsNone(self.tick())
        self.assertEqual(self.argvs(), [])
        self.assertEqual(self.deez("watchdog", "--digest"), (0, "clean\n", ""))
        self.assertEqual(self.deez("watchdog"), (0, "clean, no tick\n", ""))
        self.assertEqual(self.argvs(), [])

        self.stalled_ticket()
        self.log.unlink()

        self.assertIsNotNone(self.tick())
        self.assertEqual(len(self.argvs()), 1)

    def test_dead_worker_with_running_assignment_is_an_anomaly(self):
        self.daemon_alive()
        ticket_id, assignment_id = self.dispatch()
        started = self.run_worker(assignment_id, "REPORT ready done")

        digest = self.digest()

        self.assertTrue(digest.startswith("## unreaped turn\n"), digest)
        self.assertIn(
            f"{assignment_id} on {ticket_id}: pid {started.pid} is dead and "
            f"{assignment_id}.json has no .reaped marker",
            block(digest, "unreaped turn"),
        )
        self.assertIn(f"more: deez super show {assignment_id}", block(digest, "unreaped turn"))

        workers.reap(self.store, self.root)

        self.assertEqual(self.digest(), "")

    def test_stalled_ticket_after_failed_report_is_an_anomaly(self):
        self.daemon_alive()
        ticket_id, assignment_id = self.stalled_ticket()
        report_id = self.store.show(ticket_id)["related"]
        report_id = next(i for i, _s in report_id if i.startswith("r_"))

        digest = self.digest()

        self.assertEqual(
            digest,
            "## stalled ticket\n"
            f"{ticket_id} fix-readme-typo: {assignment_id} ended with failed {report_id}: boom\n"
            f"more: deez super show {ticket_id}; deez super show {assignment_id}",
        )

        self.store.retry(ticket_id)

        self.assertEqual(self.digest(), "")

    def test_stale_heartbeat_reports_daemon_down(self):
        self.assertIn("no live daemon pid in", block(self.digest(), "daemon down"))

        self.daemon_alive(at=later(minutes=-5))
        stale = block(self.digest(), "daemon down")

        self.assertIn("heartbeat is 300s old, limit 120s", stale)

        self.daemon_alive()
        self.assertEqual(self.digest(), "")

        (self.root / "daemon.lock.d" / "pid").write_text(str(dead_pid()), encoding="utf-8")
        self.assertIn("no live daemon pid in", block(self.digest(), "daemon down"))

    def test_heartbeat_is_written_by_every_daemon_pass(self):
        def no_reap(store, root):
            return []

        daemon.one_pass(self.store, self.settings(), self.root, HUB, reap=no_reap,
                        now=lambda: "2026-11-02T10:00:00+00:00")

        heartbeat = (self.root / "daemon.heartbeat").read_text(encoding="utf-8")
        self.assertEqual(heartbeat.strip(), "2026-11-02T10:00:00+00:00")

    def test_unanswered_waiting_question_is_an_anomaly_and_a_reply_clears_it(self):
        ticket_id, assignment_id = self.dispatch()
        self.run_worker(assignment_id, "REPORT waiting which branch should I use?")
        workers.reap(self.store, self.root)
        two_hours_on = later(hours=2)
        self.daemon_alive(at=two_hours_on)

        self.assertEqual(self.digest(), "")
        unanswered = block(self.digest(now=lambda: two_hours_on), "unanswered question")

        self.assertIn(f"{ticket_id} fix-readme-typo: waiting", unanswered)
        self.assertIn("which branch should I use?", unanswered)
        self.assertIn("no reply on terminal:default", unanswered)

        self.store.reply("terminal:default", "the worker asks which branch to use")

        self.assertEqual(self.digest(now=lambda: two_hours_on), "")

    def test_requeued_trigger_returns_to_the_queue(self):
        self.daemon_alive()
        asked, _receipt = terminal.ask(self.store, "fix the typo")
        first = router.wake(self.store, self.settings(), self.root, HUB)

        self.assertEqual(self.store.queued(), [])
        undecided = block(self.digest(), "undecided")
        self.assertIn(f"{asked.id}: decided unavailable", undecided)
        self.assertIn(f"router made no decision in {first.wake_id}", undecided)

        requeued = self.deez("requeue", asked.id)

        self.assertEqual(requeued, (0, f"requeued {asked.id}\n", ""))
        self.assertEqual([t.id for t in self.store.queued()], [asked.id])
        self.assertEqual(self.store.undecided([asked.id]), [asked.id])
        self.assertEqual(self.digest(), "")

        second = router.wake(self.store, self.settings(), self.root, HUB)

        self.assertEqual(second.batch, 1)
        self.assertEqual(self.store.queued(), [])
        self.assertIn(f"router made no decision in {second.wake_id}", block(self.digest(), "undecided"))

        self.deez("requeue", asked.id)
        os.environ["FAKE_CLAUDE_SCRIPT"] = f"deez super ignore {asked.id} --reason chatter"
        router.wake(self.store, self.settings(), self.root, HUB)

        self.assertEqual(self.store.queued(), [])
        self.assertEqual(self.digest(), "")

    def test_requeue_refuses_an_accepted_trigger(self):
        ticket_id, _assignment_id = self.dispatch()
        origin = self.store.ticket_origin(ticket_id)

        refused = self.deez("requeue", origin.id)

        self.assertEqual(refused[0], 2)
        self.assertIn(f"{origin.id} is accepted as {ticket_id}", refused[2])
        self.assertEqual(self.store.queued(), [])

    def test_retry_ends_stalled_assignment_and_starts_new(self):
        self.daemon_alive()
        ticket_id, assignment_id = self.stalled_ticket()

        code, out, err = self.deez("retry", ticket_id)

        fresh = self.store.assignment_for(ticket_id)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, f"retry {ticket_id} → {fresh.id} pending\n")
        self.assertNotEqual(fresh.id, assignment_id)
        self.assertEqual(str(fresh.state), "pending")
        self.assertEqual(str(self.store.show(assignment_id)["state"]), "ended")
        self.assertEqual(self.store.pending_assignments(), [fresh])
        self.assertEqual(self.digest(), "")

    def test_tick_creates_session_once_then_resumes_and_records_tick(self):
        first = self.tick()
        second = self.tick()

        one, two = self.argvs()
        sid = one[one.index("--session-id") + 1]
        self.assertRegex(sid, UUID)
        self.assertNotIn("--resume", one)
        self.assertEqual(two[two.index("--resume") + 1], sid)
        self.assertNotIn("--session-id", two)
        self.assertEqual((self.root / "watchdog.session").read_text(encoding="utf-8").strip(), sid)
        self.assertFalse((self.root / "router.session").exists())
        self.assertRegex(first.tick_id, r"^x_[0-9a-f]{10}$")
        shown = self.store.show(second.tick_id)
        self.assertEqual(
            (shown["exit_code"], shown["cost_usd"], shown["session_id"], shown["result"]),
            (0, 0.001, sid, "ok"),
        )
        self.assertIn("## daemon down", shown["digest"])
        self.assertIsNotNone(shown["ended_at"])

        code, out, err = self.deez("watchdog")

        self.assertEqual((code, err), (0, ""))
        printed = re.fullmatch(r"tick (x_[0-9a-f]{10}) cost 0\.0010\n", out)
        self.assertIsNotNone(printed, out)
        self.assertEqual(self.store.show(printed.group(1))["session_id"], sid)

    def test_failed_tick_drops_a_new_session_and_names_the_tick(self):
        os.environ["FAKE_CLAUDE_EXIT"] = "1"

        with self.assertRaisesRegex(SuperError, r"watchdog tick (x_[0-9a-f]{10}) failed with exit 1") as caught:
            self.tick()

        tick_id = re.search(r"x_[0-9a-f]{10}", str(caught.exception)).group(0)
        shown = self.store.show(tick_id)
        self.assertEqual(shown["exit_code"], 1)
        self.assertIn("fake claude failed with 1", shown["result"])
        self.assertFalse((self.root / "watchdog.session").exists())

    def test_tick_passes_digest_agent_prompt_and_allowlist(self):
        (self.root / "sources.toml").write_text('[watchdog]\nmodel = "haiku"\n', encoding="utf-8")
        seen = self.tmp / "seen-state"
        os.environ["FAKE_CLAUDE_SCRIPT"] = f'echo "$DEEZ_SUPER_STATE" > {seen}'

        self.tick()

        (argv,) = self.argvs()
        body = (HUB / "agents" / "super-watchdog.md").read_text(encoding="utf-8").split("---\n", 2)[2]
        self.assertEqual(argv[:2], ["-p", "--model"])
        self.assertEqual(argv[argv.index("--model") + 1], "haiku")
        self.assertEqual(argv[argv.index("--tools") + 1], "Bash")
        start = argv.index("--allowedTools") + 1
        self.assertEqual(argv[start:start + 4], ALLOWLIST)
        self.assertEqual(argv[start + 4], "--permission-mode")
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "dontAsk")
        self.assertEqual(argv[argv.index("--output-format") + 1], "json")
        self.assertIn("--strict-mcp-config", argv)
        self.assertEqual(argv[argv.index("--setting-sources") + 1], "project,local")
        system_prompt = argv[argv.index("--append-system-prompt") + 1]
        self.assertEqual(system_prompt, body.strip())
        self.assertIn("You are the Watchdog", system_prompt)
        self.assertLess(len(system_prompt.split()), 300)
        self.assertEqual(argv[-1], self.digest())
        self.assertTrue(argv[-1].startswith("## daemon down\n"))
        self.assertEqual(seen.read_text(encoding="utf-8").strip(), str(self.root))

    def test_long_turns_failed_wakes_source_errors_and_orphan_worktrees(self):
        (self.root / "sources.toml").write_text(
            '[watchdog]\nmax_turn_minutes = 30\n\n[sources.github]\nenabled = true\n',
            encoding="utf-8",
        )
        self.daemon_alive(at=later(hours=1))
        ticket_id, assignment_id = self.dispatch()
        self.store.start_assignment(assignment_id, "sid", os.getpid(), self.root)
        ended_id, _ended_assignment = self.dispatch("another thing", "another-thing")
        self.store.stop(ended_id, "daryl", "not needed")
        orphan = self.root / "worktrees" / "scratch-repo" / ended_id
        orphan.mkdir(parents=True)
        (self.root / "worktrees" / "scratch-repo" / ticket_id).mkdir()
        wake_id = self.store.begin_wake([])
        self.store.end_wake(wake_id, 1, None, None, "boom")
        self.store.set_cursor("github", "last_error", "gh api exited 1: bad credentials")

        digest = self.digest(now=lambda: later(hours=1))

        self.assertEqual(
            [line for line in digest.splitlines() if line.startswith("## ")],
            ["## long turn", "## failed wakes", "## source errors", "## orphan worktree"],
        )
        self.assertIn(f"{assignment_id} on {ticket_id}: pid {os.getpid()} running 60 minutes, limit 30",
                      block(digest, "long turn"))
        self.assertIn(f"1 wake failed in 24 hours: {wake_id} exit 1", block(digest, "failed wakes"))
        self.assertIn("github: gh api exited 1: bad credentials", block(digest, "source errors"))
        self.assertIn(f"{orphan}: {ended_id} has ended", block(digest, "orphan worktree"))
        self.assertNotIn(ticket_id, block(digest, "orphan worktree"))
        self.assertEqual(digest.count("\nmore: "), 4)

        self.store.set_cursor("github", "last_error", "")
        self.assertNotIn("## source errors", self.digest(now=lambda: later(hours=1)))

    def test_install_plan_lists_both_plists(self):
        (self.root / "sources.toml").write_text('[watchdog]\ninterval_seconds = 900\n', encoding="utf-8")
        home = self.tmp / "home"
        agents = self.tmp / "agents"
        daemon_plist = agents / "com.dboon.super-clanker.plist"
        watchdog_plist = agents / "com.dboon.super-watchdog.plist"
        domain = f"gui/{os.getuid()}"

        planned = launchd.install(HUB, self.root, home, agents, apply=False)

        self.assertIn(f"would create {daemon_plist}", planned)
        self.assertIn(f"would create {watchdog_plist}", planned)
        self.assertFalse(agents.exists())

        launchd.install(HUB, self.root, home, agents, apply=True)

        written = plistlib.loads(watchdog_plist.read_bytes())
        self.assertEqual(written["Label"], "com.dboon.super-watchdog")
        self.assertEqual(written["ProgramArguments"], [str(HUB / "bin" / "deez"), "super", "watchdog"])
        self.assertEqual((written["StartInterval"], written["RunAtLoad"]), (900, False))
        self.assertNotIn("KeepAlive", written)
        self.assertEqual(written["StandardOutPath"], str(self.root / "log" / "watchdog.out.log"))
        self.assertEqual(written["StandardErrorPath"], str(self.root / "log" / "watchdog.err.log"))
        self.assertEqual(written["EnvironmentVariables"]["DEEZ_SUPER_STATE"], str(self.root))
        self.assertTrue(daemon_plist.exists())
        calls = [json.loads(line) for line in self.launchctl_log.read_text(encoding="utf-8").splitlines()]
        self.assertIn(["bootstrap", domain, str(watchdog_plist)], calls)
        self.assertNotIn(["kickstart", "-k", f"{domain}/com.dboon.super-watchdog"], calls)
        self.assertIn(
            f"would replace {watchdog_plist} (unchanged)",
            launchd.install(HUB, self.root, home, agents, apply=False),
        )

        launchd.uninstall(home, agents, apply=True)

        self.assertFalse(watchdog_plist.exists())
        self.assertFalse(daemon_plist.exists())

    def test_watchdog_config_is_validated(self):
        (self.root / "sources.toml").write_text('[watchdog]\ninterval_seconds = 0\n', encoding="utf-8")

        with self.assertRaisesRegex(SuperError, "watchdog.interval_seconds must be a positive integer"):
            self.settings()


if __name__ == "__main__":
    unittest.main()
