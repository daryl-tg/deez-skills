import asyncio
import importlib.util
import time
import unittest
from pathlib import Path

DEEZ = Path("/hub/bin/deez")
TEXTUAL = importlib.util.find_spec("textual")

if TEXTUAL:
    from deezlib.superclanker import procs, ui_model
    from deezlib.superclanker.ui_app import BoardApp, VerbResult


def ticket(ticket_id, state="open", needs_you=False, question=None, assignment="a_1", slug=None):
    return ui_model.TicketRow(
        ticket_id=ticket_id, slug=slug or f"slug-{ticket_id}", state=state, repo="repo", age_s=60,
        worker_state="running" if state == "open" else "ended", assignment_id=assignment,
        session_id="s_1", worktree="/w", pid=42, last_report="waiting" if needs_you else "progress",
        question=question, needs_you=needs_you, rss_kb=2048,
    )


def snapshot(rows=(), **changes):
    fields = dict(
        initialised=True, stale=False, error=None, free_pct=41, held=None,
        health=ui_model.DaemonHealth(7, True, 3), spend_today=1.84, rows=list(rows), anomalies=[],
        peers=[], attribution=procs.Attribution({}, {}, set()), top=[], table={}, inbox_text="",
        inbox_offset=0, max_running=3, taken_at=0.0,
    )
    fields.update(changes)
    return ui_model.Snapshot(**fields)


class Rig:
    def __init__(self, snap, verb_delay=0.0, result=None):
        self.snap = snap
        self.calls = []
        self.snapshots = 0
        self.verb_delay = verb_delay
        self.result = result

    def snapshot_fn(self, root, previous, cadence):
        self.snapshots += 1
        return self.snap

    def verb(self, argv):
        time.sleep(self.verb_delay)
        self.calls.append(argv)
        return self.result or VerbResult(argv, 0, "ok", "")

    def app(self):
        return BoardApp(Path("/state"), snapshot_fn=self.snapshot_fn, verb=self.verb, deez=DEEZ)


def settle(pilot):
    return pilot.pause(0.3)


def toasts(app):
    return [note.message for note in app._notifications]


def labels(app):
    table = app.query_one("#rows")
    return [str(table.get_row_at(index)[0]) for index in range(table.row_count)]


@unittest.skipUnless(TEXTUAL, "textual not installed")
class BoardTest(unittest.IsolatedAsyncioTestCase):
    async def test_needs_you_rows_listed_first(self):
        rig = Rig(snapshot(
            [ticket("k_2"), ticket("k_9", needs_you=True, question="merge?")],
            anomalies=[("orphan worktree", [(["/w/k_0"], "orphan at /w/k_0")])],
        ))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            shown = labels(pilot.app)
        self.assertEqual(shown[0], "NEEDS YOU")
        self.assertIn("k_9", shown[1])
        self.assertIn("orphan worktree", shown[2])
        self.assertEqual(shown[3], "TICKETS")
        self.assertIn("k_2", shown[4])

    async def test_ended_hidden_until_e(self):
        rig = Rig(snapshot([ticket("k_1"), ticket("k_3", state="ended")]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            self.assertFalse(any("k_3" in label for label in labels(pilot.app)))
            await pilot.press("e")
            await settle(pilot)
            self.assertTrue(any("k_3" in label for label in labels(pilot.app)))
            await pilot.press("e")
            await settle(pilot)
            self.assertFalse(any("k_3" in label for label in labels(pilot.app)))

    async def select_ticket(self, pilot, ticket_id):
        table = pilot.app.query_one("#rows")
        for index, label in enumerate(labels(pilot.app)):
            if ticket_id in label:
                table.move_cursor(row=index)
        await settle(pilot)

    async def test_ask_sends_ask_verb(self):
        rig = Rig(snapshot([ticket("k_1")]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await pilot.press("a")
            await pilot.press(*"hello")
            await pilot.press("enter")
            await settle(pilot)
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "ask", "hello", "--thread", "default"]])

    async def test_reply_sends_note(self):
        rig = Rig(snapshot([ticket("k_9", needs_you=True, question="merge?")]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await self.select_ticket(pilot, "k_9")
            await pilot.press("r")
            await pilot.press(*"keep")
            await pilot.press("enter")
            await settle(pilot)
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "note", "k_9", "--text", "keep"]])

    async def test_note_sends_note(self):
        rig = Rig(snapshot([ticket("k_1")]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await self.select_ticket(pilot, "k_1")
            await pilot.press("n")
            await pilot.press(*"hi")
            await pilot.press("enter")
            await settle(pilot)
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "note", "k_1", "--text", "hi"]])

    async def test_stop_needs_reason_and_y(self):
        rig = Rig(snapshot([ticket("k_1")]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await self.select_ticket(pilot, "k_1")
            await pilot.press("s")
            await pilot.press(*"done")
            await pilot.press("enter")
            await settle(pilot)
            text = " ".join(str(w.render()) for w in pilot.app.screen.query("Static"))
            self.assertIn("worktree is removed", text)
            self.assertIn("takeover session", text)
            await pilot.press("n")
            await settle(pilot)
            self.assertEqual(rig.calls, [])
            await pilot.press("s")
            await pilot.press(*"done")
            await pilot.press("enter")
            await pilot.press("y")
            await settle(pilot)
        self.assertEqual(
            rig.calls,
            [[str(DEEZ), "super-clanker", "stop", "k_1", "--reason", "done", "--by", "operator"]],
        )

    async def test_kill_retry_kick_need_confirm(self):
        rig = Rig(snapshot([ticket("k_1")]))
        expected = {
            "k": ["kill", "a_1"],
            "R": ["retry", "k_1"],
            "K": ["kick", "daemon"],
        }
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await self.select_ticket(pilot, "k_1")
            for key, verb in expected.items():
                await pilot.press(key)
                await settle(pilot)
                await pilot.press("n")
                await settle(pilot)
            self.assertEqual(rig.calls, [])
            for key, verb in expected.items():
                before = len(rig.calls)
                await pilot.press(key)
                await pilot.press("y")
                await settle(pilot)
                self.assertEqual(rig.calls[before:], [[str(DEEZ), "super-clanker", *verb]])

    async def test_requeue_from_anomaly_row_needs_no_confirm(self):
        rig = Rig(snapshot(anomalies=[("undecided", [(["t_5", "d_1"], "t_5: decided unavailable")])]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await pilot.press("Q")
            await settle(pilot)
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "requeue", "t_5"]])

    async def test_palette_splits_free_text(self):
        rig = Rig(snapshot([ticket("k_1")]))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await pilot.press("colon")
            await pilot.press(*"status --json")
            await pilot.press("enter")
            await settle(pilot)
        self.assertEqual(rig.calls, [[str(DEEZ), "super-clanker", "status", "--json"]])

    async def test_failed_verb_shows_exit_and_stderr(self):
        rig = Rig(snapshot([ticket("k_1")]), result=VerbResult([], 2, "", "boom"))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await pilot.press("a")
            await pilot.press(*"x")
            await pilot.press("enter")
            await settle(pilot)
            shown = toasts(pilot.app)
        self.assertTrue(any("exit 2" in note and "boom" in note for note in shown), shown)

    async def test_slow_verb_does_not_block_refresh(self):
        rig = Rig(snapshot([ticket("k_1")]), verb_delay=3.0)
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            await pilot.press("a")
            await pilot.press(*"x")
            await pilot.press("enter")
            before = rig.snapshots
            await pilot.pause(2.4)
            self.assertGreater(rig.snapshots, before)
            self.assertEqual(rig.calls, [])
            await pilot.pause(1.5)
        self.assertEqual(len(rig.calls), 1)

    async def test_not_initialised_notice(self):
        rig = Rig(snapshot(initialised=False, error="daemon not initialised", health=None))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            notice = str(pilot.app.query_one("#notice").render())
        self.assertIn("daemon not initialised", notice)

    async def test_stale_marker(self):
        rig = Rig(snapshot(stale=True, error="database is locked"))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            header = str(pilot.app.query_one("#header").render())
        self.assertIn("STALE", header)
        self.assertIn("database is locked", header)

    async def test_header_shows_totals(self):
        attribution = procs.Attribution({"k_1": {1}}, {"me": {2}}, {3})
        table = {
            1: procs.Proc(1, 0, 0, 1048576, "w"),
            2: procs.Proc(2, 0, 0, 2097152, "p"),
            3: procs.Proc(3, 0, 0, 524288, "o"),
        }
        rig = Rig(snapshot([ticket("k_1")], attribution=attribution, table=table, held=5))
        async with rig.app().run_test() as pilot:
            await settle(pilot)
            header = str(pilot.app.query_one("#header").render())
        for text in ("41% free", "held: yes", "daemon ok 3s", "$1.84", "workers 1/3", "1.0 GB", "2.0 GB", "0.5 GB"):
            self.assertIn(text, header)


if __name__ == "__main__":
    unittest.main()
