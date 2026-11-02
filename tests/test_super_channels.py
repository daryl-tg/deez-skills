import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import channels, config, daemon
from deezlib.superclanker.domain import Trigger, trigger_id
from deezlib.superclanker.store import Store
from tests import fake_forge
from tests.test_super_daemon import FakeWake, FakeWorkers, no_reap

PR_THREAD = "gh:acme/widgets#12"
MR_THREAD = "gl:openmarketxyz/js-backend/openmarket-registry!221"
SOURCES = """\
[sources.github]
enabled = true
mode = "candidates"
senders = ["daryl-tg"]
mentions = ["@daryl-tg"]
scopes = ["acme/widgets"]

[sources.gitlab]
enabled = true
mode = "candidates"
senders = ["daryl37"]
scopes = ["openmarketxyz/js-backend/openmarket-registry"]
"""


class ChannelsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.root = self.tmp / "state"
        patcher = mock.patch.dict(os.environ, {"USER": "daryl", "DEEZ_SUPER_STATE": str(self.root)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        self.log = fake_forge.install(self)
        (self.root / "sources.toml").write_text(SOURCES, encoding="utf-8")
        self.settings = config.load(self.root)

    def thread(self, thread_id, source):
        self.store.receive(Trigger(
            trigger_id(source, thread_id), source, thread_id, thread_id, "someone", False, "hi",
            None, "2026-11-02T09:00:00+00:00", {},
        ))

    def sent(self, reply):
        return self.store.show(reply.id)["sent_at"] is not None

    def test_github_reply_posts_comment_and_marks_sent(self):
        self.thread(PR_THREAD, "github")
        self.thread("terminal:default", "terminal")
        reply = self.store.reply(PR_THREAD, "rebased onto main; build is green")
        terminal = self.store.reply("terminal:default", "for the terminal")

        lines = channels.deliver(self.store, self.settings)

        self.assertEqual(lines, [])
        self.assertEqual(fake_forge.calls(self.log), [
            ["gh", "pr", "comment", "12", "--repo", "acme/widgets", "--body",
             "rebased onto main; build is green"],
        ])
        self.assertEqual((self.sent(reply), self.sent(terminal)), (True, False))
        self.assertEqual(channels.deliver(self.store, self.settings), [])
        self.assertEqual(len(fake_forge.calls(self.log)), 1)

    def test_gitlab_reply_posts_note_and_marks_sent(self):
        self.thread(MR_THREAD, "gitlab")
        reply = self.store.reply(MR_THREAD, "split the migration into its own MR")

        lines = channels.deliver(self.store, self.settings)

        self.assertEqual(lines, [])
        self.assertEqual(fake_forge.calls(self.log), [
            ["glab", "api",
             "projects/openmarketxyz%2Fjs-backend%2Fopenmarket-registry/merge_requests/221/notes",
             "-f", "body=split the migration into its own MR"],
        ])
        self.assertTrue(self.sent(reply))

    def test_failed_post_leaves_reply_unsent_with_error_line(self):
        fixtures = self.tmp / "fixtures"
        shutil.copytree(fake_forge.FIXTURES, fixtures)
        (fixtures / "gh-pr-comment-12-acme-widgets.stderr").write_text(
            "GraphQL: Resource not accessible by integration (addComment)\n", encoding="utf-8"
        )
        self.thread(PR_THREAD, "github")
        reply = self.store.reply(PR_THREAD, "done")

        with mock.patch.dict(os.environ, {"FAKE_FORGE_FIXTURES": str(fixtures)}):
            lines = channels.deliver(self.store, self.settings)

        self.assertEqual(lines, [
            f"{reply.id}: GraphQL: Resource not accessible by integration (addComment)"
        ])
        self.assertFalse(self.sent(reply))
        self.assertEqual([r.id for r in self.store.unsent_replies()], [reply.id])

    def test_om_reply_stays_unsent_and_is_reported(self):
        self.thread("om:room1:root", "omchat")
        reply = self.store.reply("om:room1:root", "shipped")

        lines = channels.deliver(self.store, self.settings)

        self.assertEqual(lines, [f"{reply.id}: om channel not implemented"])
        self.assertFalse(self.sent(reply))
        self.assertEqual(fake_forge.calls(self.log), [])

    def test_daemon_pass_polls_due_sources_and_delivers_replies(self):
        wake, crew = FakeWake(), FakeWorkers()

        def one_pass(now):
            return daemon.one_pass(
                self.store, config.load(self.root), self.root, cli.REPO_ROOT, wake=wake,
                launch=crew.launch, resume=crew.resume, reap=no_reap, now=lambda: now,
            )

        first = one_pass("2026-11-02T10:00:00+00:00")
        self.store.reply(PR_THREAD, "looking at the build failure")
        self.store.reply(MR_THREAD, "on it")
        second = one_pass("2026-11-02T10:00:05+00:00")

        self.assertEqual((first.polled, first.errors), (8, ()))
        self.assertEqual(len(wake.batches[0]), 5)
        self.assertEqual((second.polled, second.replies_sent, second.errors), (0, 2, ()))
        self.assertEqual(self.store.unsent_replies(), [])
        listings = [call for call in fake_forge.calls(self.log) if call[1:3] == ["pr", "list"]]
        self.assertEqual(len(listings), 1)
        self.assertIn(
            ["gh", "pr", "comment", "12", "--repo", "acme/widgets", "--body",
             "looking at the build failure"],
            fake_forge.calls(self.log),
        )
        self.assertIn(" polled=8", first.line("2026-11-02T10:00:00+00:00"))
        self.assertEqual(self.store.cursor("github", "last_poll"), "2026-11-02T10:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
