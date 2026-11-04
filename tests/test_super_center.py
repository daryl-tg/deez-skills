import asyncio
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from deezlib.superclanker import center_model
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.store import Store

TEXTUAL = importlib.util.find_spec("textual")
DEEZ = Path("/hub/bin/deez")

if TEXTUAL:
    from deezlib.superclanker.center_app import CenterApp
    from deezlib.superclanker.ui_app import VerbResult


def terminal_trigger(index, text):
    return Trigger(
        id=trigger_id("terminal", f"evt-{index}"), source="terminal", source_event_id=f"evt-{index}",
        thread_id="terminal:default", actor="dboon", addressed=True, text=text, parent_id=None,
        received_at=f"2026-11-04T06:0{index}:00+00:00", meta={},
    )


class Seeded(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "state"
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)

    def ticket(self, index, text="fix the [bold] tape", report=None, question=None, start=True, end=None):
        trigger = terminal_trigger(index, text)
        self.store.receive(trigger)
        ticket = self.store.accept(
            trigger.id, f"slug-{index}", Strength.explicit, "dboon/deez-skills",
            ["addressed-request"], "policy-1", "asked",
        )
        assignment = self.store.assignment_for(ticket.id)
        if start:
            self.store.start_assignment(assignment.id, f"sid-{index}", 4242, f"/w/{index}")
        if report:
            self.store.report(assignment.id, report, f"report {index}", question=question)
        if end:
            self.store.end_ticket(ticket.id, end)
        return ticket, assignment, trigger


class LoadTest(Seeded):
    def test_dossier_carries_request_scope_reports_notes_and_costs(self):
        ticket, assignment, trigger = self.ticket(1, report="waiting", question="Publish now?")
        self.store.add_input(ticket.id, "note", "playbook: ~/skills/clanker-mode/playbooks/feature.md")
        self.store.add_input(ticket.id, "note", "repo: ~/github/deez-skills")
        wake = self.store.begin_wake([trigger.id])
        self.store.end_wake(wake, 0, 0.25, "s", "ok")
        (self.root / "log").mkdir(exist_ok=True)
        (self.root / "log" / f"{assignment.id}.json").write_text(json.dumps(
            {"total_cost_usd": 1.5, "num_turns": 12, "modelUsage": {"claude-opus-5-5": {}}, "duration_ms": 9000}
        ))

        world = center_model.load(self.root)

        dossier = world.dossiers[0]
        self.assertEqual(dossier.id, ticket.id)
        self.assertEqual(dossier.request, "fix the [bold] tape")
        self.assertEqual(dossier.scope, "dboon/deez-skills")
        self.assertEqual(dossier.playbook, "feature")
        self.assertEqual(dossier.repo, "~/github/deez-skills")
        self.assertEqual(dossier.question, "Publish now?")
        self.assertEqual([kind for _, kind, _ in dossier.reports], ["waiting"])
        self.assertEqual(len(dossier.notes), 2)
        self.assertEqual(dossier.worker_cost, 1.5)
        self.assertEqual(dossier.turns[0].model, "opus-5-5")
        self.assertAlmostEqual(dossier.router_cost, 0.25)
        self.assertTrue(dossier.needs_you)
        self.assertAlmostEqual(world.spend_today, 0.25)

    def test_terminal_thread_interleaves_asks_and_replies(self):
        self.ticket(1, text="first ask")
        self.store.reply("terminal:default", "dispatched")

        messages = center_model.load(self.root).threads["terminal:default"]

        self.assertEqual([(m.who, m.text) for m in messages], [("you", "first ask"), ("router", "dispatched")])

    def test_missing_state_loads_an_empty_world(self):
        world = center_model.load(Path(self.root) / "absent")
        self.assertEqual(world.dossiers, [])


class StageTest(Seeded):
    def stage_of(self, ticket):
        world = center_model.load(self.root)
        return center_model.stage(next(d for d in world.dossiers if d.id == ticket.id))

    def test_stages_follow_ticket_and_worker_state(self):
        running, _, _ = self.ticket(1, report="progress")
        waiting, _, _ = self.ticket(2, report="waiting", question="ok?")
        ready, _, _ = self.ticket(3, report="ready")
        queued, _, _ = self.ticket(4, start=False)
        ended, _, _ = self.ticket(5, report="ready", end="done")

        self.assertEqual(self.stage_of(running), "RUNNING")
        self.assertEqual(self.stage_of(waiting), "NEEDS YOU")
        self.assertEqual(self.stage_of(ready), "READY")
        self.assertEqual(self.stage_of(queued), "QUEUED")
        self.assertEqual(self.stage_of(ended), "ENDED")


class Verbs:
    def __init__(self):
        self.calls = []

    def __call__(self, argv):
        self.calls.append(list(argv))
        return VerbResult(argv, 0, "ok\n", "")


@unittest.skipUnless(TEXTUAL, "textual not installed")
class AppTest(Seeded):
    def app(self, verbs):
        return CenterApp(self.root, verb=verbs, deez=DEEZ, refresh_s=3600)

    def run_app(self, verbs, script):
        async def go():
            app = self.app(verbs)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await script(app, pilot)
                await app.workers.wait_for_complete()
                await pilot.pause()
                return app
        return asyncio.run(go())

    def test_typing_a_message_asks_the_router(self):
        self.ticket(1)
        verbs = Verbs()

        async def script(app, pilot):
            app.query_one("#input").focus()
            await pilot.press(*"-why [red] slow")
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertEqual(verbs.calls, [[str(DEEZ), "super-clanker", "ask", "--", "-why [red] slow"]])

    def test_note_mode_notes_the_selected_ticket(self):
        ticket, _, _ = self.ticket(1)
        verbs = Verbs()

        async def script(app, pilot):
            await pilot.press("ctrl+t")
            await pilot.press(*"use main")
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertEqual(verbs.calls, [[str(DEEZ), "super-clanker", "note", ticket.id, "--text=use main"]])

    def test_reload_shows_tickets_created_after_launch(self):
        self.ticket(1)
        counts = []

        async def script(app, pilot):
            counts.append(app.query_one("#blotter").row_count)
            self.ticket(2)
            app.reload()
            await app.workers.wait_for_complete()
            await pilot.pause()
            counts.append(app.query_one("#blotter").row_count)

        self.run_app(Verbs(), script)

        self.assertEqual(counts, [1, 2])

    def test_bracketed_text_renders_in_every_view(self):
        self.ticket(1, text="[/x] broken [bold", report="blocked", question="[ERROR] which?")

        async def script(app, pilot):
            for _ in range(3):
                await pilot.press("v")
                await pilot.pause()
            await pilot.press("z")
            await pilot.pause()

        app = self.run_app(Verbs(), script)

        self.assertEqual(app.view_mode, "TABLE")

    def test_failed_verb_is_shown_in_the_router_log(self):
        self.ticket(1)

        def failing(argv):
            return VerbResult(argv, 2, "", "boom: no daemon")

        async def script(app, pilot):
            app.query_one("#input").focus()
            await pilot.press(*"hello")
            await pilot.press("enter")

        app = self.run_app(failing, script)

        self.assertIn("boom: no daemon", app.log_text())


if __name__ == "__main__":
    unittest.main()
