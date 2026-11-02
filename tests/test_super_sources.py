import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from deezlib.superclanker import config, sources
from deezlib.superclanker.domain import trigger_id
from deezlib.superclanker.sources import github, gitlab, omchat
from deezlib.superclanker.store import Store, SuperError
from tests import fake_forge

PR_THREAD = "gh:acme/widgets#12"
MR_THREAD = "gl:openmarketxyz/js-backend/openmarket-registry!221"
NOW = "2026-11-02T10:00:00+00:00"
GITHUB = """\
[sources.github]
enabled = true
mode = "candidates"
senders = ["daryl-tg"]
mentions = ["@daryl-tg", "@super-clanker"]
scopes = ["acme/widgets"]
poll_seconds = 60
"""
GITLAB = """\
[sources.gitlab]
enabled = true
mode = "candidates"
senders = ["daryl37"]
mentions = ["@daryl37"]
scopes = ["openmarketxyz/js-backend/openmarket-registry"]
"""


class SourcesTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "state"
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        self.log = fake_forge.install(self)

    def policy(self, name, text):
        (self.root / "sources.toml").write_text(text, encoding="utf-8")
        return config.load(self.root).policy(name)

    def poll_github(self, now=NOW):
        return github.poll(self.store, self.policy("github", GITHUB), now=lambda: now)

    def poll_gitlab(self, text=GITLAB):
        return gitlab.poll(self.store, self.policy("gitlab", text), now=lambda: NOW)

    def by_event(self, triggers):
        return {trigger.source_event_id: trigger for trigger in triggers}

    def test_review_comment_becomes_trigger_on_pr_thread(self):
        polled = self.by_event(self.poll_github())

        comment = polled["comment:1001"]
        self.assertEqual(
            (comment.id, comment.source, comment.thread_id, comment.actor, comment.text,
             comment.parent_id, comment.received_at),
            (trigger_id("github", "comment:1001"), "github", PR_THREAD, "rev-alice",
             "[src/io.py] this leaks a handle", None, "2026-11-02T09:11:00Z"),
        )
        self.assertEqual(comment.meta, {
            "pr": 12, "repo": "acme/widgets",
            "url": "https://github.com/acme/widgets/pull/12#discussion_r1001",
            "thread": "PRRT_t1", "resolved": False,
        })
        review = polled["review:rev-alice:2026-11-02T09:10:00Z"]
        self.assertEqual(
            (review.actor, review.text, review.thread_id),
            ("rev-alice", "review CHANGES_REQUESTED: needs a test", PR_THREAD),
        )
        conversation = polled["issuecomment:IC_kw1"]
        self.assertEqual(
            (conversation.actor, conversation.text, conversation.meta["url"]),
            ("rev-carol", "@super-clanker can you rebase this?",
             "https://github.com/acme/widgets/pull/12#issuecomment-1"),
        )
        self.assertEqual(self.store.show(PR_THREAD)["source"], "github")
        self.assertEqual(self.store.show(comment.id)["text"], "[src/io.py] this leaks a handle")

    def test_own_comment_dropped(self):
        polled = self.poll_github()

        self.assertEqual(sorted(trigger.source_event_id for trigger in polled), [
            "check:12:build:FAILURE:2026-11-02T09:05:00Z",
            "check:12:ci/legacy:SUCCESS:",
            "comment:1001",
            "comment:1003",
            "issuecomment:IC_kw1",
            "review:rev-alice:2026-11-02T09:10:00Z",
        ])
        self.assertNotIn("daryl-tg", {trigger.actor for trigger in polled})

    def test_mention_in_body_makes_trigger_addressed(self):
        polled = self.by_event(self.poll_github())

        addressed = {event: trigger.addressed for event, trigger in polled.items()}
        self.assertEqual(addressed, {
            "comment:1001": False,
            "comment:1003": True,
            "issuecomment:IC_kw1": True,
            "review:rev-alice:2026-11-02T09:10:00Z": False,
            "check:12:build:FAILURE:2026-11-02T09:05:00Z": False,
            "check:12:ci/legacy:SUCCESS:": False,
        })

    def test_ci_failure_is_trigger_without_sender(self):
        polled = self.by_event(self.poll_github())

        failure = polled["check:12:build:FAILURE:2026-11-02T09:05:00Z"]
        self.assertEqual(
            (failure.actor, failure.addressed, failure.text, failure.thread_id),
            (None, False, "CI build FAILURE on daryl/fix-build", PR_THREAD),
        )
        self.assertEqual(polled["check:12:ci/legacy:SUCCESS:"].text,
                         "CI ci/legacy SUCCESS on daryl/fix-build")

    def test_cursor_prevents_replay(self):
        first = self.poll_github("2026-11-02T10:00:00+00:00")
        second = self.poll_github("2026-11-02T10:05:00+00:00")

        self.assertEqual((len(first), second), (6, []))
        self.assertEqual(len(self.store.show(PR_THREAD)["related"]), 6)
        self.assertEqual(self.store.cursor("github", "last_poll"), "2026-11-02T10:05:00+00:00")

    def test_thread_followup_sets_parent_to_first_comment(self):
        polled = self.by_event(self.poll_github())

        self.assertEqual(polled["comment:1003"].parent_id, trigger_id("github", "comment:1001"))
        self.assertEqual(polled["comment:1003"].meta["thread"], "PRRT_t1")
        self.assertIsNone(polled["issuecomment:IC_kw1"].parent_id)

    def test_gitlab_note_and_pipeline_become_triggers_on_mr_thread(self):
        polled = self.by_event(self.poll_gitlab())

        self.assertEqual(sorted(polled), ["note:501", "pipeline:9001:failed"])
        note = polled["note:501"]
        self.assertEqual(
            (note.source, note.thread_id, note.actor, note.addressed, note.text, note.received_at),
            ("gitlab", MR_THREAD, "rev-dana", True, "@daryl37 please split the migration out",
             "2026-11-02T08:00:00.000Z"),
        )
        self.assertEqual(note.meta, {
            "project_id": 77, "iid": 221,
            "web_url": "https://gitlab.com/openmarketxyz/js-backend/openmarket-registry/-/merge_requests/221",
        })
        pipeline = polled["pipeline:9001:failed"]
        self.assertEqual(
            (pipeline.actor, pipeline.addressed, pipeline.text, pipeline.thread_id),
            (None, False, "CI pipeline failed on daryl/registry-fix", MR_THREAD),
        )
        called = " ".join(" ".join(call) for call in fake_forge.calls(self.log))
        self.assertNotIn("projects/88", called)

    def test_gitlab_system_notes_skipped(self):
        polled = self.poll_gitlab()

        self.assertNotIn("note:502", {trigger.source_event_id for trigger in polled})
        self.assertNotIn("added 1 commit", {trigger.text for trigger in polled})

    def test_gitlab_without_scopes_keeps_every_open_mr(self):
        unscoped = GITLAB.replace('scopes = ["openmarketxyz/js-backend/openmarket-registry"]\n', "")

        polled = self.poll_gitlab(unscoped)

        self.assertEqual(polled, [])
        self.assertIn(
            "no fixture for glab-api-projects-88-merge_requests-5-notes",
            self.store.cursor("gitlab", "last_error"),
        )

    def test_omchat_unreachable_records_error_and_returns_nothing(self):
        def refused(url, timeout):
            self.assertEqual((url, timeout), ("http://127.0.0.1:31337/healthz", 2))
            raise urllib.error.URLError("connection refused")

        polled = omchat.poll(
            self.store, config.default_policy("omchat"), now=lambda: NOW, urlopen=refused,
        )

        self.assertEqual(polled, [])
        self.assertEqual(self.store.cursor("omchat", "last_error"), "om daemon unreachable")
        self.assertEqual(self.store.cursor("omchat", "last_poll"), NOW)

    def test_omchat_reachable_reports_rooms_read_not_implemented(self):
        healthy = mock.MagicMock()

        polled = omchat.poll(
            self.store, config.default_policy("omchat"), now=lambda: NOW,
            urlopen=lambda url, timeout: healthy,
        )

        self.assertEqual(polled, [])
        self.assertEqual(
            self.store.cursor("omchat", "last_error"),
            "om rooms read not implemented; see openapi.json",
        )

    def test_poller_tool_failure_records_last_error_and_does_not_raise(self):
        empty = Path(tempfile.mkdtemp())
        self.addCleanup(empty.rmdir)
        with mock.patch.dict(os.environ, {"FAKE_FORGE_FIXTURES": str(empty)}):
            polled = self.poll_github()

        self.assertEqual(polled, [])
        self.assertIn(
            "no fixture for gh-pr-list-acme-widgets", self.store.cursor("github", "last_error")
        )
        self.assertEqual(self.store.cursor("github", "last_poll"), NOW)
        self.assertEqual(self.store.queued(), [])

    def test_missing_tool_records_last_error(self):
        with mock.patch.dict(os.environ, {"PATH": str(self.root)}):
            polled = self.poll_github()

        self.assertEqual(polled, [])
        self.assertIn("gh", self.store.cursor("github", "last_error"))

    def test_successful_poll_clears_last_error(self):
        empty = Path(tempfile.mkdtemp())
        self.addCleanup(empty.rmdir)
        with mock.patch.dict(os.environ, {"FAKE_FORGE_FIXTURES": str(empty)}):
            self.poll_github()

        self.poll_github("2026-11-02T10:05:00+00:00")

        self.assertEqual(self.store.cursor("github", "last_error"), "")

    def test_due_respects_poll_seconds(self):
        policy = self.policy("github", GITHUB)

        self.assertTrue(sources.due(self.store, policy, lambda: NOW))
        github.poll(self.store, policy, now=lambda: NOW)
        self.assertFalse(sources.due(self.store, policy, lambda: "2026-11-02T10:00:59+00:00"))
        self.assertTrue(sources.due(self.store, policy, lambda: "2026-11-02T10:01:00+00:00"))
        self.assertEqual(sources.POLLERS["github"], github.poll)

    def test_poll_seconds_and_mentions_are_validated(self):
        zero_cadence = GITHUB.replace("poll_seconds = 60", "poll_seconds = 0")
        bare_mention = GITHUB.replace(
            'mentions = ["@daryl-tg", "@super-clanker"]', 'mentions = "@x"'
        )
        with self.assertRaisesRegex(SuperError, r"github.poll_seconds must be a positive integer"):
            self.policy("github", zero_cadence)
        with self.assertRaisesRegex(SuperError, r"github.mentions must be a list of strings"):
            self.policy("github", bare_mention)
        defaults = config.default_policy("github")
        self.assertEqual((defaults.poll_seconds, defaults.mentions), (120, ()))


if __name__ == "__main__":
    unittest.main()
