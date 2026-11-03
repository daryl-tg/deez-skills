import json
import os
import tempfile
import time
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from deezlib.superclanker import ui_model
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.store import Store

NOW = datetime(2026, 11, 3, 7, 0, 0, tzinfo=timezone.utc)


def write_session(directory, name, **fields):
    body = {"pid": 1, "name": name, "cwd": "/w", "status": "idle", "sessionId": f"sid-{name}",
            "kind": "interactive"}
    body.update(fields)
    (Path(directory) / f"{name}.json").write_text(json.dumps(body), encoding="utf-8")


class TempTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)


class PeersTest(TempTest):
    def test_peers_skip_dead_malformed_and_noninteractive(self):
        write_session(self.tmp, "good", pid=11)
        write_session(self.tmp, "dead", pid=12)
        write_session(self.tmp, "sdk", pid=13, kind="sdk")
        (self.tmp / "broken.json").write_text("{nope", encoding="utf-8")
        (self.tmp / "notes.txt").write_text("{}", encoding="utf-8")

        found = ui_model.read_peers(self.tmp, alive=lambda pid: pid in (11, 13))

        self.assertEqual(found, [ui_model.Peer("good", 11, "/w", "idle", "sid-good")])

    def test_peers_sorted_by_name(self):
        write_session(self.tmp, "zed", pid=11)
        write_session(self.tmp, "abe", pid=12)
        names = [p.name for p in ui_model.read_peers(self.tmp, alive=lambda pid: True)]
        self.assertEqual(names, ["abe", "zed"])

    def test_peers_reject_group_and_bool_pids(self):
        for name, pid in (("zero", 0), ("neg", -5), ("one", 1), ("flag", True)):
            write_session(self.tmp, name, pid=pid)
        self.assertEqual(ui_model.read_peers(self.tmp, alive=lambda pid: True), [])

    def test_peers_missing_directory_is_empty(self):
        self.assertEqual(ui_model.read_peers(self.tmp / "absent", alive=lambda pid: True), [])


class InboxTest(TempTest):
    def test_inbox_reads_new_text_from_offset(self):
        path = self.tmp / "in.log"
        path.write_text("one\n", encoding="utf-8")
        text, offset = ui_model.read_inbox(path, 0)
        self.assertEqual((text, offset), ("one\n", 4))
        path.write_text("one\ntwo\n", encoding="utf-8")
        self.assertEqual(ui_model.read_inbox(path, offset), ("two\n", 8))

    def test_inbox_restarts_when_file_shrank(self):
        path = self.tmp / "in.log"
        path.write_text("new\n", encoding="utf-8")
        self.assertEqual(ui_model.read_inbox(path, 99), ("new\n", 4))

    def test_inbox_offset_is_position_after_the_read(self):
        path = self.tmp / "in.log"
        path.write_text("one\n", encoding="utf-8")
        real_open = open

        def appending_open(target, *args, **kwargs):
            stream = real_open(target, *args, **kwargs)
            with real_open(target, "ab") as extra:
                extra.write(b"late\n")
            return stream

        with mock.patch("builtins.open", appending_open):
            text, offset = ui_model.read_inbox(path, 0)
        self.assertEqual(offset, len(text.encode()))
        again, _ = ui_model.read_inbox(path, offset)
        self.assertEqual(text + again, "one\nlate\n")

    def test_inbox_first_read_starts_within_the_keep_window(self):
        path = self.tmp / "in.log"
        line = "x" * 99 + "\n"
        path.write_text(line * 2000, encoding="utf-8")
        text, offset = ui_model.read_inbox(path, 0)
        self.assertLessEqual(len(text), ui_model.INBOX_KEEP_BYTES)
        self.assertEqual(offset, path.stat().st_size)

    def test_inbox_missing_is_empty(self):
        self.assertEqual(ui_model.read_inbox(self.tmp / "absent.log", 5), ("", 0))


class HealthTest(TempTest):
    def test_daemon_health_reads_lock_and_heartbeat_age(self):
        (self.tmp / "daemon.lock.d").mkdir()
        (self.tmp / "daemon.lock.d" / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
        beat = (NOW - timedelta(seconds=7)).isoformat(timespec="seconds")
        (self.tmp / "daemon.heartbeat").write_text(beat + "\n", encoding="utf-8")

        health = ui_model.read_daemon_health(self.tmp, NOW)

        self.assertEqual(health, ui_model.DaemonHealth(os.getpid(), True, 7))

    def test_heartbeat_with_naive_timestamp_is_none(self):
        (self.tmp / "daemon.heartbeat").write_text("2026-11-03T06:59:00\n", encoding="utf-8")
        self.assertIsNone(ui_model._heartbeat_age(self.tmp, NOW))

    def test_daemon_health_without_lock(self):
        health = ui_model.read_daemon_health(self.tmp, NOW)
        self.assertEqual(health, ui_model.DaemonHealth(None, False, None))

    def test_held_parses_int_and_empty(self):
        path = self.tmp / "daemon.held"
        path.write_text("42\n", encoding="utf-8")
        self.assertEqual(ui_model.read_held(self.tmp), 42)
        path.write_text("\n", encoding="utf-8")
        self.assertIsNone(ui_model.read_held(self.tmp))
        path.unlink()
        self.assertIsNone(ui_model.read_held(self.tmp))


class HelpersTest(TempTest):
    def test_repo_of_worktree_path(self):
        root = self.tmp
        self.assertEqual(ui_model.repo_of(str(root / "worktrees" / "scratch-repo" / "k_1"), root), "scratch-repo")
        self.assertEqual(ui_model.repo_of(str(root / "work" / "k_1"), root), "-")
        self.assertEqual(ui_model.repo_of(None, root), "-")

    def test_local_midnight_utc(self):
        original = os.environ.get("TZ")

        def restore():
            if original is None:
                os.environ.pop("TZ", None)
            else:
                os.environ["TZ"] = original
            time.tzset()

        self.addCleanup(restore)
        with mock.patch.dict(os.environ, {"TZ": "Asia/Kuala_Lumpur"}):
            time.tzset()
            self.assertEqual(ui_model.local_midnight_utc(NOW), "2026-11-02T16:00:00+00:00")


PS_LINES = (
    "  100     1   501   1000 /bin/zsh\n"
    "  101   100   501   2000 claude worker\n"
    "  102   101   501   5000 node tsc\n"
    "  200     1   501   700 stray-dev-server\n"
    "  300     1   501   400 claude peer\n"
)


def fake_run(stdout=PS_LINES, calls=None):
    def run(argv, **kwargs):
        if calls is not None:
            calls.append(argv)
        return SimpleNamespace(stdout=stdout, returncode=0)
    return run


class Counter:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class Clock:
    def __init__(self):
        self.value = 1000.0

    def __call__(self):
        return self.value


def build_trigger(index):
    return Trigger(
        id=trigger_id("github", f"evt-{index}"), source="github", source_event_id=f"evt-{index}",
        thread_id=f"github:dboon/deez-skills#{index}", actor="dboon", addressed=True,
        text="please", parent_id=None, received_at="2026-11-03T06:00:00+00:00", meta={},
    )


class AssemblyTest(TempTest):
    def setUp(self):
        super().setUp()
        self.root = self.tmp / "state"
        self.sessions = self.tmp / "sessions"
        self.sessions.mkdir()
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        self.clock = Clock()
        self.cadence = ui_model.Cadence(self.clock)
        self.free = Counter(55)
        self.leftovers = Counter([])
        self.ps_calls = []

    def ticket(self, index, report=None, pid=None, worktree=None, end=None):
        trigger = build_trigger(index)
        self.store.receive(trigger)
        ticket = self.store.accept(
            trigger.id, f"slug-{index}", Strength.explicit, "dboon/deez-skills",
            ["addressed-request"], "policy-1", "asked",
        )
        assignment = self.store.assignment_for(ticket.id)
        if pid is not None:
            self.store.start_assignment(assignment.id, f"sid-{index}", pid, worktree)
        if report:
            self.store.report(assignment.id, report, f"text {index}", question="Which?")
        if end:
            self.store.end_ticket(ticket.id, end)
        return ticket

    def build(self, previous=None, **overrides):
        options = dict(
            now=lambda: NOW, run=fake_run(calls=self.ps_calls), free_pct=self.free,
            leftovers=self.leftovers, sessions_dir=self.sessions,
        )
        options.update(overrides)
        return ui_model.build_snapshot(self.root, previous, self.cadence, **options)

    def test_rows_order_needs_you_first(self):
        quiet = self.ticket(1)
        waiting = self.ticket(2, report="waiting")
        done = self.ticket(3, end="done")
        newer = self.ticket(4)

        rows = self.build().rows

        self.assertEqual([row.ticket_id for row in rows], [waiting.id, newer.id, quiet.id, done.id])
        self.assertTrue(rows[0].needs_you)
        self.assertEqual(rows[0].question, "Which?")
        self.assertEqual(rows[0].last_report, "waiting")
        self.assertFalse(rows[1].needs_you)

    def test_worker_rss_includes_reparented_leftovers(self):
        ticket = self.ticket(1, pid=101, worktree=str(self.root / "worktrees" / "scratch" / "k_1"))
        self.leftovers.result = [200]

        snapshot = self.build()

        row = snapshot.rows[0]
        self.assertEqual(row.ticket_id, ticket.id)
        self.assertEqual(row.repo, "scratch")
        self.assertEqual(row.worker_state, "running")
        self.assertEqual(row.rss_kb, 2000 + 5000 + 700)

    def test_cadence_skips_slow_probes_within_ten_seconds(self):
        self.ticket(1, pid=101, worktree=str(self.root / "w"))
        first = self.build()
        self.clock.value += 3
        self.build(first)

        self.assertEqual(self.free.calls, 1)
        self.assertEqual(self.leftovers.calls, 1)
        self.assertEqual(len(self.ps_calls), 1)

    def test_slow_probes_return_after_ten_seconds(self):
        first = self.build()
        self.clock.value += 11
        second = self.build(first)
        self.assertEqual(self.free.calls, 2)
        self.assertEqual(len(self.ps_calls), 2)
        self.assertEqual(second.free_pct, 55)

    def test_cadence_tolerates_a_timer_firing_slightly_early(self):
        clock = Clock()
        cadence = ui_model.Cadence(clock)
        self.assertTrue(cadence.due("fast", 2))
        clock.value += 1.9
        self.assertTrue(cadence.due("fast", 2))
        clock.value += 1.0
        self.assertFalse(cadence.due("fast", 2))

    def test_inbox_shrink_resets_kept_text_in_snapshot(self):
        inbox = self.root / "inbox" / "terminal-default.log"
        inbox.parent.mkdir(parents=True)
        inbox.write_text("old old old\n", encoding="utf-8")
        first = self.build()
        inbox.write_text("new\n", encoding="utf-8")
        self.clock.value += 3
        second = self.build(first)
        self.assertEqual(second.inbox_text, "new\n")

    def test_kept_inbox_text_is_bounded(self):
        inbox = self.root / "inbox" / "terminal-default.log"
        inbox.parent.mkdir(parents=True)
        line = "y" * 99 + "\n"
        inbox.write_text(line * 2000, encoding="utf-8")
        first = self.build()
        with open(inbox, "a", encoding="utf-8") as stream:
            stream.write(line * 2000)
        self.clock.value += 3
        second = self.build(first)
        self.assertLessEqual(len(first.inbox_text), ui_model.INBOX_KEEP_BYTES)
        self.assertLessEqual(len(second.inbox_text), ui_model.INBOX_KEEP_BYTES)
        self.assertTrue(second.inbox_text.endswith(line))

    def test_slow_probe_failures_only_blank_their_own_field(self):
        self.ticket(1)
        first = self.build()
        self.clock.value += 11
        broken = mock.Mock(side_effect=RuntimeError("bad config"))
        second = self.build(first, load_config=broken)
        self.assertFalse(second.stale)
        self.assertIsNone(second.error)
        self.assertEqual(second.max_running, first.max_running)
        self.assertEqual(second.anomalies, first.anomalies)
        self.clock.value += 11
        with mock.patch.object(Store, "spend_since", side_effect=RuntimeError("locked")):
            third = self.build(second)
        self.assertFalse(third.stale)
        self.assertIsNone(third.spend_today)
        with mock.patch("deezlib.superclanker.watchdog.anomalies", side_effect=RuntimeError("x")):
            self.clock.value += 11
            fourth = self.build(third)
        self.assertFalse(fourth.stale)
        self.assertEqual(fourth.anomalies, third.anomalies)

    def test_nothing_due_returns_previous_untouched(self):
        first = self.build()
        self.clock.value += 1
        self.assertIs(self.build(first), first)

    def test_missing_db_reports_not_initialised(self):
        snapshot = ui_model.build_snapshot(
            self.tmp / "absent", None, self.cadence, now=lambda: NOW, run=fake_run(),
            free_pct=self.free, leftovers=self.leftovers, sessions_dir=self.sessions,
        )
        self.assertFalse(snapshot.initialised)
        self.assertEqual(snapshot.error, "daemon not initialised")
        self.assertEqual(snapshot.rows, [])

    def test_db_error_keeps_last_snapshot_marked_stale(self):
        self.ticket(1)
        first = self.build()
        self.store.close()
        db = self.root / "super.db"
        db.unlink()
        db.mkdir()
        self.clock.value += 3

        second = self.build(first)

        self.assertTrue(second.stale)
        self.assertTrue(second.initialised)
        self.assertTrue(second.error)
        self.assertEqual(second.rows, first.rows)

    def test_db_error_without_previous_has_empty_stale_snapshot(self):
        self.store.close()
        db = self.root / "super.db"
        db.unlink()
        db.mkdir()
        snapshot = self.build()
        self.assertTrue(snapshot.stale)
        self.assertEqual(snapshot.rows, [])

    def test_free_pct_failure_is_none(self):
        self.free.result = RuntimeError("no memory_pressure")
        snapshot = self.build()
        self.assertIsNone(snapshot.free_pct)
        self.assertFalse(snapshot.stale)

    def test_needs_you_rose(self):
        self.ticket(1)
        quiet = self.build()
        self.assertFalse(ui_model.needs_you_rose(None, quiet))
        self.ticket(2, report="blocked")
        self.clock.value += 3
        loud = self.build(quiet)
        self.assertTrue(ui_model.needs_you_rose(quiet, loud))
        self.assertFalse(ui_model.needs_you_rose(loud, loud))
        self.assertFalse(ui_model.needs_you_rose(loud, quiet))
        held = replace(quiet, held=30)
        self.assertTrue(ui_model.needs_you_rose(quiet, held))
        self.assertFalse(ui_model.needs_you_rose(held, replace(quiet, held=20)))
        self.assertTrue(ui_model.needs_you_rose(held, quiet))

    def test_spend_today_uses_local_midnight(self):
        stamps = []
        def recording(store, stamp):
            stamps.append(stamp)
            return 1.5

        with mock.patch.object(Store, "spend_since", recording):
            snapshot = self.build()

        self.assertEqual(stamps, [ui_model.local_midnight_utc(NOW)])
        self.assertEqual(snapshot.spend_today, 1.5)

    def test_peers_and_inbox_flow_into_snapshot(self):
        write_session(self.sessions, "alpha", pid=os.getpid())
        inbox = self.root / "inbox" / "terminal-default.log"
        inbox.parent.mkdir(parents=True)
        inbox.write_text("hello\n", encoding="utf-8")

        first = self.build()
        inbox.write_text("hello\nagain\n", encoding="utf-8")
        self.clock.value += 3
        second = self.build(first)

        self.assertEqual([peer.name for peer in first.peers], ["alpha"])
        self.assertEqual(first.inbox_text, "hello\n")
        self.assertEqual(second.inbox_text, "hello\nagain\n")
        self.assertEqual(second.inbox_offset, 12)


if __name__ == "__main__":
    unittest.main()
