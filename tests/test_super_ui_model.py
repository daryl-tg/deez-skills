import json
import os
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from deezlib.superclanker import ui_model

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


if __name__ == "__main__":
    unittest.main()
