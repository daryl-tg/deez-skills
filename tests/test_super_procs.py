import signal
import subprocess
import unittest
from types import SimpleNamespace

from deezlib.superclanker import procs

TABLE_PS = "  10     1   501  1000 /bin/zsh\n  11    10   501  2000 claude\n  12    11   501  5000 node tsc\n  20     1   501   300 sleep 9\n  30     1     0   100 /usr/sbin/root\ngarbage line\n"


def fake_run(stdout, returncode=0):
    def run(argv, **kwargs):
        return SimpleNamespace(stdout=stdout, returncode=returncode)
    return run


def raising(exc):
    def run(argv, **kwargs):
        raise exc()
    return run


class TableTest(unittest.TestCase):
    def test_read_table_parses_and_skips_garbage(self):
        table = procs.read_table(run=fake_run(TABLE_PS))
        self.assertEqual(sorted(table), [10, 11, 12, 20, 30])
        self.assertEqual(table[12], procs.Proc(12, 11, 501, 5000, "node tsc"))

    def test_read_table_failure_is_empty(self):
        self.assertEqual(procs.read_table(run=raising(OSError)), {})
        self.assertEqual(procs.read_table(run=fake_run("", returncode=1)), {})

    def test_subtree_and_rss(self):
        table = procs.read_table(run=fake_run(TABLE_PS))
        self.assertEqual(procs.subtree(table, 10), {10, 11, 12})
        self.assertEqual(procs.tree_rss_kb(table, {10, 11, 12}), 8000)
        self.assertEqual(procs.subtree(table, 999), set())

    def test_attribute_counts_each_pid_once_worker_first(self):
        table = procs.read_table(run=fake_run(TABLE_PS))
        got = procs.attribute(table, {"k_1": [11]}, {"peer-a": 10})
        self.assertEqual(got.workers, {"k_1": {11, 12}})
        self.assertEqual(got.peers, {"peer-a": {10}})
        self.assertEqual(got.other, {20, 30})

    def test_child_trees_sorted_by_rss(self):
        table = procs.read_table(run=fake_run(TABLE_PS))
        self.assertEqual(procs.child_trees(table, 10), [(11, 7000, "claude")])

    def test_top_trees(self):
        table = procs.read_table(run=fake_run(TABLE_PS))
        self.assertEqual([pid for pid, _, _ in procs.top_trees(table, n=2)], [10, 20])


def table_of(*procs_):
    return {proc.pid: proc for proc in procs_}


PEER_TABLE = table_of(
    procs.Proc(1, 0, 0, 10, "launchd"),
    procs.Proc(10, 1, 501, 100, "tmux"),
    procs.Proc(11, 10, 501, 100, "python board"),
    procs.Proc(40, 1, 501, 100, "python x super-clanker daemon"),
    procs.Proc(41, 1, 501, 100, "python x super-clanker watchdog"),
    procs.Proc(70, 1, 501, 100, "claude peer"),
    procs.Proc(71, 70, 501, 100, "node child"),
    procs.Proc(72, 71, 501, 100, "grandchild"),
    procs.Proc(80, 1, 0, 100, "rootowned"),
    procs.Proc(90, 1, 501, 100, "worker claude"),
)


class ProtectionTest(unittest.TestCase):
    def test_protected_includes_own_ancestors_main_listeners_and_daemon(self):
        table = table_of(
            procs.Proc(1, 0, 0, 10, "launchd"),
            procs.Proc(10, 1, 501, 100, "tmux"),
            procs.Proc(11, 10, 501, 100, "python board"),
            procs.Proc(40, 1, 501, 100, "python x super-clanker daemon"),
        )
        got = procs.protected(table, 11, {50}, {60})
        self.assertTrue({1, 10, 11, 40, 50, 60} <= got)

    def test_kill_refusal_reasons(self):
        protected = procs.protected(PEER_TABLE, 11, set(), set())
        def refusal(target):
            return procs.kill_refusal(PEER_TABLE, target, protected, 501, {90})
        self.assertEqual(refusal(999), "not running")
        self.assertEqual(refusal(1), "system process")
        self.assertEqual(refusal(80), "another user's process")
        self.assertEqual(refusal(90), "Worker: use k")
        self.assertEqual(refusal(40), "protected")
        self.assertIsNone(refusal(71))

    def test_kill_refuses_tree_containing_protected(self):
        self.assertEqual(
            procs.kill_refusal(PEER_TABLE, 70, {72}, 501, set()), "protected",
        )

    def test_port_listeners_and_main_session_tolerate_failure(self):
        self.assertEqual(procs.port_listeners(run=raising(OSError)), set())
        self.assertEqual(procs.main_session_pids(PEER_TABLE, run=raising(OSError)), set())

    def test_port_listeners_collects_pids_per_port(self):
        calls = []
        def run(argv, **kwargs):
            calls.append(argv)
            return SimpleNamespace(stdout="77\n78\n", returncode=0)
        self.assertEqual(procs.port_listeners(run=run), {77, 78})
        self.assertEqual(
            [argv[2] for argv in calls],
            [f"-iTCP:{port}" for port in procs.PROTECTED_PORTS],
        )
        self.assertTrue(all(argv[0] == procs.LSOF for argv in calls))

    def test_main_session_pids_are_pane_subtrees(self):
        run = fake_run("70\n")
        self.assertEqual(procs.main_session_pids(PEER_TABLE, run=run), {70, 71, 72})


class KillTreeTest(unittest.TestCase):
    def setUp(self):
        self.target = PEER_TABLE[70]

    def test_kill_refuses_when_pid_was_reused(self):
        reused = table_of(procs.Proc(70, 1, 501, 100, "something else"))
        sent = []
        got = procs.kill_tree(
            self.target, read=lambda: reused,
            kill=lambda pid, sig: sent.append((pid, sig)),
        )
        self.assertEqual(got, [])
        self.assertEqual(sent, [])

    def test_kill_terms_then_kills_survivors(self):
        sent = []
        clock = {"now": 0.0}
        stubborn = {71}
        def kill(pid, sig):
            sent.append((pid, sig))
            if sig == signal.SIGKILL:
                stubborn.discard(pid)
            elif sig == 0 and pid not in stubborn:
                raise ProcessLookupError
        def sleep(seconds):
            clock["now"] += seconds
        got = procs.kill_tree(
            self.target, read=lambda: PEER_TABLE, kill=kill, sleep=sleep,
            clock=lambda: clock["now"], grace_seconds=3,
        )
        self.assertEqual(sorted(got), [70, 71, 72])
        terms = [pid for pid, sig in sent if sig == signal.SIGTERM]
        self.assertEqual(terms, [72, 71, 70])
        kills = [pid for pid, sig in sent if sig == signal.SIGKILL]
        self.assertEqual(kills, [71])
        self.assertGreaterEqual(clock["now"], 3)

    def test_permission_error_pid_is_skipped(self):
        def kill(pid, sig):
            if pid == 72:
                raise PermissionError
            if sig == 0:
                raise ProcessLookupError
        got = procs.kill_tree(
            self.target, read=lambda: PEER_TABLE, kill=kill,
            sleep=lambda s: None, grace_seconds=0,
        )
        self.assertEqual(sorted(got), [70, 71])

    def test_kill_tree_real_process(self):
        child = subprocess.Popen(["/bin/sleep", "600"], start_new_session=True)
        self.addCleanup(lambda: (child.kill(), child.wait()))
        target = procs.read_table()[child.pid]
        got = procs.kill_tree(target, grace_seconds=3)
        self.assertIn(child.pid, got)
        child.wait(timeout=5)
        self.assertIsNotNone(child.returncode)


if __name__ == "__main__":
    unittest.main()
