import plistlib
import signal
import unittest
from types import SimpleNamespace
from unittest import mock

from deezlib import memguard
from deezlib.memguard import (
    Paused,
    Proc,
    launch_agent_plist,
    parse_free_pct,
    parse_top,
    plan,
    safe_tick,
    weekly_plist,
    weekly_report,
)

MIN = 60
NOW = 1_800_000_000
CLAUDE = Proc(pid=100, ppid=1, age_s=3 * 86400, mem_mb=500, args="claude --resume abc")
DAEMON = Proc(pid=101, ppid=1, age_s=3 * 86400, mem_mb=700, args="bun packages/cli/src/bootstrap.ts run")


def typecheck_job(shell_pid, age_s, tsc_mb, parent=100):
    return [
        Proc(shell_pid, parent, age_s, 2, "/bin/zsh -c eval 'cd /r/openmarket-internal-x && bun run typecheck'"),
        Proc(shell_pid + 1, shell_pid, age_s, 3, "bun run typecheck"),
        Proc(shell_pid + 2, shell_pid + 1, age_s - 5, 40, "bun scripts/typecheck-cli.ts"),
        Proc(shell_pid + 3, shell_pid + 2, age_s - 10, tsc_mb,
             "node /r/node_modules/typescript/bin/tsc --noEmit -p /tmp/om-cli-typecheck-x/source.json"),
    ]


def paused(root, procs, paused_at):
    tree = [p.pid for p in procs if p.pid >= root and p.pid < root + 4]
    args = next(p.args for p in procs if p.pid == root)
    return Paused(root=root, pids=tree, paused_at=paused_at, args=args, mem_mb=5000)


def summary(actions):
    return [(a.kind, a.root, a.reason) for a in actions]


class PlanTest(unittest.TestCase):
    def test_healthy_memory_and_long_jobs_are_left_alone(self):
        procs = [CLAUDE, DAEMON] + typecheck_job(200, 90 * MIN, 6000)
        self.assertEqual(plan(procs, free_pct=60, paused={}), [])

    def test_critical_memory_pauses_newest_job_as_a_whole_tree(self):
        procs = [CLAUDE, DAEMON] + typecheck_job(200, 20 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        actions = plan(procs, free_pct=10, paused={})
        self.assertEqual(summary(actions), [("pause", 300, "memory-critical")])
        self.assertEqual(sorted(actions[0].pids), [300, 301, 302, 303])
        self.assertEqual(actions[0].mem_mb, 5045)

    def test_critical_memory_pauses_the_next_running_job_when_newest_is_already_paused(self):
        procs = [CLAUDE] + typecheck_job(200, 20 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        state = {300: paused(300, procs, NOW - 60)}
        self.assertEqual(summary(plan(procs, free_pct=10, paused=state)), [("pause", 200, "memory-critical")])

    def test_critical_memory_never_touches_claude_or_daemons(self):
        self.assertEqual(plan([CLAUDE, DAEMON], free_pct=3, paused={}), [])

    def test_recovered_memory_resumes_the_longest_paused_job_first_one_per_tick(self):
        procs = [CLAUDE] + typecheck_job(200, 20 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        state = {300: paused(300, procs, NOW - 600), 200: paused(200, procs, NOW - 60)}
        self.assertEqual(summary(plan(procs, free_pct=40, paused=state)), [("resume", 300, "memory-recovered")])

    def test_between_thresholds_nothing_is_paused_or_resumed(self):
        procs = [CLAUDE] + typecheck_job(200, 20 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        state = {300: paused(300, procs, NOW - 600)}
        self.assertEqual(plan(procs, free_pct=22, paused=state), [])

    def test_last_resort_kills_newest_paused_job_only_when_nothing_is_left_to_pause(self):
        procs = [CLAUDE] + typecheck_job(200, 20 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        state = {300: paused(300, procs, NOW - 600), 200: paused(200, procs, NOW - 60)}
        self.assertEqual(summary(plan(procs, free_pct=4, paused=state)), [("kill", 300, "last-resort")])

    def test_below_last_resort_a_running_job_is_paused_not_killed(self):
        procs = [CLAUDE] + typecheck_job(300, 2 * MIN, 5000)
        self.assertEqual(summary(plan(procs, free_pct=3, paused={})), [("pause", 300, "memory-critical")])

    def test_orphaned_heavy_job_is_killed(self):
        procs = [CLAUDE, Proc(400, 1, 3 * MIN, 900, "bun test --max-concurrency 4 a.test.ts")]
        self.assertEqual(summary(plan(procs, free_pct=60, paused={})), [("kill", 400, "orphaned")])

    def test_orphaned_paused_job_is_killed_and_not_resumed(self):
        procs = [CLAUDE] + typecheck_job(300, 2 * MIN, 5000, parent=1)
        state = {300: paused(300, procs, NOW - 600)}
        self.assertEqual(summary(plan(procs, free_pct=60, paused=state)), [("kill", 300, "orphaned")])

    def test_paused_job_that_exited_is_forgotten(self):
        state = {300: Paused(300, [300, 301], NOW - 600, "bun run typecheck", 5000)}
        self.assertEqual(summary(plan([CLAUDE], free_pct=60, paused=state)), [("forget", 300, "gone")])

    def test_paused_pid_reused_by_another_command_is_forgotten_not_resumed(self):
        state = {300: Paused(300, [300], NOW - 600, "bun run typecheck", 5000)}
        procs = [CLAUDE, Proc(300, 100, 10, 50, "vim notes.md")]
        self.assertEqual(summary(plan(procs, free_pct=60, paused=state)), [("forget", 300, "gone")])

    def test_small_jobs_are_ignored(self):
        procs = [CLAUDE, Proc(500, 100, 90 * MIN, 20, "/bin/zsh -c ps -ax | grep typecheck")]
        self.assertEqual(plan(procs, free_pct=5, paused={}), [])

    def test_other_test_runners_and_builds_count_as_heavy(self):
        for args in ["npx vitest run", "node node_modules/.bin/jest", "bun tools/om-chat-gate.ts regressions",
                     "npx playwright test", "node node_modules/.bin/next build", "bun tools/test-fast.ts"]:
            procs = [CLAUDE, Proc(600, 100, 2 * MIN, 2000, args)]
            self.assertEqual([a.root for a in plan(procs, free_pct=8, paused={})], [600], args)

    def test_dev_servers_and_mcp_servers_are_not_heavy(self):
        for args in ["/opt/homebrew/bin/om mcp serve --stdio", "node playwright-mcp", "vite preview --host 127.0.0.1",
                     "bun server.ts", "/opt/homebrew/bin/om run --daemon-internal"]:
            procs = [CLAUDE, Proc(700, 1, 90 * MIN, 3000, args)]
            self.assertEqual(plan(procs, free_pct=5, paused={}), [], args)


class FailsafeTest(unittest.TestCase):
    def test_any_error_resumes_every_paused_job_and_clears_state(self):
        state = {300: Paused(300, [300, 301], NOW, "bun run typecheck", 5000),
                 200: Paused(200, [200], NOW, "bun test a.test.ts", 900)}
        sent = []

        def broken_planner(*_):
            raise RuntimeError("boom")

        events = safe_tick([CLAUDE], 50, state, NOW, send=lambda pid, sig: sent.append((pid, sig)),
                           planner=broken_planner)
        self.assertEqual(sorted(sent), [(200, signal.SIGCONT), (300, signal.SIGCONT), (301, signal.SIGCONT)])
        self.assertEqual(state, {})
        self.assertEqual([e["event"] for e in events], ["error", "resume", "resume"])

    def test_pause_then_resume_sends_stop_then_cont_to_the_whole_tree(self):
        procs = [CLAUDE] + typecheck_job(300, 2 * MIN, 5000)
        state, sent = {}, []
        safe_tick(procs, 10, state, NOW, send=lambda pid, sig: sent.append((pid, sig)))
        self.assertEqual(sorted(sent), [(p, signal.SIGSTOP) for p in (300, 301, 302, 303)])
        self.assertIn(300, state)
        sent.clear()
        safe_tick(procs, 45, state, NOW + 300, send=lambda pid, sig: sent.append((pid, sig)))
        self.assertEqual(sorted(sent), [(p, signal.SIGCONT) for p in (300, 301, 302, 303)])
        self.assertEqual(state, {})


class ReportTest(unittest.TestCase):
    def test_week_summary_counts_actions_and_flags_kills(self):
        day = 86400
        events = [
            {"ts": NOW - 8 * day, "event": "pause", "root": 1, "mem_mb": 9000, "args": "too old"},
            {"ts": NOW - 3 * day, "event": "sample", "free": 9},
            {"ts": NOW - 3 * day, "event": "pause", "root": 300, "mem_mb": 6000,
             "args": "/bin/zsh -c eval 'cd /r/openmarket-internal-approvals && bun run typecheck'"},
            {"ts": NOW - 3 * day + 420, "event": "resume", "root": 300, "paused_s": 420},
            {"ts": NOW - 2 * day, "event": "sample", "free": 41},
            {"ts": NOW - day, "event": "kill", "root": 400, "reason": "orphaned", "mem_mb": 900,
             "args": "bun test a.test.ts"},
        ]
        report = weekly_report(events, NOW)
        self.assertIn("Lowest free memory: 9%", report)
        self.assertIn("Paused: 1", report)
        self.assertIn("Resumed: 1", report)
        self.assertIn("Longest pause: 7 min", report)
        self.assertIn("Killed: 1", report)
        self.assertIn("orphaned", report)
        self.assertIn("openmarket-internal-approvals", report)
        self.assertNotIn("too old", report)

    def test_quiet_week_says_nothing_needed(self):
        report = weekly_report([{"ts": NOW - 100, "event": "sample", "free": 55}], NOW)
        self.assertIn("Nothing paused or killed", report)


class LaunchAgentTest(unittest.TestCase):
    def test_watchdog_plist_runs_the_hub_entrypoint_every_30_seconds(self):
        plist = plistlib.loads(launch_agent_plist("/hub").encode())
        self.assertEqual(plist["Label"], "com.dboon.memguard")
        self.assertEqual(plist["ProgramArguments"], ["/hub/bin/memguard"])
        self.assertEqual(plist["StartInterval"], 30)
        self.assertTrue(plist["RunAtLoad"])

    def test_weekly_plist_runs_report_monday_morning(self):
        plist = plistlib.loads(weekly_plist("/hub").encode())
        self.assertEqual(plist["Label"], "com.dboon.memguard.weekly")
        self.assertEqual(plist["ProgramArguments"], ["/hub/bin/memguard", "report"])
        self.assertEqual(plist["StartCalendarInterval"], {"Weekday": 1, "Hour": 9, "Minute": 0})


class ParseTest(unittest.TestCase):
    def test_parse_free_pct(self):
        out = "The system has 25769803776 (1572864 pages with a page size of 16384).\n\nSystem-wide memory free percentage: 12%\n"
        self.assertEqual(parse_free_pct(out), 12)

    def test_free_pct_bounds_memory_pressure_with_a_timeout(self):
        seen = []

        def run(argv, **kwargs):
            seen.append((argv, kwargs.get("timeout")))
            return SimpleNamespace(stdout="System-wide memory free percentage: 41%\n")

        with mock.patch.object(memguard.subprocess, "run", run):
            self.assertEqual(memguard.free_pct(), 41)
            self.assertEqual(memguard.free_pct(timeout_seconds=2), 41)

        self.assertEqual(seen, [(["memory_pressure"], 5), (["memory_pressure"], 2)])

    def test_parse_top_converts_units_to_mb(self):
        out = "Processes: 900 total\n\nPID    MEM\n72868  6679M\n12     512K\n13     2G\n14     1024B\n"
        self.assertEqual(parse_top(out), {72868: 6679.0, 12: 0.5, 13: 2048.0, 14: 1024 / 1048576})


if __name__ == "__main__":
    unittest.main()
