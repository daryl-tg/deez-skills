import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, fields, replace
from enum import StrEnum
from pathlib import Path

from deezlib.superclanker.domain import (
    ID_PREFIXES,
    Assignment,
    AssignmentState,
    Decision,
    DecisionKind,
    Mandate,
    Report,
    ReportKind,
    Strength,
    Subscription,
    Thread,
    Ticket,
    TicketState,
    Trigger,
    _short_digest,
    new_id,
    utc_now,
)


class SuperError(Exception):
    pass


class InputKind(StrEnum):
    note = "note"
    trigger = "trigger"


class TicketOutcome(StrEnum):
    merged = "merged"
    closed = "closed"
    dropped = "dropped"
    done = "done"


@dataclass(frozen=True)
class Wake:
    id: str
    started_at: str
    ended_at: str | None
    trigger_ids: tuple
    exit_code: int | None
    cost_usd: float | None
    session_id: str | None
    result: str | None
    denials: tuple | None


@dataclass(frozen=True)
class Reply:
    id: str
    thread_id: str
    text: str
    created_at: str
    sent_at: str | None


@dataclass(frozen=True)
class Input:
    id: str
    ticket_id: str
    kind: InputKind
    text: str
    created_at: str
    delivered_at: str | None


@dataclass(frozen=True)
class Tick:
    id: str
    started_at: str
    ended_at: str | None
    digest: str
    exit_code: int | None
    cost_usd: float | None
    session_id: str | None
    result: str | None
    denials: tuple | None


_ROUTER_PREFIXES = {Wake: "w_", Reply: "p_", Input: "i_", Tick: "x_"}
_PREFIXES = {**ID_PREFIXES, **_ROUTER_PREFIXES}


def _new_router_id(kind):
    return _ROUTER_PREFIXES[kind] + _short_digest(uuid.uuid4().hex)


_SCHEMA = """
CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY, source TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS triggers (
    id TEXT PRIMARY KEY, source TEXT NOT NULL, source_event_id TEXT NOT NULL,
    thread_id TEXT NOT NULL, actor TEXT, addressed INTEGER NOT NULL, text TEXT NOT NULL,
    parent_id TEXT, received_at TEXT NOT NULL, meta TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS triggers_by_thread ON triggers (thread_id);
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY, thread_id TEXT NOT NULL, trigger_ids TEXT NOT NULL,
    kind TEXT NOT NULL, strength TEXT NOT NULL, reason TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS mandates (
    id TEXT PRIMARY KEY, ticket_id TEXT NOT NULL, policy_version TEXT NOT NULL,
    strength TEXT NOT NULL, scope TEXT NOT NULL, rules TEXT NOT NULL, sender TEXT,
    source TEXT NOT NULL, created_at TEXT NOT NULL, withdrawn_at TEXT);
CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY, slug TEXT NOT NULL, thread_id TEXT NOT NULL,
    mandate_id TEXT NOT NULL, state TEXT NOT NULL, created_at TEXT NOT NULL,
    ended_at TEXT, ended_by TEXT, outcome TEXT);
CREATE INDEX IF NOT EXISTS tickets_by_thread ON tickets (thread_id);
CREATE TABLE IF NOT EXISTS acceptances (
    trigger_id TEXT PRIMARY KEY, ticket_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS assignments (
    id TEXT PRIMARY KEY, ticket_id TEXT NOT NULL, state TEXT NOT NULL, session_id TEXT,
    pid INTEGER, worktree TEXT, started_at TEXT, ended_at TEXT);
CREATE INDEX IF NOT EXISTS assignments_by_ticket ON assignments (ticket_id);
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY, assignment_id TEXT NOT NULL, kind TEXT NOT NULL, text TEXT NOT NULL,
    question TEXT, evidence TEXT, created_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS reports_by_assignment ON reports (assignment_id);
CREATE TABLE IF NOT EXISTS subscriptions (
    ticket_id TEXT NOT NULL, thread_id TEXT NOT NULL, context_only INTEGER NOT NULL,
    PRIMARY KEY (ticket_id, thread_id));
CREATE TABLE IF NOT EXISTS fanouts (
    trigger_id TEXT NOT NULL, ticket_id TEXT NOT NULL, created_at TEXT NOT NULL,
    PRIMARY KEY (trigger_id, ticket_id));
CREATE TABLE IF NOT EXISTS wakes (
    id TEXT PRIMARY KEY, started_at TEXT NOT NULL, ended_at TEXT, trigger_ids TEXT NOT NULL,
    exit_code INTEGER, cost_usd REAL, session_id TEXT, result TEXT, denials TEXT);
CREATE TABLE IF NOT EXISTS replies (
    id TEXT PRIMARY KEY, thread_id TEXT NOT NULL, text TEXT NOT NULL,
    created_at TEXT NOT NULL, sent_at TEXT);
CREATE INDEX IF NOT EXISTS replies_by_thread ON replies (thread_id);
CREATE TABLE IF NOT EXISTS inputs (
    id TEXT PRIMARY KEY, ticket_id TEXT NOT NULL, kind TEXT NOT NULL, text TEXT NOT NULL,
    created_at TEXT NOT NULL, delivered_at TEXT);
CREATE INDEX IF NOT EXISTS inputs_by_ticket ON inputs (ticket_id);
CREATE TABLE IF NOT EXISTS cursors (
    source TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, updated_at TEXT NOT NULL,
    PRIMARY KEY (source, key));
CREATE TABLE IF NOT EXISTS ticks (
    id TEXT PRIMARY KEY, started_at TEXT NOT NULL, ended_at TEXT, digest TEXT NOT NULL,
    exit_code INTEGER, cost_usd REAL, session_id TEXT, result TEXT, denials TEXT);
CREATE TABLE IF NOT EXISTS requeues (
    trigger_id TEXT NOT NULL, requeued_at TEXT NOT NULL, decisions_before INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS requeues_by_trigger ON requeues (trigger_id);
"""

_NEWEST_DECISION = (
    "(SELECT MAX(decisions.rowid) FROM decisions, json_each(decisions.trigger_ids) AS decided "
    "WHERE decided.value = triggers.id)"
)
_NEWEST_REQUEUE = (
    "(SELECT MAX(requeues.decisions_before) FROM requeues WHERE requeues.trigger_id = triggers.id)"
)
_UNDECIDED = (
    "NOT EXISTS (SELECT 1 FROM fanouts WHERE fanouts.trigger_id = triggers.id) "
    f"AND ({_NEWEST_DECISION} IS NULL OR {_NEWEST_REQUEUE} >= {_NEWEST_DECISION})"
)

_TABLES = {
    Thread: "threads",
    Trigger: "triggers",
    Decision: "decisions",
    Mandate: "mandates",
    Ticket: "tickets",
    Assignment: "assignments",
    Report: "reports",
    Subscription: "subscriptions",
    Wake: "wakes",
    Reply: "replies",
    Input: "inputs",
    Tick: "ticks",
}


def _optional_tuple(raw):
    return None if raw is None else tuple(json.loads(raw))


def _json_tuple(raw):
    return tuple(json.loads(raw))


_DECODERS = {
    Trigger: {"addressed": bool, "meta": json.loads},
    Decision: {"trigger_ids": _json_tuple, "kind": DecisionKind, "strength": Strength},
    Mandate: {"strength": Strength, "rules": _json_tuple},
    Ticket: {"state": TicketState},
    Assignment: {"state": AssignmentState},
    Report: {"kind": ReportKind, "evidence": _optional_tuple},
    Subscription: {"context_only": bool},
    Wake: {"trigger_ids": _json_tuple, "denials": _json_tuple},
    Tick: {"denials": _json_tuple},
    Input: {"kind": InputKind},
}


def _columns(kind):
    return [field.name for field in fields(kind)]


def _encode(value):
    if isinstance(value, (tuple, list, dict)):
        return json.dumps(value)
    return value


def _decode(kind, row):
    decoders = _DECODERS.get(kind, {})
    return kind(**{
        name: decoders[name](value) if name in decoders and value is not None else value
        for name, value in zip(_columns(kind), row)
    })


def _clip(text, width=60):
    line = " ".join(text.split())
    return line if len(line) <= width else line[: width - 1] + "…"


def _summary(record):
    match record:
        case Thread():
            return f"thread from {record.source}"
        case Trigger():
            return f"trigger from {record.actor}: {_clip(record.text)}"
        case Ticket():
            return f"ticket {record.state} {record.slug}"
        case Mandate():
            withdrawn = ", withdrawn" if record.withdrawn_at else ""
            return f"mandate {record.strength} {record.scope}{withdrawn}"
        case Assignment():
            return f"assignment {record.state}"
        case Report():
            return f"report {record.kind}: {_clip(record.text)}"
        case Decision():
            return f"decision {record.kind}: {_clip(record.reason)}"
        case Subscription():
            return "subscribed, context only" if record.context_only else "subscribed"
        case Wake():
            return f"wake exit {record.exit_code} cost {record.cost_usd}"
        case Reply():
            return f"reply: {_clip(record.text)}"
        case Input():
            return f"input {record.kind}: {_clip(record.text)}"
        case Tick():
            return f"tick exit {record.exit_code} cost {record.cost_usd}"


def _neighbours(records):
    return [(record.id, _summary(record)) for record in records]


def state_root(env, home):
    override = env.get("DEEZ_SUPER_STATE")
    if override:
        return Path(override)
    return Path(home) / ".local" / "state" / "deez-skills" / "super"


class Store:
    def __init__(self, connection):
        self._db = connection

    @classmethod
    def open(cls, root):
        root = Path(root)
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(root, 0o700)
        connection = sqlite3.connect(root / "super.db", isolation_level=None)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.executescript(_SCHEMA)
        ticket_columns = {row[1] for row in connection.execute("PRAGMA table_info(tickets)")}
        if "outcome" not in ticket_columns:
            connection.execute("ALTER TABLE tickets ADD COLUMN outcome TEXT")
        wake_columns = {row[1] for row in connection.execute("PRAGMA table_info(wakes)")}
        if "denials" not in wake_columns:
            connection.execute("ALTER TABLE wakes ADD COLUMN denials TEXT")
        tick_columns = {row[1] for row in connection.execute("PRAGMA table_info(ticks)")}
        if "denials" not in tick_columns:
            connection.execute("ALTER TABLE ticks ADD COLUMN denials TEXT")
        return cls(connection)

    @classmethod
    def open_read_only(cls, root):
        path = Path(root) / "super.db"
        if not path.is_file():
            raise SuperError(f"super-clanker not initialised: {path}")
        return cls(sqlite3.connect(f"file:{path}?mode=ro", uri=True, isolation_level=None))

    def close(self):
        self._db.close()

    @contextmanager
    def _transaction(self):
        self._db.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        self._db.execute("COMMIT")

    def _insert(self, record, conflict=""):
        names = _columns(type(record))
        cursor = self._db.execute(
            f"INSERT {conflict} INTO {_TABLES[type(record)]} ({', '.join(names)}) "
            f"VALUES ({', '.join('?' * len(names))})",
            [_encode(getattr(record, name)) for name in names],
        )
        return cursor.rowcount

    def _select(self, kind, where="1", params=(), order="ORDER BY rowid"):
        rows = self._db.execute(
            f"SELECT {', '.join(_columns(kind))} FROM {_TABLES[kind]} WHERE {where} {order}",
            params,
        )
        return [_decode(kind, row) for row in rows]

    def _get(self, kind, record_id):
        found = self._select(kind, "id = ?", (record_id,))
        return found[0] if found else None

    def _require(self, kind, record_id):
        record = self._get(kind, record_id)
        if record is None:
            raise SuperError(f"no {kind.__name__.lower()} {record_id}")
        return record

    def _latest_assignment(self, ticket_id):
        found = self._select(Assignment, "ticket_id = ?", (ticket_id,), "ORDER BY rowid DESC LIMIT 1")
        return found[0] if found else None

    def _last_report(self, ticket_id):
        found = self._select(
            Report, "assignment_id IN (SELECT id FROM assignments WHERE ticket_id = ?)",
            (ticket_id,), "ORDER BY rowid DESC LIMIT 1",
        )
        return found[0] if found else None

    def receive(self, trigger):
        with self._transaction():
            self._insert(Thread(trigger.thread_id, trigger.source, trigger.received_at), "OR IGNORE")
            stored = self._insert(trigger, "OR IGNORE")
        return "stored" if stored else "duplicate"

    def accept(self, trigger_id, slug, strength, scope, rules, policy_version, reason):
        strength = Strength(strength)
        with self._transaction():
            accepted = self._db.execute(
                "SELECT ticket_id FROM acceptances WHERE trigger_id = ?", (trigger_id,)
            ).fetchone()
            if accepted:
                return self._require(Ticket, accepted[0])
            trigger = self._require(Trigger, trigger_id)
            created_at = utc_now()
            ticket = Ticket(
                new_id(Ticket), slug, trigger.thread_id, new_id(Mandate), TicketState.open,
                created_at, None, None,
            )
            for record in (
                Decision(
                    new_id(Decision), trigger.thread_id, (trigger_id,), DecisionKind.accept,
                    strength, reason, created_at,
                ),
                ticket,
                Mandate(
                    ticket.mandate_id, ticket.id, policy_version, strength, scope, tuple(rules),
                    trigger.actor, trigger.source, created_at, None,
                ),
                Assignment(
                    new_id(Assignment), ticket.id, AssignmentState.pending,
                    None, None, None, None, None,
                ),
                Subscription(ticket.id, trigger.thread_id, False),
            ):
                self._insert(record)
            self._db.execute(
                "INSERT INTO acceptances (trigger_id, ticket_id) VALUES (?, ?)",
                (trigger_id, ticket.id),
            )
        return ticket

    def ignore(self, trigger_id, reason):
        with self._transaction():
            trigger = self._require(Trigger, trigger_id)
            decision = Decision(
                new_id(Decision), trigger.thread_id, (trigger_id,), DecisionKind.ignore,
                Strength.not_admitted, reason, utc_now(),
            )
            self._insert(decision)
        return decision

    def stop(self, ticket_id, by, reason):
        with self._transaction():
            ticket = self._require(Ticket, ticket_id)
            mandate = self._require(Mandate, ticket.mandate_id)
            if mandate.withdrawn_at is not None:
                return ticket
            ended_at = utc_now()
            self._db.execute(
                "UPDATE tickets SET state = ?, ended_at = ?, ended_by = ? WHERE id = ?",
                (TicketState.ended, ended_at, by, ticket_id),
            )
            self._db.execute(
                "UPDATE mandates SET withdrawn_at = ? WHERE id = ?", (ended_at, mandate.id)
            )
            self._db.execute(
                "UPDATE assignments SET state = ?, ended_at = ? WHERE ticket_id = ? AND state != ?",
                (AssignmentState.ended, ended_at, ticket_id, AssignmentState.ended),
            )
            self._insert(Decision(
                new_id(Decision), ticket.thread_id, (), DecisionKind.stop, Strength.explicit,
                reason, ended_at,
            ))
        return replace(ticket, state=TicketState.ended, ended_at=ended_at, ended_by=by)

    def subscribe(self, ticket_id, thread_id, context_only=False):
        with self._transaction():
            self._require(Ticket, ticket_id)
            self._db.execute(
                "INSERT INTO subscriptions (ticket_id, thread_id, context_only) VALUES (?, ?, ?) "
                "ON CONFLICT (ticket_id, thread_id) DO UPDATE SET context_only = excluded.context_only",
                (ticket_id, thread_id, context_only),
            )
        return Subscription(ticket_id, thread_id, context_only)

    def unsubscribe(self, ticket_id, thread_id):
        with self._transaction():
            self._db.execute(
                "DELETE FROM subscriptions WHERE ticket_id = ? AND thread_id = ?",
                (ticket_id, thread_id),
            )

    def queued(self):
        return self._select(Trigger, _UNDECIDED, order="ORDER BY received_at, rowid")

    def undecided(self, trigger_ids):
        return [
            trigger.id for trigger in self._select(
                Trigger, f"id IN (SELECT value FROM json_each(?)) AND {_UNDECIDED}",
                (json.dumps(list(trigger_ids)),),
            )
        ]

    def mark_unavailable(self, trigger_ids, reason):
        with self._transaction():
            for trigger_id in self.undecided(trigger_ids):
                trigger = self._require(Trigger, trigger_id)
                self._insert(Decision(
                    new_id(Decision), trigger.thread_id, (trigger_id,), DecisionKind.unavailable,
                    Strength.not_admitted, reason, utc_now(),
                ))

    def begin_wake(self, trigger_ids):
        wake = Wake(
            _new_router_id(Wake), utc_now(), None, tuple(trigger_ids), None, None, None, None, None
        )
        with self._transaction():
            self._insert(wake)
        return wake.id

    def end_wake(self, wake_id, exit_code, cost_usd, session_id, result, denials=None):
        with self._transaction():
            self._require(Wake, wake_id)
            self._db.execute(
                "UPDATE wakes SET ended_at = ?, exit_code = ?, cost_usd = ?, session_id = ?, "
                "result = ?, denials = ? WHERE id = ?",
                (utc_now(), exit_code, cost_usd, session_id, result, _encode(denials), wake_id),
            )

    def inflight_wake(self):
        found = self._select(
            Wake, "ended_at IS NULL", order="ORDER BY started_at DESC, rowid DESC LIMIT 1"
        )
        return found[0] if found else None

    def recent_wakes(self, limit=12):
        return self._select(
            Wake, order="ORDER BY started_at DESC, rowid DESC LIMIT ?", params=(limit,)
        )

    def expire_wake(self, wake_id):
        with self._transaction():
            self._require(Wake, wake_id)
            self._db.execute(
                "UPDATE wakes SET ended_at = ?, exit_code = NULL, result = ? "
                "WHERE id = ? AND ended_at IS NULL",
                (utc_now(), "expired by daemon", wake_id),
            )

    def begin_tick(self, digest):
        tick = Tick(_new_router_id(Tick), utc_now(), None, digest, None, None, None, None, None)
        with self._transaction():
            self._insert(tick)
        return tick.id

    def end_tick(self, tick_id, exit_code, cost_usd, session_id, result, denials=None):
        with self._transaction():
            self._require(Tick, tick_id)
            self._db.execute(
                "UPDATE ticks SET ended_at = ?, exit_code = ?, cost_usd = ?, session_id = ?, "
                "result = ?, denials = ? WHERE id = ?",
                (utc_now(), exit_code, cost_usd, session_id, result, _encode(denials), tick_id),
            )

    def requeue(self, trigger_id):
        with self._transaction():
            self._require(Trigger, trigger_id)
            accepted = self._db.execute(
                "SELECT ticket_id FROM acceptances WHERE trigger_id = ?", (trigger_id,)
            ).fetchone()
            if accepted:
                raise SuperError(f"{trigger_id} is accepted as {accepted[0]}; nothing to requeue")
            if self._db.execute(
                "SELECT 1 FROM fanouts WHERE trigger_id = ?", (trigger_id,)
            ).fetchone():
                raise SuperError(f"{trigger_id} went to a ticket's worker; nothing to requeue")
            if self.undecided([trigger_id]):
                return
            self._db.execute(
                "INSERT INTO requeues (trigger_id, requeued_at, decisions_before) "
                "VALUES (?, ?, (SELECT COALESCE(MAX(rowid), 0) FROM decisions))",
                (trigger_id, utc_now()),
            )

    def reply(self, thread_id, text):
        with self._transaction():
            self._require(Thread, thread_id)
            reply = Reply(_new_router_id(Reply), thread_id, text, utc_now(), None)
            self._insert(reply)
        return reply

    def ticket_origin(self, ticket_id):
        row = self._db.execute(
            "SELECT trigger_id FROM acceptances WHERE ticket_id = ? ORDER BY rowid LIMIT 1",
            (ticket_id,),
        ).fetchone()
        if row is None:
            raise SuperError(f"no accepted trigger for ticket {ticket_id}")
        return self._require(Trigger, row[0])

    def assignment_for(self, ticket_id):
        assignment = self._latest_assignment(ticket_id)
        if assignment is None:
            raise SuperError(f"no assignment for ticket {ticket_id}")
        return assignment

    def start_assignment(self, assignment_id, session_id, pid, worktree):
        with self._transaction():
            self._require(Assignment, assignment_id)
            self._db.execute(
                "UPDATE assignments SET state = CASE WHEN state = ? THEN state ELSE ? END, "
                "session_id = ?, pid = ?, worktree = ?, started_at = ? WHERE id = ?",
                (AssignmentState.ended, AssignmentState.running, session_id, pid, str(worktree),
                 utc_now(), assignment_id),
            )
            return self._require(Assignment, assignment_id)

    def running_assignments(self):
        return self._select(Assignment, "state = ?", (AssignmentState.running,))

    def stopped_assignments(self):
        return self._select(
            Assignment,
            "pid IS NOT NULL "
            "AND ticket_id IN (SELECT id FROM tickets WHERE ended_by IS NOT NULL) "
            "AND rowid = (SELECT MAX(rowid) FROM assignments AS latest "
            "WHERE latest.ticket_id = assignments.ticket_id)",
        )

    def pending_assignments(self):
        return self._select(
            Assignment,
            "state = ? AND ticket_id IN (SELECT id FROM tickets WHERE state = ?)",
            (AssignmentState.pending, TicketState.open),
            "ORDER BY (SELECT created_at FROM tickets WHERE tickets.id = assignments.ticket_id), "
            "(SELECT rowid FROM tickets WHERE tickets.id = assignments.ticket_id), rowid",
        )

    def mark_delivered(self, input_ids):
        with self._transaction():
            self._db.execute(
                "UPDATE inputs SET delivered_at = ? "
                "WHERE id IN (SELECT value FROM json_each(?)) AND delivered_at IS NULL",
                (utc_now(), json.dumps(list(input_ids))),
            )

    def end_ticket(self, ticket_id, outcome):
        outcome = TicketOutcome(outcome)
        with self._transaction():
            self._require(Ticket, ticket_id)
            self._db.execute(
                "UPDATE tickets SET state = ?, ended_at = ?, outcome = ? WHERE id = ? AND state = ?",
                (TicketState.ended, utc_now(), outcome, ticket_id, TicketState.open),
            )
            return self._require(Ticket, ticket_id)

    def unsent_replies(self):
        return self._select(Reply, "sent_at IS NULL")

    def mark_sent(self, reply_id):
        with self._transaction():
            self._require(Reply, reply_id)
            self._db.execute(
                "UPDATE replies SET sent_at = ? WHERE id = ? AND sent_at IS NULL",
                (utc_now(), reply_id),
            )

    def add_input(self, ticket_id, kind, text):
        kind = InputKind(kind)
        with self._transaction():
            self._require(Ticket, ticket_id)
            pending = self._select(
                Input, "ticket_id = ? AND kind = ? AND text = ? AND delivered_at IS NULL",
                (ticket_id, kind, text),
            )
            if pending:
                return pending[0]
            entry = Input(_new_router_id(Input), ticket_id, kind, text, utc_now(), None)
            self._insert(entry)
        return entry

    def undelivered_inputs(self, ticket_id):
        return self._select(Input, "ticket_id = ? AND delivered_at IS NULL", (ticket_id,))

    def inputs(self, ticket_id):
        return self._select(Input, "ticket_id = ?", (ticket_id,))

    def reopen(self, ticket_id):
        with self._transaction():
            ticket = self._require(Ticket, ticket_id)
            if ticket.ended_by is not None:
                raise SuperError(f"{ticket_id} was stopped by {ticket.ended_by}; it stays ended")
            self._db.execute(
                "UPDATE tickets SET state = ?, ended_at = NULL, outcome = NULL WHERE id = ?",
                (TicketState.open, ticket_id),
            )
            return self._require(Ticket, ticket_id)

    def succeed_assignment(self, ticket_id):
        with self._transaction():
            previous = self.assignment_for(ticket_id)
            successor = Assignment(
                new_id(Assignment), ticket_id, AssignmentState.pending, previous.session_id,
                None, previous.worktree, None, None,
            )
            self._insert(successor)
        return successor

    def revivable(self):
        return [ticket.id for ticket in self._select(
            Ticket,
            "ended_by IS NULL "
            "AND EXISTS (SELECT 1 FROM inputs WHERE inputs.ticket_id = tickets.id "
            "AND inputs.delivered_at IS NULL AND inputs.kind = 'trigger') "
            "AND (SELECT state FROM assignments WHERE assignments.ticket_id = tickets.id "
            "ORDER BY rowid DESC LIMIT 1) = ?",
            (AssignmentState.ended,),
        )]

    def retry(self, ticket_id):
        with self._transaction():
            ticket = self._require(Ticket, ticket_id)
            if ticket.state is TicketState.ended:
                raise SuperError(f"{ticket_id} has ended; nothing to retry")
            ended_at = utc_now()
            self._db.execute(
                "UPDATE assignments SET state = ?, ended_at = ? WHERE ticket_id = ? AND state != ?",
                (AssignmentState.ended, ended_at, ticket_id, AssignmentState.ended),
            )
            fresh = Assignment(
                new_id(Assignment), ticket_id, AssignmentState.pending, None, None, None, None, None
            )
            self._insert(fresh)
        return fresh

    def cursor(self, source, key):
        row = self._db.execute(
            "SELECT value FROM cursors WHERE source = ? AND key = ?", (source, key)
        ).fetchone()
        return row[0] if row else None

    def set_cursor(self, source, key, value):
        with self._transaction():
            self._db.execute(
                "INSERT INTO cursors (source, key, value, updated_at) VALUES (?, ?, ?, ?) "
                "ON CONFLICT (source, key) DO UPDATE SET value = excluded.value, "
                "updated_at = excluded.updated_at",
                (source, key, value, utc_now()),
            )

    def fanout_targets(self, thread_id):
        rows = self._db.execute(
            "SELECT tickets.id FROM subscriptions "
            "JOIN tickets ON tickets.id = subscriptions.ticket_id "
            "WHERE subscriptions.thread_id = ? AND NOT subscriptions.context_only "
            "AND (tickets.state = ? OR tickets.ended_by IS NULL) ORDER BY tickets.rowid",
            (thread_id, TicketState.open),
        )
        return [ticket_id for (ticket_id,) in rows]

    def record_fanout(self, trigger_id, ticket_ids):
        with self._transaction():
            self._require(Trigger, trigger_id)
            created_at = utc_now()
            for ticket_id in ticket_ids:
                self._require(Ticket, ticket_id)
                self._db.execute(
                    "INSERT OR IGNORE INTO fanouts (trigger_id, ticket_id, created_at) "
                    "VALUES (?, ?, ?)",
                    (trigger_id, ticket_id, created_at),
                )

    def report(self, assignment_id, kind, text, question=None, evidence=None):
        kind = ReportKind(kind)
        with self._transaction():
            self._require(Assignment, assignment_id)
            report = Report(
                new_id(Report), assignment_id, kind, text, question,
                None if evidence is None else tuple(evidence), utc_now(),
            )
            self._insert(report)
            if kind.ends_assignment:
                self._db.execute(
                    "UPDATE assignments SET state = ?, ended_at = ? WHERE id = ? AND state != ?",
                    (AssignmentState.ended, report.created_at, assignment_id, AssignmentState.ended),
                )
        return report

    def show(self, obj_id):
        kind = next(
            (kind for kind, prefix in _PREFIXES.items() if obj_id.startswith(prefix)), Thread
        )
        record = self._get(kind, obj_id)
        if record is None:
            raise SuperError(f"nothing has id {obj_id}")
        shown = {name: getattr(record, name) for name in _columns(kind)}
        shown["related"] = self._related[kind](self, record)
        return shown

    def _trigger_neighbours(self, trigger):
        return _neighbours([
            self._require(Thread, trigger.thread_id),
            *self._select(Ticket, "thread_id = ?", (trigger.thread_id,)),
            *self._select(
                Decision,
                "EXISTS (SELECT 1 FROM json_each(decisions.trigger_ids) WHERE value = ?)",
                (trigger.id,),
            ),
        ])

    def _thread_neighbours(self, thread):
        subscriptions = self._select(Subscription, "thread_id = ?", (thread.id,))
        return [
            *_neighbours(self._select(
                Trigger, "thread_id = ?", (thread.id,), "ORDER BY rowid DESC LIMIT 10"
            )),
            *_neighbours(self._select(Ticket, "thread_id = ?", (thread.id,))),
            *[(sub.ticket_id, _summary(sub)) for sub in subscriptions],
            *_neighbours(self._select(Reply, "thread_id = ?", (thread.id,))),
        ]

    def _ticket_neighbours(self, ticket):
        last_report = self._last_report(ticket.id)
        subscriptions = self._select(Subscription, "ticket_id = ?", (ticket.id,))
        return [
            *_neighbours([
                self._require(Mandate, ticket.mandate_id),
                self._require(Thread, ticket.thread_id),
                *self._select(Assignment, "ticket_id = ?", (ticket.id,)),
                *([last_report] if last_report else []),
            ]),
            *[(sub.thread_id, _summary(sub)) for sub in subscriptions],
            *_neighbours(self.undelivered_inputs(ticket.id)),
        ]

    def _assignment_neighbours(self, assignment):
        return _neighbours([
            self._require(Ticket, assignment.ticket_id),
            *self._select(Report, "assignment_id = ?", (assignment.id,)),
        ])

    def _mandate_neighbours(self, mandate):
        return _neighbours([self._require(Ticket, mandate.ticket_id)])

    def _decision_neighbours(self, decision):
        return _neighbours([
            self._require(Thread, decision.thread_id),
            *[self._require(Trigger, trigger_id) for trigger_id in decision.trigger_ids],
        ])

    def _report_neighbours(self, report):
        return _neighbours([self._require(Assignment, report.assignment_id)])

    def _wake_neighbours(self, wake):
        return _neighbours([self._require(Trigger, trigger_id) for trigger_id in wake.trigger_ids])

    def _reply_neighbours(self, reply):
        return _neighbours([self._require(Thread, reply.thread_id)])

    def _input_neighbours(self, entry):
        return _neighbours([self._require(Ticket, entry.ticket_id)])

    def _tick_neighbours(self, _tick):
        return []

    _related = {
        Trigger: _trigger_neighbours,
        Thread: _thread_neighbours,
        Ticket: _ticket_neighbours,
        Assignment: _assignment_neighbours,
        Mandate: _mandate_neighbours,
        Decision: _decision_neighbours,
        Report: _report_neighbours,
        Wake: _wake_neighbours,
        Reply: _reply_neighbours,
        Input: _input_neighbours,
        Tick: _tick_neighbours,
    }

    def board(self):
        return [
            (ticket, self._latest_assignment(ticket.id), self._last_report(ticket.id))
            for ticket in self._select(Ticket)
        ]

    def spend_since(self, stamp):
        return sum(
            self._db.execute(
                f"SELECT COALESCE(SUM(cost_usd), 0) FROM {table} WHERE started_at >= ?", (stamp,)
            ).fetchone()[0]
            for table in ("wakes", "ticks")
        )

    def status(self):
        rows = []
        for ticket in self._select(Ticket):
            assignment = self._latest_assignment(ticket.id)
            report = self._last_report(ticket.id)
            rows.append({
                "ticket": ticket.id,
                "state": ticket.state,
                "slug": ticket.slug,
                "assignment": assignment.state if assignment else None,
                "last_report": report.kind if report else None,
                "attention": report is not None and report.kind is ReportKind.waiting,
            })
        return rows
