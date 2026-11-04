import json
import os
import re
import sqlite3
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from deezlib.superclanker import config
from deezlib.superclanker.reviews import find_review_url
from deezlib.superclanker.store import SuperError
from deezlib.superclanker.ui_model import local_midnight_utc

DB_NAME = "super.db"
STAGES = ["INBOX", "QUEUED", "RUNNING", "NEEDS YOU", "TO MERGE", "READY", "ENDED"]
ATTENTION_KINDS = ("waiting", "blocked", "failed")
READY_STALE_AFTER = timedelta(hours=6)
WAITING_STALE_AFTER = timedelta(days=3)
IDLE_STALE_AFTER = timedelta(days=1)
KEPT_NAME = "center-kept.json"


@dataclass
class Turn:
    assignment: str
    n: int
    cost: float
    turns: int
    model: str
    duration_s: float
    stop: str
    result: str = ""


@dataclass
class ActivityLine:
    at: datetime | None
    kind: str
    text: str


@dataclass
class Event:
    at: datetime
    kind: str
    text: str


@dataclass
class Dossier:
    id: str
    slug: str
    state: str
    created: datetime
    ended: datetime | None
    ended_by: str | None
    outcome: str | None
    thread: str
    source: str
    actor: str
    request: str
    link: str | None
    scope: str
    playbook: str | None
    repo: str | None
    worker_state: str
    worker_started: datetime | None
    assignment: str | None
    session: str | None
    pid: int | None
    worktree: str | None
    last_kind: str | None
    last_text: str | None
    last_at: datetime | None
    question: str | None
    evidence: list[str]
    reports: list[tuple[datetime, str, str]]
    notes: list[tuple[datetime, str, bool]]
    turns: list[Turn]
    router_cost: float
    events: list[Event] = field(default_factory=list)
    answer: str | None = None
    earlier_answers: list[str] = field(default_factory=list)

    @property
    def worker_cost(self):
        return sum(turn.cost for turn in self.turns)

    @property
    def review_url(self):
        return find_review_url([*self.evidence, *(text for _at, _kind, text in reversed(self.reports)), self.answer or ""])

    @property
    def awaiting_merge(self):
        return stage(self) == "TO MERGE"

    @property
    def needs_you(self):
        return self.state == "open" and self.last_kind in ATTENTION_KINDS


@dataclass
class Message:
    at: datetime
    who: str
    text: str


@dataclass
class World:
    dossiers: list[Dossier]
    threads: dict[str, list[Message]]
    spend_today: float
    max_running: int = 3
    free_pct: int | None = None
    peers: int = 0
    daemon_ok: bool | None = None
    heartbeat_s: float | None = None
    error: str | None = None
    demo: bool = False

    @property
    def workers_running(self):
        return sum(1 for d in self.dossiers if d.state == "open" and d.worker_state == "running")


def parse_time(raw):
    if not raw:
        return None
    moment = datetime.fromisoformat(raw)
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def stage(dossier):
    if dossier.state != "open":
        return "ENDED"
    running = dossier.worker_state == "running"
    reported_after_start = dossier.last_at and (
        dossier.worker_started is None or dossier.last_at >= dossier.worker_started
    )
    if dossier.needs_you and (not running or reported_after_start):
        return "NEEDS YOU"
    if dossier.last_kind == "ready" and (not running or reported_after_start):
        return "TO MERGE" if dossier.review_url else "READY"
    if running:
        return "RUNNING"
    if dossier.assignment is None:
        return "INBOX"
    if dossier.worker_state == "pending":
        return "QUEUED"
    return "RUNNING" if dossier.last_kind == "progress" else "QUEUED"


def read_turns(log_dir, assignment_id):
    found = []
    for path in sorted(Path(log_dir).glob(f"{assignment_id}*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
            index = 0 if path.stem == assignment_id else int(path.stem.rsplit(".", 1)[-1])
        except (OSError, ValueError):
            continue
        if not isinstance(body, dict):
            continue
        models = list((body.get("modelUsage") or {}).keys())
        found.append(Turn(
            assignment_id, index, float(body.get("total_cost_usd") or 0), int(body.get("num_turns") or 0),
            ",".join(model.removeprefix("claude-") for model in models) or "-",
            (body.get("duration_ms") or 0) / 1000, body.get("stop_reason") or "-",
            body.get("result") if isinstance(body.get("result"), str) else "",
        ))
    return found


def _note_value(notes, prefix):
    for note in notes:
        if note["text"].startswith(prefix):
            return note["text"].split(":", 1)[1].strip()
    return None


def _link(meta):
    if meta.get("web_url"):
        return meta["web_url"]
    if meta.get("pr") and meta.get("repo"):
        return f"https://github.com/{meta['repo']}/pull/{meta['pr']}"
    return None


def _evidence(raw):
    try:
        value = json.loads(raw or "[]")
    except ValueError:
        return []
    return [str(item) for item in value] if isinstance(value, list) else []


def _events(dossier, assignments):
    events = [Event(dossier.created, "ticket", f"opened from {dossier.source}")]
    for assignment in assignments:
        if assignment["started_at"]:
            events.append(Event(parse_time(assignment["started_at"]), "worker", f"{assignment['id']} started"))
        if assignment["ended_at"]:
            events.append(Event(parse_time(assignment["ended_at"]), "worker", f"{assignment['id']} ended"))
    events += [Event(at, kind, text) for at, kind, text in dossier.reports]
    events += [Event(at, "note", text) for at, text, _ in dossier.notes]
    if dossier.ended:
        events.append(Event(dossier.ended, "ticket", f"ended by {dossier.ended_by}"))
    return sorted(events, key=lambda event: event.at)


def _dossier(query, ticket, log_dir):
    triggers = query(
        "SELECT tr.* FROM acceptances a JOIN triggers tr ON tr.id = a.trigger_id "
        "WHERE a.ticket_id = ? ORDER BY tr.received_at", ticket["id"],
    )
    trigger = triggers[0] if triggers else None
    mandates = query("SELECT * FROM mandates WHERE id = ?", ticket["mandate_id"])
    mandate = mandates[0] if mandates else None
    assignments = query("SELECT * FROM assignments WHERE ticket_id = ? ORDER BY rowid", ticket["id"])
    last_assignment = assignments[-1] if assignments else None
    reports = query(
        "SELECT r.* FROM reports r JOIN assignments a ON a.id = r.assignment_id "
        "WHERE a.ticket_id = ? ORDER BY r.created_at, r.rowid", ticket["id"],
    )
    last_report = reports[-1] if reports else None
    notes = query("SELECT * FROM inputs WHERE ticket_id = ? ORDER BY created_at, rowid", ticket["id"])
    router_cost = query(
        "SELECT COALESCE(SUM(w.cost_usd), 0) AS c FROM wakes w, json_each(w.trigger_ids) j "
        "JOIN acceptances a ON a.trigger_id = j.value WHERE a.ticket_id = ?", ticket["id"],
    )[0]["c"]
    try:
        meta = json.loads(trigger["meta"] or "{}") if trigger else {}
    except ValueError:
        meta = {}
    playbook = _note_value(notes, "playbook:")
    dossier = Dossier(
        id=ticket["id"], slug=ticket["slug"], state=ticket["state"], created=parse_time(ticket["created_at"]),
        ended=parse_time(ticket["ended_at"]), ended_by=ticket["ended_by"], outcome=ticket["outcome"],
        thread=ticket["thread_id"], source=trigger["source"] if trigger else "-",
        actor=(trigger["actor"] or "-") if trigger else "-", request=trigger["text"] if trigger else "",
        link=_link(meta if isinstance(meta, dict) else {}), scope=mandate["scope"] if mandate else "",
        playbook=Path(playbook).stem if playbook else None, repo=_note_value(notes, "repo:"),
        worker_state=last_assignment["state"] if last_assignment else "-",
        worker_started=parse_time(last_assignment["started_at"]) if last_assignment else None,
        assignment=last_assignment["id"] if last_assignment else None,
        session=last_assignment["session_id"] if last_assignment else None,
        pid=last_assignment["pid"] if last_assignment else None,
        worktree=last_assignment["worktree"] if last_assignment else None,
        last_kind=last_report["kind"] if last_report else None,
        last_text=last_report["text"] if last_report else None,
        last_at=parse_time(last_report["created_at"]) if last_report else None,
        question=last_report["question"] if last_report else None,
        evidence=_evidence(last_report["evidence"]) if last_report else [],
        reports=[(parse_time(r["created_at"]), r["kind"], r["text"]) for r in reports],
        notes=[(parse_time(n["created_at"]), n["text"], bool(n["delivered_at"])) for n in notes],
        turns=[turn for a in assignments for turn in read_turns(log_dir, a["id"])],
        router_cost=float(router_cost or 0),
    )
    dossier.events = _events(dossier, assignments)
    found = answers(dossier.turns)
    dossier.answer = found[-1] if found else None
    dossier.earlier_answers = found[:-1]
    return dossier


def _threads(query):
    threads = {}
    for thread in query("SELECT id FROM threads WHERE id LIKE 'terminal:%'"):
        messages = [Message(parse_time(r["received_at"]), "you", r["text"])
                    for r in query("SELECT * FROM triggers WHERE thread_id = ?", thread["id"])]
        messages += [Message(parse_time(r["created_at"]), "router", r["text"])
                     for r in query("SELECT * FROM replies WHERE thread_id = ?", thread["id"])]
        threads[thread["id"]] = sorted(messages, key=lambda message: message.at)
    return threads


def _max_running(root):
    try:
        return config.load(root).workers.max_running
    except (SuperError, OSError, ValueError):
        return World.max_running


def load(root, now=None):
    root = Path(root)
    database = root / DB_NAME
    if not database.exists():
        return World([], {}, 0.0)
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    try:
        def query(sql, *params):
            return connection.execute(sql, params).fetchall()

        tickets = query("SELECT * FROM tickets ORDER BY created_at DESC, rowid DESC")
        dossiers = [_dossier(query, ticket, root / "log") for ticket in tickets]
        midnight = local_midnight_utc(now or datetime.now(timezone.utc))
        spend = query("SELECT COALESCE(SUM(cost_usd), 0) AS c FROM wakes WHERE started_at >= ?", midnight)[0]["c"]
        return World(dossiers, _threads(query), float(spend or 0), max_running=_max_running(root))
    finally:
        connection.close()


def last_activity(dossier):
    return max((event.at for event in dossier.events if event.at), default=dossier.created)


def activity_mark(dossier):
    return f"{last_activity(dossier).isoformat()}#{len(dossier.events)}"


def span(delta):
    seconds = max(delta.total_seconds(), 0)
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if seconds >= size:
            return f"{int(seconds // size)}{unit}"
    return f"{int(seconds)}s"


def stale_reason(dossier, now):
    idle = now - last_activity(dossier)
    if dossier.state != "open":
        if dossier.outcome == "dropped" and dossier.ended_by is None and idle >= IDLE_STALE_AFTER:
            return f"dropped {span(idle)} ago, worktree kept"
        return None
    current = stage(dossier)
    if current in ("RUNNING", "QUEUED", "INBOX"):
        return None
    if current == "TO MERGE":
        return f"review open, waiting on your merge {span(idle)}" if idle >= WAITING_STALE_AFTER else None
    if current == "READY":
        return f"ready, untouched {span(idle)}" if idle >= READY_STALE_AFTER else None
    if current == "NEEDS YOU":
        return f"{dossier.last_kind}, waiting on you {span(idle)}" if idle >= WAITING_STALE_AFTER else None
    return f"quiet {span(idle)}" if idle >= IDLE_STALE_AFTER else None


def read_kept(root):
    try:
        kept = json.loads((Path(root) / KEPT_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return kept if isinstance(kept, dict) else {}


def keep(root, dossier):
    kept = read_kept(root)
    kept[dossier.id] = activity_mark(dossier)
    handle, temp = tempfile.mkstemp(dir=root, prefix=".center-kept.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        json.dump(kept, stream, indent=2, sort_keys=True)
    os.replace(temp, Path(root) / KEPT_NAME)


def stale_tickets(world, root, now):
    kept = read_kept(root)
    found = []
    for dossier in world.dossiers:
        if kept.get(dossier.id) == activity_mark(dossier):
            continue
        reason = stale_reason(dossier, now)
        if reason:
            found.append((dossier, reason))
    return found


REPORT_TAIL = re.compile(r"\n*^REPORT (progress|waiting|ready|blocked|failed|dropped) .*\Z", re.M | re.S)
ACTIVITY_LIMIT = 400
TOOL_FIELDS = ("command", "file_path", "path", "pattern", "description", "url", "query", "prompt")


def answers(turns):
    order = list(dict.fromkeys(turn.assignment for turn in turns))
    ranked = sorted(turns, key=lambda turn: (order.index(turn.assignment), turn.n))
    cleaned = (REPORT_TAIL.sub("", turn.result).strip() for turn in ranked if turn.result)
    return [text for text in cleaned if text]


def _tool_text(name, given):
    if not isinstance(given, dict):
        return name
    for key in TOOL_FIELDS:
        value = given.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().splitlines()[0]
    return next((str(value) for value in given.values()), "")


def _transcript(dossier, projects_dir):
    if not dossier.session:
        return None
    return next(Path(projects_dir).glob(f"*/{dossier.session}.jsonl"), None)


def activity(dossier, projects_dir, limit=ACTIVITY_LIMIT):
    path = _transcript(dossier, projects_dir)
    if path is None:
        return []
    found = []
    try:
        with path.open(encoding="utf-8", errors="replace") as stream:
            for raw in stream:
                try:
                    entry = json.loads(raw)
                except ValueError:
                    continue
                if not isinstance(entry, dict) or entry.get("type") != "assistant":
                    continue
                at = _parse_stamp(entry.get("timestamp"))
                for part in (entry.get("message") or {}).get("content") or []:
                    if not isinstance(part, dict):
                        continue
                    if part.get("type") == "text" and (part.get("text") or "").strip():
                        found.append(ActivityLine(at, "say", " ".join(part["text"].split())))
                    elif part.get("type") == "tool_use":
                        name = part.get("name") or "tool"
                        found.append(ActivityLine(at, name, _tool_text(name, part.get("input"))))
    except OSError:
        return []
    return found[-limit:]


def _parse_stamp(raw):
    try:
        return parse_time(raw.replace("Z", "+00:00")) if isinstance(raw, str) else None
    except ValueError:
        return None


def review_label(url):
    if not url:
        return None
    number = url.rstrip("/").rsplit("/", 1)[-1]
    return f"MR !{number}" if "/merge_requests/" in url else f"PR #{number}"
