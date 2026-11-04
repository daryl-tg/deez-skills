import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from functools import partial
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli, memguard
from deezlib.superclanker import config, daemon, router, workers
from deezlib.superclanker import sweep as sweeping
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.sources import terminal
from deezlib.superclanker.store import Store, SuperError

HUB = cli.REPO_ROOT


def dead_pid():
    process = subprocess.Popen(["true"])
    process.wait()
    return process.pid


def shifted(stamp, seconds):
    moved = datetime.fromisoformat(stamp) + timedelta(seconds=seconds)
    return moved.isoformat(timespec="seconds")


class FakeWake:
    def __init__(self, during=None):
        self.batches = []
        self.during = during

    def __call__(self, store, settings, root, hub_root):
        ids = [trigger.id for trigger, _verdict in router.triage(store, settings).router_items]
        self.batches.append(ids)
        wake_id = store.begin_wake(ids)
        if self.during:
            self.during(len(self.batches))
        for trigger_id_ in ids:
            store.ignore(trigger_id_, "decided by fake router")
        store.end_wake(wake_id, 0, 0.0, "session", "ok")
        return router.WakeResult(wake_id, len(ids), len(ids), 0, 0.0, "ok")


class FakeWorkers:
    def __init__(self, fail=()):
        self.launched = []
        self.resumed = []
        self.revived = []
        self.fail = fail

    def launch(self, store, settings, assignment_id, hub_root, root):
        self.launched.append(assignment_id)
        if assignment_id in self.fail:
            raise SuperError(f"cannot launch {assignment_id}")
        return store.start_assignment(assignment_id, "session", os.getpid(), root)

    def resume(self, store, settings, assignment_id, hub_root, root):
        self.resumed.append(assignment_id)
        return store.start_assignment(assignment_id, "session", os.getpid(), root)

    def revive(self, store, settings, ticket_id, hub_root, root):
        self.revived.append(ticket_id)


def no_reap(store, root):
    return []


def plenty_free():
    return 100


class FakeStop:
    def __init__(self):
        self.calls = []

    def __call__(self, store, assignment_id, **kwargs):
        self.calls.append((assignment_id, kwargs))


class FakeTerminate:
    def __init__(self, order=None):
        self.terminated = []
        self.order = order

    def __call__(self, assignment):
        self.terminated.append(assignment.id)
        if self.order is not None:
            self.order.append("terminate")


def nothing_left(worktree):
    return []


def left_by(*pids):
    return lambda worktree: list(pids)


class FakeSweeper:
    def __init__(self):
        self.swept = []

    def __call__(self, worktree):
        self.swept.append(Path(worktree))
        return []


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


class DaemonTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "state"
        patcher = mock.patch.dict(
            os.environ, {"USER": "daryl", "DEEZ_SUPER_STATE": str(self.root)}
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        free = mock.patch.object(memguard, "free_pct", plenty_free)
        free.start()
        self.addCleanup(free.stop)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        self.wake = FakeWake()
        self.workers = FakeWorkers()
        self.sweeper = FakeSweeper()
        self.blocked = {}

    def sources(self, text):
        (self.root / "sources.toml").write_text(text, encoding="utf-8")

    def one_pass(self, wake=None, reap=no_reap, revive=None, stop=None, free_pct=plenty_free,
                 sweeper=None, git=None, leftovers=nothing_left, terminate=None, **now):
        return daemon.one_pass(
            self.store, config.load(self.root), self.root, HUB, wake=wake or self.wake,
            launch=self.workers.launch, resume=self.workers.resume,
            revive=revive or self.workers.revive, reap=reap, stop=stop or FakeStop(),
            free_pct=free_pct, sweeper=sweeper or self.sweeper,
            blocked=self.blocked, leftovers=leftovers, terminate=terminate or FakeTerminate(),
            **({} if git is None else {"git": git}), **now,
        )

    def repo_with_worktree(self, ticket):
        repo = self.root.parent / "repo"
        if not repo.exists():
            repo.mkdir()
            git(repo, "init", "-q", "-b", "main")
            git(repo, "config", "user.name", "tester")
            git(repo, "config", "user.email", "tester@example.com")
            (repo / "file.txt").write_text("one\n", encoding="utf-8")
            git(repo, "add", "file.txt")
            git(repo, "commit", "-q", "-m", "first")
        worktree = self.root / "worktrees" / repo.name / ticket.id
        worktree.parent.mkdir(parents=True, exist_ok=True)
        git(repo, "worktree", "add", "-q", "-b", f"daryl/{ticket.slug}", str(worktree))
        return repo, worktree

    def ask(self, text, thread="default"):
        trigger, _receipt = terminal.ask(self.store, text, thread_name=thread)
        return trigger

    def forge(self, text, number=1, event=None):
        self.sources('[sources.github]\nenabled = true\nmode = "explicit-only"\nsenders = ["daryl-tg"]\n')
        event = event or f"pr{number}-{len(self.store.queued())}-{text[:8]}"
        trigger = Trigger(
            trigger_id("github", event), "github", event, f"github:dboon/x#{number}", "daryl-tg", True,
            text, None, "2026-11-02T10:00:00+00:00", {},
        )
        self.store.receive(trigger)
        return trigger

    def forge_ticket(self, text, number=1):
        opened = self.forge(text, number, event=f"open-{number}")
        ticket = self.store.accept(opened.id, f"slug-{number}", Strength.explicit, "x", [], "p1", "asked")
        return ticket, self.store.assignment_for(ticket.id).id

    def ticket(self, text, thread="default"):
        trigger = self.ask(text, thread)
        ticket = self.store.accept(
            trigger.id, f"slug-{thread}", Strength.explicit, thread, [], "p1", "asked"
        )
        return ticket, self.store.assignment_for(ticket.id).id

    def inbox(self, name="default"):
        return self.root / "inbox" / f"terminal-{name}.log"

    def failing_wake(self):
        ended = []

        def wake(store, settings, root, hub_root):
            ids = [trigger.id for trigger, _verdict in router.triage(store, settings).router_items]
            wake_id = store.begin_wake(ids)
            store.end_wake(wake_id, 1, None, None, "boom")
            ended.append(store.show(wake_id)["ended_at"])
            raise SuperError(f"router wake {wake_id} failed with exit 1")

        return wake, ended

    def test_second_pass_with_no_new_triggers_does_not_wake(self):
        asked = self.ask("ping")
        first = self.one_pass()
        second = self.one_pass()
        self.assertEqual(self.wake.batches, [[asked.id]])
        self.assertTrue(first.wake_id.startswith("w_"))
        self.assertEqual(second, daemon.PassResult(0, 0, 0, 0, None, 0, ()))

    def test_triggers_during_wake_batch_into_next_wake(self):
        arrivals = []

        def arrive(wake_number):
            if wake_number == 1:
                arrivals.append(self.ask("and also this"))

        self.wake = FakeWake(during=arrive)
        first = self.ask("ping")
        self.one_pass()
        self.one_pass()
        self.one_pass()
        self.assertEqual(self.wake.batches, [[first.id], [arrivals[0].id]])

    def test_terminal_ask_reaches_the_router_while_a_terminal_ticket_is_open(self):
        ticket, assignment_id = self.ticket("fix the typo")
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root)
        new_task = self.ask("start something else")
        result = self.one_pass()
        self.assertEqual(result.fanned_out, 0)
        self.assertEqual(self.wake.batches, [[new_task.id]])
        self.assertEqual(self.store.undelivered_inputs(ticket.id), [])
        self.assertEqual(self.workers.resumed, [])

    def test_fanout_records_input_and_resumes_idle_worker(self):
        ticket, assignment_id = self.forge_ticket("fix the typo")
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root)
        follow_up = self.forge("also the second typo")
        result = self.one_pass()
        inputs = self.store.undelivered_inputs(ticket.id)
        self.assertEqual(result.fanned_out, 1)
        self.assertEqual(
            [(entry.kind, entry.text) for entry in inputs], [("trigger", follow_up.id)]
        )
        self.assertEqual(self.workers.resumed, [assignment_id])
        self.assertEqual(result.resumed, 1)
        self.assertEqual(self.wake.batches, [])
        self.assertEqual(self.store.queued(), [])

    def test_pass_revives_ended_ticket_with_new_input(self):
        tmp = Path(self.root).parent
        bin_dir = tmp / "bin"
        bin_dir.mkdir()
        shutil.copy(Path(__file__).with_name("fake_claude.py"), bin_dir / "claude")
        (bin_dir / "claude").chmod(0o755)
        argv_log = tmp / "argv.jsonl"
        os.environ.update({
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_CLAUDE_LOG": str(argv_log),
        })
        ticket, assignment_id = self.forge_ticket("fix the typo")
        self.store.start_assignment(assignment_id, "sid-1", dead_pid(), self.root)
        self.store.report(assignment_id, "ready", "fixed it")
        stopped, stopped_assignment = self.ticket("tidy the changelog", "other")
        self.store.stop(stopped.id, "daryl", "not needed")
        self.store.add_input(stopped.id, "note", "late fact")
        follow_up = self.forge("the second typo is still there")

        result = self.one_pass(revive=workers.revive)

        revived = self.store.assignment_for(ticket.id)
        deadline = time.monotonic() + 2
        while workers.alive(revived.pid):
            self.assertLess(time.monotonic(), deadline, "fake worker did not exit")
            time.sleep(0.01)
        self.assertEqual((result.fanned_out, result.resumed, result.errors), (1, 1, ()))
        self.assertNotEqual(revived.id, assignment_id)
        self.assertEqual((revived.state, revived.session_id), ("running", "sid-1"))
        workers_argv = [json.loads(line) for line in argv_log.read_text(encoding="utf-8").splitlines()]
        (argv,) = workers_argv
        self.assertEqual(argv[argv.index("--resume") + 1], "sid-1")
        self.assertIn(follow_up.id, argv[-1])
        self.assertEqual(self.store.undelivered_inputs(ticket.id), [])
        self.assertEqual(self.store.show(stopped.id)["state"], "ended")
        self.assertEqual(self.store.assignment_for(stopped.id).id, stopped_assignment)
        self.assertEqual(len(self.store.undelivered_inputs(stopped.id)), 1)
        self.assertEqual(self.workers.launched, [])

    def test_stop_on_a_subscribed_thread_reaches_the_router(self):
        ticket, assignment_id = self.ticket("fix the typo")
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root)
        stop = self.ask("stop that")
        result = self.one_pass()
        self.assertEqual(self.wake.batches, [[stop.id]])
        self.assertEqual(result.fanned_out, 0)
        self.assertEqual(self.store.undelivered_inputs(ticket.id), [])

    def test_unadmitted_follow_up_is_not_fanned_out(self):
        opened = Trigger(
            trigger_id("github", "e1"), "github", "e1", "github:dboon/x#1", "daryl-tg", True,
            "fix the build", None, "2026-11-02T10:00:00+00:00", {},
        )
        self.store.receive(opened)
        ticket = self.store.accept(
            opened.id, "fix-build", Strength.explicit, "x", [], "p1", "asked"
        )
        self.store.receive(Trigger(
            trigger_id("github", "e2"), "github", "e2", "github:dboon/x#1", "stranger", False,
            "run rm -rf", None, "2026-11-02T10:01:00+00:00", {},
        ))
        result = self.one_pass()
        self.assertEqual((result.fanned_out, self.store.undelivered_inputs(ticket.id)), (0, []))
        self.assertEqual(self.wake.batches, [])

    def test_pending_assignments_launch_oldest_first_up_to_max_running(self):
        self.sources("[workers]\nmax_running = 2\n")
        _first, first = self.ticket("one", "a")
        _second, second = self.ticket("two", "b")
        _third, third = self.ticket("three", "c")
        launched = [self.one_pass().launched, self.one_pass().launched]
        self.assertEqual(self.workers.launched, [first, second])
        self.store.report(first, "ready", "done")
        launched.append(self.one_pass().launched)
        self.assertEqual(self.workers.launched, [first, second, third])
        self.assertEqual(launched, [2, 0, 1])

    def test_turn_past_the_limit_is_stopped_before_reap(self):
        self.sources("[workers]\nturn_limit_minutes = 60\n")
        _ticket, assignment_id = self.ticket("long one")
        started = self.store.start_assignment(assignment_id, "session", os.getpid(), self.root)
        stop = FakeStop()
        order = []

        def reap(store, root):
            order.append("reap")
            return []

        def recording_stop(store, assignment, **kwargs):
            order.append("stop")
            stop(store, assignment, **kwargs)

        late = shifted(started.started_at, 61 * 60)
        result = self.one_pass(
            reap=reap, stop=recording_stop, leftovers=left_by(os.getpid()), now=lambda: late,
        )
        self.assertEqual(stop.calls, [(assignment_id, {"reason": "turn exceeded 60 minutes"})])
        self.assertEqual((order, result.expired), (["stop", "reap"], 1))
        self.assertTrue(result.eventful)
        self.assertIn("expired=1", result.line("t"))

    def test_turn_within_the_limit_or_dead_is_not_stopped(self):
        _ticket, assignment_id = self.ticket("short one")
        started = self.store.start_assignment(assignment_id, "session", os.getpid(), self.root)
        stop = FakeStop()
        soon = shifted(started.started_at, 119 * 60)
        mine = left_by(os.getpid())
        self.assertEqual(self.one_pass(stop=stop, leftovers=mine, now=lambda: soon).expired, 0)
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root)
        late = shifted(started.started_at, 500 * 60)
        self.assertEqual(self.one_pass(stop=stop, leftovers=mine, now=lambda: late).expired, 0)
        self.assertEqual(stop.calls, [])

    def test_over_limit_pid_whose_cwd_left_the_worktree_is_not_stopped(self):
        _ticket, assignment_id = self.ticket("reused pid")
        started = self.store.start_assignment(assignment_id, "session", os.getpid(), self.root)
        stop = FakeStop()
        seen = []

        def leftovers(worktree):
            seen.append(Path(worktree))
            return [os.getpid() + 1]

        late = shifted(started.started_at, 500 * 60)
        result = self.one_pass(stop=stop, leftovers=leftovers, now=lambda: late)
        self.assertEqual((stop.calls, result.expired, result.errors), ([], 0, ()))
        self.assertEqual(seen, [self.root])

    def test_unsignalable_over_limit_worker_is_recorded_not_raised(self):
        _ticket, assignment_id = self.ticket("foreign pid")
        _other, other_id = self.ticket("second over limit", "other")
        started = self.store.start_assignment(assignment_id, "session", os.getpid(), self.root)
        self.store.start_assignment(other_id, "session", os.getpid(), self.root)
        refused = []

        def refuse(pid, signum):
            refused.append(pid)
            raise PermissionError(1, "Operation not permitted")

        late = shifted(started.started_at, 500 * 60)
        result = self.one_pass(
            stop=partial(workers.stop, kill=refuse, sweep=nothing_left),
            leftovers=left_by(os.getpid()), now=lambda: late,
        )
        self.assertEqual((result.expired, len(result.errors)), (0, 2))
        self.assertIn(str(os.getpid()), result.errors[0])
        self.assertEqual(refused.count(-os.getpid()), 2)
        self.assertTrue((self.root / "daemon.heartbeat").exists())

    def test_stopped_ticket_live_worker_is_terminated_before_its_worktree_is_removed(self):
        ticket, assignment_id = self.ticket("stopped while running")
        _repo, worktree = self.repo_with_worktree(ticket)
        self.store.start_assignment(assignment_id, "session", os.getpid(), worktree)
        self.store.stop(ticket.id, "router", "not needed")
        order = []
        terminate = FakeTerminate(order)

        def sweeper(path):
            order.append("remove")
            return []

        result = self.one_pass(
            terminate=terminate, sweeper=sweeper, leftovers=left_by(os.getpid()),
        )
        self.assertEqual(terminate.terminated, [assignment_id])
        self.assertEqual((order, result.removed, result.errors), (["terminate", "remove"], 1, ()))

    def test_stopped_ticket_worker_outside_its_worktree_is_untouched(self):
        ticket, assignment_id = self.ticket("stopped elsewhere")
        self.store.start_assignment(assignment_id, "session", os.getpid(), self.root / "work" / ticket.id)
        self.store.stop(ticket.id, "router", "not needed")
        terminate = FakeTerminate()
        result = self.one_pass(terminate=terminate, leftovers=left_by(os.getpid() + 1))
        self.assertEqual((terminate.terminated, result.errors), ([], ()))

    def test_stopped_ticket_with_dead_or_reaped_worker_is_not_inspected(self):
        ticket, assignment_id = self.ticket("long gone")
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root / "work" / ticket.id)
        _later, reaped_id = self.ticket("reaped already", "other")
        self.store.start_assignment(reaped_id, "session", os.getpid(), self.root / "work" / "k_x")
        (self.root / "log").mkdir(parents=True, exist_ok=True)
        (self.root / "log" / f"{reaped_id}.json").write_text("{}", encoding="utf-8")
        (self.root / "log" / f"{reaped_id}.reaped").write_text("", encoding="utf-8")
        for row in self.store.status():
            self.store.stop(row["ticket"], "router", "not needed")
        seen = []

        def leftovers(worktree):
            seen.append(worktree)
            return [os.getpid()]

        terminate = FakeTerminate()
        self.one_pass(terminate=terminate, leftovers=leftovers)
        self.assertEqual((terminate.terminated, seen), ([], []))

    def test_failed_termination_of_a_stopped_worker_is_recorded_not_raised(self):
        ticket, assignment_id = self.ticket("stubborn")
        self.store.start_assignment(assignment_id, "session", os.getpid(), self.root / "work" / ticket.id)
        self.store.stop(ticket.id, "router", "not needed")

        def terminate(assignment):
            raise SuperError(f"cannot signal worker pid {assignment.pid}")

        result = self.one_pass(terminate=terminate, leftovers=left_by(os.getpid()))
        self.assertEqual(result.errors, (f"cannot signal worker pid {os.getpid()}",))
        self.assertTrue((self.root / "daemon.heartbeat").exists())

    def test_stopped_scratch_ticket_worker_process_is_killed_once(self):
        ticket, assignment_id = self.ticket("scratch work")
        scratch = self.root / "work" / ticket.id
        scratch.mkdir(parents=True)
        child = subprocess.Popen(
            ["sleep", "600"], cwd=scratch, start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.addCleanup(child.wait)
        self.addCleanup(lambda: child.poll() is None and child.kill())
        deadline = time.monotonic() + 5
        while child.pid not in sweeping.leftovers(scratch) and time.monotonic() < deadline:
            time.sleep(0.05)
        self.store.start_assignment(assignment_id, "session", child.pid, scratch)
        self.store.stop(ticket.id, "router", "not needed")
        calls = []

        def terminate(assignment):
            calls.append(assignment.id)
            workers.terminate(assignment, grace_seconds=1)

        self.one_pass(terminate=terminate, leftovers=sweeping.leftovers)
        self.assertIsNotNone(child.wait(timeout=5))
        self.one_pass(terminate=terminate, leftovers=sweeping.leftovers)
        self.assertEqual(calls, [assignment_id])

    def test_pending_assignment_is_held_below_the_free_memory_threshold(self):
        _ticket, assignment_id = self.ticket("heavy")
        result = self.one_pass(free_pct=lambda: 10)
        self.assertEqual((self.workers.launched, result.launched, result.held), ([], 0, 10))
        self.assertIn("held=mem10%", result.line("t"))
        self.assertTrue(result.eventful)
        again = self.one_pass(free_pct=lambda: 10)
        self.assertEqual(again.held, 10)
        self.assertFalse(again.eventful)
        released = self.one_pass(free_pct=lambda: 50)
        self.assertEqual((self.workers.launched, released.held), ([assignment_id], None))
        self.assertNotIn("held=", released.line("t"))

    def test_ended_ticket_worktree_is_swept_and_removed_but_branch_is_kept(self):
        ticket, _assignment_id = self.ticket("finished")
        repo, worktree = self.repo_with_worktree(ticket)
        self.store.stop(ticket.id, "daryl", "done")
        result = self.one_pass()
        self.assertFalse(worktree.exists())
        self.assertIn(f"daryl/{ticket.slug}", git(repo, "branch", "--list", f"daryl/{ticket.slug}"))
        self.assertEqual((result.removed, result.errors, self.sweeper.swept), (1, (), [worktree]))
        self.assertTrue(result.eventful)
        self.assertIn(" removed=1 ", result.line("t"))
        self.assertEqual(self.one_pass().removed, 0)

    def test_dirty_worktree_of_ended_ticket_is_kept_and_reported(self):
        ticket, _assignment_id = self.ticket("dirty")
        _repo, worktree = self.repo_with_worktree(ticket)
        (worktree / "scratch.txt").write_text("unsaved\n", encoding="utf-8")
        (worktree / "file.txt").write_text("changed\n", encoding="utf-8")
        self.store.stop(ticket.id, "daryl", "done")
        result = self.one_pass()
        self.assertTrue(worktree.exists())
        self.assertEqual((result.removed, len(result.errors), self.sweeper.swept), (0, 1, []))
        self.assertIn(str(worktree), result.errors[0])

    def test_dropped_ticket_worktree_is_kept_for_revival(self):
        ticket, _assignment_id = self.ticket("dropped")
        _repo, worktree = self.repo_with_worktree(ticket)
        self.store.end_ticket(ticket.id, "dropped")
        result = self.one_pass()
        self.assertTrue(worktree.exists())
        self.assertEqual((result.removed, result.errors, self.sweeper.swept), (0, (), []))

    def test_failed_removal_is_retried_only_after_ten_minutes(self):
        ticket, _assignment_id = self.ticket("dirty")
        _repo, worktree = self.repo_with_worktree(ticket)
        (worktree / "file.txt").write_text("changed\n", encoding="utf-8")
        self.store.stop(ticket.id, "daryl", "done")
        first = self.one_pass()
        second = self.one_pass()
        later = shifted(daemon.utc_now(), 601)
        third = self.one_pass(now=lambda: later)
        self.assertEqual((len(first.errors), len(second.errors), len(third.errors)), (1, 0, 1))
        self.assertEqual(self.sweeper.swept, [])

    def test_at_most_two_worktrees_are_removed_per_pass(self):
        worktrees = []
        for name in ("a", "b", "c"):
            ticket, _assignment_id = self.ticket(f"finished {name}", name)
            worktrees.append(self.repo_with_worktree(ticket)[1])
            self.store.stop(ticket.id, "daryl", "done")
        first = self.one_pass()
        self.assertEqual((first.removed, sum(path.exists() for path in worktrees)), (2, 1))
        self.assertEqual(self.one_pass().removed, 1)

    def test_worktree_entry_that_cannot_be_resolved_is_skipped(self):
        ticket, _assignment_id = self.ticket("looped")
        _repo, worktree = self.repo_with_worktree(ticket)
        self.store.stop(ticket.id, "daryl", "done")
        real_resolve = Path.resolve

        def resolve(path, *args, **kwargs):
            if path.name == ticket.id:
                raise RuntimeError("Symlink loop")
            return real_resolve(path, *args, **kwargs)

        with mock.patch.object(Path, "resolve", resolve):
            result = self.one_pass()
        self.assertEqual((result.removed, result.errors, self.sweeper.swept), (0, (), []))
        self.assertTrue(worktree.exists())

    def test_symlinked_worktree_entry_is_neither_swept_nor_removed(self):
        ticket, _assignment_id = self.ticket("linked")
        outside = self.root.parent / "elsewhere"
        outside.mkdir()
        link = self.root / "worktrees" / "repo" / ticket.id
        link.parent.mkdir(parents=True)
        link.symlink_to(outside)
        self.store.stop(ticket.id, "daryl", "done")
        result = self.one_pass()
        self.assertEqual((result.removed, result.errors, self.sweeper.swept), (0, (), []))
        self.assertTrue(outside.exists())

    def test_non_git_worktree_directory_is_not_swept(self):
        ticket, _assignment_id = self.ticket("plain")
        plain = self.root / "worktrees" / "repo" / ticket.id
        plain.mkdir(parents=True)
        self.store.stop(ticket.id, "daryl", "done")
        result = self.one_pass()
        self.assertEqual((result.removed, len(result.errors), self.sweeper.swept), (0, 1, []))

    def test_git_timeout_lands_in_errors(self):
        ticket, _assignment_id = self.ticket("slow")
        _repo, worktree = self.repo_with_worktree(ticket)
        self.store.stop(ticket.id, "daryl", "done")
        seen = []

        def slow_git(argv, **kwargs):
            seen.append(kwargs.get("timeout"))
            raise subprocess.TimeoutExpired(argv, kwargs.get("timeout"))

        result = self.one_pass(git=slow_git)
        self.assertEqual((result.removed, len(result.errors)), (0, 1))
        self.assertTrue(worktree.exists())
        self.assertEqual(seen, [10])

    def test_open_ticket_worktree_is_untouched(self):
        ticket, _assignment_id = self.ticket("still going")
        _repo, worktree = self.repo_with_worktree(ticket)
        result = self.one_pass()
        self.assertTrue(worktree.exists())
        self.assertEqual((result.removed, result.errors, self.sweeper.swept), (0, (), []))

    def test_hold_clearing_is_eventful_once(self):
        self.one_pass(free_pct=lambda: 10)
        cleared = self.one_pass(free_pct=lambda: 50)
        self.assertTrue(cleared.eventful)
        self.assertFalse(self.one_pass(free_pct=lambda: 50).eventful)

    def test_held_pass_skips_resume_and_revive(self):
        ticket, assignment_id = self.ticket("busy")
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root)
        self.store.add_input(ticket.id, "trigger", self.ask("more", "default").id)
        self.one_pass(free_pct=lambda: 10)
        self.assertEqual((self.workers.resumed, self.workers.revived), ([], []))

    def test_free_memory_read_failure_does_not_block_launch(self):
        _ticket, assignment_id = self.ticket("unknown memory")

        def broken():
            raise OSError("no memory_pressure")

        result = self.one_pass(free_pct=broken)
        self.assertEqual((self.workers.launched, result.held), ([assignment_id], None))

    def test_reaped_report_is_in_the_next_wake_batch(self):
        ticket, assignment_id = self.ticket("fix the typo")
        self.store.start_assignment(assignment_id, "session", dead_pid(), self.root)
        log = self.root / "log" / f"{assignment_id}.json"
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(json.dumps({"result": "REPORT ready fixed both typos"}), encoding="utf-8")
        result = self.one_pass(reap=workers.reap)
        self.assertEqual(result.reaped, 1)
        [batch] = self.wake.batches
        reported = self.store.show(batch[0])
        self.assertEqual(
            (len(batch), reported["thread_id"], reported["text"]),
            (1, f"worker:{ticket.id}", "REPORT ready fixed both typos"),
        )

    def test_inflight_wake_blocks_until_expired(self):
        self.ask("ping")
        stuck = self.store.begin_wake([])
        started = self.store.show(stuck)["started_at"]
        blocked = self.one_pass(now=lambda: shifted(started, 60))
        self.assertEqual((blocked.wake_id, self.wake.batches), (None, []))
        late = shifted(started, router.WAKE_TIMEOUT_SECONDS + 1)
        woken = self.one_pass(now=lambda: late)
        expired = self.store.show(stuck)
        self.assertEqual(len(self.wake.batches), 1)
        self.assertTrue(woken.wake_id.startswith("w_"))
        self.assertEqual((expired["exit_code"], expired["result"]), (None, "expired by daemon"))
        self.assertIsNotNone(expired["ended_at"])
        self.assertIsNone(self.store.inflight_wake())

    def test_launch_error_is_recorded_not_raised(self):
        _first, first = self.ticket("one", "a")
        _second, second = self.ticket("two", "b")
        self.workers = FakeWorkers(fail=(first,))
        result = self.one_pass()
        self.assertEqual(self.workers.launched, [first, second])
        self.assertEqual((result.launched, result.errors), (1, (f"cannot launch {first}",)))

    def test_wake_error_is_recorded_not_raised(self):
        self.ask("ping")

        def failing_wake(store, settings, root, hub_root):
            raise SuperError("router wake w_x failed with exit 1")

        result = self.one_pass(wake=failing_wake)
        self.assertEqual(
            (result.wake_id, result.errors), (None, ("router wake w_x failed with exit 1",))
        )

    def test_failed_wake_backs_off_then_retries(self):
        asked = self.ask("ping")
        failing, ended = self.failing_wake()

        first = self.one_pass(wake=failing)
        held = self.one_pass(wake=failing, now=lambda: shifted(ended[0], 29))
        self.assertEqual(len(ended), 1)
        self.assertEqual((first.wake_id, len(first.errors)), (None, 1))
        self.assertEqual((held.wake_id, held.errors, held.eventful), ("backoff", (), False))
        self.assertIn(" wake=backoff ", held.line("2026-11-02T10:00:00+00:00"))

        retried = self.one_pass(wake=failing, now=lambda: shifted(ended[0], 31))
        self.assertEqual((retried.wake_id, len(ended)), (None, 2))

        held_longer = self.one_pass(now=lambda: shifted(ended[1], 59))
        woken = self.one_pass(now=lambda: shifted(ended[1], 61))
        self.assertEqual(held_longer.wake_id, "backoff")
        self.assertTrue(woken.wake_id.startswith("w_"))
        self.assertEqual(self.wake.batches, [[asked.id]])

    def test_successful_wake_resets_backoff(self):
        first = self.ask("ping")
        failing, ended = self.failing_wake()
        self.one_pass(wake=failing)

        recovered = self.one_pass(now=lambda: shifted(ended[0], 31))
        second = self.ask("ping again", thread="other")
        again = self.one_pass(now=lambda: shifted(ended[0], 32))

        self.assertTrue(recovered.wake_id.startswith("w_"))
        self.assertTrue(again.wake_id.startswith("w_"))
        self.assertEqual(self.wake.batches, [[first.id], [second.id]])

    def test_terminal_reply_lands_in_inbox_and_is_marked_sent(self):
        asked = self.ask("ping")
        self.store.ignore(asked.id, "answered inline")
        github = Trigger(
            trigger_id("github", "e1"), "github", "e1", "github:dboon/x#1", "dboon", True,
            "hi", None, "2026-11-02T10:00:00+00:00", {},
        )
        self.store.receive(github)
        self.store.ignore(github.id, "not for us")
        pong = self.store.reply("terminal:default", "pong")
        elsewhere = self.store.reply("github:dboon/x#1", "later")
        first = self.one_pass()
        second = self.one_pass()
        self.assertEqual(self.inbox().read_text(encoding="utf-8"), f"{pong.created_at}  pong\n")
        self.assertEqual([reply.id for reply in self.store.unsent_replies()], [elsewhere.id])
        self.assertEqual((first.replies_sent, second.replies_sent), (1, 0))

    def run_daemon(self, passes=1):
        slept = []
        out = StringIO()
        with redirect_stdout(out):
            code = daemon.run(self.root, HUB, passes=passes, sleep=slept.append)
        return code, out.getvalue(), slept

    def queue_reply(self, text="pong"):
        asked = self.ask("ping")
        self.store.ignore(asked.id, "answered inline")
        return self.store.reply("terminal:default", text)

    def test_lock_stale_when_owner_dead(self):
        lock = self.root / "daemon.lock.d"
        lock.mkdir()
        (lock / "pid").write_text(str(dead_pid()), encoding="utf-8")
        reply = self.queue_reply()
        code, out, _slept = self.run_daemon()
        self.assertEqual((code, out), (0, ""))
        self.assertEqual(self.inbox().read_text(encoding="utf-8"), f"{reply.created_at}  pong\n")
        self.assertFalse(lock.exists())

    def test_lock_live_owner_refuses(self):
        lock = self.root / "daemon.lock.d"
        lock.mkdir()
        (lock / "pid").write_text(str(os.getpid()), encoding="utf-8")
        self.queue_reply()
        code, out, _slept = self.run_daemon()
        self.assertEqual((code, out), (0, f"daemon already running as {os.getpid()}\n"))
        self.assertFalse(self.inbox().exists())
        self.assertEqual((lock / "pid").read_text(encoding="utf-8"), str(os.getpid()))

    def test_sigterm_ends_the_loop_and_releases_the_lock(self):
        slept = []

        def sleep_then_terminate(seconds):
            slept.append(seconds)
            os.kill(os.getpid(), signal.SIGTERM)

        before = signal.getsignal(signal.SIGTERM)
        code = daemon.run(self.root, HUB, interval_seconds=7, sleep=sleep_then_terminate)
        self.assertEqual((code, slept), (0, [7]))
        self.assertFalse((self.root / "daemon.lock.d").exists())
        self.assertIs(signal.getsignal(signal.SIGTERM), before)

    def test_run_hands_every_pass_the_same_removal_backoff(self):
        handed = []

        def fake_pass(store, settings, root, hub_root, **kwargs):
            handed.append(kwargs["blocked"])
            kwargs["blocked"]["seen"] = len(handed)
            return daemon.PassResult(0, 0, 0, 0, None, 0, ())

        daemon.run(self.root, HUB, interval_seconds=0, passes=2, sleep=lambda _s: None,
                   one_pass=fake_pass)
        self.assertIs(handed[0], handed[1])
        self.assertEqual(handed[0], {"seen": 2})
        self.assertFalse(hasattr(daemon, "failed_removals"))

    def test_daemon_log_is_quiet_on_empty_pass(self):
        log = self.root / "log" / "daemon.log"
        _code, _out, slept = self.run_daemon(passes=2)
        self.assertFalse(log.exists())
        self.assertEqual(slept, [5])
        self.queue_reply()
        self.run_daemon(passes=2)
        [line] = log.read_text(encoding="utf-8").splitlines()
        self.assertRegex(
            line,
            r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00  "
            r"fanout=0 reaped=0 expired=0 removed=0 resumed=0 launched=0 wake=- replies=1 errors=0$",
        )

    def test_log_rotates_to_a_single_previous_file_over_the_limit(self):
        result = daemon.PassResult(0, 0, 0, 1, None, 0, ())
        log = self.root / "log" / "daemon.log"
        older = log.with_name("daemon.log.1")
        daemon.log_pass(self.root, result, limit=100)
        self.assertFalse(older.exists())
        first = log.read_text(encoding="utf-8")
        for _ in range(4):
            daemon.log_pass(self.root, result, limit=100)
        self.assertEqual(sorted(path.name for path in log.parent.iterdir()), ["daemon.log", "daemon.log.1"])
        self.assertLessEqual(log.stat().st_size, 100 + len(first))
        self.assertTrue(older.read_text(encoding="utf-8").startswith(first))

    def test_pass_and_inbox_verbs_print_the_line_and_the_reply(self):
        reply = self.queue_reply("pong from the router")

        def deez(*argv):
            out, err = StringIO(), StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["super-clanker", *argv])
            return code, out.getvalue(), err.getvalue()

        empty = deez("inbox")
        passed = deez("pass")
        quiet = deez("pass")
        shown = deez("inbox")
        self.assertEqual(empty, (0, "inbox empty\n", ""))
        self.assertEqual((passed[0], quiet[0]), (0, 0))
        self.assertRegex(
            passed[1],
            r"^\S+  fanout=0 reaped=0 expired=0 removed=0 resumed=0 launched=0 wake=- replies=1 errors=0\n$",
        )
        self.assertRegex(quiet[1], r"replies=0 errors=0\n$")
        self.assertEqual(
            (self.root / "log" / "daemon.log").read_text(encoding="utf-8"), passed[1]
        )
        self.assertEqual(shown, (0, f"{reply.created_at}  pong from the router\n", ""))


if __name__ == "__main__":
    unittest.main()


class RefusedSettleTest(unittest.TestCase):
    def test_refused_triggers_are_ignored_without_a_wake(self):
        import tempfile
        from pathlib import Path
        from deezlib.superclanker import config as superconfig, daemon
        from deezlib.superclanker.domain import Trigger
        from deezlib.superclanker.store import Store
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "sources.toml").write_text('[sources.github]\nenabled = true\nmode = "explicit-only"\nsenders = ["daryl-tg"]\n')
        store = Store.open(root); self.addCleanup(store.close)
        store.receive(Trigger(
            id="t_refused0001", source="github", source_event_id="check:1:b:F:x",
            thread_id="gh:acme/widgets#12", actor=None, addressed=False, text="CI b F",
            parent_id=None, received_at="2026-11-02T10:00:00+00:00", meta={},
        ))
        calls = []
        result = daemon.one_pass(store, superconfig.load(root), root, root,
                                 wake=lambda *a, **k: calls.append(a), launch=lambda *a, **k: None,
                                 resume=lambda *a, **k: None, reap=lambda *a, **k: [])
        self.assertEqual(calls, [])
        self.assertEqual(store.queued(), [])
        self.assertEqual(result.wake_id, None)


class SourceChangeRestartTest(unittest.TestCase):
    def test_daemon_exits_when_its_source_changes(self):
        import os, tempfile, time
        from pathlib import Path
        from deezlib.superclanker import daemon
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        src = root / "pkg"; src.mkdir(); (src / "a.py").write_text("x = 1\n")
        stamp = daemon.source_stamp(src)
        self.assertEqual(stamp, daemon.source_stamp(src))
        later = time.time() + 5
        os.utime(src / "a.py", (later, later))
        self.assertNotEqual(stamp, daemon.source_stamp(src))
        passes = []
        def fake_pass(*a, **k):
            passes.append(1)
            if len(passes) == 2:
                (src / "b.py").write_text("y = 2\n")
            return daemon.PassResult(0, 0, 0, 0, None, 0, ())
        code = daemon.run(root, root, interval_seconds=0, passes=10, sleep=lambda _s: None,
                          one_pass=fake_pass, source_dir=src)
        self.assertEqual(code, 0)
        self.assertEqual(len(passes), 2)
