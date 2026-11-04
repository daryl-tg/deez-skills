import argparse
import getpass
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.message import Message as TextualMessage
from textual.widgets import DataTable, Label, RichLog, Static, TextArea

from deezlib import memguard
from deezlib.superclanker import center_model, clipboard
from deezlib.superclanker.center_model import STAGES, Message
from deezlib.superclanker.store import state_root
from deezlib.superclanker.ui_app import run_verb
from deezlib.superclanker.ui_launch import REPO_ROOT
from deezlib.superclanker.ui_model import read_daemon_health, read_peers

AMBER = "#FFB000"
WHITE = "#E8E8E8"
DIM = "#7A7A7A"
GREEN = "#3DDC84"
YELLOW = "#FFD84D"
RED = "#FF5252"
CYAN = "#4FC3F7"
BAND = "#1A1200"
CARD = "#111111"

KIND_COLOR = {"progress": WHITE, "waiting": YELLOW, "blocked": RED, "failed": RED, "ready": GREEN,
              "note": CYAN, "ticket": DIM, "worker": DIM}
WORKER_COLOR = {"running": GREEN, "pending": YELLOW, "ended": DIM}
SRC_SHORT = {"terminal": "term", "github": "gh", "gitlab": "gl", "omchat": "omc"}
MODES = ["TABLE", "KANBAN", "GRAPH"]
STAGE_COLOR = {"INBOX": AMBER, "QUEUED": YELLOW, "RUNNING": GREEN, "NEEDS YOU": YELLOW, "TO MERGE": CYAN,
               "READY": GREEN, "ENDED": DIM}
STAGE_GLYPH = {"INBOX": "◌", "QUEUED": "◔", "RUNNING": "▶", "NEEDS YOU": "?", "TO MERGE": "⇡", "READY": "✓",
               "ENDED": "■"}
MARKER = {"progress": ("◆", WHITE), "waiting": ("?", YELLOW), "blocked": ("✕", RED), "failed": ("✕", RED),
          "ready": ("✓", GREEN), "note": ("✉", CYAN)}
REFRESH_S = 2.0
PEERS_DIR = Path.home() / ".claude" / "sessions"


def open_in_browser(url):
    subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def utcnow():
    return datetime.now(timezone.utc)


def fit(s, n, right=False):
    s = " ".join(str(s if s is not None else "-").split())
    if len(s) > n:
        s = s[: max(n - 1, 0)] + "…"
    return s.rjust(n) if right else s.ljust(n)


def clock(dt):
    return dt.astimezone().strftime("%H:%M:%S") if dt else "-"


def short_repo(r):
    return Path(r).name if r else "-"


def tokens(count):
    return center_model.fmt_tokens(count)


def age(moment):
    if not moment:
        return "-"
    seconds = (utcnow() - moment).total_seconds()
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if seconds >= size:
            return f"{int(seconds // size)}{unit}"
    return f"{int(max(seconds, 0))}s"


def mem_text(world):
    return "-" if world.free_pct is None else f"{world.free_pct}%"


def mem_bar(world, width):
    pct = world.free_pct or 0
    return bar(pct, 100, width, GREEN if pct > 25 else RED)


def daemon_text(world, t):
    if world.daemon_ok is None:
        t.append("?", style=DIM)
    elif world.daemon_ok:
        t.append("ok", style=GREEN)
    else:
        t.append("DOWN", style=f"bold {RED}")
    if world.heartbeat_s is not None:
        t.append(f" beat {int(world.heartbeat_s)}s ago", style=DIM)


def ordered(world):
    return sorted(world.dossiers, key=lambda d: (not d.needs_you, not d.awaiting_merge, -d.created.timestamp()))


def status_text(world):
    needs = sum(1 for d in world.dossiers if d.needs_you)
    t = Text(no_wrap=True, overflow="ellipsis")
    t.append(" SUPER-CLANKER ", style=f"bold {AMBER}")
    t.append(" LIVE ", style=f"bold #000000 on {GREEN}")
    if world.error:
        t.append(f" {world.error} ", style=f"bold #000000 on {RED}")
    sep = ("  ·  ", DIM)
    t.append(*sep)
    t.append(datetime.now().strftime("%H:%M:%S"), style=f"bold {WHITE}")
    t.append(*sep)
    t.append("daemon ", style=DIM)
    daemon_text(world, t)
    t.append(*sep)
    t.append("workers ", style=DIM)
    t.append(f"{world.workers_running}/{world.max_running}", style=f"bold {GREEN if world.workers_running else DIM}")
    t.append(*sep)
    t.append("needs-you ", style=DIM)
    t.append(str(needs), style=f"bold {RED if needs else DIM}")
    t.append(*sep)
    merges = sum(1 for d in world.dossiers if d.awaiting_merge)
    t.append("to-merge ", style=DIM)
    t.append(str(merges), style=f"bold {CYAN if merges else DIM}")
    t.append(*sep)
    t.append("tokens today ", style=DIM)
    t.append(tokens(world.tokens_today), style=WHITE)
    t.append(*sep)
    t.append("mem ", style=DIM)
    t.append(f"{mem_text(world)} free", style=WHITE)
    t.append(*sep)
    t.append("peers ", style=DIM)
    t.append(str(world.peers), style=WHITE)
    return t


def legend_text(items):
    t = Text(no_wrap=True, overflow="ellipsis")
    for key, label in items:
        t.append(f" {key} ", style=f"bold reverse {AMBER}")
        t.append(f" {label} ", style=WHITE)
    return t


def stale_strip_text(stale):
    t = Text(no_wrap=True, overflow="ellipsis")
    t.append(f" {len(stale)} STALE ", style=f"bold #000000 on {RED}")
    t.append("  ")
    t.append(" A ", style=f"bold reverse {AMBER}")
    t.append(" archive all  ", style=WHITE)
    t.append(" R ", style=f"bold reverse {AMBER}")
    t.append(" review one by one  ", style=WHITE)
    names = ", ".join(f"{d.slug} ({reason})" for d, reason in stale[:3])
    t.append(names + (" …" if len(stale) > 3 else ""), style=DIM)
    return t


def stale_list_text(stale):
    t = Text()
    for d, reason in stale:
        t.append(f"{d.id}  ", style=CYAN)
        t.append(f"{fit(d.slug, 28)} ", style=WHITE)
        t.append(f"{reason}\n", style=DIM)
    return t


MAIN_KEYS = [("TAB", "PANEL"), ("↑↓←→", "MOVE"), ("V", "VIEW"), ("Z", "ZOOM"), ("N", "NEW TASK"),
             ("^T", "ASK/NOTE"), ("I", "ASK ABOUT TASK"), ("O", "OPEN PR"), ("ESC", "BLOTTER"), ("Q", "QUIT")]
ZOOM_KEYS = [("ESC", "BACK"), ("Z", "BACK"), ("↑↓←→", "MOVE"), ("Q", "QUIT")]


def attention_cell(d):
    if d.needs_you:
        return Text("!", style=f"bold {RED}")
    if d.awaiting_merge:
        return Text("⇡", style=f"bold {CYAN}")
    return Text(" ")


def report_cell(d, kind):
    if d.state == "open" and d.review_url:
        return Text(fit(center_model.review_label(d.review_url), 8), style=f"bold {CYAN}")
    return Text(fit(kind, 8), style=KIND_COLOR.get(kind, DIM))


def blotter_row(d, wide, flash):
    kind = d.last_kind or "-"
    cells = [
        attention_cell(d),
        Text(fit(d.id[2:], 10 if wide else 8), style=CYAN),
        Text(fit(d.worker_state, 7), style=WORKER_COLOR.get(d.worker_state, DIM)),
        report_cell(d, kind),
        Text(fit(d.slug, 24 if wide else 14), style=f"bold {WHITE}"),
        Text(fit(SRC_SHORT.get(d.source, d.source), 6 if wide else 4), style=DIM),
        Text(fit(short_repo(d.repo), 16 if wide else 9), style=WHITE),
        Text(fit(d.playbook or "-", 13 if wide else 8), style=WHITE),
        Text(fit(age(d.created), 4, True), style=WHITE),
    ]
    if wide:
        cells += [
            Text(fit(d.actor, 8), style=DIM),
            Text(fit(d.state, 6), style=DIM),
            Text(fit(len(d.reports), 3, True), style=WHITE),
            Text(fit(tokens(sum(turn.tokens_out for turn in d.turns)), 6, True), style=DIM),
        ]
    cells.append(Text(fit(tokens(d.tokens), 6, True), style=f"bold {WHITE}"))
    if flash:
        for c in cells:
            c.stylize("reverse")
    return cells


def fill_blotter(table, world, wide, flashing=()):
    avail = table.size.width or 60
    table.clear(columns=True)
    cols = [("!", 1), ("ID", 10 if wide else 8), ("WRK", 7), ("RPT", 8), ("SLUG", 24 if wide else 14),
            ("SRC", 6 if wide else 4), ("REPO", 16 if wide else 9), ("PLAYBOOK", 13 if wide else 8), ("AGE", 4)]
    if wide:
        cols += [("ACTOR", 8), ("STATE", 6), ("RPTS", 3), ("OUT", 6)]
    cols.append(("TOKENS", 6))
    used = sum(w + 1 for _, w in cols)
    last_w = max(12, avail - used - 1)
    for label, w in cols:
        right = label in ("AGE", "TOKENS", "OUT", "RPTS")
        table.add_column(Text(fit(label, w, right), style=f"bold {AMBER}"), width=w + 1)
    table.add_column(Text(fit("LAST REPORT", last_w), style=f"bold {AMBER}"), width=last_w + 1)
    for d in ordered(world):
        cells = blotter_row(d, wide, d.id in flashing)
        last = Text(fit(d.last_text or "-", last_w), style=KIND_COLOR.get(d.last_kind or "-", DIM))
        if d.id in flashing:
            last.stylize("reverse")
        table.add_row(*cells, last, key=d.id)


def rule(t, title, width=44):
    t.append("\n")
    t.append(f"─ {title} ", style=f"bold {AMBER}")
    t.append("─" * max(2, width - len(title) - 3) + "\n", style="#3A2A00")


def kv(t, label, value, style=WHITE):
    t.append(f"{label:<9}", style=DIM)
    t.append(f"{value}\n", style=style)


def dossier_text(d, full, activity=()):
    t = Text()
    if d is None:
        t.append("no ticket selected", style=DIM)
        return t
    kind = d.last_kind or "-"
    t.append(f"{d.id}", style=f"bold {CYAN}")
    t.append("  ")
    t.append(f"{d.slug}\n", style=f"bold {WHITE}")
    t.append(f"ticket {d.state}", style=DIM if d.state != "open" else WHITE)
    t.append("  worker ", style=DIM)
    t.append(d.worker_state, style=WORKER_COLOR.get(d.worker_state, DIM))
    t.append("  report ", style=DIM)
    t.append(kind, style=f"bold {KIND_COLOR.get(kind, DIM)}")
    t.append(f"  {d.source}/{d.actor}  age {age(d.created)}\n", style=DIM)
    if d.question:
        t.append("\n")
        t.append(" ASKS YOU ", style=f"bold #000000 on {YELLOW}")
        t.append(f" {d.question}\n", style=f"bold {YELLOW}")
    elif d.last_kind == "blocked":
        t.append("\n")
        t.append(" BLOCKED ", style=f"bold #000000 on {RED}")
        t.append(f" {d.last_text}\n", style=RED)
    t.append("\n")
    kv(t, "REVIEW", d.review_url or "none yet", f"bold {CYAN}" if d.review_url else DIM)
    rule(t, "LATEST REPORT")
    t.append(f"{kind:<9}", style=f"bold {KIND_COLOR.get(kind, DIM)}")
    t.append(f"{d.last_text or '-'}\n", style=WHITE)
    answer_text(t, d.answer, full)
    if full and d.earlier_answers:
        rule(t, f"EARLIER ANSWERS ({len(d.earlier_answers)}, newest first)")
        for earlier in reversed(d.earlier_answers):
            t.append(earlier.rstrip() + "\n\n", style="#BBBBBB")
    activity_text(t, activity, full)
    rule(t, "DETAILS")
    kv(t, "LINK", d.link or "-", CYAN if d.link else DIM)
    kv(t, "PLAYBOOK", d.playbook or "-")
    kv(t, "REPO", d.repo or "-")
    kv(t, "TREE", ("…/" + "/".join(Path(d.worktree).parts[-2:])) if d.worktree else "-")
    kv(t, "WORKER", f"{d.assignment or '-'}  sess {(d.session or '-')[:12]}  pid {d.pid or '-'}")
    rule(t, "TOKENS")
    for i, u in enumerate(d.turns):
        t.append(f"run {i:<3} ", style=DIM)
        t.append(f"{tokens(u.tokens):>6}", style=WHITE)
        t.append(f"  in {tokens(u.tokens_in)} · cache {tokens(u.tokens_cached)} · out {tokens(u.tokens_out)}", style=DIM)
        t.append(f"  {u.turns} turns  {u.model}  {u.duration_s:.0f}s\n", style=DIM)
    if d.inflight:
        t.append("running  ", style=DIM)
        t.append(f"{tokens(d.inflight):>6}", style=GREEN)
        t.append("  this run so far\n", style=DIM)
    t.append("TOTAL    ", style=f"bold {AMBER}")
    t.append(f"{tokens(d.tokens):>6}\n", style=f"bold {WHITE}")
    rule(t, "REQUEST")
    req = d.request or "-"
    t.append((req if full else req[:220] + ("…" if len(req) > 220 else "")) + "\n", style=WHITE)
    rule(t, "MANDATE")
    scope = d.scope or "-"
    t.append((scope if full else scope[:220] + ("…" if len(scope) > 220 else "")) + "\n", style=WHITE)
    rule(t, "EVIDENCE")
    for e in d.evidence or []:
        t.append(f"{e}\n", style=CYAN)
    if not d.evidence:
        t.append("none\n", style=DIM)
    rule(t, "NOTES")
    for at, txt, delivered in d.notes:
        t.append(f"{clock(at)} ", style=DIM)
        t.append("✓ " if delivered else "… ", style=GREEN if delivered else YELLOW)
        t.append(f"{txt}\n", style=WHITE)
    if not d.notes:
        t.append("none\n", style=DIM)
    if full:
        rule(t, f"REPORT HISTORY ({len(d.reports)})")
        for at, k, txt in d.reports:
            t.append(f"{clock(at)} ", style=DIM)
            t.append(f"{k:<9}", style=KIND_COLOR.get(k, DIM))
            t.append(f"{txt}\n", style=WHITE)
        rule(t, f"TIMELINE ({len(d.events)})")
        for e in sorted(d.events, key=lambda e: e.at):
            t.append(f"{clock(e.at)} ", style=DIM)
            t.append(f"{e.kind:<9}", style=KIND_COLOR.get(e.kind, DIM))
            t.append(f"{e.text}\n", style=WHITE)
    return t


ANSWER_CHARS = 1500
ACTIVITY_LINES = 30
ACTIVITY_COLOR = {"say": WHITE, "Bash": AMBER, "Read": CYAN, "Edit": GREEN, "Write": GREEN,
                  "Grep": CYAN, "Glob": CYAN, "Agent": YELLOW, "Task": YELLOW}


def answer_text(t, answer, full):
    rule(t, "ANSWER")
    if not answer:
        t.append("no answer yet\n", style=DIM)
        return
    shown = answer if full or len(answer) <= ANSWER_CHARS else answer[:ANSWER_CHARS] + "\n… z shows the rest"
    t.append(shown.rstrip() + "\n", style=WHITE)


def activity_text(t, lines, full):
    lines = list(lines)
    rule(t, f"ACTIVITY ({len(lines)})")
    if not lines:
        t.append("no transcript yet\n", style=DIM)
        return
    for line in lines if full else lines[-ACTIVITY_LINES:]:
        t.append(f"{clock(line.at)} ", style=DIM)
        t.append(f"{fit(line.kind, 6)} ", style=f"bold {ACTIVITY_COLOR.get(line.kind, DIM)}")
        t.append((line.text if full else fit(line.text, 200).rstrip()) + "\n",
                 style=WHITE if line.kind == "say" else "#BBBBBB")


def bar(n, total, width, color):
    filled = round(width * n / total) if total else 0
    t = Text()
    t.append("█" * filled, style=color)
    t.append("░" * (width - filled), style="#3A3A3A")
    return t


def system_text(world):
    t = Text(no_wrap=True, overflow="ellipsis")
    t.append(f"{'WORKERS':<9}", style=DIM)
    t.append(f"{world.workers_running}/{world.max_running}  ", style=f"bold {WHITE}")
    t.append_text(bar(world.workers_running, world.max_running, 14, GREEN))
    t.append("\n")
    t.append(f"{'TOKENS':<9}", style=DIM)
    t.append(f"{tokens(world.tokens_today)} today", style=f"bold {WHITE}")
    t.append(f"   all tasks {tokens(sum(d.tokens for d in world.dossiers))}\n", style=DIM)
    t.append(f"{'MEMORY':<9}", style=DIM)
    t.append(f"{mem_text(world)} free  ", style=f"bold {WHITE}")
    t.append_text(mem_bar(world, 14))
    t.append("\n")
    t.append(f"{'PEERS':<9}", style=DIM)
    t.append(f"{world.peers} interactive sessions\n", style=WHITE)
    t.append(f"{'DAEMON':<9}", style=DIM)
    daemon_text(world, t)
    t.append("\n")
    return t


def all_events(world):
    out = [(e, d) for d in world.dossiers for e in d.events]
    return sorted(out, key=lambda x: x[0].at, reverse=True)


def tape_text(world, limit=None):
    t = Text(no_wrap=True, overflow="ellipsis")
    for e, d in all_events(world)[:limit]:
        t.append(f"{clock(e.at)} ", style=DIM)
        t.append(f"{d.id[2:12]:<10} ", style=CYAN)
        t.append(f"{e.kind:<8} ", style=KIND_COLOR.get(e.kind, DIM))
        t.append(f"{' '.join(e.text.split())}\n", style=WHITE)
    return t


def system_compact(world):
    sep = (" │ ", "#3A2A00")
    t = Text(no_wrap=True, overflow="ellipsis")
    t.append("WORKERS ", style=DIM)
    t.append(f"{world.workers_running}/{world.max_running} ", style=f"bold {WHITE}")
    t.append_text(bar(world.workers_running, world.max_running, 8, GREEN))
    t.append(*sep)
    t.append("TOKENS ", style=DIM)
    t.append(tokens(world.tokens_today), style=f"bold {WHITE}")
    t.append(*sep)
    t.append("MEM ", style=DIM)
    t.append(f"{mem_text(world)} ", style=f"bold {WHITE}")
    t.append_text(mem_bar(world, 8))
    t.append("\n")
    t.append("PEERS ", style=DIM)
    t.append(str(world.peers), style=WHITE)
    t.append(*sep)
    t.append("DAEMON ", style=DIM)
    daemon_text(world, t)
    t.append(*sep)
    needs = sum(1 for d in world.dossiers if d.needs_you)
    t.append("NEEDS YOU ", style=DIM)
    t.append(str(needs), style=f"bold {RED if needs else DIM}")
    t.append("\n")
    t.append("─ TAPE · newest first ", style=f"bold {AMBER}")
    t.append("─" * 40 + "\n", style="#3A2A00")
    t.append_text(tape_text(world, 4))
    return t


def thread_lines(world):
    lines = []
    for m in world.threads.get("terminal:default", []):
        t = Text()
        t.append(f"{clock(m.at)} ", style=DIM)
        if m.who == "system":
            t.append(m.text, style=f"italic {DIM}")
        else:
            t.append(f"{m.who:<7}", style=f"bold {AMBER if m.who.startswith('you') else GREEN}")
            t.append(m.text, style=WHITE)
        lines.append(t)
    return lines


class KanbanView(Widget, can_focus=True):
    BINDINGS = [("left", "move(-1,0)"), ("right", "move(1,0)"), ("up", "move(0,-1)"), ("down", "move(0,1)"),
                ("enter", "open")]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.lane_off = [0] * len(STAGES)
        self.last_sel = None
        self.lane_w = 10

    def scroll_lane(self, x, d):
        i = min(len(STAGES) - 1, max(0, (x - 1) // (self.lane_w + 1)))
        self.lane_off[i] = max(0, self.lane_off[i] + d)
        self.refresh()

    def on_mouse_scroll_down(self, event):
        self.scroll_lane(event.x, 1)
        event.stop()

    def on_mouse_scroll_up(self, event):
        self.scroll_lane(event.x, -1)
        event.stop()

    def lanes(self):
        return [self.app.lane(s) for s in STAGES]

    def action_move(self, dx, dy):
        lanes = self.lanes()
        sel = self.app.selected_id
        li = ci = None
        for i, lane in enumerate(lanes):
            for j, d in enumerate(lane):
                if d.id == sel:
                    li, ci = i, j
        if li is None:
            first = next((l for l in lanes if l), None)
            if first:
                self.app.pick(first[0].id)
            return
        if dx:
            i = li + dx
            while 0 <= i < len(lanes) and not lanes[i]:
                i += dx
            if 0 <= i < len(lanes):
                self.app.pick(lanes[i][min(ci, len(lanes[i]) - 1)].id)
        elif dy:
            j = ci + dy
            if 0 <= j < len(lanes[li]):
                self.app.pick(lanes[li][j].id)

    def action_open(self):
        self.app.action_open()

    def render(self):
        w, h = self.size.width, self.size.height
        gap = 1
        lanes_n = len(STAGES)
        lw = max(8, (w - gap * (lanes_n - 1)) // lanes_n)
        lanes = self.lanes()
        sel = self.app.selected_id
        per = max(1, (h - 2) // 4)
        self.lane_w = lw
        if self.last_sel != sel:
            for i, lane in enumerate(lanes):
                idx = next((j for j, d in enumerate(lane) if d.id == sel), None)
                if idx is not None:
                    o = self.lane_off[i]
                    self.lane_off[i] = idx if idx < o else (idx - per + 1 if idx >= o + per else o)
            self.last_sel = sel
        offsets = [max(0, min(self.lane_off[i], len(lane) - per)) for i, lane in enumerate(lanes)]
        self.lane_off = offsets
        out = []
        for y in range(h):
            line = Text(no_wrap=True, overflow="crop")
            for i, stage in enumerate(STAGES):
                if i:
                    line.append(" " * gap)
                lane = lanes[i]
                if y == 0:
                    hot = stage == "NEEDS YOU" and lane
                    style = f"bold #000000 on {RED}" if hot else f"bold {AMBER} on {BAND}"
                    up = offsets[i]
                    down = max(0, len(lane) - offsets[i] - per)
                    suffix = (f"▲{up}" if up else "") + (f"▼{down}" if down else "")
                    line.append(fit(f" {stage} {len(lane)}", lw - len(suffix) - 1) + suffix + " ", style=style)
                elif y == 1:
                    line.append("─" * lw, style="#3A2A00")
                else:
                    slot, row = divmod(y - 2, 4)
                    k = slot + offsets[i]
                    if k >= len(lane):
                        line.append(fit("  —" if (slot == 0 and row == 0 and not lane) else "", lw), style=DIM)
                    elif row == 3:
                        line.append(" " * lw)
                    else:
                        line.append_text(self.card_line(lane[k], stage, row, lw, sel))
            out.append(line)
        res = Text(no_wrap=True, overflow="crop")
        for i, line in enumerate(out):
            if i:
                res.append("\n")
            res.append_text(line)
        return res

    def card_line(self, d, stage, row, lw, sel):
        app = self.app
        if d.id == sel:
            style = f"bold #000000 on {AMBER}"
        elif app.flashing(d.id):
            style = f"bold #000000 on {WHITE}"
        else:
            style = f"{WHITE} on {CARD}"
        edge_color = STAGE_COLOR[stage]
        glyph = STAGE_GLYPH[stage]
        gcolor = edge_color
        if d.last_kind == "blocked" and stage == "NEEDS YOU":
            glyph, gcolor = "✕", RED
        if row == 0:
            body = fit(f" {glyph} {d.id[2:]}", lw - 1)
        elif row == 1:
            body = fit(f"   {d.slug}", lw - 1)
        else:
            body = fit(f"   {age(app.since.get(d.id))} · {tokens(d.tokens)} tok", lw - 1)
        t = Text(no_wrap=True, overflow="crop")
        t.append("▌", style=f"{edge_color} on {CARD}" if d.id != sel and not app.flashing(d.id) else style)
        t.append(body, style=style)
        if row == 0 and d.id != sel and not app.flashing(d.id):
            t.stylize(f"bold {gcolor}", 2, 3)
            t.stylize(f"bold {CYAN}", 4, lw)
        elif row == 1 and d.id != sel and not app.flashing(d.id):
            t.stylize(f"bold {WHITE}", 1, lw)
        elif row == 2 and d.id != sel and not app.flashing(d.id):
            t.stylize(DIM, 1, lw)
        return t



OUTCOMES = [("IN FLIGHT", AMBER, "◉"), ("WAITING", YELLOW, "?"), ("BLOCKED", RED, "✕"), ("TO MERGE", CYAN, "⇡"),
            ("READY", GREEN, "✓"), ("ENDED", DIM, "■")]
OUTCOME_INDEX = {name: i for i, (name, _, _) in enumerate(OUTCOMES)}
DIR_N, DIR_S, DIR_E, DIR_W = 1, 2, 4, 8
BOX = {4: "─", 8: "─", 12: "─", 1: "│", 2: "│", 3: "│", 6: "┌", 10: "┐", 5: "└", 9: "┘", 7: "├", 11: "┤",
       14: "┬", 13: "┴", 15: "┼"}
SOURCE_ORDER = ["terminal", "github", "gitlab", "omchat"]


def dim(color, f=0.5):
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return f"#{int(r * f):02x}{int(g * f):02x}{int(b * f):02x}"


def outcome_of(app, d):
    stage = app.stage.get(d.id, "ENDED")
    if stage == "ENDED":
        return "ENDED"
    if stage in ("READY", "TO MERGE"):
        return stage
    if stage == "NEEDS YOU":
        return "BLOCKED" if d.last_kind in ("blocked", "failed") else "WAITING"
    return "IN FLIGHT"


def ticket_color(app, d):
    stage = app.stage.get(d.id, "ENDED")
    if stage == "NEEDS YOU" and d.last_kind in ("blocked", "failed"):
        return RED
    return STAGE_COLOR[stage]


def graph_order(app):
    return sorted(app.world.dossiers, key=lambda d: (OUTCOME_INDEX[outcome_of(app, d)], -app.since[d.id].timestamp()))


def route_cells(xa, y1, xend, y2):
    xt = xa + (xend - xa) // 2
    if y1 == y2:
        return [(x, y1) for x in range(xa, xend + 1)]
    step = 1 if y2 > y1 else -1
    cells = [(x, y1) for x in range(xa, xt + 1)]
    cells += [(xt, y) for y in range(y1 + step, y2 + step, step)]
    cells += [(x, y2) for x in range(xt + 1, xend + 1)]
    return cells


def place_nodes(wants, height, lo, hi):
    items = sorted(wants, key=lambda w: w[1])
    placed = []
    cursor = lo
    for key, want, h in items:
        y = max(want, cursor)
        placed.append([key, y, h])
        cursor = y + h + 1
    overflow = cursor - 1 - (hi + 1)
    if overflow > 0:
        bottom = hi + 1
        for p in reversed(placed):
            p[1] = min(p[1], bottom - p[2])
            bottom = p[1] - 1
    return {k: y for k, y, _ in placed}


CARD_ROWS = 3
CARD_GAP = 1
CARD_MAX_WIDTH = 60


def session_title(d):
    return (d.slug or d.id).replace("-", " ").strip()


def session_label(d):
    sid = d.session[:8] if d.session else "no session yet"
    return f"{sid} · {d.id}"


def session_meta(d):
    runs = len({turn.assignment for turn in d.turns}) or (1 if d.assignment else 0)
    return f"{d.worker_state} · {tokens(d.tokens)} tokens · {runs} run{'' if runs == 1 else 's'} · {age(d.created)}"


class GraphView(Widget, can_focus=True):
    BINDINGS = [("up", "move(-1)"), ("down", "move(1)"), ("enter", "open")]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.voff = 0
        self.last_sel = None
        self.hits = []

    def on_mouse_scroll_down(self, event):
        self.voff += 2
        self.refresh()
        event.stop()

    def on_mouse_scroll_up(self, event):
        self.voff = max(0, self.voff - 2)
        self.refresh()
        event.stop()

    def on_click(self, event):
        offset = event.get_content_offset(self)
        if offset is None:
            return
        hit = next((did for x0, y0, x1, y1, did in self.hits
                    if x0 <= offset.x < x1 and y0 <= offset.y < y1), None)
        if hit is None:
            return
        event.stop()
        self.focus()
        if hit == self.app.selected_id:
            self.app.action_open()
        else:
            self.app.pick(hit)

    def action_move(self, dy):
        rows = graph_order(self.app)
        if not rows:
            return
        idx = next((i for i, d in enumerate(rows) if d.id == self.app.selected_id), 0)
        self.app.pick(rows[min(max(idx + dy, 0), len(rows) - 1)].id)

    def action_open(self):
        self.app.action_open()

    def render(self):
        app = self.app
        W, H = self.size.width, self.size.height
        order = graph_order(app)
        self.hits = []
        if W < 70 or H < 8 or not order:
            return Text("")
        sel = app.selected()
        vis = H - 2
        pitch = CARD_ROWS + CARD_GAP
        ys = {d.id: i * pitch for i, d in enumerate(order)}
        total = len(order) * pitch - CARD_GAP
        idx = next((i for i, d in enumerate(order) if d.id == app.selected_id), 0)
        sy = ys[order[idx].id]
        if total <= vis:
            self.voff = 0
        else:
            if self.last_sel != app.selected_id:
                if sy < self.voff:
                    self.voff = sy
                elif sy + CARD_ROWS > self.voff + vis:
                    self.voff = sy + CARD_ROWS - vis
                self.last_sel = app.selected_id
            self.voff = max(0, min(self.voff, total - vis))
        off = self.voff
        lo, hi = off, off + min(vis, total) - 1

        widths = [12, 16, 0, 14]
        room = W - widths[0] - widths[1] - widths[3]
        widths[2] = max(30, min(CARD_MAX_WIDTH, room - 15))
        gap = max(5, (room - widths[2]) // 3)
        xs, x = [], 0
        for w in widths:
            xs.append(x)
            x += w + gap
        X_SRC, X_RT, X_SS, X_OUT = xs
        W_SRC, W_RT, W_SS, W_OUT = widths

        chars = [[" "] * W for _ in range(H)]
        styles = [[""] * W for _ in range(H)]

        def put(px, py, text, style):
            ly = py - off + 2
            if not 2 <= ly < H:
                return
            for i, ch in enumerate(text):
                if 0 <= px + i < W:
                    chars[ly][px + i] = ch
                    styles[ly][px + i] = style

        for i, title in enumerate(["SOURCES", "ROUTER", "AGENT SESSIONS", "OUTCOME"]):
            for k, ch in enumerate(title):
                if xs[i] + k < W:
                    chars[0][xs[i] + k] = ch
                    styles[0][xs[i] + k] = f"bold {AMBER}"
        for xx in range(W):
            chars[1][xx] = "─"
            styles[1][xx] = "#3A2A00"

        def title_y(d):
            return ys[d.id] + 1

        centre = (lo + hi) // 2
        router_top = max(lo, min(centre - 1, hi - 3))
        router_mid = router_top + 1

        src_groups = {}
        for d in order:
            src_groups.setdefault(d.source, []).append(d)
        src_names = [n for n in SOURCE_ORDER if n in src_groups] + [n for n in src_groups if n not in SOURCE_ORDER]
        wants = []
        for n in src_names:
            mean = sum(title_y(d) for d in src_groups[n]) / len(src_groups[n])
            wants.append((n, int(min(max(mean, lo), hi)), 1))
        src_y = place_nodes(wants, 1, lo, hi)
        out_groups = {}
        for d in order:
            out_groups.setdefault(outcome_of(app, d), []).append(d)
        wants = []
        for name, ds in out_groups.items():
            mean = sum(title_y(d) for d in ds) / len(ds)
            wants.append((name, int(min(max(mean, lo), hi)), 1))
        out_y = place_nodes(wants, 1, lo, hi)

        edges, routes = [], {}
        for n in src_names:
            cells = route_cells(X_SRC + W_SRC, src_y[n], X_RT - 1, router_mid)
            edges.append((cells, AMBER, sel is not None and sel.source == n))
        for d in order:
            hl = sel is not None and d.id == sel.id
            into = route_cells(X_RT + W_RT, router_mid, X_SS - 1, title_y(d))
            edges.append((into, ticket_color(app, d), hl))
            name = outcome_of(app, d)
            out = route_cells(X_SS + W_SS, title_y(d), X_OUT - 1, out_y[name])
            edges.append((out, OUTCOMES[OUTCOME_INDEX[name]][1], hl))
            routes[d.id] = into + out

        bits, estyle, arrows = {}, {}, {}
        for want_hl in (False, True):
            for cells, color, hl in edges:
                if hl != want_hl:
                    continue
                style = f"bold {color}" if hl else dim(color, 0.55)
                for i, (cx, cy) in enumerate(cells):
                    b = bits.get((cx, cy), 0)
                    if i == 0:
                        b |= DIR_W
                    if i + 1 < len(cells):
                        nx, ny = cells[i + 1]
                        b |= DIR_E if nx > cx else DIR_W if nx < cx else DIR_S if ny > cy else DIR_N
                    if i > 0:
                        px_, py_ = cells[i - 1]
                        b |= DIR_W if px_ < cx else DIR_E if px_ > cx else DIR_N if py_ < cy else DIR_S
                    bits[(cx, cy)] = b
                    estyle[(cx, cy)] = style
                arrows[cells[-1]] = style
        for (cx, cy), b in bits.items():
            ly = cy - off + 2
            if 2 <= ly < H and 0 <= cx < W:
                chars[ly][cx] = "▶" if (cx, cy) in arrows else BOX.get(b, "┼")
                styles[ly][cx] = estyle[(cx, cy)]

        path_ids = set()
        if sel is not None:
            path_ids = {("src", sel.source), ("out", outcome_of(app, sel))}

        def node_style(key, color):
            return f"bold #000000 on {color}" if key in path_ids else f"bold {dim(color, 0.8)}"

        for n in src_names:
            put(X_SRC, src_y[n], fit(f"{n} {len(src_groups[n])}", W_SRC), node_style(("src", n), AMBER))
        today = sum(1 for e, _ in all_events(app.world) if e.at.astimezone().date() == datetime.now().astimezone().date())
        last = next((m.text for m in reversed(app.world.threads.get("terminal:default", [])) if m.who == "router"), "-")
        for i, line in enumerate(["◈ ROUTER", f"{today} events today", f"{tokens(app.world.tokens_today)} tok today", f"» {last}"]):
            put(X_RT, router_top + i, fit(line, W_RT), f"bold #000000 on {AMBER}")

        for d in order:
            y = ys[d.id]
            color = ticket_color(app, d)
            glyph = "◉" if app.stage[d.id] == "RUNNING" else STAGE_GLYPH[app.stage[d.id]]
            if d.last_kind in ("blocked", "failed") and app.stage[d.id] == "NEEDS YOU":
                glyph = "✕"
            chosen = d.id == app.selected_id
            if app.flashing(d.id):
                title_style = f"bold #000000 on {WHITE}"
            elif chosen:
                title_style = f"bold #000000 on {AMBER}"
            else:
                title_style = f"bold {WHITE}"
            label_style = f"{DIM} on {BAND}" if chosen else DIM
            put(X_SS, y, fit(f"  {session_label(d)}", W_SS), label_style)
            put(X_SS, y + 1, fit(f"{glyph} {session_title(d)}", W_SS), title_style)
            if not chosen and not app.flashing(d.id):
                put(X_SS, y + 1, glyph, f"bold {color}")
            put(X_SS, y + 2, fit(f"  {session_meta(d)}", W_SS), f"{DIM} on {BAND}" if chosen else "#5A5A5A")
            top = y - off + 2
            if top + CARD_ROWS > 2 and top < H:
                self.hits.append((X_SS, top, X_SS + W_SS, top + CARD_ROWS, d.id))
        for name, ds in out_groups.items():
            color, glyph = next((c, g) for n, c, g in OUTCOMES if n == name)
            put(X_OUT, out_y[name], fit(f"{glyph} {name} {len(ds)}", W_OUT), node_style(("out", name), color))

        for did, t0 in app.pulses.items():
            el = time.monotonic() - t0
            route = routes.get(did)
            if route and 0 <= el < 1.0:
                cx, cy = route[min(int(el / 1.0 * len(route)), len(route) - 1)]
                ly = cy - off + 2
                if 2 <= ly < H and 0 <= cx < W:
                    chars[ly][cx] = "●"
                    styles[ly][cx] = f"bold {WHITE}"

        res = Text(no_wrap=True, overflow="crop")
        for y in range(H):
            if y:
                res.append("\n")
            run, rs = "", None
            for xx in range(W):
                if styles[y][xx] != rs and run:
                    res.append(run, style=rs)
                    run = ""
                rs = styles[y][xx]
                run += chars[y][xx]
            res.append(run, style=rs)
        return res


def fmt_span(seconds):
    if seconds >= 86400:
        return f"{seconds / 86400:.1f}d"
    if seconds >= 3600:
        return f"{seconds / 3600:.1f}h"
    return f"{seconds / 60:.0f}m"


class Band(Horizontal):
    def __init__(self, name, hint, name_id=None):
        super().__init__(classes="band")
        self._n, self._h, self._nid = name, hint, name_id

    def compose(self):
        yield Static(Text(self._n), classes="bn", id=self._nid, markup=False)
        yield Static(Text(self._h), classes="bh", markup=False)


class Panel(Vertical):
    pass


class RouterPanel(Panel):
    def on_click(self, event):
        self.app.query_one("#input").focus()


class RouterLog(RichLog, can_focus=False):
    pass


class StatusBar(Static):
    def on_mount(self):
        self.refresh_status()
        self.set_interval(1, self.refresh_status)

    def refresh_status(self):
        self.update(status_text(self.app.world))


INLINE_PASTE_LINES = 6


class PromptArea(TextArea):
    BINDINGS = [
        Binding("ctrl+v", "attach_clipboard", "attach image", show=False),
        Binding("ctrl+j,shift+enter", "newline", "new line", show=False),
    ]

    class Submitted(TextualMessage):
        def __init__(self, area, value):
            super().__init__()
            self.area = area
            self.value = value

    def __init__(self, **kwargs):
        super().__init__(soft_wrap=True, show_line_numbers=False, tab_behavior="focus",
                         compact=True, highlight_cursor_line=False, **kwargs)

    @property
    def value(self):
        return self.text

    @value.setter
    def value(self, text):
        self.text = text
        self.move_cursor(self.document.end)

    def action_attach_clipboard(self):
        self.app.attach_clipboard()

    def action_newline(self):
        self.insert("\n")

    async def _on_paste(self, event):
        text = event.text or ""
        images = clipboard.image_paths(text)
        if images:
            for image in images:
                self.app.attach(("image", str(image)))
        elif len(text.strip().splitlines()) > INLINE_PASTE_LINES:
            self.app.attach(("text", text.strip()))
        else:
            await super()._on_paste(event)
        event.stop()
        event.prevent_default()

    async def _on_key(self, event):
        if event.key == "enter":
            event.stop()
            event.prevent_default()
            self.post_message(self.Submitted(self, self.text))
            return
        if event.key == "backspace" and not self.text and self.app.attachments:
            self.app.attachments.pop()
            self.app.update_prompt()
            event.stop()
            event.prevent_default()
            return
        await super()._on_key(event)


def attachment_label(attachments):
    labels = []
    images = 0
    for kind, value in attachments:
        if kind == "task":
            labels.append(f"[task {value.split()[0]}]")
        elif kind == "image":
            images += 1
            labels.append(f"[image {images}]")
        else:
            labels.append(f"[pasted {len(value.splitlines())} lines]")
    return " ".join(labels)


def compose_message(text, attachments):
    pasted = [value for kind, value in attachments if kind == "text"]
    images = [value for kind, value in attachments if kind == "image"]
    task = next((value for kind, value in attachments if kind == "task"), None)
    opening = text or ("See the attached images." if images else "")
    parts = [f"About ticket {task}: {opening}" if task else opening]
    parts += pasted
    if images:
        parts.append("Attached images (open each with the Read tool):\n" + "\n".join(images))
    return "\n\n".join(part for part in parts if part)


class ConfirmArchive(ModalScreen):
    BINDINGS = [("y", "answer(True)", "archive"), ("n", "answer(False)", "cancel"),
                ("escape", "answer(False)", "cancel")]
    CSS = f"""
    ConfirmArchive {{ align: center middle; background: #000000 70%; }}
    #confirm {{ width: 100; height: auto; max-height: 30; border: solid {AMBER}; background: #000000; padding: 1 2; }}
    """

    def __init__(self, stale):
        super().__init__()
        self.stale = stale

    def compose(self):
        with Vertical(id="confirm"):
            yield Static(Text(f"ARCHIVE {len(self.stale)} STALE TASKS?", style=f"bold {AMBER}"))
            yield Static(stale_list_text(self.stale), markup=False)
            yield Static(legend_text([("Y", "ARCHIVE"), ("N", "CANCEL")]))

    def action_answer(self, yes):
        self.dismiss(yes)


class ReviewStale(Screen):
    BINDINGS = [("a", "archive", "archive"), ("k", "keep", "keep"), ("s", "skip", "skip"),
                ("escape", "done", "done")]

    def __init__(self, stale):
        super().__init__()
        self.stale = list(stale)
        self.index = 0

    def compose(self):
        yield StatusBar(classes="status")
        with Panel(classes="zoomed"):
            yield Band("REVIEW STALE", "a archive · k keep · s skip · esc done", name_id="review-name")
            with VerticalScroll():
                yield Static(id="review-text", markup=False)
        yield Static(legend_text([("A", "ARCHIVE"), ("K", "KEEP"), ("S", "SKIP"), ("ESC", "DONE")]), classes="legend")

    def on_mount(self):
        self.show_current()

    def show_current(self):
        if self.index >= len(self.stale):
            self.action_done()
            return
        d, reason = self.stale[self.index]
        self.query_one("#review-name", Static).update(
            Text(f"REVIEW STALE {self.index + 1}/{len(self.stale)}  {d.id}"))
        body = Text()
        body.append(" STALE ", style=f"bold #000000 on {RED}")
        body.append(f" {reason}\n\n", style=f"bold {RED}")
        body.append_text(dossier_text(d, False, self.app.activity_of(d)))
        self.query_one("#review-text", Static).update(body)

    def action_archive(self):
        self.app.archive([self.stale[self.index]])
        self.advance()

    def action_keep(self):
        self.app.keep(self.stale[self.index][0])
        self.advance()

    def action_skip(self):
        self.advance()

    def advance(self):
        self.index += 1
        self.show_current()

    def action_done(self):
        if self.app.screen is self:
            self.app.pop_screen()
            self.app.after_change()


class Zoom(Screen):
    BINDINGS = [("escape", "back", "back"), ("z", "back", "back")]

    def __init__(self, name):
        super().__init__()
        self.panel = name

    def compose(self):
        w = self.app.world
        mode = self.app.view_mode
        title = self.panel + (f" · {mode}" if self.panel == "BLOTTER" else "") + "  ZOOM"
        yield StatusBar(classes="status")
        with Panel(classes="zoomed"):
            yield Band(title, "esc back")
            if self.panel == "BLOTTER":
                if mode == "TABLE":
                    yield DataTable(id="zblotter", cursor_type="row", cell_padding=0, zebra_stripes=False)
                elif mode == "KANBAN":
                    yield KanbanView(classes="live")
                else:
                    yield GraphView(classes="live")
            elif self.panel == "DOSSIER":
                with VerticalScroll():
                    chosen = self.app.selected()
                    yield Static(dossier_text(chosen, True, self.app.activity_of(chosen)), markup=False)
            elif self.panel == "SYSTEM":
                with VerticalScroll():
                    yield Static(system_text(w), markup=False)
                    yield Static(Text("TAPE · newest first", style=f"bold {AMBER}"), markup=False)
                    yield Static(tape_text(w), id="ztape", markup=False)
            else:
                yield RichLog(id="zlog", wrap=True, markup=False, highlight=False, min_width=1)
        yield Static(legend_text(ZOOM_KEYS), classes="legend")

    def on_mount(self):
        if self.panel == "BLOTTER":
            if self.app.view_mode == "TABLE":
                self.call_after_refresh(self.build_table)
            else:
                self.query_one(".live").focus()
        elif self.panel == "ROUTER":
            log = self.query_one(RichLog)
            for line in thread_lines(self.app.world):
                log.write(line)

    def build_table(self):
        tb = self.query_one(DataTable)
        self.app.rebuild_table(tb)
        tb.focus()

    def on_data_table_row_highlighted(self, ev):
        if ev.row_key and ev.row_key.value and ev.cursor_row == ev.data_table.cursor_row:
            self.app.selected_id = ev.row_key.value

    def action_back(self):
        self.app.pop_screen()
        self.app.after_change()


class CenterApp(App):
    CSS = f"""
    Screen {{ background: #000000; color: {WHITE}; }}
    .status {{ dock: top; height: 1; background: {BAND}; }}
    .legend {{ dock: bottom; height: 1; background: #000000; }}
    #cols {{ height: 1fr; }}
    #left {{ width: 5fr; }}
    #right {{ width: 3fr; }}
    #p-blotter {{ height: 1fr; }}
    #p-system {{ height: 10; }}
    #stale-strip {{ height: 1; background: #1A0000; display: none; }}
    #p-dossier {{ height: 1fr; }}
    #p-router {{ height: 1fr; }}
    Panel {{ border: solid #3A2A00; background: #000000; }}
    Panel:focus-within {{ border: solid {AMBER}; }}
    .band {{ height: 1; background: {BAND}; }}
    .band Static {{ background: transparent; }}
    * {{ scrollbar-color: #5A4000; scrollbar-background: #000000; scrollbar-color-hover: {AMBER}; scrollbar-color-active: {AMBER}; }}
    #sysinfo {{ text-wrap: nowrap; text-overflow: ellipsis; }}
    .band .bn {{ width: 1fr; color: {AMBER}; text-style: bold; padding: 0 1; }}
    .band .bh {{ width: auto; color: {DIM}; padding: 0 1; }}
    Panel:focus-within .band {{ background: {AMBER}; }}
    Panel:focus-within .band .bn {{ color: #000000; }}
    Panel:focus-within .band .bh {{ color: #3A2A00; }}
    DataTable {{ scrollbar-size-horizontal: 0; height: 1fr; background: #000000; scrollbar-size: 1 1; }}
    DataTable > .datatable--header {{ background: #000000; }}
    DataTable > .datatable--cursor {{ background: #5A4000; color: #FFFFFF; }}
    DataTable:focus > .datatable--cursor {{ background: {AMBER}; color: #000000; text-style: bold; }}
    DataTable > .datatable--hover {{ background: #000000; }}
    KanbanView, GraphView {{ height: 1fr; width: 1fr; background: #000000; padding: 0 1; }}
    #kanban, #graph {{ display: none; }}
    #blotter-foot {{ height: 2; padding: 0 1; background: #0D0D0D; overflow: hidden; }}
    VerticalScroll {{ overflow-x: hidden; background: #000000; scrollbar-size: 1 1; padding: 0 1; }}
    Static {{ background: #000000; }}
    #inputrow {{ height: auto; max-height: 7; background: #0D0D0D; }}
    #prompt {{ width: auto; color: {AMBER}; text-style: bold; padding: 0 0 0 1; background: #0D0D0D; }}
    PromptArea {{ border: none; height: auto; max-height: 6; width: 1fr; padding: 0 1; background: #0D0D0D; color: {WHITE}; }}
    PromptArea:focus {{ border: none; background: #1A1200; }}
    PromptArea > .text-area--placeholder {{ color: {DIM}; }}
    RichLog {{ background: #000000; padding: 0 3 0 0; overflow-x: hidden; scrollbar-size-horizontal: 0; scrollbar-size: 1 1; height: 1fr; }}
    """

    BINDINGS = [
        ("q", "quit", "quit"),
        ("z", "zoom", "zoom"),
        ("n", "new", "new"),
        ("v", "view", "view"),
        ("escape", "blotter", "blotter"),
        ("ctrl+t", "target", "target"),
        ("ctrl+v", "attach_clipboard", "attach image"),
        ("i", "inquire", "ask about task"),
        ("o", "open_review", "open review"),
        ("a", "archive_all", "archive stale"),
        ("r", "review", "review stale"),
    ]

    def __init__(self, root, *, verb=run_verb, deez=REPO_ROOT / "bin/deez", refresh_s=REFRESH_S,
                 load=center_model.load, probe=None, now=None, grab_image=clipboard.grab_image,
                 projects=Path.home() / ".claude" / "projects", opener=None):
        super().__init__()
        self.root = Path(root)
        self.verb = verb
        self.deez = Path(deez)
        self.refresh_s = refresh_s
        self.load_world = load
        self.probe = probe or self.probe_host
        self.now = now or utcnow
        self.grab_image = grab_image
        self.projects = Path(projects)
        self.opener = opener or open_in_browser
        self.activity_cache = {}
        self.attachments = []
        self.stale = []
        self.archiving = set()
        self.world = center_model.World([], {}, 0.0)
        self.local = []
        self.loading = False
        self.mode = "ask"
        self.view_idx = 0
        self.flash = {}
        self.pulses = {}
        self.stage = {}
        self.since = {}
        self.selected_id = None
        self.adopt(self.read_world(), mark=False)

    @property
    def view_mode(self):
        return MODES[self.view_idx]

    def selected(self):
        return next((d for d in self.world.dossiers if d.id == self.selected_id), None)

    def lane(self, stage):
        return sorted([d for d in self.world.dossiers if self.stage.get(d.id) == stage],
                      key=lambda d: self.since[d.id], reverse=True)

    def flashing(self, did):
        return time.monotonic() < self.flash.get(did, 0)

    def compose(self) -> ComposeResult:
        w = self.world
        yield StatusBar(classes="status")
        with Horizontal(id="cols"):
            with Vertical(id="left"):
                yield Static(id="stale-strip", markup=False)
                with Panel(id="p-blotter"):
                    yield Band("BLOTTER · TABLE", "v view · ↑↓←→ move · enter open · z zoom", name_id="blotter-name")
                    yield DataTable(id="blotter", cursor_type="row", cell_padding=0)
                    yield Static(id="blotter-foot", markup=False)
                    yield KanbanView(id="kanban", classes="live")
                    yield GraphView(id="graph", classes="live")
                with Panel(id="p-system"):
                    yield Band("SYSTEM · TAPE", "z zoom")
                    with VerticalScroll(id="system-scroll"):
                        yield Static(system_compact(w), id="sysinfo", markup=False)
            with Vertical(id="right"):
                with Panel(id="p-dossier"):
                    yield Band("DOSSIER", "o open PR · i ask about it · z full report", name_id="dossier-name")
                    with VerticalScroll(id="dossier-scroll"):
                        yield Static(id="dossier-text", markup=False)
                with RouterPanel(id="p-router"):
                    yield Band("ROUTER", "^t target · enter send · n new task")
                    yield RouterLog(id="log", wrap=True, markup=False, highlight=False, min_width=1)
                    with Horizontal(id="inputrow"):
                        yield Label("", id="prompt", markup=False)
                        yield PromptArea(id="input", placeholder="type here · enter sends · ctrl+j new line · ctrl+v image")
        yield Static(legend_text(MAIN_KEYS), classes="legend")

    def on_mount(self):
        self.call_after_refresh(self.first_paint)
        self.render_log()
        self.update_prompt()
        self.query_one("#blotter", DataTable).focus()
        self.set_interval(self.refresh_s, self.reload)
        self.set_interval(0.1, self.anim_tick)

    def probe_host(self, world):
        health = read_daemon_health(self.root, utcnow())
        world.daemon_ok = health.alive
        world.heartbeat_s = health.heartbeat_age_s
        world.peers = len(read_peers(PEERS_DIR))
        try:
            world.free_pct = memguard.free_pct()
        except Exception:
            world.free_pct = None

    def read_world(self):
        try:
            world = self.load_world(self.root)
        except Exception as exc:
            world = center_model.World(list(self.world.dossiers), dict(self.world.threads),
                                       self.world.spend_today, error=f"load failed: {exc}")
        try:
            self.probe(world)
        except Exception as exc:
            world.error = world.error or f"probe failed: {exc}"
        for d in world.dossiers:
            d.inflight = center_model.inflight_tokens(d, self.projects)
            world.tokens_today += d.inflight
        return world

    def reload(self):
        if self.loading:
            return
        self.loading = True
        self.run_worker(self.reload_in_thread, thread=True, exclusive=True, group="reload")

    def reload_in_thread(self):
        try:
            world = self.read_world()
        finally:
            self.loading = False
        self.call_from_thread(self.apply_world, world)

    def apply_world(self, world):
        thread_before = len(self.world.threads.get("terminal:default", []))
        self.adopt(world, mark=True)
        if len(self.world.threads.get("terminal:default", [])) != thread_before:
            self.render_log()
        self.after_change()

    def adopt(self, world, mark):
        previous = {d.id: (self.stage.get(d.id), d.last_at) for d in self.world.dossiers}
        thread = world.threads.setdefault("terminal:default", [])
        thread.extend(self.local)
        thread.sort(key=lambda message: message.at)
        self.world = world
        for d in world.dossiers:
            self.stage[d.id] = center_model.stage(d)
            self.since[d.id] = max((e.at for e in d.events), default=d.created)
            if mark and previous.get(d.id) != (self.stage[d.id], d.last_at):
                self.mark(d)
        self.stale = [(d, reason) for d, reason in center_model.stale_tickets(world, self.root, self.now())
                      if d.id not in self.archiving]
        ids = {d.id for d in world.dossiers}
        if self.selected_id not in ids:
            self.selected_id = ordered(world)[0].id if world.dossiers else None

    def log_text(self):
        return "\n".join(f"{m.who} {m.text}" for m in self.world.threads.get("terminal:default", []))

    def say(self, text):
        message = Message(utcnow(), "system", text)
        self.local.append(message)
        self.world.threads.setdefault("terminal:default", []).append(message)
        self.render_log()

    def submit(self, argv):
        self.run_worker(lambda: self.call_verb(argv), thread=True, group="verbs")

    def call_verb(self, argv):
        result = self.verb(argv)
        self.call_from_thread(self.verb_done, result)

    def verb_done(self, result):
        verb = result.argv[2] if len(result.argv) > 2 else "?"
        if verb == "archive" and len(result.argv) > 3:
            self.archiving.discard(result.argv[3])
        if result.returncode == 0:
            self.say(f"{verb}: {' '.join(result.stdout.split()) or 'ok'}")
        else:
            tail = " ".join((result.stderr or "").strip().splitlines()[-3:])
            self.say(f"{verb} failed (exit {result.returncode}): {tail}")
        self.reload()

    def first_paint(self):
        self.after_change()

    def on_resize(self, event):
        self.call_after_refresh(self.rebuild_all_tables)
        self.call_after_refresh(self.render_log)

    def rebuild_table(self, tb):
        fill_blotter(tb, self.world, tb.id == "zblotter", {k for k in self.flash if self.flashing(k)})
        if self.selected_id and tb.row_count:
            tb.move_cursor(row=tb.get_row_index(self.selected_id))

    def rebuild_all_tables(self):
        for scr in self.screen_stack:
            for tb in scr.query(DataTable):
                self.rebuild_table(tb)

    def on_data_table_row_highlighted(self, ev):
        if ev.data_table.id == "blotter" and ev.row_key and ev.row_key.value:
            if ev.cursor_row == ev.data_table.cursor_row:
                self.pick(ev.row_key.value)

    def on_data_table_row_selected(self, ev):
        if ev.data_table.id == "blotter":
            self.push_screen(Zoom("DOSSIER"))

    def pick(self, did):
        moved = did != self.selected_id
        self.selected_id = did
        self.refresh_panels(moved)
        self.refresh_views()
        self.update_prompt()

    def refresh_views(self):
        for scr in self.screen_stack:
            for v in scr.query(".live"):
                v.refresh()
        for scr in self.screen_stack:
            for tb in scr.query(DataTable):
                if self.selected_id and tb.row_count:
                    idx = tb.get_row_index(self.selected_id)
                    if tb.cursor_row != idx:
                        tb.move_cursor(row=idx)

    def refresh_panels(self, reset_scroll):
        main = self.screen_stack[0]
        d = self.selected()
        main.query_one("#dossier-text", Static).update(dossier_text(d, False, self.activity_of(d)))
        main.query_one("#dossier-name", Static).update(Text(f"DOSSIER  {d.id}" if d else "DOSSIER"))
        main.query_one("#sysinfo", Static).update(system_compact(self.world))
        rows = ordered(self.world)
        pos = next((i for i, r in enumerate(rows) if d and r.id == d.id), 0) + 1
        foot = Text()
        if d:
            foot.append(f"{pos}/{len(rows)} ", style=DIM)
            foot.append(f"{d.last_kind or '-'} ", style=f"bold {KIND_COLOR.get(d.last_kind or '-', DIM)}")
            foot.append(d.last_text or "-", style=WHITE)
        main.query_one("#blotter-foot", Static).update(foot)
        if reset_scroll:
            main.query_one("#dossier-scroll").scroll_home(animate=False)
        for scr in self.screen_stack[1:]:
            for s in scr.query("#ztape"):
                s.update(tape_text(self.world))

    def render_stale(self):
        strip = self.screen_stack[0].query_one("#stale-strip", Static)
        strip.display = bool(self.stale)
        strip.update(stale_strip_text(self.stale) if self.stale else "")

    def action_archive_all(self):
        if self.in_zoom() or not self.stale:
            return
        chosen = list(self.stale)

        def answered(yes):
            if yes:
                self.archive(chosen)

        self.push_screen(ConfirmArchive(chosen), answered)

    def action_review(self):
        if self.in_zoom() or not self.stale:
            return
        self.push_screen(ReviewStale(self.stale))

    def archive(self, items):
        by = getpass.getuser()
        for d, reason in items:
            self.archiving.add(d.id)
            self.submit([str(self.deez), "super-clanker", "archive", d.id, "--reason", f"stale: {reason}", "--by", by])
        self.stale = [(d, reason) for d, reason in self.stale if d.id not in self.archiving]
        self.render_stale()

    def keep(self, dossier):
        center_model.keep(self.root, dossier)
        self.stale = [(d, reason) for d, reason in self.stale if d.id != dossier.id]
        self.render_stale()

    def after_change(self):
        self.render_stale()
        self.rebuild_all_tables()
        self.refresh_panels(False)
        self.refresh_views()
        for scr in self.screen_stack:
            for sb in scr.query(StatusBar):
                sb.refresh_status()

    def render_log(self):
        log = self.query_one("#log", RichLog)
        log.clear()
        for line in thread_lines(self.world):
            log.write(line)
        log.scroll_end(animate=False)

    def update_prompt(self):
        d = self.selected()
        label = {
            "ask": "router (ask) > ",
            "note": f"this ticket {d.id if d else ''} (note) > ",
            "new": "new task > ",
        }[self.mode]
        prompt = Text(label)
        if self.attachments:
            prompt = Text(label.rstrip("> ") + " ")
            prompt.append(attachment_label(self.attachments), style=f"bold {CYAN}")
            prompt.append(" > ")
        self.query_one("#prompt", Label).update(prompt)

    def activity_of(self, d):
        if d is None or not d.session:
            return []
        path = next(self.projects.glob(f"*/{d.session}.jsonl"), None)
        try:
            stamp = (path, path.stat().st_mtime_ns, path.stat().st_size) if path else None
        except OSError:
            stamp = None
        cached = self.activity_cache.get(d.session)
        if cached and cached[0] == stamp:
            return cached[1]
        lines = center_model.activity(d, self.projects) if stamp else []
        self.activity_cache[d.session] = (stamp, lines)
        return lines

    def action_open_review(self):
        d = self.selected()
        if self.in_zoom() or d is None:
            return
        if not d.review_url:
            self.say(f"no review link on {d.id} yet")
            return
        self.opener(d.review_url)
        self.say(f"opened {d.review_url}")

    def action_inquire(self):
        d = self.selected()
        if self.in_zoom() or d is None:
            return
        self.attachments = [a for a in self.attachments if a[0] != "task"]
        self.attachments.insert(0, ("task", f"{d.id} ({d.slug})"))
        self.mode = "ask"
        self.update_prompt()
        self.query_one("#input", PromptArea).focus()

    def attach(self, attachment):
        self.attachments.append(attachment)
        self.update_prompt()

    def attach_clipboard(self):
        self.query_one("#input", PromptArea).focus()
        self.run_worker(self.grab_in_thread, thread=True, group="clipboard")

    def grab_in_thread(self):
        found = self.grab_image(self.root / "attachments")
        self.call_from_thread(self.grabbed, found)

    def grabbed(self, found):
        if found is None:
            self.say("no image on the clipboard (copy a screenshot or an image file, then ctrl+v)")
            return
        self.attach(("image", str(found)))

    def in_zoom(self):
        return len(self.screen_stack) > 1

    def action_open(self):
        if self.in_zoom():
            self.screen.action_back()
        else:
            self.push_screen(Zoom("DOSSIER"))

    def action_zoom(self):
        if self.in_zoom():
            return
        w = self.focused
        while w is not None and not isinstance(w, Panel):
            w = w.parent
        name = {"p-blotter": "BLOTTER", "p-dossier": "DOSSIER", "p-system": "SYSTEM", "p-router": "ROUTER"}.get(
            w.id if w else "", "BLOTTER")
        self.push_screen(Zoom(name))

    def action_view(self):
        if self.in_zoom():
            return
        self.view_idx = (self.view_idx + 1) % len(MODES)
        self.apply_view()

    def apply_view(self):
        mode = self.view_mode
        ids = {"TABLE": "#blotter", "KANBAN": "#kanban", "GRAPH": "#graph"}
        for m, sel in ids.items():
            self.query_one(sel).display = m == mode
        self.query_one("#blotter-name", Static).update(Text(f"BLOTTER · {mode}"))
        self.query_one("#blotter-foot").display = mode == "TABLE"
        self.query_one(ids[mode]).focus()
        self.refresh_views()

    def action_new(self):
        if self.in_zoom():
            return
        self.mode = "new"
        self.update_prompt()
        self.query_one("#input", PromptArea).focus()

    def action_target(self):
        if self.in_zoom():
            return
        self.mode = "note" if self.mode != "note" else "ask"
        self.update_prompt()
        self.query_one("#input", PromptArea).focus()

    def action_blotter(self):
        if self.in_zoom():
            return
        if self.mode == "new":
            self.mode = "ask"
            self.update_prompt()
        ids = {"TABLE": "#blotter", "KANBAN": "#kanban", "GRAPH": "#graph"}
        self.query_one(ids[self.view_mode]).focus()

    def action_attach_clipboard(self):
        if not self.in_zoom():
            self.attach_clipboard()

    def on_prompt_area_submitted(self, ev):
        typed = ev.value.strip()
        if not typed and not self.attachments:
            return
        text = compose_message(typed, self.attachments)
        ev.area.value = ""
        self.attachments = []
        self.update_prompt()
        d = self.selected()
        if self.mode == "note" and d:
            self.say(f"note {d.id}: {text}")
            self.submit([str(self.deez), "super-clanker", "tell", d.id, f"--text={text}"])
        else:
            self.submit([str(self.deez), "super-clanker", "ask", "--", text])
        if self.mode == "new":
            self.mode = "ask"
            self.update_prompt()

    def mark(self, d):
        self.flash[d.id] = time.monotonic() + 1.0
        self.pulses[d.id] = time.monotonic()

    def anim_tick(self):
        now = time.monotonic()
        if any(now - t < 1.1 for t in self.pulses.values()):
            self.refresh_views()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="center_app")
    parser.add_argument("--state", type=Path)
    args = parser.parse_args(argv)
    root = args.state or state_root(os.environ, Path.home())
    os.environ["DEEZ_SUPER_STATE"] = str(root)
    CenterApp(root).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
