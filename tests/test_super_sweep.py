import os
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from deezlib.superclanker import sweep


def lsof_output(*entries):
    return "".join(f"p{pid}\nfcwd\nn{path}\n" for pid, path in entries)


def fake_lsof(stdout, returncode=0):
    def run(argv, **kwargs):
        return SimpleNamespace(returncode=returncode, stdout=stdout, stderr="")
    return run


class LeftoversTest(unittest.TestCase):
    def test_matches_worktree_and_paths_below_it(self):
        run = fake_lsof(lsof_output((11, "/wt/k_1"), (12, "/wt/k_1/src/deep"), (13, "/elsewhere")))

        self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [11, 12])

    def test_sibling_sharing_a_name_prefix_does_not_match(self):
        run = fake_lsof(lsof_output((21, "/wt/k_10"), (22, "/wt/k_1")))

        self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [22])

    def test_own_pid_is_excluded(self):
        run = fake_lsof(lsof_output((os.getpid(), "/wt/k_1"), (31, "/wt/k_1")))

        self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [31])

    def test_private_alias_resolves_equal(self):
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp).resolve()
            alias = str(real).removeprefix("/private") if str(real).startswith("/private") else str(real)
            run = fake_lsof(lsof_output((41, str(real))))

            self.assertEqual(sweep.leftovers(alias, run=run), [41])

    def test_path_that_cannot_be_resolved_is_skipped(self):
        run = fake_lsof(lsof_output((61, "/wt/k_1/loop"), (62, "/wt/k_1/ok")))
        real_resolve = Path.resolve

        def resolve(path, *args, **kwargs):
            if path.name == "loop":
                raise RuntimeError("Symlink loop")
            return real_resolve(path, *args, **kwargs)

        with mock.patch.object(Path, "resolve", resolve):
            self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [62])

    def test_lsof_exiting_one_with_output_still_finds_leftovers(self):
        run = fake_lsof(lsof_output((51, "/wt/k_1")), returncode=1)

        self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [51])

    def test_missing_lsof_yields_nothing(self):
        def run(argv, **kwargs):
            raise FileNotFoundError("lsof")

        self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [])

    def test_lsof_timeout_yields_nothing(self):
        def run(argv, **kwargs):
            raise subprocess.TimeoutExpired(argv, 1)

        self.assertEqual(sweep.leftovers("/wt/k_1", run=run), [])

    def test_lsof_with_no_matches_exiting_one_yields_nothing(self):
        self.assertEqual(sweep.leftovers("/wt/k_1", run=fake_lsof("", returncode=1)), [])


class SweepTest(unittest.TestCase):
    def test_terms_every_leftover_and_returns_them(self):
        gone = set()
        sent = []

        def kill(pid, signum):
            sent.append((pid, signum))
            if signum == signal.SIGTERM:
                gone.add(pid)
            if pid in gone and signum == 0:
                raise ProcessLookupError

        run = fake_lsof(lsof_output((61, "/wt/k_1"), (62, "/wt/k_1/x")))

        swept = sweep.sweep("/wt/k_1", run=run, kill=kill, grace_seconds=1)

        self.assertEqual(swept, [61, 62])
        self.assertIn((61, signal.SIGTERM), sent)
        self.assertNotIn((61, signal.SIGKILL), sent)

    def test_kills_survivors_after_grace(self):
        sent = []

        def kill(pid, signum):
            sent.append((pid, signum))

        run = fake_lsof(lsof_output((71, "/wt/k_1")))

        swept = sweep.sweep("/wt/k_1", run=run, kill=kill, grace_seconds=0)

        self.assertEqual(swept, [71])
        self.assertEqual(sent[0], (71, signal.SIGTERM))
        self.assertEqual(sent[-1], (71, signal.SIGKILL))

    def test_vanished_process_is_ignored(self):
        def kill(pid, signum):
            raise ProcessLookupError

        run = fake_lsof(lsof_output((81, "/wt/k_1")))

        self.assertEqual(sweep.sweep("/wt/k_1", run=run, kill=kill, grace_seconds=0), [81])

    def test_unsignalable_process_is_omitted_without_raising(self):
        sent = []

        def kill(pid, signum):
            sent.append((pid, signum))
            if pid == 91:
                raise PermissionError

        run = fake_lsof(lsof_output((91, "/wt/k_1"), (92, "/wt/k_1/x")))

        swept = sweep.sweep("/wt/k_1", run=run, kill=kill, grace_seconds=0)

        self.assertEqual(swept, [92])
        self.assertIn((92, signal.SIGKILL), sent)

    def test_nothing_to_sweep_returns_empty(self):
        self.assertEqual(sweep.sweep("/wt/k_1", run=fake_lsof(""), grace_seconds=0), [])


class SweepRealProcessTest(unittest.TestCase):
    def test_kills_detached_process_whose_cwd_is_in_the_worktree(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        worktree = Path(tmp.name) / "k_1"
        inside = worktree / "app"
        inside.mkdir(parents=True)
        child = subprocess.Popen(
            ["sleep", "600"], cwd=inside, start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.addCleanup(child.wait)
        self.addCleanup(lambda: child.poll() is None and child.kill())
        deadline = time.monotonic() + 5
        while child.pid not in sweep.leftovers(worktree) and time.monotonic() < deadline:
            time.sleep(0.05)

        swept = sweep.sweep(worktree, grace_seconds=3)

        self.assertIn(child.pid, swept)
        self.assertIsNotNone(child.wait(timeout=5))
