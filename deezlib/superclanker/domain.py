import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum


class Strength(StrEnum):
    explicit = "explicit"
    inferred = "inferred"
    not_admitted = "not_admitted"


class DecisionKind(StrEnum):
    accept = "accept"
    stop = "stop"
    ignore = "ignore"
    unavailable = "unavailable"


class ReportKind(StrEnum):
    progress = "progress"
    waiting = "waiting"
    ready = "ready"
    blocked = "blocked"
    failed = "failed"
    dropped = "dropped"

    @property
    def ends_assignment(self):
        return self in (ReportKind.ready, ReportKind.failed, ReportKind.dropped)


class TicketState(StrEnum):
    open = "open"
    ended = "ended"


class AssignmentState(StrEnum):
    pending = "pending"
    running = "running"
    ended = "ended"


@dataclass(frozen=True)
class Trigger:
    id: str
    source: str
    source_event_id: str
    thread_id: str
    actor: str | None
    addressed: bool
    text: str
    parent_id: str | None
    received_at: str
    meta: dict


@dataclass(frozen=True)
class Thread:
    id: str
    source: str
    created_at: str


@dataclass(frozen=True)
class Decision:
    id: str
    thread_id: str
    trigger_ids: tuple
    kind: DecisionKind
    strength: Strength
    reason: str
    created_at: str


@dataclass(frozen=True)
class Mandate:
    id: str
    ticket_id: str
    policy_version: str
    strength: Strength
    scope: str
    rules: tuple
    sender: str | None
    source: str
    created_at: str
    withdrawn_at: str | None


@dataclass(frozen=True)
class Ticket:
    id: str
    slug: str
    thread_id: str
    mandate_id: str
    state: TicketState
    created_at: str
    ended_at: str | None
    ended_by: str | None


@dataclass(frozen=True)
class Assignment:
    id: str
    ticket_id: str
    state: AssignmentState
    session_id: str | None
    pid: int | None
    worktree: str | None
    started_at: str | None
    ended_at: str | None


@dataclass(frozen=True)
class Report:
    id: str
    assignment_id: str
    kind: ReportKind
    text: str
    question: str | None
    evidence: tuple | None
    created_at: str


@dataclass(frozen=True)
class Subscription:
    ticket_id: str
    thread_id: str
    context_only: bool


ID_PREFIXES = {
    Trigger: "t_",
    Decision: "d_",
    Mandate: "m_",
    Ticket: "k_",
    Assignment: "a_",
    Report: "r_",
}


def _short_digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def new_id(kind):
    return ID_PREFIXES[kind] + _short_digest(uuid.uuid4().hex)


def trigger_id(source, source_event_id):
    return ID_PREFIXES[Trigger] + _short_digest(json.dumps([source, source_event_id]))


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
