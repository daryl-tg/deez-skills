import argparse
import os
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import DataTable, Footer, Input, Label, Static, TabbedContent, TabPane

from deezlib.superclanker import procs
from deezlib.superclanker.store import state_root
from deezlib.superclanker.ui_format import header_text, report_text, ticket_label
from deezlib.superclanker.ui_memory import MemoryMixin, memory_table, protect_table, read_session_peers
from deezlib.superclanker.ui_model import Cadence, attention_count, build_snapshot, needs_you_rose
from deezlib.superclanker.ui_takeover import TakeoverMixin, run_tmux
from deezlib.superclanker.workers import alive

REPO_ROOT = Path(__file__).resolve().parents[2]
VERB_TIMEOUT_S = 60
TIMEOUT_EXIT = 124
REFRESH_S = 2
LOG_REFRESH_S = 5
LOG_LINES = 80
STDERR_TAIL_LINES = 3
CONFIRMED_VERBS = ("stop", "kill", "retry", "kick")
ROUTER_LOG_KEEP = 50
STOP_WARNING = (
    "Stop {ticket}? The worktree is removed (if clean) and any process in it, "
    "a takeover session included, is killed."
)
HELP = "\n".join([
    "a ask the Router      r answer the question   n note to Worker",
    "enter show             s stop Ticket           k kill Worker",
    "t take over Ticket     x kill Memory process   Q requeue trigger",
    "R retry                K kick the daemon       e toggle ended",
    "/ filter rows          : run any verb          escape focus Tickets",
    "q quit                 ? this help",
])


@dataclass(frozen=True)
class VerbResult:
    argv: list
    returncode: int
    stdout: str
    stderr: str


def run_verb(argv):
    try:
        done = subprocess.run(
            argv, capture_output=True, text=True, timeout=VERB_TIMEOUT_S, stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return VerbResult(argv, TIMEOUT_EXIT, "", f"timed out after {VERB_TIMEOUT_S}s")
    except OSError as exc:
        return VerbResult(argv, 127, "", str(exc))
    return VerbResult(argv, done.returncode, done.stdout or "", done.stderr or "")


class PromptScreen(ModalScreen):
    BINDINGS = [Binding("escape", "cancel", "cancel")]

    def __init__(self, title, value=""):
        super().__init__()
        self.title_text = title
        self.value = value

    def compose(self):
        with Vertical(id="dialog"):
            yield Label(self.title_text, markup=False)
            yield Input(value=self.value, id="prompt")

    def on_input_submitted(self, event):
        self.dismiss(event.value.strip() or None)

    def action_cancel(self):
        self.dismiss(None)


class ConfirmScreen(ModalScreen):
    BINDINGS = [
        Binding("y", "yes", "yes"),
        Binding("n,escape", "no", "no"),
    ]

    def __init__(self, text):
        super().__init__()
        self.text = text

    def compose(self):
        with Vertical(id="dialog"):
            yield Static(self.text, markup=False)
            yield Static("y confirm / n cancel")

    def action_yes(self):
        self.dismiss(True)

    def action_no(self):
        self.dismiss(False)


class HelpScreen(ModalScreen):
    BINDINGS = [Binding("escape,question_mark,q", "close", "close")]

    def compose(self):
        with Vertical(id="dialog"):
            yield Static(HELP)

    def action_close(self):
        self.dismiss(None)


class BoardApp(MemoryMixin, TakeoverMixin, App):
    CSS = """
    #header { height: 3; padding: 0 1; background: $boost; }
    #notice { color: $warning; padding: 0 1; }
    #rows { height: 1fr; }
    #detail { height: 12; }
    #dialog { width: 80; height: auto; padding: 1 2; border: round $accent; background: $surface; }
    PromptScreen, ConfirmScreen, HelpScreen { align: center middle; }
    """
    BINDINGS = [
        Binding("a", "ask", "ask"),
        Binding("r", "reply", "reply"),
        Binding("n", "note", "note"),
        Binding("enter", "show", "show"),
        Binding("s", "stop", "stop"),
        Binding("k", "kill", "kill"),
        Binding("t", "takeover", "takeover"),
        Binding("x", "memory_kill", "kill process"),
        Binding("R", "retry", "retry"),
        Binding("Q", "requeue", "requeue"),
        Binding("K", "kick", "kick"),
        Binding("e", "ended", "ended"),
        Binding("colon", "palette", ":"),
        Binding("slash", "filter", "/ filter"),
        Binding("question_mark", "help", "? help"),
        Binding("q", "quit", "quit"),
    ]

    def __init__(self, root, *, snapshot_fn=build_snapshot, verb=run_verb,
                 deez=REPO_ROOT / "bin/deez", clock=time.monotonic, refresh_s=REFRESH_S,
                 protect=protect_table, kill_tree=procs.kill_tree, tmux=run_tmux,
                 in_tmux=lambda: "TMUX" in os.environ, bell=None, pid_alive=alive, sleep=time.sleep, read_table=procs.read_table,
                 read_peers=read_session_peers, which=shutil.which):
        super().__init__()
        self.init_memory(protect, kill_tree, read_table, read_peers)
        self.init_takeover(tmux, in_tmux, pid_alive, sleep, which)
        self.ring = bell or self.bell
        self.title_applied = "board"
        self.root = Path(root)
        self.snapshot_fn = snapshot_fn
        self.verb = verb
        self.deez = Path(deez)
        self.clock = clock
        self.refresh_s = refresh_s
        self.cadence = Cadence(clock)
        self.snap = None
        self.entries = {}
        self.show_ended = False
        self.filter_text = ""
        self.verb_log = []
        self.refreshing = False
        self.log_loaded_at = None
        self.shown = None
        self.selected = None
        self.log_inflight = False

    def compose(self):
        yield Static("", id="header", markup=False)
        yield Static("", id="notice", markup=False)
        yield DataTable(id="rows", cursor_type="row")
        with TabbedContent(id="detail"):
            with TabPane("Report", id="report"):
                yield Static("", id="report-text", markup=False)
            with TabPane("Log", id="log"):
                yield Static("", id="log-text", markup=False)
            with TabPane("Router", id="router"):
                yield Static("", id="router-text", markup=False)
                yield Input(placeholder="ask the Router", id="ask")
            with TabPane("Memory", id="memory"):
                yield memory_table()
            with TabPane("Sessions", id="sessions"):
                yield Static("", id="sessions-text", markup=False)
        yield Footer()

    def on_mount(self):
        table = self.query_one("#rows", DataTable)
        table.add_column("rows", key="label")
        table.show_header = False
        table.focus()
        self.set_interval(self.refresh_s, self.refresh_snapshot)
        self.refresh_snapshot()

    def refresh_snapshot(self):
        if self.refreshing:
            return
        self.refreshing = True
        self.run_worker(self.fetch_snapshot, thread=True, exit_on_error=False)

    def fetch_snapshot(self):
        try:
            snap = self.snapshot_fn(self.root, self.snap, self.cadence)
        except Exception as exc:
            self.call_from_thread(self.snapshot_failed, str(exc))
            return
        self.call_from_thread(self.apply_snapshot, snap)

    def snapshot_failed(self, error):
        self.refreshing = False
        self.query_one("#notice", Static).update(f"refresh failed: {error}")

    def apply_snapshot(self, snap):
        self.refreshing = False
        previous, self.snap = self.snap, snap
        self.alert(previous, snap)
        self.refresh_protection()
        self.query_one("#header", Static).update(header_text(snap))
        self.query_one("#notice", Static).update("" if snap.initialised else "daemon not initialised")
        self.render_rows()
        self.render_tabs()
        self.maybe_reload_log()

    def alert(self, previous, snap):
        if needs_you_rose(previous, snap):
            self.ring()
        count = attention_count(snap)
        title = f"board(!{count})" if count else "board"
        if title != self.title_wanted and os.environ.get("TMUX_PANE") and self.in_tmux():
            self.title_wanted = title
            self.apply_title()

    def apply_title(self):
        if self.title_busy:
            return
        self.title_busy = True
        self.run_worker(self.write_title, thread=True, exit_on_error=False)

    def write_title(self):
        try:
            while self.title_applied != self.title_wanted:
                title = self.title_wanted
                self.tmux(["tmux", "rename-window", "-t", os.environ["TMUX_PANE"], title])
                self.title_applied = title
        except Exception:
            self.title_wanted = self.title_applied
        finally:
            self.call_from_thread(self.title_idle)

    def title_idle(self):
        self.title_busy = False
        if self.title_applied != self.title_wanted:
            self.apply_title()

    def visible_entries(self):
        snap = self.snap
        needs = [("ticket", row) for row in snap.rows if row.needs_you]
        for kind, items in snap.anomalies:
            needs.extend(("anomaly", (kind, refs, line)) for refs, line in items)
        tickets = [
            ("ticket", row) for row in snap.rows
            if not row.needs_you and (self.show_ended or row.state == "open")
        ]
        wanted = self.filter_text.lower()
        keep = [
            entry for entry in (*needs, *tickets)
            if wanted in self.entry_label(entry).lower()
        ]
        needs_kept = [entry for entry in keep if entry in needs]
        tickets_kept = [entry for entry in keep if entry in tickets]
        shown = []
        if needs_kept:
            shown.append(("section", "NEEDS YOU"))
            shown.extend(needs_kept)
        shown.append(("section", "TICKETS"))
        shown.extend(tickets_kept)
        return shown

    def entry_label(self, entry):
        kind, value = entry
        if kind == "ticket":
            label = ticket_label(value) + (" (taken over)" if value.ticket_id in self.taken_over else "")
            return f"! {label}" if value.needs_you else label
        if kind == "anomaly":
            return f"! anomaly {value[0]}  {value[2]}"
        return value

    def render_rows(self):
        table = self.query_one("#rows", DataTable)
        previous = self.current_key()
        row_at = table.cursor_row
        table.clear()
        self.entries = {}
        for index, entry in enumerate(self.visible_entries()):
            key = f"{index}"
            self.entries[key] = entry
            table.add_row(Text(self.entry_label(entry)), key=key)
        keys = list(self.entries)
        target = next(
            (key for key in keys if self.identity(self.entries[key]) == previous and previous), None,
        )
        if target is not None:
            table.move_cursor(row=keys.index(target))
        elif keys:
            table.move_cursor(row=self.first_selectable(keys, row_at))
        self.refresh_bindings()

    def first_selectable(self, keys, preferred):
        start = min(preferred, len(keys) - 1)
        order = [*range(start, len(keys)), *range(start)]
        return next((i for i in order if self.entries[keys[i]][0] != "section"), start)

    def identity(self, entry):
        kind, value = entry
        if kind == "ticket":
            return ("ticket", value.ticket_id)
        if kind == "anomaly":
            return ("anomaly", value[0], tuple(value[1]))
        return ("section", value)

    def current_entry(self):
        table = self.query_one("#rows", DataTable)
        if not self.entries or table.row_count == 0:
            return None
        try:
            key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key.value
        except Exception:
            return None
        return self.entries.get(key)

    def current_key(self):
        entry = self.current_entry()
        return self.identity(entry) if entry else None

    def current_ticket(self):
        entry = self.current_entry()
        return entry[1] if entry and entry[0] == "ticket" else None

    def current_anomaly(self):
        entry = self.current_entry()
        return entry[1] if entry and entry[0] == "anomaly" else None

    def on_data_table_row_selected(self, event):
        if event.data_table.id == "rows" and self.current_ticket():
            self.action_show()

    def on_data_table_row_highlighted(self, event):
        if event.data_table.id != "rows":
            return
        selected = self.current_key()
        if selected != self.selected:
            self.selected = selected
            self.shown = None
            self.log_loaded_at = None
        self.refresh_bindings()
        self.render_tabs()
        self.maybe_reload_log()

    def render_tabs(self):
        snap = self.snap
        if snap is None:
            return
        row = self.current_ticket()
        pinned = self.shown if row and self.shown and self.shown[0] == row.ticket_id else None
        self.query_one("#report-text", Static).update(
            pinned[1] if pinned else report_text(row) if row else ""
        )
        self.query_one("#router-text", Static).update(
            "\n".join([snap.inbox_text.rstrip(), *self.verb_log]).strip()
        )
        self.render_memory()
        self.query_one("#sessions-text", Static).update(
            "\n".join(f"{p.name}  {p.pid}  {p.status}  {p.cwd}" for p in snap.peers) or "no peer sessions"
        )

    def maybe_reload_log(self):
        row = self.current_ticket()
        if row is None or not row.assignment_id:
            return
        if self.query_one("#detail", TabbedContent).active != "log":
            return
        now = self.clock()
        if self.log_inflight:
            return
        if self.log_loaded_at is not None and now - self.log_loaded_at < LOG_REFRESH_S:
            return
        self.log_loaded_at = now
        self.log_inflight = True
        assignment = row.assignment_id
        argv = self.argv("log", assignment, "--lines", str(LOG_LINES))
        self.run_worker(lambda: self.fetch_log(assignment, argv), thread=True, exit_on_error=False)

    def fetch_log(self, assignment, argv):
        result = self.verb(argv)
        self.call_from_thread(self.log_done, assignment, result.stdout or result.stderr)

    def log_done(self, assignment, text):
        self.log_inflight = False
        row = self.current_ticket()
        if row is not None and row.assignment_id == assignment:
            self.query_one("#log-text", Static).update(text)
        else:
            self.log_loaded_at = None
            self.maybe_reload_log()

    def on_tabbed_content_tab_activated(self, _event):
        self.log_loaded_at = None
        self.maybe_reload_log()

    def argv(self, *parts):
        return [str(self.deez), "super-clanker", *parts]

    def check_action(self, action, parameters):
        row = self.current_ticket()
        anomaly = self.current_anomaly()
        if action in ("reply", "note", "stop", "retry"):
            return row is not None and (action != "stop" or row.state == "open")
        if action in ("show", "takeover"):
            return row is not None
        if action == "memory_kill":
            return self.can_kill_memory()
        if action == "kill":
            return row is not None and row.worker_state == "running"
        if action == "requeue":
            return anomaly is not None and anomaly[0] == "undecided"
        return True

    def submit(self, argv, show_in=None):
        self.run_worker(lambda: self.execute(argv, show_in), thread=True, exit_on_error=False)

    def execute(self, argv, show_in):
        result = self.verb(argv)
        self.call_from_thread(self.verb_done, argv, result, show_in)

    def verb_done(self, argv, result, show_in):
        name = " ".join(argv[2:4])
        if result.returncode != 0:
            tail = "\n".join(result.stderr.strip().splitlines()[-STDERR_TAIL_LINES:])
            summary = f"{name}: exit {result.returncode} {tail}".strip()
            self.notify(summary, severity="error", timeout=10, markup=False)
        else:
            summary = f"{name}: ok"
            first = result.stdout.strip().splitlines()[:1]
            self.notify(" ".join([summary, *first]), markup=False)
        self.verb_log = [*self.verb_log, f"> {summary}"][-ROUTER_LOG_KEEP:]
        if show_in is not None and result.returncode == 0:
            self.shown = (show_in, result.stdout)
        self.render_tabs()
        self.refresh_snapshot()

    def confirm(self, text, argv):
        self.ask(text, lambda: self.submit(argv))

    def ask(self, text, then):
        self.push_screen(ConfirmScreen(text), lambda yes: yes and then())

    def prompt(self, title, then):
        def answered(text):
            if text:
                then(text)

        self.push_screen(PromptScreen(title), answered)

    def action_ask(self):
        self.query_one("#detail", TabbedContent).active = "router"
        self.query_one("#ask", Input).focus()

    def on_input_submitted(self, event):
        if event.input.id != "ask":
            return
        text = event.value.strip()
        if text:
            self.submit(self.argv("ask", text, "--thread", "default"))
        event.input.value = ""
        self.query_one("#rows", DataTable).focus()

    def key_escape(self):
        self.query_one("#rows", DataTable).focus()

    def action_reply(self):
        row = self.current_ticket()
        question = f" ({row.question})" if row.question else ""
        self.prompt(f"Answer for {row.ticket_id}{question}", lambda text: self.submit(
            self.argv("note", row.ticket_id, "--text", text)))

    def action_note(self):
        row = self.current_ticket()
        self.prompt(f"Note to {row.ticket_id}", lambda text: self.submit(
            self.argv("note", row.ticket_id, "--text", text)))

    def action_show(self):
        row = self.current_ticket()
        self.query_one("#detail", TabbedContent).active = "report"
        self.submit(self.argv("show", row.ticket_id), row.ticket_id)

    def action_stop(self):
        row = self.current_ticket()

        def reasoned(reason):
            self.confirm(
                STOP_WARNING.format(ticket=row.ticket_id),
                self.argv("stop", row.ticket_id, "--reason", reason, "--by", "operator"),
            )

        self.prompt(f"Reason for stopping {row.ticket_id}", reasoned)

    def action_kill(self):
        row = self.current_ticket()
        self.confirm(f"Kill the Worker {row.assignment_id}?", self.argv("kill", row.assignment_id))

    def action_retry(self):
        row = self.current_ticket()
        self.confirm(f"Retry {row.ticket_id}?", self.argv("retry", row.ticket_id))

    def action_requeue(self):
        trigger = self.current_anomaly()[1][0]
        self.submit(self.argv("requeue", trigger))

    def action_kick(self):
        self.confirm("Kick the daemon?", self.argv("kick", "daemon"))

    def action_ended(self):
        self.show_ended = not self.show_ended
        if self.snap:
            self.render_rows()

    def action_palette(self):
        def run(text):
            try:
                parts = shlex.split(text)
            except ValueError as exc:
                self.notify(f"bad command: {exc}", severity="error", markup=False)
                return
            if not parts:
                return
            argv = self.argv(*parts)
            if parts[0] in CONFIRMED_VERBS:
                self.confirm(f"Run {' '.join(parts)}?", argv)
            else:
                self.submit(argv)

        self.prompt("deez super-clanker", run)

    def action_filter(self):
        def apply(text):
            self.filter_text = "" if text == "-" else text
            if self.snap:
                self.render_rows()

        self.push_screen(PromptScreen("Filter rows (- clears)", self.filter_text), apply)

    def action_help(self):
        self.push_screen(HelpScreen())


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ui_app")
    parser.add_argument("--state", type=Path)
    args = parser.parse_args(argv)
    root = args.state or state_root(os.environ, Path.home())
    os.environ["DEEZ_SUPER_STATE"] = str(root)
    BoardApp(root).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
