import unittest

from deezlib.memguard import Proc, launch_agent_plist, parse_free_pct, parse_top, plan

MIN = 60
CLAUDE = Proc(pid=100, ppid=1, age_s=3 * 86400, mem_mb=500, args="claude --resume abc")
DAEMON = Proc(pid=101, ppid=1, age_s=3 * 86400, mem_mb=700, args="bun packages/cli/src/bootstrap.ts run")


def typecheck_job(shell_pid, age_s, tsc_mb, parent=100):
    return [
        Proc(shell_pid, parent, age_s, 2, "/bin/zsh -c eval 'cd x && bun run typecheck'"),
        Proc(shell_pid + 1, shell_pid, age_s, 3, "bun run typecheck"),
        Proc(shell_pid + 2, shell_pid + 1, age_s - 5, 40, "bun scripts/typecheck-cli.ts"),
        Proc(shell_pid + 3, shell_pid + 2, age_s - 10, tsc_mb,
             "node /r/node_modules/typescript/bin/tsc --noEmit -p /tmp/om-cli-typecheck-x/source.json"),
    ]


class PlanTest(unittest.TestCase):
    def test_healthy_memory_and_young_jobs_kill_nothing(self):
        procs = [CLAUDE, DAEMON] + typecheck_job(200, 5 * MIN, 6000)
        self.assertEqual(plan(procs, free_pct=60), [])

    def test_critical_memory_kills_newest_heavy_job_from_its_root(self):
        procs = [CLAUDE, DAEMON] + typecheck_job(200, 20 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        kills = plan(procs, free_pct=10)
        self.assertEqual([k.root for k in kills], [300])
        self.assertEqual(sorted(kills[0].pids), [300, 301, 302, 303])
        self.assertEqual(kills[0].mem_mb, 5045)
        self.assertEqual(kills[0].reason, "memory-critical")

    def test_critical_memory_never_touches_claude_or_daemons(self):
        procs = [CLAUDE, DAEMON]
        self.assertEqual(plan(procs, free_pct=3), [])

    def test_job_running_past_age_limit_is_killed_even_when_memory_is_fine(self):
        procs = [CLAUDE] + typecheck_job(200, 50 * MIN, 6000) + typecheck_job(300, 2 * MIN, 5000)
        kills = plan(procs, free_pct=60)
        self.assertEqual([(k.root, k.reason) for k in kills], [(200, "over-age")])

    def test_orphaned_heavy_job_is_killed(self):
        procs = [CLAUDE, Proc(400, 1, 3 * MIN, 900, "bun test --max-concurrency 4 a.test.ts")]
        kills = plan(procs, free_pct=60)
        self.assertEqual([(k.root, k.reason) for k in kills], [(400, "orphaned")])

    def test_small_jobs_are_ignored(self):
        procs = [CLAUDE, Proc(500, 100, 90 * MIN, 20, "/bin/zsh -c ps -ax | grep typecheck")]
        self.assertEqual(plan(procs, free_pct=5), [])

    def test_other_test_runners_and_builds_count_as_heavy(self):
        for args in ["npx vitest run", "node node_modules/.bin/jest", "bun tools/om-chat-gate.ts regressions",
                     "npx playwright test", "node node_modules/.bin/next build", "bun tools/test-fast.ts"]:
            procs = [CLAUDE, Proc(600, 100, 2 * MIN, 2000, args)]
            self.assertEqual([k.root for k in plan(procs, free_pct=8)], [600], args)

    def test_dev_servers_and_mcp_servers_are_not_heavy(self):
        for args in ["/opt/homebrew/bin/om mcp serve --stdio", "node playwright-mcp", "vite preview --host 127.0.0.1",
                     "bun server.ts", "/opt/homebrew/bin/om run --daemon-internal"]:
            procs = [CLAUDE, Proc(700, 1, 90 * MIN, 3000, args)]
            self.assertEqual(plan(procs, free_pct=5), [], args)


class ParseTest(unittest.TestCase):
    def test_parse_free_pct(self):
        out = "The system has 25769803776 (1572864 pages with a page size of 16384).\n\nSystem-wide memory free percentage: 12%\n"
        self.assertEqual(parse_free_pct(out), 12)

    def test_parse_top_converts_units_to_mb(self):
        out = "Processes: 900 total\n\nPID    MEM\n72868  6679M\n12     512K\n13     2G\n14     1024B\n"
        self.assertEqual(parse_top(out), {72868: 6679.0, 12: 0.5, 13: 2048.0, 14: 1024 / 1048576})


class LaunchAgentTest(unittest.TestCase):
    def test_plist_runs_the_hub_entrypoint_every_30_seconds(self):
        import plistlib
        plist = plistlib.loads(launch_agent_plist("/hub").encode())
        self.assertEqual(plist["Label"], "com.dboon.memguard")
        self.assertEqual(plist["ProgramArguments"], ["/hub/bin/memguard"])
        self.assertEqual(plist["StartInterval"], 30)
        self.assertTrue(plist["RunAtLoad"])


if __name__ == "__main__":
    unittest.main()
