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


if __name__ == "__main__":
    unittest.main()
