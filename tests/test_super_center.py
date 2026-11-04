import asyncio
from datetime import timedelta
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from deezlib.superclanker import center_model
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.store import Store

TEXTUAL = importlib.util.find_spec("textual")
DEEZ = Path("/hub/bin/deez")

if TEXTUAL:
    from textual import events

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

    def test_worker_cap_comes_from_sources_toml(self):
        (self.root / "sources.toml").write_text("[workers]\nmax_running = 6\n")

        self.assertEqual(center_model.load(self.root).max_running, 6)

    def test_review_url_comes_from_the_reports(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        self.store.report(assignment.id, "ready", "PR open: https://github.com/daryl-tg/deez-skills/pull/42.",
                          evidence=["https://github.com/daryl-tg/deez-skills/pull/42"])
        other, second, _ = self.ticket(2, report="progress")
        self.store.report(second.id, "ready", "MR https://gitlab.com/om/rooms-client/-/merge_requests/812")
        plain, _, _ = self.ticket(3, report="ready")

        found = {d.id: d.review_url for d in center_model.load(self.root).dossiers}

        self.assertEqual(found[ticket.id], "https://github.com/daryl-tg/deez-skills/pull/42")
        self.assertEqual(found[other.id], "https://gitlab.com/om/rooms-client/-/merge_requests/812")
        self.assertIsNone(found[plain.id])

    def write_turn(self, assignment_id, suffix="", models=None):
        log = self.root / "log"
        log.mkdir(exist_ok=True)
        usage = models or {"claude-opus-5-5": {"inputTokens": 18, "cacheCreationInputTokens": 50000,
                                               "cacheReadInputTokens": 350000, "outputTokens": 6500}}
        (log / f"{assignment_id}{suffix}.json").write_text(json.dumps({"modelUsage": usage, "num_turns": 3}))

    def test_tokens_add_up_every_model_a_worker_used(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        self.write_turn(assignment.id, models={
            "claude-opus-5-5": {"inputTokens": 10, "cacheCreationInputTokens": 1000, "cacheReadInputTokens": 20000, "outputTokens": 500},
            "claude-haiku-5-5": {"inputTokens": 5, "cacheCreationInputTokens": 200, "cacheReadInputTokens": 3000, "outputTokens": 100},
        })
        self.write_turn(assignment.id, ".1")

        dossier = center_model.load(self.root).dossiers[0]

        first = dossier.turns[0]
        self.assertEqual((first.tokens_in, first.tokens_cached, first.tokens_out), (1215, 23000, 600))
        self.assertEqual(first.tokens, 24815)
        self.assertEqual(dossier.tokens, 24815 + 406518)

    def test_tokens_today_counts_worker_runs_and_router_wakes(self):
        ticket, assignment, trigger = self.ticket(1, report="progress")
        self.write_turn(assignment.id)
        wake = self.store.begin_wake([trigger.id])
        self.store.end_wake(wake, 0, 0.05, "s", "ok", tokens=1000)

        world = center_model.load(self.root)

        self.assertEqual(world.tokens_today, 406518 + 1000)

    def test_a_database_from_before_wake_tokens_still_loads(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        self.write_turn(assignment.id)
        self.store.close()
        raw = sqlite3.connect(self.root / "super.db")
        raw.execute("ALTER TABLE wakes DROP COLUMN tokens")
        raw.commit()
        raw.close()

        world = center_model.load(self.root)

        self.assertEqual(world.tokens_today, 406518)

    def test_format_tokens_is_short(self):
        self.assertEqual(
            [center_model.fmt_tokens(n) for n in (0, 812, 6500, 406518, 1234567)],
            ["0", "812", "6.5k", "407k", "1.2M"],
        )

    def test_terminal_thread_interleaves_asks_and_replies(self):
        self.ticket(1, text="first ask")
        self.store.reply("terminal:default", "dispatched")

        messages = center_model.load(self.root).threads["terminal:default"]

        self.assertEqual([(m.who, m.text) for m in messages], [("you", "first ask"), ("router", "dispatched")])

    def test_missing_state_loads_an_empty_world(self):
        world = center_model.load(Path(self.root) / "absent")
        self.assertEqual(world.dossiers, [])


def write_transcript(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for at, content in entries:
        lines.append(json.dumps({"type": "assistant", "timestamp": at, "message": {"content": content}}))
    lines.append(json.dumps({"type": "user", "timestamp": "2026-11-04T06:09:00Z",
                             "message": {"content": [{"type": "tool_result", "content": "ok"}]}}))
    path.write_text("\n".join(lines) + "\n")


class ActivityTest(Seeded):
    def test_answer_is_the_latest_turns_final_message(self):
        ticket, assignment, _ = self.ticket(1, report="ready")
        log = self.root / "log"
        log.mkdir(exist_ok=True)
        (log / f"{assignment.id}.json").write_text(json.dumps({"result": "first turn"}))
        (log / f"{assignment.id}.1.json").write_text(json.dumps({"result": "second turn"}))
        (log / f"{assignment.id}.10.json").write_text(json.dumps({"result": "tenth turn\nREPORT ready done"}))

        dossier = center_model.load(self.root).dossiers[0]

        self.assertEqual(dossier.answer, "tenth turn")

    def test_earlier_answers_are_kept_oldest_first(self):
        ticket, first, _ = self.ticket(1, report="ready")
        log = self.root / "log"
        log.mkdir(exist_ok=True)
        (log / f"{first.id}.json").write_text(json.dumps({"result": "the findings write-up"}))
        (log / f"{first.id}.1.json").write_text(json.dumps({"result": "answer to a follow-up"}))

        dossier = center_model.load(self.root).dossiers[0]

        self.assertEqual(dossier.answer, "answer to a follow-up")
        self.assertEqual(dossier.earlier_answers, ["the findings write-up"])

    def test_activity_reads_the_worker_session_transcript(self):
        ticket, assignment, _ = self.ticket(1)
        projects = self.root.parent / "projects"
        write_transcript(projects / "-w-1" / "sid-1.jsonl", [
            ("2026-11-04T06:01:00Z", [{"type": "thinking", "thinking": "hmm"},
                                      {"type": "text", "text": "Reading the handler first."}]),
            ("2026-11-04T06:02:00Z", [{"type": "tool_use", "name": "Bash",
                                       "input": {"command": "git log --oneline -3\necho done"}}]),
            ("2026-11-04T06:03:00Z", [{"type": "tool_use", "name": "Read",
                                       "input": {"file_path": "/repo/src/tape.ts"}}]),
            ("2026-11-04T06:04:00Z", [{"type": "tool_use", "name": "Agent",
                                       "input": {"description": "map the relay", "prompt": "long"}}]),
        ])
        dossier = center_model.load(self.root).dossiers[0]

        lines = center_model.activity(dossier, projects)

        self.assertEqual([(line.kind, line.text) for line in lines], [
            ("say", "Reading the handler first."),
            ("Bash", "git log --oneline -3"),
            ("Read", "/repo/src/tape.ts"),
            ("Agent", "map the relay"),
        ])

    def test_running_turn_tokens_come_from_the_transcript(self):
        self.ticket(1, report="progress")
        projects = self.root.parent / "projects"
        session = projects / "-w-1" / "sid-1.jsonl"
        session.parent.mkdir(parents=True)

        def entry(message_id, out):
            return json.dumps({"type": "assistant", "timestamp": "2026-11-04T06:05:00Z", "message": {
                "id": message_id, "content": [],
                "usage": {"input_tokens": 10, "cache_creation_input_tokens": 100,
                          "cache_read_input_tokens": 1000, "output_tokens": out}}})

        session.write_text("\n".join([entry("m1", 5), entry("m1", 50), entry("m2", 20)]) + "\n")
        subagent = session.with_suffix("") / "subagents" / "agent-1.jsonl"
        subagent.parent.mkdir(parents=True)
        subagent.write_text(entry("s1", 7) + "\n")
        dossier = center_model.load(self.root).dossiers[0]

        self.assertEqual(center_model.inflight_tokens(dossier, projects), (1110 + 50) + (1110 + 20) + (1110 + 7))

    def test_finished_turns_are_not_counted_again_from_the_transcript(self):
        ticket, assignment, _ = self.ticket(1, report="ready")
        log = self.root / "log"
        log.mkdir(exist_ok=True)
        (log / f"{assignment.id}.json").write_text(json.dumps({"modelUsage": {}}))
        projects = self.root.parent / "projects"
        write_transcript(projects / "-w-1" / "sid-1.jsonl", [("2026-11-04T06:02:00Z", [])])
        dossier = center_model.load(self.root).dossiers[0]

        self.assertEqual(center_model.inflight_tokens(dossier, projects), 0)

    def test_activity_without_a_transcript_is_empty(self):
        self.ticket(1, start=False)
        dossier = center_model.load(self.root).dossiers[0]

        self.assertEqual(center_model.activity(dossier, self.root / "none"), [])


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


class StaleTest(Seeded):
    def dossier(self, ticket):
        return next(d for d in center_model.load(self.root).dossiers if d.id == ticket.id)

    def test_ready_ticket_goes_stale_after_six_quiet_hours(self):
        ticket, _, _ = self.ticket(1, report="ready")
        d = self.dossier(ticket)
        quiet = center_model.last_activity(d)

        self.assertIsNone(center_model.stale_reason(d, quiet + timedelta(hours=5)))
        self.assertIn("ready", center_model.stale_reason(d, quiet + timedelta(hours=7)))

    def test_waiting_ticket_goes_stale_after_three_days(self):
        ticket, _, _ = self.ticket(1, report="waiting", question="ok?")
        d = self.dossier(ticket)
        quiet = center_model.last_activity(d)

        self.assertIsNone(center_model.stale_reason(d, quiet + timedelta(days=2)))
        self.assertIn("waiting", center_model.stale_reason(d, quiet + timedelta(days=4)))

    def test_running_worker_is_never_stale(self):
        ticket, _, _ = self.ticket(1, report="progress")
        d = self.dossier(ticket)

        self.assertIsNone(center_model.stale_reason(d, center_model.last_activity(d) + timedelta(days=30)))

    def test_dropped_ticket_holding_its_worktree_goes_stale_after_a_day(self):
        ticket, _, _ = self.ticket(1, report="dropped")
        self.store.end_ticket(ticket.id, "dropped")
        d = self.dossier(ticket)

        self.assertIn("dropped", center_model.stale_reason(d, center_model.last_activity(d) + timedelta(days=2)))

    def test_archived_or_stopped_ticket_is_not_stale(self):
        ticket, _, _ = self.ticket(1, report="ready")
        self.store.archive(ticket.id, "dboon", "stale")
        d = self.dossier(ticket)

        self.assertIsNone(center_model.stale_reason(d, center_model.last_activity(d) + timedelta(days=30)))

    def test_kept_ticket_is_skipped_until_it_moves_again(self):
        ticket, assignment, _ = self.ticket(1, report="ready")
        d = self.dossier(ticket)
        later = center_model.last_activity(d) + timedelta(days=1)
        center_model.keep(self.root, d)

        self.assertEqual(center_model.stale_tickets(center_model.load(self.root), self.root, later), [])

        self.store.add_input(ticket.id, "note", "one more thing")
        moved = center_model.load(self.root)
        self.assertEqual(center_model.stale_tickets(moved, self.root, later + timedelta(days=1))[0][0].id, ticket.id)


class MergeTest(Seeded):
    def with_review(self, index, url="https://github.com/o/r/pull/42"):
        ticket, assignment, _ = self.ticket(index, report="progress")
        self.store.report(assignment.id, "ready", f"PR open: {url}", evidence=[url])
        return ticket

    def dossier(self, ticket):
        return next(d for d in center_model.load(self.root).dossiers if d.id == ticket.id)

    def test_ready_with_an_open_review_waits_on_your_merge(self):
        waiting = self.dossier(self.with_review(1))
        plain = self.dossier(self.ticket(2, report="ready")[0])

        self.assertEqual(center_model.stage(waiting), "TO MERGE")
        self.assertTrue(waiting.awaiting_merge)
        self.assertEqual(center_model.stage(plain), "READY")
        self.assertFalse(plain.awaiting_merge)

    def test_review_label_names_pull_and_merge_requests(self):
        self.assertEqual(center_model.review_label("https://github.com/o/r/pull/42"), "PR #42")
        self.assertEqual(center_model.review_label("https://gitlab.com/g/p/-/merge_requests/812"), "MR !812")

    def test_waiting_merge_goes_stale_after_three_days(self):
        d = self.dossier(self.with_review(1))
        quiet = center_model.last_activity(d)

        self.assertIsNone(center_model.stale_reason(d, quiet + timedelta(days=1)))
        self.assertIn("merge", center_model.stale_reason(d, quiet + timedelta(days=4)))


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

        self.assertEqual(verbs.calls, [[str(DEEZ), "super-clanker", "tell", ticket.id, "--text=use main"]])

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

    def test_reload_keeps_the_dossier_scrolled_where_you_left_it(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        for index in range(40):
            self.store.report(assignment.id, "progress", f"step {index}")
            self.store.add_input(ticket.id, "note", f"fact {index}")
        offsets = []

        async def script(app, pilot):
            scroller = app.query_one("#dossier-scroll")
            scroller.scroll_end(animate=False)
            await pilot.pause()
            offsets.append(scroller.scroll_y)
            for _ in range(2):
                app.reload()
                await app.workers.wait_for_complete()
                await pilot.pause()
            offsets.append(scroller.scroll_y)

        self.run_app(Verbs(), script)

        self.assertGreater(offsets[0], 0)
        self.assertEqual(offsets[1], offsets[0])

    def test_picking_another_ticket_starts_its_dossier_at_the_top(self):
        first, assignment, _ = self.ticket(1, report="progress")
        for index in range(40):
            self.store.add_input(first.id, "note", f"fact {index}")
        self.ticket(2, report="progress")
        offsets = []

        async def script(app, pilot):
            app.query_one("#blotter").focus()
            scroller = app.query_one("#dossier-scroll")
            scroller.scroll_end(animate=False)
            await pilot.pause()
            await pilot.press("down")
            await pilot.pause()
            offsets.append(scroller.scroll_y)

        self.run_app(Verbs(), script)

        self.assertEqual(offsets, [0])

    def test_dossier_shows_the_answer_and_the_activity_feed(self):
        ticket, assignment, _ = self.ticket(1, report="ready")
        log = self.root / "log"
        log.mkdir(exist_ok=True)
        (log / f"{assignment.id}.json").write_text(json.dumps({"result": "Root cause: a cold-boot race."}))
        projects = self.root.parent / "projects"
        write_transcript(projects / "-w-1" / "sid-1.jsonl", [
            ("2026-11-04T06:02:00Z", [{"type": "tool_use", "name": "Grep", "input": {"pattern": "awayCoverage"}}]),
        ])
        texts = []

        async def script(app, pilot):
            texts.append(str(app.query_one("#dossier-text").render()))

        async def go():
            app = CenterApp(self.root, verb=Verbs(), deez=DEEZ, refresh_s=3600, projects=projects)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await script(app, pilot)
        asyncio.run(go())

        self.assertIn("ANSWER", texts[0])
        self.assertIn("REVIEW", texts[0])
        self.assertIn("Root cause: a cold-boot race.", texts[0])
        self.assertIn("ACTIVITY", texts[0])
        self.assertIn("awayCoverage", texts[0])
        self.assertLess(texts[0].index("ACTIVITY"), texts[0].index("REQUEST"))
        self.assertLess(texts[0].index("ANSWER"), texts[0].index("TOKENS"))

    def test_i_loads_the_ticket_into_the_prompt_and_asks_about_it(self):
        ticket, _, _ = self.ticket(1)
        verbs = Verbs()
        labels = []

        async def script(app, pilot):
            await pilot.press("i")
            await pilot.pause()
            labels.append(str(app.query_one("#prompt").render()))
            await pilot.press(*"why the race?")
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertIn(f"[task {ticket.id}]", labels[0])
        self.assertEqual(verbs.calls[0][:4], [str(DEEZ), "super-clanker", "ask", "--"])
        self.assertEqual(verbs.calls[0][4], f"About ticket {ticket.id} (slug-1): why the race?")

    def test_router_replies_wrap_inside_the_panel(self):
        self.ticket(1)
        self.store.reply("terminal:default", "finding " * 80)
        widths = []

        async def script(app, pilot):
            await pilot.pause()
            log = app.query_one("#log")
            widths.append((max(line.cell_length for line in log.lines), log.scrollable_content_region.width))

        self.run_app(Verbs(), script)

        longest, room = widths[0]
        self.assertLessEqual(longest, room)

    def test_clicking_the_router_panel_puts_you_in_the_prompt(self):
        self.ticket(1)
        self.store.reply("terminal:default", "earlier reply")
        focused = []

        async def script(app, pilot):
            app.query_one("#blotter").focus()
            await pilot.click("#log")
            await pilot.pause()
            focused.append(app.focused.id if app.focused else None)
            app.query_one("#blotter").focus()
            await pilot.click("#p-router")
            await pilot.pause()
            focused.append(app.focused.id if app.focused else None)

        self.run_app(Verbs(), script)

        self.assertEqual(focused, ["input", "input"])

    def test_blotter_and_status_show_tasks_waiting_on_your_merge(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        self.store.report(assignment.id, "ready", "PR open: https://github.com/o/r/pull/42", evidence=["https://github.com/o/r/pull/42"])
        seen = []

        async def script(app, pilot):
            table = app.query_one("#blotter")
            seen.append(" ".join(str(cell) for cell in table.get_row(ticket.id)))
            seen.append(str(app.query_one(".status").render()))

        self.run_app(Verbs(), script)

        self.assertIn("PR #42", seen[0])
        self.assertIn("⇡", seen[0])
        self.assertIn("to-merge 1", seen[1])

    def test_o_opens_the_selected_review(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        self.store.report(assignment.id, "ready", "PR open: https://github.com/o/r/pull/42", evidence=["https://github.com/o/r/pull/42"])
        opened = []

        async def go():
            app = CenterApp(self.root, verb=Verbs(), deez=DEEZ, refresh_s=3600, opener=opened.append)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await pilot.press("o")
                await pilot.pause()
        asyncio.run(go())

        self.assertEqual(opened, ["https://github.com/o/r/pull/42"])

    def test_o_without_a_review_says_so(self):
        self.ticket(1, report="progress")
        opened, logs = [], []

        async def go():
            app = CenterApp(self.root, verb=Verbs(), deez=DEEZ, refresh_s=3600, opener=opened.append)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await pilot.press("o")
                await pilot.pause()
                logs.append(app.log_text())
        asyncio.run(go())

        self.assertEqual(opened, [])
        self.assertIn("no review link", logs[0])

    def test_blotter_dossier_and_status_show_tokens_not_dollars(self):
        ticket, assignment, _ = self.ticket(1, report="progress")
        log = self.root / "log"
        log.mkdir(exist_ok=True)
        (log / f"{assignment.id}.json").write_text(json.dumps({"total_cost_usd": 4.2, "modelUsage": {
            "claude-opus-5-5": {"inputTokens": 18, "cacheCreationInputTokens": 50000,
                                "cacheReadInputTokens": 350000, "outputTokens": 6500}}}))
        seen = {}

        async def script(app, pilot):
            table = app.query_one("#blotter")
            seen["row"] = " ".join(str(cell) for cell in table.get_row(ticket.id))
            seen["header"] = " ".join(str(column.label) for column in table.columns.values())
            seen["status"] = str(app.query_one(".status").render())
            seen["dossier"] = str(app.query_one("#dossier-text").render())

        self.run_app(Verbs(), script)

        self.assertIn("TOKENS", seen["header"])
        self.assertNotIn("COST", seen["header"])
        self.assertIn("407k", seen["row"])
        self.assertNotIn("$", seen["row"])
        self.assertIn("tokens today 407k", seen["status"])
        self.assertNotIn("$", seen["status"])
        self.assertIn("TOKENS", seen["dossier"])
        self.assertIn("cache 350k", seen["dossier"])
        self.assertNotIn("$", seen["dossier"])

    def test_running_task_shows_tokens_so_far(self):
        ticket, _, _ = self.ticket(1, report="progress")
        projects = self.root.parent / "projects"
        session = projects / "-w-1" / "sid-1.jsonl"
        session.parent.mkdir(parents=True)
        session.write_text(json.dumps({"type": "assistant", "timestamp": "2026-11-04T06:05:00Z", "message": {
            "id": "m1", "content": [], "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0,
                                                 "cache_read_input_tokens": 52000, "output_tokens": 1000}}}) + "\n")
        rows = []

        async def go():
            app = CenterApp(self.root, verb=Verbs(), deez=DEEZ, refresh_s=3600, projects=projects)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                rows.append(" ".join(str(cell) for cell in app.query_one("#blotter").get_row(ticket.id)))
        asyncio.run(go())

        self.assertIn("53k", rows[0])

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


@unittest.skipUnless(TEXTUAL, "textual not installed")
class GraphTest(Seeded):
    def run_graph(self, script):
        async def go():
            app = CenterApp(self.root, verb=Verbs(), deez=DEEZ, refresh_s=3600)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await pilot.press("v", "v")
                await pilot.pause()
                await script(app, pilot)
        asyncio.run(go())

    def lines(self, app):
        return str(app.query_one("#graph").render()).splitlines()

    def test_session_card_shows_the_muted_session_id_above_the_title(self):
        self.ticket(1, text="fix tape", report="progress")
        found = []

        async def script(app, pilot):
            found.append(self.lines(app))

        self.run_graph(script)

        lines = found[0]
        title_row = next(i for i, line in enumerate(lines) if "slug 1" in line)
        column = lines[title_row].index("slug 1")
        self.assertIn("sid-1", lines[title_row - 1][column - 2:])
        self.assertIn("AGENT SESSIONS", lines[0])

    def test_every_kanban_lane_fits_on_the_header_row(self):
        self.ticket(1, report="progress")
        rows = []

        async def go():
            app = CenterApp(self.root, verb=Verbs(), deez=DEEZ, refresh_s=3600)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await pilot.press("v")
                await pilot.pause()
                kanban = app.query_one("#kanban")
                rows.append((str(kanban.render()).splitlines()[0], kanban.size.width))
        asyncio.run(go())

        header, width = rows[0]
        self.assertLessEqual(len(header), width)
        for stage in center_model.STAGES:
            self.assertIn(stage.split()[0], header)

    def test_clicking_a_session_selects_it_and_clicking_again_opens_it(self):
        first, _, _ = self.ticket(1, report="progress")
        self.ticket(2, report="progress")
        seen = []

        async def script(app, pilot):
            lines = self.lines(app)
            row = next(i for i, line in enumerate(lines) if "slug 1" in line)
            column = lines[row].index("slug 1")
            graph = app.query_one("#graph")
            offset = (column + graph.styles.padding.left, row)
            await pilot.click("#graph", offset=offset)
            await pilot.pause()
            seen.append(app.selected_id)
            await pilot.click("#graph", offset=offset)
            await pilot.pause()
            seen.append(type(app.screen).__name__)

        self.run_graph(script)

        self.assertEqual(seen, [first.id, "Zoom"])


@unittest.skipUnless(TEXTUAL, "textual not installed")
class CleanupPromptTest(Seeded):
    def run_app(self, verbs, script, days_later=2):
        async def go():
            ticket_now = center_model.load(self.root)
            moment = max(center_model.last_activity(d) for d in ticket_now.dossiers) + timedelta(days=days_later)
            app = CenterApp(self.root, verb=verbs, deez=DEEZ, refresh_s=3600, now=lambda: moment)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                await script(app, pilot)
                await app.workers.wait_for_complete()
                await pilot.pause()
        asyncio.run(go())

    def test_strip_counts_stale_tickets(self):
        self.ticket(1, report="ready")
        self.ticket(2, report="progress")
        seen = []

        async def script(app, pilot):
            seen.append(str(app.query_one("#stale-strip").render()))

        self.run_app(Verbs(), script)

        self.assertIn("1 STALE", seen[0])

    def test_archive_all_asks_first_then_archives_each(self):
        first, _, _ = self.ticket(1, report="ready")
        second, _, _ = self.ticket(2, report="ready")
        verbs = Verbs()
        before_yes = []

        async def script(app, pilot):
            await pilot.press("a")
            await pilot.pause()
            before_yes.append(list(verbs.calls))
            await pilot.press("y")

        self.run_app(verbs, script)

        self.assertEqual(before_yes, [[]])
        archived = sorted(call[3] for call in verbs.calls)
        self.assertEqual(archived, sorted([first.id, second.id]))
        self.assertEqual(verbs.calls[0][:3], [str(DEEZ), "super-clanker", "archive"])
        self.assertIn("--by", verbs.calls[0])

    def test_declining_archives_nothing(self):
        self.ticket(1, report="ready")
        verbs = Verbs()

        async def script(app, pilot):
            await pilot.press("a")
            await pilot.pause()
            await pilot.press("n")

        self.run_app(verbs, script)

        self.assertEqual(verbs.calls, [])

    def test_failed_archive_puts_the_ticket_back_in_the_strip(self):
        self.ticket(1, report="ready")
        strips = []

        def failing(argv):
            return VerbResult(argv, 1, "", "database is locked")

        async def script(app, pilot):
            await pilot.press("a")
            await pilot.pause()
            await pilot.press("y")
            await app.workers.wait_for_complete()
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()
            strips.append(str(app.query_one("#stale-strip").render()))

        self.run_app(failing, script)

        self.assertIn("1 STALE", strips[0])

    def test_review_keeps_one_and_archives_the_next(self):
        self.ticket(1, report="ready")
        self.ticket(2, report="ready")
        verbs = Verbs()
        strips = []

        async def script(app, pilot):
            await pilot.press("r")
            await pilot.pause()
            await pilot.press("k")
            await pilot.pause()
            await pilot.press("a")
            await pilot.pause()
            strips.append(str(app.query_one("#stale-strip").render()))

        self.run_app(verbs, script)

        self.assertEqual(len(verbs.calls), 1)
        self.assertEqual(verbs.calls[0][2], "archive")
        self.assertEqual(len(center_model.read_kept(self.root)), 1)


@unittest.skipUnless(TEXTUAL, "textual not installed")
class AttachmentTest(Seeded):
    def setUp(self):
        super().setUp()
        self.shots = self.root.parent / "shots"
        self.shots.mkdir()
        self.grabs = []

    def grab(self, dest):
        self.grabs.append(dest)
        path = self.shots / f"clip-{len(self.grabs)}.png"
        path.write_bytes(b"png")
        return path

    def run_app(self, verbs, script, grab=None):
        async def go():
            app = CenterApp(self.root, verb=verbs, deez=DEEZ, refresh_s=3600, grab_image=grab or self.grab)
            async with app.run_test(size=(160, 48)) as pilot:
                await pilot.pause()
                app.query_one("#input").focus()
                await script(app, pilot)
                await app.workers.wait_for_complete()
                await pilot.pause()
        asyncio.run(go())

    def test_ctrl_v_attaches_the_clipboard_image_to_the_ask(self):
        self.ticket(1)
        verbs = Verbs()
        labels = []

        async def script(app, pilot):
            await pilot.press("ctrl+v")
            await pilot.pause()
            labels.append(str(app.query_one("#prompt").render()))
            await pilot.press(*"what is this")
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertIn("[image 1]", labels[0])
        self.assertEqual(self.grabs, [self.root / "attachments"])
        text = verbs.calls[0][-1]
        self.assertTrue(text.startswith("what is this"))
        self.assertIn(str(self.shots / "clip-1.png"), text)

    def test_ctrl_v_without_an_image_says_so(self):
        verbs = Verbs()
        logs = []

        async def script(app, pilot):
            await pilot.press("ctrl+v")
            await pilot.pause()
            logs.append(app.log_text())

        self.run_app(verbs, script, grab=lambda dest: None)

        self.assertIn("no image on the clipboard", logs[0])
        self.assertEqual(verbs.calls, [])

    def test_dropped_image_path_attaches_instead_of_typing(self):
        self.ticket(1)
        shot = self.shots / "Screen Shot.png"
        shot.write_bytes(b"png")
        verbs = Verbs()
        values = []

        async def script(app, pilot):
            app.query_one("#input").post_message(events.Paste(str(shot).replace(" ", "\\ ")))
            await pilot.pause()
            values.append(app.query_one("#input").value)
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertEqual(values, [""])
        self.assertIn(str(shot.resolve()), verbs.calls[0][-1])

    def test_short_multi_line_paste_goes_into_the_box(self):
        self.ticket(1)
        verbs = Verbs()

        async def script(app, pilot):
            app.query_one("#input").post_message(events.Paste("line one\nline two\nline three"))
            await pilot.pause()
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertEqual(verbs.calls[0][-1], "line one\nline two\nline three")

    def test_long_paste_becomes_a_chip_and_is_kept_whole(self):
        self.ticket(1)
        verbs = Verbs()
        labels = []
        pasted = "\n".join(f"line {n}" for n in range(12))

        async def script(app, pilot):
            app.query_one("#input").post_message(events.Paste(pasted))
            await pilot.pause()
            labels.append(str(app.query_one("#prompt").render()))
            await pilot.press(*"see paste")
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertIn("[pasted 12 lines]", labels[0])
        self.assertIn(pasted, verbs.calls[0][-1])

    def test_single_line_paste_types_into_the_box(self):
        values = []

        async def script(app, pilot):
            app.query_one("#input").post_message(events.Paste("fix the tape"))
            await pilot.pause()
            values.append(app.query_one("#input").value)

        self.run_app(Verbs(), script)

        self.assertEqual(values, ["fix the tape"])

    def test_long_message_wraps_so_all_of_it_shows(self):
        heights = []

        async def script(app, pilot):
            await pilot.press(*("word " * 60))
            await pilot.pause()
            heights.append(app.query_one("#input").size.height)

        self.run_app(Verbs(), script)

        self.assertGreaterEqual(heights[0], 3)

    def test_ctrl_j_adds_a_line_without_sending(self):
        self.ticket(1)
        verbs = Verbs()

        async def script(app, pilot):
            await pilot.press("a", "ctrl+j", "b")
            await pilot.pause()
            await pilot.press("enter")

        self.run_app(verbs, script)

        self.assertEqual([call[-1] for call in verbs.calls], ["a\nb"])

    def test_backspace_on_an_empty_box_drops_the_last_attachment(self):
        verbs = Verbs()
        labels = []

        async def script(app, pilot):
            await pilot.press("ctrl+v")
            await pilot.press("ctrl+v")
            await pilot.press("backspace")
            await pilot.pause()
            labels.append(str(app.query_one("#prompt").render()))

        self.run_app(verbs, script)

        self.assertIn("[image 1]", labels[0])
        self.assertNotIn("[image 2]", labels[0])

    def test_images_alone_can_be_sent_and_then_clear(self):
        self.ticket(1)
        verbs = Verbs()
        labels = []

        async def script(app, pilot):
            await pilot.press("ctrl+v")
            await pilot.press("enter")
            await pilot.pause()
            labels.append(str(app.query_one("#prompt").render()))

        self.run_app(verbs, script)

        self.assertEqual(len(verbs.calls), 1)
        self.assertIn(str(self.shots / "clip-1.png"), verbs.calls[0][-1])
        self.assertNotIn("[image", labels[0])

    def test_note_carries_attachments_to_the_ticket(self):
        ticket, _, _ = self.ticket(1)
        verbs = Verbs()

        async def script(app, pilot):
            await pilot.press("ctrl+t")
            await pilot.press("ctrl+v")
            await pilot.press(*"this one")
            await pilot.press("enter")

        self.run_app(verbs, script)

        call = verbs.calls[0]
        self.assertEqual(call[2:4], ["tell", ticket.id])
        self.assertTrue(call[4].startswith("--text=this one"))
        self.assertIn(str(self.shots / "clip-1.png"), call[4])


if __name__ == "__main__":
    unittest.main()
