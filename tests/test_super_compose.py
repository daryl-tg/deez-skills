import os
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import config
from deezlib.superclanker.compose import partition, wake_prompt
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.gate import Admission
from deezlib.superclanker.store import Store

PR = "github:daryl-tg/deez-skills#7"
ADDRESSED = Admission(Strength.explicit, "addressed", "daryl-tg addressed the agent")


class ComposeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        self.config = config.load(self.root)
        self.events = 0

    def received(self, text, thread=PR, parent_id=None):
        self.events += 1
        event_id = f"evt-{self.events}"
        trigger = Trigger(
            id=trigger_id("github", event_id),
            source="github",
            source_event_id=event_id,
            thread_id=thread,
            actor="daryl-tg",
            addressed=True,
            text=text,
            parent_id=parent_id,
            received_at=f"2026-11-02T10:{self.events:02d}:00+00:00",
            meta={},
        )
        self.store.receive(trigger)
        return trigger

    def ticket_on(self, thread=PR):
        first = self.received("please fix the build", thread)
        return self.store.accept(
            first.id, "fix-build", Strength.explicit, "daryl-tg/deez-skills", [], "policy-1",
            "asked directly",
        )

    def capped(self, wake_cap_chars):
        router = replace(self.config.router, wake_cap_chars=wake_cap_chars)
        return replace(self.config, router=router)

    def queued_ids(self):
        return [trigger.id for trigger in self.store.queued()]

    def test_long_content_spills_with_pointer(self):
        long = self.received("x" * 2500)

        lines = wake_prompt([(long, ADDRESSED)], self.config, self.store).splitlines()

        self.assertIn(f"## {long.id}  github  {PR}  daryl-tg  addressed  explicit/addressed", lines)
        self.assertIn("text: " + "x" * 200 + " …[+2300 chars]", lines)
        self.assertIn(f"more: deez super-clanker show {long.id}", lines)

    def test_short_content_inlines_parent_and_thread_tickets(self):
        ticket = self.ticket_on()
        assignment = next(
            i for i, _ in self.store.show(ticket.id)["related"] if i.startswith("a_")
        )
        self.store.report(assignment, "ready", "diff at " + "y" * 80)
        parent = self.received("the original question")
        reply = self.received("and the answer", parent_id=parent.id)

        lines = wake_prompt([(reply, ADDRESSED)], self.config, self.store).splitlines()

        self.assertIn("text: and the answer", lines)
        self.assertIn("parent: the original question", lines)
        self.assertIn(
            f'tickets on thread: {ticket.id} open · last report: ready "diff at '
            + "y" * 52 + '…"',
            lines,
        )
        self.assertIn("accept mode: observe · policy version: unset · rules: (none)", lines)
        self.assertIn("batch: 1 trigger", lines)

    def test_subscribed_thread_trigger_is_not_in_router_batch(self):
        ticket = self.ticket_on()
        followup = self.received("also update the changelog")
        elsewhere = self.received("new request", thread="github:daryl-tg/deez-skills#8")

        router_batch, fanout = partition([followup, elsewhere], self.store)

        self.assertEqual([t.id for t in router_batch], [elsewhere.id])
        self.assertEqual(
            {k: [t.id for t in ts] for k, ts in fanout.items()}, {ticket.id: [followup.id]}
        )
        prompt = wake_prompt([(t, ADDRESSED) for t in router_batch], self.config, self.store)
        self.assertNotIn(followup.id, prompt)
        self.assertIn(f"## {elsewhere.id}  ", prompt)

    def test_terminal_asks_go_to_the_router_not_the_open_terminal_tickets(self):
        ticket = self.ticket_on("terminal:default")
        ask = replace(self.received("start a new task", "terminal:default"), source="terminal")

        router_batch, fanout = partition([ask], self.store)

        self.assertEqual(([t.id for t in router_batch], fanout), ([ask.id], {}))
        self.assertIsNotNone(ticket)

    def test_stop_on_subscribed_thread_reaches_router_too(self):
        ticket = self.ticket_on()
        stop = self.received("  STOP this, wrong repo ")
        bare = self.received("stop")
        stopwatch = self.received("stopwatch is broken")

        router_batch, fanout = partition([stop, bare, stopwatch], self.store)

        self.assertEqual([t.id for t in router_batch], [stop.id, bare.id])
        self.assertEqual([t.id for t in fanout[ticket.id]], [stop.id, bare.id, stopwatch.id])

    def test_person_stopped_or_context_only_ticket_leaves_thread_to_router(self):
        stopped = self.ticket_on()
        self.store.stop(stopped.id, "daryl-tg", "not needed")
        watcher = self.ticket_on("github:daryl-tg/deez-skills#9")
        self.store.subscribe(watcher.id, PR, context_only=True)
        followup = self.received("one more thing")

        router_batch, fanout = partition([followup], self.store)

        self.assertEqual(([t.id for t in router_batch], fanout), ([followup.id], {}))

    def test_fanned_out_and_decided_triggers_leave_the_queue(self):
        ticket = self.ticket_on()
        ignored = self.received("thanks!")
        self.store.ignore(ignored.id, "small talk")
        fanned = self.received("also the docs")
        self.store.record_fanout(fanned.id, [ticket.id])
        self.store.record_fanout(fanned.id, [ticket.id])
        waiting = self.received("a new request", thread="github:daryl-tg/deez-skills#8")
        earlier = Trigger(
            id=trigger_id("github", "late-delivery"), source="github",
            source_event_id="late-delivery", thread_id=PR, actor="daryl-tg", addressed=True,
            text="sent first, delivered last", parent_id=None,
            received_at="2026-11-02T09:00:00+00:00", meta={},
        )
        self.store.receive(earlier)

        self.assertEqual(self.queued_ids(), [earlier.id, waiting.id])

    def test_over_cap_shrinks_then_lists_also_queued(self):
        triggers = [
            self.received(f"{n}" * 300, thread=f"github:daryl-tg/deez-skills#{n}")
            for n in range(10)
        ]
        items = [(t, ADDRESSED) for t in triggers]
        full = wake_prompt(items, self.config, self.store)

        shrunk = wake_prompt(items, self.capped(3400), self.store)
        listed = wake_prompt(items, self.capped(1500), self.store)

        self.assertGreater(len(full), 3400)
        self.assertLessEqual(len(shrunk), 3400)
        self.assertNotIn("## also queued", shrunk)
        self.assertIn("text: " + "3" * 50 + " …[+250 chars]", shrunk.splitlines())

        self.assertLessEqual(len(listed), 1500)
        self.assertTrue(listed.startswith("# super-clanker wake\n"))
        self.assertIn("batch: 10 triggers", listed.splitlines())
        self.assertIn("\n## verbs\ndeez super-clanker dispatch <trigger> --slug <kebab>", listed)
        self.assertIn("deez super-clanker note <ticket> --text <text>", listed)
        blocks = re.findall(r"^## (t_[0-9a-f]{10})  ", listed, re.M)
        tail = listed.split("\n## also queued\n", 1)[1].splitlines()
        self.assertTrue(blocks)
        every_line = [
            f"{t.id} github github:daryl-tg/deez-skills#{n}" for n, t in enumerate(triggers)
        ]
        self.assertEqual(tail, every_line[len(blocks):])
        self.assertEqual(blocks, [t.id for t in triggers][: len(blocks)])
        self.assertIn("text: " + "0" * 50 + " …[+250 chars]", listed.splitlines())


class ComposeCliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = {"DEEZ_SUPER_STATE": self.tmp.name, "USER": "dboon"}

    def deez_super(self, *argv):
        out, err = StringIO(), StringIO()
        with mock.patch.dict(os.environ, self.env), redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", *argv])
        return code, out.getvalue(), err.getvalue()

    def asked(self, *argv):
        _code, out, _err = self.deez_super("ask", *argv)
        return re.match(r"trigger (t_[0-9a-f]{10}) ", out).group(1)

    def test_dry_run_writes_nothing(self):
        first = self.asked("fix the build")
        store = Store.open(self.tmp.name)
        self.addCleanup(store.close)
        ticket = store.accept(first, "fix-build", Strength.explicit, "local", [], "unset", "asked")
        stranger = Trigger(
            id=trigger_id("github", "evt-1"), source="github", source_event_id="evt-1",
            thread_id=PR, actor="someone", addressed=True, text="hi", parent_id=None,
            received_at="2026-11-02T10:00:00+00:00", meta={},
        )
        store.receive(stranger)
        followup = self.asked("also the docs")
        fresh = self.asked("--thread", "other", "a new request")
        queued_before = [t.id for t in store.queued()]

        code, printed, _ = self.deez_super("compose", "--dry-run")
        again = self.deez_super("compose", "--dry-run")

        self.assertEqual(code, 0)
        self.assertEqual(again, (0, printed, ""))
        lines = printed.splitlines()
        self.assertEqual(lines[0], f"not admitted: {stranger.id}")
        self.assertNotIn(f"fanout: {followup} → {ticket.id}", lines)
        self.assertIn(
            f"## {fresh}  terminal  terminal:other  dboon  addressed  explicit/addressed", lines
        )
        self.assertIn(f"## {followup}  terminal  terminal:default  dboon", printed)
        self.assertNotIn(f"## {stranger.id}", printed)
        self.assertEqual([t.id for t in store.queued()], queued_before)
        self.assertCountEqual(queued_before, [stranger.id, followup, fresh])

    def test_compose_without_dry_run_is_refused(self):
        self.assertEqual(
            self.deez_super("compose"),
            (2, "", "deez: compose only supports --dry-run until unit 3\n"),
        )


if __name__ == "__main__":
    unittest.main()
