import os
from dataclasses import dataclass

from rich.text import Text
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import DataTable, Input, Label

from deezlib.superclanker import procs
from deezlib.superclanker.ui_format import gb


@dataclass(frozen=True)
class MemoryRow:
    pid: int
    group: str
    rss_kb: int
    command: str

    def label(self):
        return f"{self.group:7} {self.pid:>7}  {gb(self.rss_kb):>5} GB  {self.command}"


def protect_table(table):
    return procs.protected(table, os.getpid(), procs.main_session_pids(table), procs.port_listeners())


def memory_table():
    table = DataTable(id="memory-rows", cursor_type="row")
    table.add_column("processes", key="label")
    table.show_header = False
    return table


def _group(attribution, pid):
    if attribution is None:
        return "other"
    if any(pid in pids for pids in attribution.workers.values()):
        return "worker"
    if any(pid in pids for pids in attribution.peers.values()):
        return "peer"
    return "other"


def memory_rows(snap):
    candidates = list(snap.top)
    for peer in snap.peers:
        candidates.extend(procs.child_trees(snap.table, peer.pid))
    rows = {}
    for pid, rss_kb, command in candidates:
        rows.setdefault(pid, MemoryRow(pid, _group(snap.attribution, pid), rss_kb, command))
    return list(rows.values())


class TypedNameScreen(ModalScreen):
    BINDINGS = [Binding("escape", "cancel", "cancel")]

    def __init__(self, expected, names):
        super().__init__()
        self.name_text = expected
        self.names = names

    def compose(self):
        with Vertical(id="dialog"):
            yield Label(f"This kills peer session(s): {', '.join(self.names)}", markup=False)
            yield Label(f"Type {self.name_text} to confirm", markup=False)
            yield Input(id="typed-name")

    def on_input_submitted(self, event):
        matched = event.value == self.name_text
        if not matched:
            self.app.notify("name did not match; nothing killed", severity="warning", markup=False)
        self.dismiss(matched)

    def action_cancel(self):
        self.dismiss(False)


class MemoryMixin:
    def init_memory(self, protect, kill_tree, read_table):
        self.read_table = read_table
        self.protect = protect
        self.kill_tree = kill_tree
        self.protected_pids = None
        self.protected_for = None
        self.protect_inflight = False
        self.memory_shown = None

    def refresh_protection(self):
        table = self.snap.table
        if self.protect_inflight or not table or table is self.protected_for:
            return
        self.protect_inflight = True
        self.run_worker(lambda: self.compute_protection(table), thread=True, exit_on_error=False)

    def compute_protection(self, table):
        try:
            result = self.protect(table)
        except Exception:
            result = None
        self.call_from_thread(self.protection_done, table, result)

    def protection_done(self, table, result):
        self.protect_inflight = False
        self.protected_pids = result
        self.protected_for = table
        self.refresh_protection()

    def memory_pid(self):
        table = self.query_one("#memory-rows", DataTable)
        if table.row_count == 0:
            return None
        return int(table.coordinate_to_cell_key(table.cursor_coordinate).row_key.value)

    def render_memory(self):
        rows = memory_rows(self.snap)
        if rows == self.memory_shown:
            return
        self.memory_shown = rows
        table = self.query_one("#memory-rows", DataTable)
        keep = self.memory_pid()
        table.clear()
        for row in rows:
            table.add_row(Text(row.label()), key=str(row.pid))
        if keep is not None and any(row.pid == keep for row in rows):
            table.move_cursor(row=table.get_row_index(str(keep)))

    def can_kill_memory(self):
        table = self.query_one("#memory-rows", DataTable)
        return self.focused is table and self.memory_pid() is not None

    def action_memory_kill(self):
        snap = self.snap
        pid = self.memory_pid()
        workers = set().union(*snap.attribution.workers.values()) if snap.attribution else set()
        known = self.protected_pids if self.protected_for is snap.table else None
        reason = procs.kill_refusal(snap.table, pid, known, os.getuid(), workers)
        if reason:
            self.notify(reason, severity="warning", markup=False)
            return
        target = snap.table[pid]
        members = procs.subtree(snap.table, pid)
        peers = [peer for peer in snap.peers if peer.pid in members]

        def go():
            self.run_worker(lambda: self.run_kill(target, workers), thread=True, exit_on_error=False)

        if peers:
            expected = peers[0].name if len(peers) == 1 else f"kill {len(peers)} sessions"
            names = [peer.name for peer in peers]
            self.push_screen(TypedNameScreen(expected, names), lambda matched: matched and go())
        else:
            self.ask(f"Kill {pid} {target.command} and everything under it?", go)

    def run_kill(self, target, workers):
        try:
            fresh = self.read_table()
            try:
                known = self.protect(fresh)
            except Exception:
                known = None
            reason = procs.kill_refusal(fresh, target.pid, known, os.getuid(), workers)
            killed = [] if reason else self.kill_tree(target)
        except Exception as exc:
            reason = f"kill failed: {exc}"
        if reason:
            self.call_from_thread(self.notify, reason, severity="warning", markup=False)
            return
        self.call_from_thread(self.kill_done, target, killed)

    def kill_done(self, target, killed):
        text = f"killed {len(killed)} process(es) under {target.pid}" if killed else f"{target.pid} changed; nothing killed"
        self.notify(text, markup=False)
        self.refresh_snapshot()
