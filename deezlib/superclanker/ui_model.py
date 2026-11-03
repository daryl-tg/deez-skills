import json
import subprocess
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path

from deezlib import memguard
from deezlib.superclanker import config, daemon, procs, sweep, watchdog, workers
from deezlib.superclanker.domain import AssignmentState, ReportKind, TicketState
from deezlib.superclanker.store import Store

LOCK_DIR = "daemon.lock.d"
INBOX_THREAD = "terminal:default"
NOT_INITIALISED = "daemon not initialised"
INBOX_KEEP_BYTES = 65536
DUE_TOLERANCE_S = 0.25
FAST = 2
MID = 5
SLOW = 10


@dataclass(frozen=True)
class Peer:
    name: str
    pid: int
    cwd: str
    status: str
    session_id: str


@dataclass(frozen=True)
class DaemonHealth:
    pid: int | None
    alive: bool
    heartbeat_age_s: int | None


def _peer(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        pid = data.get("pid")
        if data.get("kind") != "interactive" or type(pid) is not int or pid <= 1:
            return None
        return Peer(
            str(data.get("name") or path.stem), pid, str(data.get("cwd") or ""),
            str(data.get("status") or ""), str(data.get("sessionId") or ""),
        )
    except (OSError, ValueError, AttributeError):
        return None


def read_peers(sessions_dir, alive=workers.alive):
    found = (_peer(path) for path in Path(sessions_dir).glob("*.json"))
    return sorted((peer for peer in found if peer and alive(peer.pid)), key=lambda peer: peer.name)


def _read_inbox(path, offset):
    try:
        with open(path, "rb") as stream:
            size = stream.seek(0, 2)
            reset = offset > size
            start = 0 if reset else offset
            if start == 0:
                start = max(0, size - INBOX_KEEP_BYTES)
            stream.seek(start)
            data = stream.read()
            cut = data.rfind(b"\n") + 1
            if cut:
                data = data[:cut]
            return data.decode("utf-8", errors="replace"), start + len(data), reset
    except FileNotFoundError:
        return "", 0, offset > 0


def read_inbox(path, offset):
    text, new_offset, _reset = _read_inbox(path, offset)
    return text, new_offset


def _heartbeat_age(root, now):
    try:
        beat = daemon.heartbeat_path(root).read_text(encoding="utf-8").strip()
        return int((now - datetime.fromisoformat(beat)).total_seconds())
    except (OSError, ValueError, TypeError):
        return None


def read_daemon_health(root, now):
    pid = daemon._lock_owner(Path(root) / LOCK_DIR)
    return DaemonHealth(pid, workers.alive(pid), _heartbeat_age(root, now))


def read_held(root):
    try:
        return int(daemon.held_path(root).read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def repo_of(worktree, root):
    if not worktree:
        return "-"
    try:
        parts = Path(worktree).relative_to(Path(root) / "worktrees").parts
    except ValueError:
        return "-"
    return parts[0] if len(parts) >= 2 else "-"


def local_midnight_utc(now):
    local = now.astimezone()
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight.astimezone(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class TicketRow:
    ticket_id: str
    slug: str
    state: str
    repo: str
    age_s: int
    worker_state: str | None
    assignment_id: str | None
    session_id: str | None
    worktree: str | None
    pid: int | None
    last_report: str | None
    question: str | None
    needs_you: bool
    rss_kb: int | None


@dataclass(frozen=True)
class Snapshot:
    initialised: bool
    stale: bool
    error: str | None
    free_pct: int | None
    held: int | None
    health: DaemonHealth | None
    spend_today: float | None
    rows: list
    anomalies: list
    peers: list
    attribution: procs.Attribution | None
    top: list
    table: dict
    inbox_text: str
    inbox_offset: int
    max_running: int
    taken_at: float
    leftover_pids: dict = field(default_factory=dict)


class Cadence:
    def __init__(self, clock=time.monotonic):
        self._clock = clock
        self._last = {}

    def due(self, name, every_s):
        now = self._clock()
        last = self._last.get(name)
        if last is not None and now - last < every_s - DUE_TOLERANCE_S:
            return False
        self._last[name] = now
        return True


def _empty(taken_at, **fields):
    base = dict(
        initialised=True, stale=False, error=None, free_pct=None, held=None, health=None,
        spend_today=None, rows=[], anomalies=[], peers=[], attribution=None, top=[], table={},
        inbox_text="", inbox_offset=0, max_running=0, taken_at=taken_at,
    )
    base.update(fields)
    return Snapshot(**base)


def _age(now, stamp):
    return max(0, int((now - datetime.fromisoformat(stamp)).total_seconds()))


def _row(root, now, ticket, assignment, report):
    kind = report.kind if report else None
    return TicketRow(
        ticket_id=ticket.id, slug=ticket.slug, state=str(ticket.state),
        repo=repo_of(assignment.worktree if assignment else None, root),
        age_s=_age(now, ticket.created_at),
        worker_state=str(assignment.state) if assignment else None,
        assignment_id=assignment.id if assignment else None,
        session_id=assignment.session_id if assignment else None,
        worktree=assignment.worktree if assignment else None,
        pid=assignment.pid if assignment else None,
        last_report=str(kind) if kind else None,
        question=report.question if report else None,
        needs_you=kind in (ReportKind.waiting, ReportKind.blocked),
        rss_kb=None,
    )


def _ordered(board):
    newest = sorted(board[::-1], key=lambda entry: entry[0].created_at, reverse=True)
    return sorted(
        newest,
        key=lambda entry: (
            not (entry[2] and entry[2].kind in (ReportKind.waiting, ReportKind.blocked)),
            entry[0].state != TicketState.open,
        ),
    )


def _worker_roots(board, leftover_pids):
    roots = {}
    for ticket, assignment, _report in board:
        if assignment and assignment.state == AssignmentState.running and assignment.pid:
            roots[ticket.id] = [assignment.pid, *leftover_pids.get(ticket.id, ())]
    return roots


def _with_rss(rows, table, attribution):
    sized = []
    for row in rows:
        pids = attribution.workers.get(row.ticket_id)
        rss = procs.tree_rss_kb(table, pids) if pids else None
        sized.append(replace(row, rss_kb=rss))
    return sized


def _free_pct(probe):
    try:
        return probe()
    except Exception:
        return None


def _leftover_pids(board, leftovers):
    found = {}
    for ticket, assignment, _report in board:
        if assignment and assignment.state == AssignmentState.running and assignment.worktree:
            found[ticket.id] = list(leftovers(assignment.worktree))
    return found


def build_snapshot(root, previous, cadence, *, now=lambda: datetime.now(timezone.utc),
                   run=subprocess.run, free_pct=memguard.free_pct, leftovers=sweep.leftovers,
                   sessions_dir=Path.home() / ".claude" / "sessions", load_config=config.load):
    root = Path(root)
    moment = now()
    taken_at = moment.timestamp()
    if not (root / "super.db").exists():
        return _empty(taken_at, initialised=False, error=NOT_INITIALISED)
    fast = cadence.due("fast", FAST) or previous is None
    mid = cadence.due("mid", MID) or previous is None
    slow = cadence.due("slow", SLOW) or previous is None
    if previous is not None and not (fast or mid or slow):
        return previous
    try:
        store = Store.open_read_only(root)
        try:
            return _assemble(
                root, previous, store, moment, taken_at, mid, slow,
                run, free_pct, leftovers, sessions_dir, load_config,
            )
        finally:
            store.close()
    except Exception as exc:
        if previous is None:
            return _empty(taken_at, stale=True, error=str(exc))
        return replace(previous, stale=True, error=str(exc))


def _attempt(probe, fallback):
    try:
        return probe()
    except Exception:
        return fallback


def _slow_fields(root, store, moment, base, load_config):
    settings = _attempt(lambda: load_config(root), None)
    stamp = moment.isoformat(timespec="seconds")
    found = _attempt(
        lambda: [
            (kind, items) for kind, items, _more in
            watchdog.anomalies(store, settings, root, stamp)
        ],
        base.anomalies,
    ) if settings else base.anomalies
    return dict(
        spend_today=_attempt(lambda: store.spend_since(local_midnight_utc(moment)), None),
        anomalies=found,
        max_running=settings.workers.max_running if settings else base.max_running,
    )


def _assemble(root, previous, store, moment, taken_at, mid, slow,
              run, free_pct, leftovers, sessions_dir, load_config):
    base = previous or _empty(taken_at)
    board = _ordered(store.board())
    leftover_pids = _leftover_pids(board, leftovers) if slow else base.leftover_pids
    values = dict(
        initialised=True, stale=False, error=None, taken_at=taken_at, leftover_pids=leftover_pids,
        health=read_daemon_health(root, moment), held=read_held(root),
    )
    text, offset, reset = _read_inbox(daemon.inbox_path(root, INBOX_THREAD), base.inbox_offset)
    kept = "" if reset else base.inbox_text
    values.update(inbox_text=(kept + text)[-INBOX_KEEP_BYTES:], inbox_offset=offset)
    table = procs.read_table(run) if mid else base.table
    peers = read_peers(sessions_dir) if mid else base.peers
    if mid:
        values.update(top=procs.top_trees(table), table=table, peers=peers)
    if slow:
        values.update(free_pct=_free_pct(free_pct))
        values.update(_slow_fields(root, store, moment, base, load_config))
    attribution = procs.attribute(
        table, _worker_roots(board, leftover_pids), {peer.name: peer.pid for peer in peers},
    )
    rows = [_row(root, moment, *entry) for entry in board]
    values.update(attribution=attribution, rows=_with_rss(rows, table, attribution))
    return replace(base, **values)


def attention_count(snapshot):
    return (
        sum(row.needs_you for row in snapshot.rows)
        + sum(len(items) for _kind, items in snapshot.anomalies)
    )


def needs_you_rose(previous, current):
    if previous is None:
        return False
    if (previous.held is None) != (current.held is None):
        return True
    return attention_count(current) > attention_count(previous)
