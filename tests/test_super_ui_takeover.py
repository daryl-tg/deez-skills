import contextlib
import dataclasses
import importlib.util
import subprocess
import threading
import unittest
from unittest import mock

TEXTUAL = importlib.util.find_spec("textual")

if TEXTUAL:
    from deezlib.superclanker.ui_app import BoardApp
    from tests.test_super_ui_app import DEEZ, Rig, Tmux, labels, settle, snapshot, ticket, toasts, until

SESSION_ARGV = ["claude", "--resume", "s_1"]


async def settle_ui(pilot):
    await pilot.pause()
    await pilot.pause()


class Alive:
    def __init__(self, rig, polls_alive):
        self.rig = rig
        self.polls_alive = polls_alive
        self.polls = 0
        self.pids = []

    def __call__(self, pid):
        self.pids.append(pid)
        self.polls += 1
        return self.polls <= self.polls_alive

    def sleep(self, seconds):
        self.rig.clock.now += seconds


@unittest.skipUnless(TEXTUAL, "textual not installed")
class TakeoverTest(unittest.IsolatedAsyncioTestCase):
    async def test_takeover_live_worker_kills_then_opens_tmux_window(self):
        rig = Rig(snapshot([ticket("k_1")]))
        alive = Alive(rig, 3)
        windows = Tmux()
        app = rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=alive, sleep=alive.sleep)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await settle(pilot)
            text = " ".join(str(w.render()) for w in pilot.app.screen.query("Static"))
            self.assertIn("a later input can revive it", text)
            self.assertEqual(rig.calls, [])
            await pilot.press("y")
            await until(pilot, lambda: windows.calls)
            await settle(pilot)
            self.assertTrue(any("taken over" in label for label in labels(pilot.app)))
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "kill", "a_1"]])
        self.assertEqual(windows.calls, [["tmux", "new-window", "-n", "slug-k_1", "-c", "/w", *SESSION_ARGV]])
        self.assertNotIn(threading.get_ident(), windows.threads)

    async def test_takeover_declined_does_nothing(self):
        rig = Rig(snapshot([ticket("k_1")]))
        windows = Tmux()
        async with rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=lambda pid: True).run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("n")
            await settle(pilot)
        self.assertEqual((rig.calls, windows.calls), ([], []))

    async def test_takeover_stops_with_a_toast_when_the_worker_will_not_die(self):
        rig = Rig(snapshot([ticket("k_1")]))
        alive = Alive(rig, 10 ** 9)
        windows = Tmux()
        app = rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=alive, sleep=alive.sleep)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await until(pilot, lambda: any("did not exit" in note for note in toasts(pilot.app)))
            await settle(pilot)
            self.assertFalse(any("taken over" in label for label in labels(pilot.app)))
        self.assertEqual(windows.calls, [])

    async def test_takeover_stops_when_kill_verb_fails(self):
        from deezlib.superclanker.ui_app import VerbResult
        rig = Rig(snapshot([ticket("k_1")]), result=VerbResult([], 2, "", "nope"))
        windows = Tmux()
        app = rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=lambda pid: True)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await settle(pilot)
            await until(pilot, lambda: any("exit 2" in note for note in toasts(pilot.app)))
        self.assertEqual(windows.calls, [])

    async def test_takeover_outside_tmux_suspends(self):
        rig = Rig(snapshot([ticket("k_1")]))
        events = []

        @contextlib.contextmanager
        def suspend(_app):
            events.append("suspend")
            yield
            events.append("resume")

        def run(argv, **kwargs):
            events.append(("run", argv, kwargs))

        windows = Tmux()
        app = rig.app(tmux=windows, in_tmux=lambda: False, pid_alive=lambda pid: False)
        with mock.patch.object(BoardApp, "suspend", suspend), \
                mock.patch("deezlib.superclanker.ui_takeover.subprocess.run", run):
            async with app.run_test() as pilot:
                await settle(pilot)
                await pilot.press("t")
                await pilot.press("y")
                await until(pilot, lambda: "resume" in events)
                await settle(pilot)
                self.assertTrue(any("taken over" in label for label in labels(pilot.app)))
        self.assertEqual(events, ["suspend", ("run", SESSION_ARGV, {"cwd": "/w"}), "resume"])
        self.assertEqual((rig.calls, windows.calls), ([], []))

    async def test_takeover_acts_on_the_current_worker_when_the_ticket_was_revived(self):
        rig = Rig(snapshot([ticket("k_1")]))
        alive = Alive(rig, 2)
        windows = Tmux()
        app = rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=alive, sleep=alive.sleep)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await settle(pilot)
            revived = dataclasses.replace(ticket("k_1", assignment="a_2"), pid=77)
            pilot.app.apply_snapshot(snapshot([revived]))
            await settle(pilot)
            await pilot.press("y")
            await until(pilot, lambda: windows.calls)
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "kill", "a_2"]])
        self.assertEqual(set(alive.pids), {77})

    async def test_takeover_refused_on_a_row_already_taken_over(self):
        rig = Rig(snapshot([ticket("k_1")]))
        windows = Tmux()
        async with rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=lambda pid: False).run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await until(pilot, lambda: windows.calls)
            await settle(pilot)
            await pilot.press("t")
            await settle(pilot)
            self.assertEqual(len(pilot.app.screen_stack), 1)
            self.assertTrue(any("already taken over" in note for note in toasts(pilot.app)))
        self.assertEqual(len(windows.calls), 1)

    async def test_failed_new_window_toasts_and_does_not_mark_the_row(self):
        rig = Rig(snapshot([ticket("k_1")]))
        windows = Tmux(returncode=1)
        async with rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=lambda pid: False).run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await until(pilot, lambda: any("tmux" in note for note in toasts(pilot.app)))
            await settle(pilot)
            self.assertFalse(any("taken over" in label for label in labels(pilot.app)))

    async def test_missing_claude_outside_tmux_toasts_and_does_not_mark_the_row(self):
        rig = Rig(snapshot([ticket("k_1")]))

        @contextlib.contextmanager
        def suspend(_app):
            yield

        app = rig.app(in_tmux=lambda: False, pid_alive=lambda pid: False)
        with mock.patch.object(BoardApp, "suspend", suspend), \
                mock.patch("deezlib.superclanker.ui_takeover.subprocess.run", side_effect=FileNotFoundError("claude")):
            async with app.run_test() as pilot:
                await settle(pilot)
                await pilot.press("t")
                await pilot.press("y")
                await until(pilot, lambda: any("claude" in note for note in toasts(pilot.app)))
                await settle(pilot)
                self.assertFalse(any("taken over" in label for label in labels(pilot.app)))

    async def test_missing_claude_inside_tmux_toasts_before_killing_anything(self):
        rig = Rig(snapshot([ticket("k_1")]))
        windows = Tmux()
        alive = Alive(rig, 10 ** 9)
        app = rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=alive, sleep=alive.sleep, which=lambda name: None)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await settle(pilot)
            self.assertTrue(any("claude" in note for note in toasts(pilot.app)))
            self.assertFalse(any("taken over" in label for label in labels(pilot.app)))
        self.assertEqual((rig.calls, windows.calls), ([], []))

    async def test_second_takeover_while_one_runs_is_refused(self):
        rig = Rig(snapshot([ticket("k_1"), ticket("k_2", assignment="a_2")]))
        gate = threading.Event()
        windows = Tmux()

        def alive(pid):
            gate.wait(10)
            return False

        app = rig.app(tmux=windows, in_tmux=lambda: True, pid_alive=alive)
        try:
            async with app.run_test() as pilot:
                await settle_ui(pilot)
                await pilot.press("t")
                await pilot.press("y")
                await pilot.pause()
                table = pilot.app.query_one("#rows")
                table.move_cursor(row=[i for i, label in enumerate(labels(pilot.app)) if "k_2" in label][0])
                await pilot.pause()
                await pilot.press("t")
                await pilot.pause()
                self.assertEqual(len(pilot.app.screen_stack), 1)
                self.assertTrue(any("already running" in note for note in toasts(pilot.app)))
                gate.set()
                await until(pilot, lambda: windows.calls)
        finally:
            gate.set()
        self.assertEqual(len(windows.calls), 1)

    async def test_takeover_refused_without_session(self):
        for missing in ("session_id", "worktree"):
            with self.subTest(missing=missing):
                rig = Rig(snapshot([dataclasses.replace(ticket("k_1"), **{missing: None})]))
                windows = Tmux()
                async with rig.app(tmux=windows, in_tmux=lambda: True).run_test() as pilot:
                    await settle(pilot)
                    await pilot.press("t")
                    await settle(pilot)
                    self.assertEqual(len(pilot.app.screen_stack), 1)
                    self.assertTrue(any(missing.replace("_id", "") in note for note in toasts(pilot.app)))
                self.assertEqual((rig.calls, windows.calls), ([], []))


if __name__ == "__main__":
    unittest.main()
