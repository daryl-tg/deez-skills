import dataclasses
import importlib.util
import os
import threading
import unittest

TEXTUAL = importlib.util.find_spec("textual")

if TEXTUAL:
    from deezlib.superclanker import procs, ui_model
    from deezlib.superclanker.ui_app import BoardApp
    from tests.test_super_ui_app import Rig, settle, snapshot, ticket, toasts, until

UID = os.getuid()


def proc(pid, ppid, command, uid=UID, rss=1024):
    return procs.Proc(pid, ppid, uid, rss, command)


def memory_snapshot(**changes):
    table = {
        1: proc(1, 0, "launchd", uid=0),
        100: proc(100, 1, "node server", rss=4096),
        101: proc(101, 100, "node child", rss=2048),
        200: proc(200, 1, "claude peer", rss=8192),
        201: proc(201, 200, "peer child", rss=512),
        202: proc(202, 200, "peer other", rss=256),
        300: proc(300, 1, "worker proc", rss=100),
    }
    fields = dict(
        table=table,
        top=[(200, 8960, "claude peer"), (100, 6144, "node server")],
        peers=[ui_model.Peer("my-peer", 200, "/cwd", "busy", "s")],
        attribution=procs.attribute(table, {"k_1": [300]}, {"my-peer": 200}),
    )
    fields.update(changes)
    return snapshot([ticket("k_1")], **fields)


if TEXTUAL:
    class MemoryRig(Rig):
        def __init__(self, snap=None, protect=lambda table: set()):
            super().__init__(snap or memory_snapshot())
            self.protect = protect
            self.kills = []
            self.kill_threads = []

        def kill_tree(self, target):
            self.kills.append(target.pid)
            self.kill_threads.append(threading.get_ident())
            return [target.pid]

        def app(self, **options):
            return super().app(protect=self.protect, kill_tree=self.kill_tree, **options)


def memory_pids(app):
    table = app.query_one("#memory-rows")
    return [int(row.key.value) for row in table.ordered_rows]


async def open_memory(pilot, pid=None):
    await settle(pilot)
    pilot.app.query_one("#detail").active = "memory"
    await pilot.pause()
    if pid is not None:
        table = pilot.app.query_one("#memory-rows")
        table.move_cursor(row=table.get_row_index(str(pid)))
        await pilot.pause()


@unittest.skipUnless(TEXTUAL, "textual not installed")
class MemoryTabTest(unittest.IsolatedAsyncioTestCase):
    async def test_rows_list_top_trees_and_peer_children_once_per_pid(self):
        rig = MemoryRig()
        async with rig.app().run_test() as pilot:
            await open_memory(pilot)
            pids = memory_pids(pilot.app)
        self.assertEqual(sorted(pids), [100, 200, 201, 202])
        self.assertEqual(len(pids), len(set(pids)))

    async def test_protection_is_computed_off_the_event_loop(self):
        main = threading.get_ident()
        seen = []

        def protect(table):
            seen.append(threading.get_ident())
            return set()

        rig = MemoryRig(protect=protect)
        async with rig.app().run_test() as pilot:
            await open_memory(pilot)
        self.assertTrue(seen)
        self.assertNotIn(main, seen)

    async def test_protection_recomputed_only_when_the_table_changes(self):
        calls = []

        def protect(table):
            calls.append(table)
            return set()

        rig = MemoryRig(protect=protect)
        async with rig.app().run_test() as pilot:
            await open_memory(pilot)
            pilot.app.apply_snapshot(rig.snap)
            await settle(pilot)
            self.assertEqual(len(calls), 1)
            pilot.app.apply_snapshot(dataclasses.replace(rig.snap, table=dict(rig.snap.table)))
            await settle(pilot)
        self.assertEqual(len(calls), 2)

    async def test_memory_table_highlights_do_not_redraw_the_tabs(self):
        rig = MemoryRig()
        renders = []
        original = BoardApp.render_tabs

        def counted(app):
            renders.append(1)
            original(app)

        async with rig.app().run_test() as pilot:
            await open_memory(pilot)
            BoardApp.render_tabs = counted
            try:
                table = pilot.app.query_one("#memory-rows")
                for index in range(table.row_count):
                    table.move_cursor(row=index)
                    await settle(pilot)
                before = len(renders)
                await settle(pilot)
                await settle(pilot)
            finally:
                BoardApp.render_tabs = original
        self.assertEqual(len(renders), 0)
        self.assertEqual(before, 0)

    async def test_memory_kill_child_needs_y(self):
        rig = MemoryRig()
        async with rig.app().run_test() as pilot:
            await open_memory(pilot, 201)
            await pilot.press("x")
            await settle(pilot)
            await pilot.press("n")
            await settle(pilot)
            self.assertEqual(rig.kills, [])
            await pilot.press("x")
            await pilot.press("y")
            await settle(pilot)
            await until(pilot, lambda: rig.kills)
        self.assertEqual(rig.kills, [201])
        self.assertNotIn(threading.get_ident(), rig.kill_threads)

    async def test_memory_kill_peer_session_needs_typed_name(self):
        rig = MemoryRig()
        async with rig.app().run_test() as pilot:
            await open_memory(pilot, 200)
            await pilot.press("x")
            await settle(pilot)
            await pilot.press("y")
            await settle(pilot)
            self.assertEqual(rig.kills, [])
            await pilot.press(*"wrong")
            await pilot.press("enter")
            await settle(pilot)
            self.assertEqual(rig.kills, [])
            await pilot.press("x")
            await settle(pilot)
            await pilot.press(*"my-peer")
            await pilot.press("enter")
            await settle(pilot)
            await until(pilot, lambda: rig.kills)
        self.assertEqual(rig.kills, [200])

    async def test_memory_kill_protected_shows_reason(self):
        rig = MemoryRig(protect=lambda table: {101})
        async with rig.app().run_test() as pilot:
            await open_memory(pilot, 100)
            await pilot.press("x")
            await settle(pilot)
            self.assertIn("protected", toasts(pilot.app))
            self.assertEqual(len(pilot.app.screen_stack), 1)
        self.assertEqual(rig.kills, [])

    async def test_memory_kill_refused_when_protection_unavailable(self):
        rig = MemoryRig(protect=lambda table: None)
        async with rig.app().run_test() as pilot:
            await open_memory(pilot, 201)
            await pilot.press("x")
            await settle(pilot)
            self.assertIn("protection unavailable", toasts(pilot.app))
            self.assertEqual(len(pilot.app.screen_stack), 1)
        self.assertEqual(rig.kills, [])

    async def test_memory_kill_refused_for_other_users_process(self):
        snap = memory_snapshot()
        table = dict(snap.table)
        table[100] = proc(100, 1, "node server", uid=UID + 1)
        rig = MemoryRig(dataclasses.replace(snap, table=table))
        async with rig.app().run_test() as pilot:
            await open_memory(pilot, 100)
            await pilot.press("x")
            await settle(pilot)
            self.assertIn("another user's process", toasts(pilot.app))
        self.assertEqual(rig.kills, [])

    async def test_command_text_is_not_markup(self):
        text = "bad [/x] [b]cmd"
        snap = memory_snapshot(top=[(100, 6144, text)])
        table = dict(snap.table)
        table[100] = proc(100, 1, text)
        rig = MemoryRig(dataclasses.replace(snap, table=table))
        async with rig.app().run_test() as pilot:
            await open_memory(pilot, 100)
            cells = " ".join(str(cell) for cell in pilot.app.query_one("#memory-rows").get_row_at(0))
        self.assertIn(text, cells)


if __name__ == "__main__":
    unittest.main()
