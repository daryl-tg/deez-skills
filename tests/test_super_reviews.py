import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

from deezlib.superclanker import reviews
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.store import Store

PR = "https://github.com/openmarket-xyz/openmarket-internal/pull/2315"
MR = "https://gitlab.com/om/rooms-client/-/merge_requests/812"
NOW = datetime(2026, 11, 4, 8, 0, tzinfo=timezone.utc)


class Forge:
    def __init__(self, states=None, fail=False):
        self.states = states or {}
        self.fail = fail
        self.calls = []

    def __call__(self, argv, **kwargs):
        self.calls.append(list(argv))
        if self.fail:
            return SimpleNamespace(returncode=1, stdout="", stderr="HTTP 502")
        url = argv[3]
        state = self.states.get(url, "OPEN")
        if argv[0] == "gh":
            return SimpleNamespace(returncode=0, stdout=state + "\n", stderr="")
        return SimpleNamespace(returncode=0, stdout=json.dumps({"state": state}), stderr="")


class ReviewsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = Store.open(Path(tmp.name))
        self.addCleanup(self.store.close)

    def ticket(self, index, text=None, evidence=None, thread="terminal:default"):
        trigger = Trigger(
            id=trigger_id("terminal", f"e{index}"), source="terminal", source_event_id=f"e{index}",
            thread_id=thread, actor="dboon", addressed=True, text="do it", parent_id=None,
            received_at="2026-11-04T07:00:00+00:00", meta={},
        )
        self.store.receive(trigger)
        ticket = self.store.accept(trigger.id, f"slug-{index}", Strength.explicit, "s", [], "p", "r")
        assignment = self.store.assignment_for(ticket.id)
        self.store.start_assignment(assignment.id, "sid", 1, "/w")
        if text:
            self.store.report(assignment.id, "ready", text, evidence=evidence)
        return ticket

    def close(self, forge, now=NOW):
        return reviews.close_merged(self.store, now, run=forge)

    def test_merged_pull_request_closes_its_ticket_and_says_so(self):
        ticket = self.ticket(1, f"PR open: {PR} (ready)", [PR])
        forge = Forge({PR: "MERGED"})

        closed, errors = self.close(forge)

        self.assertEqual((closed, errors), ([ticket.id], []))
        shown = self.store.show(ticket.id)
        self.assertEqual((shown["state"], shown["ended_by"]), ("ended", "merge"))
        self.assertEqual(self.store.outcome(ticket.id), "merged")
        self.assertEqual(forge.calls[0][:3], ["gh", "pr", "view"])
        (reply,) = self.store.unsent_replies()
        self.assertEqual(reply.thread_id, "terminal:default")
        self.assertIn(PR, reply.text)

    def test_merged_review_waits_for_a_running_worker(self):
        ticket = self.ticket(1, f"PR {PR}")
        revived = self.store.retry(ticket.id)
        self.store.start_assignment(revived.id, "sid", 2, "/w")
        forge = Forge({PR: "MERGED"})

        closed, _ = self.close(forge)

        self.assertEqual(closed, [])
        self.assertEqual(self.store.show(ticket.id)["state"], "open")

        self.store.report(revived.id, "ready", "search button committed on the same branch")
        closed, _ = self.close(forge, NOW + timedelta(seconds=reviews.CHECK_SECONDS + 1))

        self.assertEqual(closed, [ticket.id])

    def test_merged_pull_request_records_its_head(self):
        ticket = self.ticket(1, f"PR {PR}")

        self.close(Forge({PR: "MERGED 4e9d500e6"}))

        self.assertEqual(self.store.merged_head(ticket.id), "4e9d500e6")
        self.assertEqual(self.store.show(ticket.id)["state"], "ended")

    def test_merge_squashes_now_or_sets_auto_merge(self):
        forge = Forge()

        reviews.merge(PR, run=forge)
        reviews.merge(PR, auto=True, run=forge)
        reviews.merge(MR, run=forge)
        reviews.merge(MR, auto=True, run=forge)

        self.assertEqual(forge.calls, [
            ["gh", "pr", "merge", PR, "--squash"],
            ["gh", "pr", "merge", PR, "--squash", "--auto"],
            ["glab", "mr", "merge", MR, "--squash", "--yes", "--auto-merge=false"],
            ["glab", "mr", "merge", MR, "--squash", "--yes", "--auto-merge"],
        ])

    def test_merge_refused_by_the_forge_says_why(self):
        with self.assertRaises(reviews.ReviewError) as caught:
            reviews.merge(PR, run=Forge(fail=True))

        self.assertIn("HTTP 502", str(caught.exception))

    def test_merged_merge_request_is_read_with_glab(self):
        ticket = self.ticket(1, f"MR {MR}")
        forge = Forge({MR: "merged"})

        closed, _ = self.close(forge)

        self.assertEqual(closed, [ticket.id])
        self.assertEqual(forge.calls[0][:3], ["glab", "mr", "view"])

    def test_open_review_and_ticket_without_one_stay_open(self):
        waiting = self.ticket(1, f"PR {PR}")
        plain = self.ticket(2, "fixed locally at abc123")
        forge = Forge()

        closed, _ = self.close(forge)

        self.assertEqual(closed, [])
        self.assertEqual(len(forge.calls), 1)
        for ticket in (waiting, plain):
            self.assertEqual(self.store.show(ticket.id)["state"], "open")

    def test_forge_threads_get_no_reply(self):
        ticket = self.ticket(1, f"PR {PR}", thread="github:openmarket-xyz/openmarket-internal#2315")

        closed, _ = self.close(Forge({PR: "MERGED"}))

        self.assertEqual(closed, [ticket.id])
        self.assertEqual(self.store.unsent_replies(), [])

    def test_checks_at_most_every_two_minutes(self):
        self.ticket(1, f"PR {PR}")
        forge = Forge()

        self.close(forge, NOW)
        self.close(forge, NOW + timedelta(seconds=60))
        self.close(forge, NOW + timedelta(seconds=reviews.CHECK_SECONDS + 1))

        self.assertEqual(len(forge.calls), 2)

    def test_forge_failure_keeps_the_ticket_and_reports_why(self):
        ticket = self.ticket(1, f"PR {PR}")

        closed, errors = self.close(Forge(fail=True))

        self.assertEqual(closed, [])
        self.assertIn("HTTP 502", errors[0])
        self.assertEqual(self.store.show(ticket.id)["state"], "open")


if __name__ == "__main__":
    unittest.main()
