import os
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import takewhile
from pathlib import Path

from deezlib.superclanker import daemon, router, sources, workers
from deezlib.superclanker.domain import (
    AssignmentState,
    DecisionKind,
    ReportKind,
    TicketState,
    utc_now,
)
from deezlib.superclanker.store import SuperError

SESSION_FILE = "watchdog.session"
ALLOWED_TOOLS = ("Bash(deez super-clanker *)",)
STALLED_REPORTS = (ReportKind.failed, ReportKind.blocked)
LOOKBACK = timedelta(hours=24)
WAKES_IN_LOOKBACK = 5000
CLIP_CHARS = 80


@dataclass(frozen=True)
class TickResult:
    tick_id: str
    denials: int
    cost_usd: float | None
    result: str | None


def _at(stamp):
    return datetime.fromisoformat(stamp)


def _clip(text):
    line = " ".join(text.split())
    return line if len(line) <= CLIP_CHARS else line[: CLIP_CHARS - 1] + "…"


def _shown(store, record_id):
    shown = store.show(record_id)
    return shown, [neighbour for neighbour, _summary in shown.pop("related")]


def _daemon_down(root, config, now):
    lock = Path(root) / "daemon.lock.d"
    owner = daemon._lock_owner(lock)
    if not workers.alive(owner):
        return [([], f"no live daemon pid in {lock / 'pid'} (found {owner or 'none'})")]
    try:
        beat = daemon.heartbeat_path(root).read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return [([], f"daemon pid {owner} is alive but {daemon.heartbeat_path(root)} is missing")]
    age = int((_at(now) - _at(beat)).total_seconds())
    limit = config.watchdog.heartbeat_stale_seconds
    if age > limit:
        return [([], f"daemon pid {owner} heartbeat is {age}s old, limit {limit}s")]
    return []


def _unreaped(store, root):
    log_dir = Path(root) / "log"
    found = []
    for assignment in store.running_assignments():
        if workers.alive(assignment.pid):
            continue
        output = workers._turn_log(
            log_dir, assignment.id, max(workers._turns(log_dir, assignment.id) - 1, 0)
        )
        if not workers._marker(output).exists():
            found.append(([assignment.id], (
                f"{assignment.id} on {assignment.ticket_id}: pid {assignment.pid} is dead and "
                f"{output.name} has no .reaped marker"
            )))
    return found


def _long_turns(store, config, now):
    limit = config.watchdog.max_turn_minutes
    found = []
    for assignment in store.running_assignments():
        if not workers.alive(assignment.pid):
            continue
        minutes = int((_at(now) - _at(assignment.started_at)).total_seconds() // 60)
        if minutes > limit:
            found.append(([assignment.id], (
                f"{assignment.id} on {assignment.ticket_id}: pid {assignment.pid} running "
                f"{minutes} minutes, limit {limit}"
            )))
    return found


def _open_tickets(store):
    tickets = []
    for row in store.status():
        if row["state"] is not TicketState.open:
            continue
        ticket, related = _shown(store, row["ticket"])
        report_id = next((i for i in related if i.startswith("r_")), None)
        report = report_id and store.show(report_id)
        tickets.append((ticket, store.assignment_for(ticket["id"]), report))
    return tickets


def _stalled(tickets):
    found = []
    for ticket, assignment, report in tickets:
        if not report or report["assignment_id"] != assignment.id:
            continue
        if report["kind"] not in STALLED_REPORTS or assignment.state is AssignmentState.pending:
            continue
        if assignment.state is AssignmentState.running and workers.alive(assignment.pid):
            continue
        found.append(([ticket["id"], assignment.id], (
            f"{ticket['id']} {ticket['slug']}: {assignment.id} ended with {report['kind']} "
            f"{report['id']}: {_clip(report['text'])}"
        )))
    return found


def _replies_since(store, thread_id, stamp):
    _thread, related = _shown(store, thread_id)
    return [
        reply_id for reply_id in related
        if reply_id.startswith("p_") and store.show(reply_id)["created_at"] >= stamp
    ]


def _unanswered(store, config, tickets, now):
    limit = timedelta(hours=config.watchdog.attention_hours)
    found = []
    for ticket, _assignment, report in tickets:
        if not report or report["kind"] is not ReportKind.waiting:
            continue
        age = _at(now) - _at(report["created_at"])
        if age <= limit or _replies_since(store, ticket["thread_id"], report["created_at"]):
            continue
        question = report["question"] or report["text"]
        found.append(([ticket["id"], report["id"]], (
            f"{ticket['id']} {ticket['slug']}: waiting {report['id']} for "
            f"{int(age.total_seconds() // 60)} minutes, no reply on {ticket['thread_id']}: "
            f"{_clip(question)}"
        )))
    return found


def _recent_wakes(store, now):
    cutoff = _at(now) - LOOKBACK
    return [wake for wake in store.recent_wakes(WAKES_IN_LOOKBACK) if _at(wake.started_at) >= cutoff]


def _undecided(store, wakes, now):
    cutoff = _at(now) - LOOKBACK
    queued = {trigger.id for trigger in store.queued()}
    seen, found = set(), []
    for trigger_id in (t for wake in reversed(wakes) for t in wake.trigger_ids):
        if trigger_id in seen or trigger_id in queued:
            continue
        seen.add(trigger_id)
        _trigger, related = _shown(store, trigger_id)
        decisions = [store.show(i) for i in related if i.startswith("d_")]
        newest = decisions[-1] if decisions else None
        if newest and newest["kind"] is DecisionKind.unavailable and _at(newest["created_at"]) >= cutoff:
            found.append(([trigger_id, newest["id"]], (
                f"{trigger_id}: decided unavailable {newest['id']} at {newest['created_at']}: "
                f"{newest['reason']}"
            )))
    return found


def _failed_wakes(wakes):
    ended = (w for w in wakes if w.ended_at is not None)
    failed = list(reversed(list(takewhile(lambda w: w.exit_code != 0, ended))))
    if not failed:
        return []
    noun = "wake" if len(failed) == 1 else "wakes"
    listed = ", ".join(
        f"{w.id} exit {'none' if w.exit_code is None else w.exit_code}" for w in failed
    )
    return [([w.id for w in failed], f"{len(failed)} {noun} failed in 24 hours: {listed}")]


def _source_errors(store, config):
    return [
        ([], f"{name}: {error} (last poll {store.cursor(name, sources.LAST_POLL) or 'never'})")
        for name, policy in config.sources.items()
        if policy.enabled and (error := store.cursor(name, sources.LAST_ERROR))
    ]


def _orphans(store, root):
    found = []
    for path in sorted((Path(root) / "worktrees").glob("*/*")):
        if not path.is_dir():
            continue
        try:
            ticket = store.show(path.name) if path.name.startswith("k_") else None
        except SuperError:
            ticket = None
        if ticket is None:
            found.append(([], f"{path}: no ticket {path.name}"))
        elif ticket["state"] is TicketState.ended:
            found.append(([path.name], f"{path}: {path.name} has ended ({ticket['ended_at']})"))
    return found


def _more(items, fallback):
    ids = [record_id for refs, _line in items for record_id in refs]
    return "; ".join(f"deez super-clanker show {record_id}" for record_id in ids) or fallback


def _anomalies(store, config, root, now):
    tickets = _open_tickets(store)
    wakes = _recent_wakes(store, now)
    return [
        (kind, items, _more(items, fallback))
        for kind, items, fallback in (
            ("daemon down", _daemon_down(root, config, now), "deez super-clanker log launchd"),
            ("unreaped turn", _unreaped(store, root), None),
            ("long turn", _long_turns(store, config, now), None),
            ("stalled ticket", _stalled(tickets), None),
            ("unanswered question", _unanswered(store, config, tickets, now), None),
            ("undecided", _undecided(store, wakes, now), None),
            ("failed wakes", _failed_wakes(wakes), None),
            ("source errors", _source_errors(store, config), "deez super-clanker log daemon"),
            ("orphan worktree", _orphans(store, root), "deez super-clanker status"),
        )
        if items
    ]


def digest(store, config, root, now=utc_now):
    return "\n\n".join(
        "\n".join([f"## {kind}", *(line for _refs, line in items), f"more: {more}"])
        for kind, items, more in _anomalies(store, config, root, now())
    )


def session_id(root):
    path = Path(root) / SESSION_FILE
    try:
        return path.read_text(encoding="utf-8").strip(), False
    except FileNotFoundError:
        pass
    sid = str(uuid.uuid4())
    handle, temp = tempfile.mkstemp(dir=root, prefix=f".{SESSION_FILE}.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(sid + "\n")
    os.chmod(temp, 0o600)
    os.replace(temp, path)
    return sid, True


def agent_prompt(hub_root):
    text = (Path(hub_root) / "agents" / "super-watchdog.md").read_text(encoding="utf-8")
    _before, _frontmatter, body = text.split("---\n", 2)
    return body.strip()


def _command(config, hub_root, sid, is_new, prompt):
    return [
        "claude", "-p", "--model", config.watchdog.model, "--tools", "Bash",
        "--allowedTools", *ALLOWED_TOOLS, "--permission-mode", "dontAsk",
        "--output-format", "json", "--strict-mcp-config", "--setting-sources", "project,local",
        "--append-system-prompt", agent_prompt(hub_root),
        "--session-id" if is_new else "--resume", sid, prompt,
    ]


def tick(store, config, root, hub_root, runner=subprocess.run):
    found = digest(store, config, root)
    if not found:
        return None
    sid, is_new = session_id(root)
    tick_id = store.begin_tick(found)
    try:
        completed = runner(
            _command(config, hub_root, sid, is_new, found), cwd=root,
            env=router._environment(root, hub_root), capture_output=True, text=True,
            timeout=router.WAKE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        completed = subprocess.CompletedProcess([], None, "", str(exc))
    outcome = router._outcome(completed)
    if outcome is None:
        store.end_tick(
            tick_id, completed.returncode, None, None, completed.stderr[-router.STDERR_TAIL_CHARS:]
        )
        if is_new:
            (Path(root) / SESSION_FILE).unlink(missing_ok=True)
        raise SuperError(f"watchdog tick {tick_id} failed with exit {completed.returncode}")
    cost = outcome.get("total_cost_usd")
    result = outcome.get("result")
    denials = router._denied_commands(outcome)
    store.end_tick(
        tick_id, completed.returncode, cost, outcome.get("session_id", sid), result, denials
    )
    return TickResult(tick_id, len(denials), cost, result)
