import contextlib
import dataclasses
import importlib.util
import unittest
from unittest import mock

TEXTUAL = importlib.util.find_spec("textual")

if TEXTUAL:
    from deezlib.superclanker.ui_app import BoardApp
    from tests.test_super_ui_app import Rig, labels, settle, snapshot, ticket, toasts, until

SESSION_ARGV = ["claude", "--resume", "s_1"]


class Alive:
    def __init__(self, rig, polls_alive):
        self.rig = rig
        self.polls_alive = polls_alive
        self.polls = 0

    def __call__(self, pid):
        self.polls += 1
        return self.polls <= self.polls_alive

    def sleep(self, seconds):
        self.rig.clock.now += seconds


@unittest.skipUnless(TEXTUAL, "textual not installed")
class TakeoverTest(unittest.IsolatedAsyncioTestCase):
    async def test_takeover_live_worker_kills_then_opens_tmux_window(self):
        rig = Rig(snapshot([ticket("k_1")]))
        alive = Alive(rig, 3)
        windows = []
        app = rig.app(tmux=windows.append, in_tmux=lambda: True, pid_alive=alive, sleep=alive.sleep)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await settle(pilot)
            text = " ".join(str(w.render()) for w in pilot.app.screen.query("Static"))
            self.assertIn("a later input can revive it", text)
            self.assertEqual(rig.calls, [])
            await pilot.press("y")
            await until(pilot, lambda: windows)
            await settle(pilot)
            self.assertTrue(any("taken over" in label for label in labels(pilot.app)))
        self.assertEqual(rig.calls, [[str(rig.app().deez), "super-clanker", "kill", "a_1"]])
        self.assertEqual(windows, [["tmux", "new-window", "-n", "slug-k_1", "-c", "/w", *SESSION_ARGV]])

    async def test_takeover_declined_does_nothing(self):
        rig = Rig(snapshot([ticket("k_1")]))
        windows = []
        async with rig.app(tmux=windows.append, in_tmux=lambda: True, pid_alive=lambda pid: True).run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("n")
            await settle(pilot)
        self.assertEqual((rig.calls, windows), ([], []))

    async def test_takeover_stops_with_a_toast_when_the_worker_will_not_die(self):
        rig = Rig(snapshot([ticket("k_1")]))
        alive = Alive(rig, 10 ** 9)
        windows = []
        app = rig.app(tmux=windows.append, in_tmux=lambda: True, pid_alive=alive, sleep=alive.sleep)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await until(pilot, lambda: any("did not exit" in note for note in toasts(pilot.app)))
            await settle(pilot)
            self.assertFalse(any("taken over" in label for label in labels(pilot.app)))
        self.assertEqual(windows, [])

    async def test_takeover_stops_when_kill_verb_fails(self):
        from deezlib.superclanker.ui_app import VerbResult
        rig = Rig(snapshot([ticket("k_1")]), result=VerbResult([], 2, "", "nope"))
        windows = []
        app = rig.app(tmux=windows.append, in_tmux=lambda: True, pid_alive=lambda pid: True)
        async with app.run_test() as pilot:
            await settle(pilot)
            await pilot.press("t")
            await pilot.press("y")
            await settle(pilot)
            await until(pilot, lambda: any("exit 2" in note for note in toasts(pilot.app)))
        self.assertEqual(windows, [])

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

        windows = []
        app = rig.app(tmux=windows.append, in_tmux=lambda: False, pid_alive=lambda pid: False)
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
        self.assertEqual((rig.calls, windows), ([], []))

    async def test_takeover_refused_without_session(self):
        for missing in ("session_id", "worktree"):
            with self.subTest(missing=missing):
                rig = Rig(snapshot([dataclasses.replace(ticket("k_1"), **{missing: None})]))
                windows = []
                async with rig.app(tmux=windows.append, in_tmux=lambda: True).run_test() as pilot:
                    await settle(pilot)
                    await pilot.press("t")
                    await settle(pilot)
                    self.assertEqual(len(pilot.app.screen_stack), 1)
                    self.assertTrue(any(missing.replace("_id", "") in note for note in toasts(pilot.app)))
                self.assertEqual((rig.calls, windows), ([], []))


if __name__ == "__main__":
    unittest.main()
