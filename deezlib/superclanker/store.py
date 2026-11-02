import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import fields, replace
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
    new_id,
    utc_now,
)


class SuperError(Exception):
    pass


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
    ended_at TEXT, ended_by TEXT);
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
"""

_TABLES = {
    Thread: "threads",
    Trigger: "triggers",
    Decision: "decisions",
    Mandate: "mandates",
    Ticket: "tickets",
    Assignment: "assignments",
    Report: "reports",
    Subscription: "subscriptions",
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
        return cls(connection)

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
            (kind for kind, prefix in ID_PREFIXES.items() if obj_id.startswith(prefix)), Thread
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
        ])

    def _thread_neighbours(self, thread):
        subscriptions = self._select(Subscription, "thread_id = ?", (thread.id,))
        return [
            *_neighbours(self._select(
                Trigger, "thread_id = ?", (thread.id,), "ORDER BY rowid DESC LIMIT 10"
            )),
            *_neighbours(self._select(Ticket, "thread_id = ?", (thread.id,))),
            *[(sub.ticket_id, _summary(sub)) for sub in subscriptions],
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

    _related = {
        Trigger: _trigger_neighbours,
        Thread: _thread_neighbours,
        Ticket: _ticket_neighbours,
        Assignment: _assignment_neighbours,
        Mandate: _mandate_neighbours,
        Decision: _decision_neighbours,
        Report: _report_neighbours,
    }

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
