import os
import re
import stat
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.store import Store, SuperError, state_root

THREAD = "github:dboon/deez-skills#12"


def github_trigger(event_id="evt-1", text="please fix the build"):
    return Trigger(
        id=trigger_id("github", event_id),
        source="github",
        source_event_id=event_id,
        thread_id=THREAD,
        actor="dboon",
        addressed=True,
        text=text,
        parent_id=None,
        received_at="2026-11-02T10:00:00+00:00",
        meta={"url": "https://github.com/dboon/deez-skills/pull/12"},
    )


def related_ids(shown):
    return [neighbour_id for neighbour_id, _summary in shown["related"]]


class SuperStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "super"
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)

    def accepted_ticket(self):
        trigger = github_trigger()
        self.store.receive(trigger)
        ticket = self.store.accept(
            trigger.id, "fix-build", Strength.explicit, "dboon/deez-skills",
            ["addressed-request"], "policy-1", "asked directly",
        )
        return trigger, ticket

    def test_state_root_honours_override_then_defaults_under_home(self):
        self.assertEqual(
            state_root({"DEEZ_SUPER_STATE": "/var/tmp/super"}, Path("/home/x")),
            Path("/var/tmp/super"),
        )
        self.assertEqual(
            state_root({}, Path("/home/x")),
            Path("/home/x/.local/state/deez-skills/super"),
        )

    def test_open_makes_a_private_directory_and_reopens_with_data(self):
        trigger = github_trigger()
        self.store.receive(trigger)
        self.store.close()

        reopened = Store.open(self.root)
        self.addCleanup(reopened.close)

        self.assertEqual(stat.S_IMODE(self.root.stat().st_mode), 0o700)
        self.assertEqual(reopened.show(trigger.id)["text"], "please fix the build")

    def test_receive_twice_stores_once(self):
        first = self.store.receive(github_trigger())
        replay = self.store.receive(github_trigger(text="the same event, replayed"))

        self.assertEqual((first, replay), ("stored", "duplicate"))
        thread = self.store.show(THREAD)
        trigger_ids = [i for i in related_ids(thread) if i.startswith("t_")]
        self.assertEqual(trigger_ids, [github_trigger().id])
        self.assertEqual(
            self.store.show(github_trigger().id)["text"], "please fix the build"
        )

    def test_accept_creates_ticket_mandate_assignment_and_subscription(self):
        trigger, ticket = self.accepted_ticket()
        again = self.store.accept(
            trigger.id, "another-slug", Strength.inferred, "elsewhere", [], "policy-2", "again",
        )

        self.assertEqual(again.id, ticket.id)
        self.assertRegex(ticket.id, r"^k_[0-9a-f]{10}$")
        shown = self.store.show(ticket.id)
        self.assertEqual(
            (shown["state"], shown["slug"], shown["thread_id"]), ("open", "fix-build", THREAD)
        )
        summaries = dict(shown["related"])
        self.assertIn(shown["mandate_id"], summaries)
        assignments = [i for i in summaries if i.startswith("a_")]
        self.assertEqual(len(assignments), 1)
        self.assertIn("pending", summaries[assignments[0]])
        self.assertIn(THREAD, summaries)
        self.assertIn("subscribed", " ".join(s for i, s in shown["related"] if i == THREAD))

        mandate = self.store.show(shown["mandate_id"])
        self.assertEqual(
            (mandate["strength"], mandate["sender"], mandate["source"], mandate["scope"]),
            ("explicit", "dboon", "github", "dboon/deez-skills"),
        )
        self.assertEqual(tuple(mandate["rules"]), ("addressed-request",))
        self.assertIsNone(mandate["withdrawn_at"])
        self.assertEqual(related_ids(mandate), [ticket.id])

        self.assertEqual(self.store.status(), [{
            "ticket": ticket.id, "state": "open", "slug": "fix-build",
            "assignment": "pending", "last_report": None, "attention": False,
        }])

    def test_show_inlines_neighbour_ids(self):
        trigger, ticket = self.accepted_ticket()

        shown_trigger = self.store.show(trigger.id)
        self.assertEqual(shown_trigger["thread_id"], THREAD)
        self.assertEqual(related_ids(shown_trigger)[0], THREAD)
        self.assertIn(ticket.id, related_ids(shown_trigger))

        shown_thread = self.store.show(THREAD)
        self.assertEqual(shown_thread["source"], "github")
        self.assertIn(ticket.id, related_ids(shown_thread))
        self.assertIn(trigger.id, related_ids(shown_thread))

        with self.assertRaises(SuperError):
            self.store.show("k_0000000000")

    def test_person_stop_withdraws_mandate(self):
        _trigger, ticket = self.accepted_ticket()

        stopped = self.store.stop(ticket.id, "dboon", "not needed any more")
        again = self.store.stop(ticket.id, "someone-else", "twice")

        self.assertEqual((stopped.state, stopped.ended_by), ("ended", "dboon"))
        self.assertEqual(again.ended_by, "dboon")
        shown = self.store.show(ticket.id)
        self.assertEqual((shown["state"], shown["ended_by"]), ("ended", "dboon"))
        self.assertIsNotNone(shown["ended_at"])
        self.assertIsNotNone(self.store.show(shown["mandate_id"])["withdrawn_at"])
        assignment = next(i for i in related_ids(shown) if i.startswith("a_"))
        self.assertEqual(self.store.show(assignment)["state"], "ended")
        self.assertEqual(self.store.status()[0]["assignment"], "ended")

    def test_waiting_report_asks_for_attention_and_ready_ends_the_assignment(self):
        _trigger, ticket = self.accepted_ticket()
        assignment = next(i for i in related_ids(self.store.show(ticket.id)) if i.startswith("a_"))

        self.store.report(assignment, "waiting", "need a call", question="Subagents or inline?")
        waiting = self.store.status()[0]
        self.store.report(assignment, "ready", "done", evidence=["bin/test passed"])
        ready = self.store.status()[0]

        self.assertEqual(
            (waiting["assignment"], waiting["last_report"], waiting["attention"]),
            ("pending", "waiting", True),
        )
        self.assertEqual(
            (ready["assignment"], ready["last_report"], ready["attention"]),
            ("ended", "ready", False),
        )
        reports = [i for i in related_ids(self.store.show(assignment)) if i.startswith("r_")]
        self.assertEqual(len(reports), 2)
        self.assertEqual(tuple(self.store.show(reports[-1])["evidence"]), ("bin/test passed",))

    def test_subscribe_converges_and_unsubscribe_removes(self):
        _trigger, ticket = self.accepted_ticket()
        other = "om:room-chat"

        self.store.subscribe(ticket.id, other, context_only=True)
        self.store.subscribe(ticket.id, other, context_only=True)
        subscribed = [s for i, s in self.store.show(ticket.id)["related"] if i == other]
        self.store.unsubscribe(ticket.id, other)
        self.store.unsubscribe(ticket.id, other)

        self.assertEqual(len(subscribed), 1)
        self.assertIn("context only", subscribed[0])
        self.assertNotIn(other, related_ids(self.store.show(ticket.id)))
        with self.assertRaises(SuperError):
            self.store.subscribe("k_0000000000", other)


class SuperCliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def deez_super(self, *argv):
        out, err = StringIO(), StringIO()
        with mock.patch.dict(os.environ, {"DEEZ_SUPER_STATE": self.tmp.name}), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", *argv])
        return code, out.getvalue(), err.getvalue()

    def test_ask_prints_the_trigger_and_show_prints_its_thread(self):
        code, asked, _ = self.deez_super("ask", "hello", "there")
        self.assertEqual(code, 0)
        match = re.fullmatch(r"trigger (t_[0-9a-f]{10}) stored on thread terminal:default\n", asked)
        self.assertIsNotNone(match, asked)

        code, shown, _ = self.deez_super("show", match.group(1))
        self.assertEqual(code, 0)
        self.assertIn("thread_id: terminal:default\n", shown)
        self.assertIn("text: hello there\n", shown)
        self.assertIn("related:\n  terminal:default  ", shown)

        self.assertEqual(self.deez_super("status")[:2], (0, "no tickets\n"))
        code, _, err = self.deez_super("show", "t_0000000000")
        self.assertEqual(code, 2)
        self.assertTrue(err.startswith("deez: "), err)

    def test_ask_on_a_named_thread(self):
        _code, asked, _ = self.deez_super("ask", "--thread", "build", "go")
        self.assertTrue(asked.endswith(" stored on thread terminal:build\n"), asked)


if __name__ == "__main__":
    unittest.main()


class RetryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Store.open(Path(self.tmp.name) / "super")
        self.addCleanup(self.store.close)
        trigger = github_trigger()
        self.store.receive(trigger)
        self.ticket = self.store.accept(
            trigger.id, "fix-build", Strength.explicit, "scope", [], "policy-1", "asked",
        )

    def test_retry_ends_stalled_assignment_and_starts_new(self):
        first = self.store.assignment_for(self.ticket.id)
        self.store.start_assignment(first.id, "sid", 4242, "/tmp/wt")
        fresh = self.store.retry(self.ticket.id)
        self.assertNotEqual(fresh.id, first.id)
        self.assertEqual(str(fresh.state), "pending")
        self.assertEqual(str(self.store.show(first.id)["state"]), "ended")
        self.assertEqual(self.store.assignment_for(self.ticket.id).id, fresh.id)

    def test_retry_refuses_ended_ticket(self):
        self.store.stop(self.ticket.id, "dboon", "no")
        with self.assertRaises(SuperError):
            self.store.retry(self.ticket.id)

    def test_inputs_lists_delivered_and_undelivered(self):
        note = self.store.add_input(self.ticket.id, "note", "repo: /r")
        self.store.mark_delivered([note.id])
        self.assertEqual([i.text for i in self.store.inputs(self.ticket.id)], ["repo: /r"])
        self.assertEqual(self.store.undelivered_inputs(self.ticket.id), [])


class RevivableTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Store.open(Path(self.tmp.name) / "super")
        self.addCleanup(self.store.close)
        trigger = github_trigger()
        self.store.receive(trigger)
        self.ticket = self.store.accept(
            trigger.id, "fix-build", Strength.explicit, "scope", [], "policy-1", "asked",
        )
        first = self.store.assignment_for(self.ticket.id)
        self.store.start_assignment(first.id, "sid", 4242, "/tmp/wt")
        self.store.report(first.id, "ready", "done")

    def test_note_alone_does_not_revive(self):
        self.store.add_input(self.ticket.id, "note", "fyi")
        self.assertEqual(self.store.revivable(), [])

    def test_person_trigger_revives(self):
        follow = github_trigger(event_id="evt-2", text="one more thing")
        self.store.receive(follow)
        self.store.add_input(self.ticket.id, "trigger", follow.id)
        self.assertEqual(self.store.revivable(), [self.ticket.id])
