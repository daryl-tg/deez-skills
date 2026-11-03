import json
import os
import re
import signal
import subprocess
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from deezlib.superclanker.domain import (
    Assignment,
    AssignmentState,
    DecisionKind,
    Mandate,
    Report,
    ReportKind,
    Ticket,
    TicketState,
    Trigger,
    trigger_id,
    utc_now,
)
from deezlib.superclanker.router import _environment
from deezlib.superclanker.store import InputKind, SuperError

REPORT_LINE = re.compile(r"^REPORT (progress|waiting|ready|blocked|failed|dropped) (.*)$", re.M)
ERR_TAIL_CHARS = 300
SESSION_FLAGS = (
    "--permission-mode", "bypassPermissions", "--output-format", "json", "--strict-mcp-config",
)
NO_REPORT = "worker exited without a report"
TICKET_MARK = ".ticket"
_children = {}


@dataclass(frozen=True)
class TicketPaths:
    notes: Path
    worktrees: Path
    scratch: Path
    log: Path


def _marked_ticket(folder):
    try:
        return (folder / TICKET_MARK).read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None


def _notes_folder(notes_root, ticket):
    shared = notes_root / ticket.slug
    if not shared.exists() or _marked_ticket(shared) == ticket.id:
        return shared
    return notes_root / f"{ticket.slug}-{ticket.id}"


def paths(root, dev_notes_root, ticket):
    root = Path(root)
    notes_root = Path(
        dev_notes_root
        or os.environ.get("DEEZ_SUPER_DEVNOTES")
        or Path.home() / "Documents" / "dev-notes"
    ).expanduser().absolute()
    return TicketPaths(
        _notes_folder(notes_root, ticket), root / "worktrees", root / "work" / ticket.id,
        root / "log",
    )


def _git(run, repo, *args):
    return run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _base(run, repo):
    for ref in ("origin/main", "main"):
        if _git(run, repo, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return ref
    return "HEAD"


def prepare_workspace(ticket, repo, slug, root, run=subprocess.run):
    where = paths(root, None, ticket)
    if repo is None:
        where.scratch.mkdir(parents=True, exist_ok=True)
        return where.scratch, None
    repo = Path(repo)
    branch = f"daryl/{slug}"
    worktree = where.worktrees / repo.name / ticket.id
    if (worktree / ".git").exists():
        return worktree, branch
    worktree.parent.mkdir(parents=True, exist_ok=True)
    if _git(run, repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}").returncode == 0:
        added = _git(run, repo, "worktree", "add", str(worktree), branch)
    else:
        added = _git(run, repo, "worktree", "add", "-b", branch, str(worktree), _base(run, repo))
    if added.returncode != 0:
        raise SuperError(f"git worktree add for {ticket.id} failed: {added.stderr.strip()}")
    return worktree, branch


def _load(store, kind, record_id):
    shown = store.show(record_id)
    shown.pop("related")
    return kind(**shown)


def _reports(store, assignment_id):
    return [
        _load(store, Report, neighbour)
        for neighbour, _summary in store.show(assignment_id)["related"]
        if neighbour.startswith("r_")
    ]


def _write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(text)
    os.replace(temp, path)


def _one_line(text):
    return " ".join(text.split())


def _noted(inputs, key):
    prefix = f"{key}: "
    found = [
        entry.text.removeprefix(prefix) for entry in inputs
        if entry.kind is InputKind.note and entry.text.startswith(prefix)
    ]
    return found[-1] if found else None


def _basis(store, trigger):
    for neighbour, _summary in store.show(trigger.id)["related"]:
        if neighbour.startswith("d_"):
            decision = store.show(neighbour)
            if decision["kind"] is DecisionKind.accept:
                return decision["reason"]
    return "-"


def _template(hub_root, name):
    return (Path(hub_root) / "templates" / name).read_text(encoding="utf-8")


def _model(config):
    return ["--model", config.workers.model] if config.workers.model else []


ROUTE_YOURSELF = (
    "No playbook was named. Pick it from the clanker-mode skill's playbook table, "
    "as a clanker-mode lead does, and copy its steps into your todo list verbatim."
)


def _playbook_line(playbook):
    if playbook is None:
        return ROUTE_YOURSELF
    return f"`{playbook}`, the playbook for this ticket. Copy its steps into your todo list verbatim."


def brief_text(hub_root, fields):
    return _template(hub_root, "super-worker-brief.md").format_map(
        {**fields, "playbook": _playbook_line(fields.get("playbook"))}
    )


def _resume_note(ticket, goal, playbook, cwd, branch, brief):
    return "\n".join([
        f"# Resume note for {ticket.id}",
        "",
        f"- Goal: {goal}",
        f"- Playbook: {playbook or 'not named; chosen from the clanker-mode table'}",
        f"- Worktree: `{cwd}`",
        f"- Branch: {branch or 'none, scratch directory'}",
        "- Status: launched, no step done yet",
        f"- Next action: read brief.md at `{brief}`",
        "",
    ])


def _turn_log(log_dir, assignment_id, turn):
    name = f"{assignment_id}.json" if turn == 0 else f"{assignment_id}.{turn}.json"
    return log_dir / name


def _turns(log_dir, assignment_id):
    turn = 0
    while _turn_log(log_dir, assignment_id, turn).exists():
        turn += 1
    return turn


def _marker(output):
    return output.with_suffix(".reaped")


def _spawn(popen, argv, cwd, root, hub_root, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as out, \
            output.with_suffix(".err").open("w", encoding="utf-8") as err:
        process = popen(
            argv, cwd=cwd, env=_environment(root, hub_root), stdin=subprocess.DEVNULL,
            stdout=out, stderr=err, start_new_session=True,
        )
    _children[process.pid] = process
    return process.pid


def launch(store, config, assignment_id, hub_root, root, dev_notes_root=None,
           popen=subprocess.Popen):
    hub_root, root = Path(hub_root), Path(root)
    assignment = _load(store, Assignment, assignment_id)
    ticket = _load(store, Ticket, assignment.ticket_id)
    if ticket.state is TicketState.ended:
        raise SuperError(f"{ticket.id} has ended; {assignment_id} will not launch")
    if assignment.state is not AssignmentState.pending:
        raise SuperError(f"{assignment_id} is {assignment.state}, not pending")
    running = len(store.running_assignments())
    limit = config.workers.max_running
    if running >= limit:
        raise SuperError(f"{running} of {limit} workers running; {assignment_id} stays pending")
    mandate = _load(store, Mandate, ticket.mandate_id)
    origin = store.ticket_origin(ticket.id)
    inputs = store.undelivered_inputs(ticket.id)
    facts = store.inputs(ticket.id)
    playbook = _noted(facts, "playbook")
    repo = _noted(facts, "repo")
    cwd, branch = prepare_workspace(ticket, repo and Path(repo), ticket.slug, root)
    where = paths(root, dev_notes_root, ticket)
    brief = where.notes / "brief.md"
    mandate_path = where.notes / "mandate.md"
    resume_note = where.notes / "resume.md"
    _write_atomic(where.notes / TICKET_MARK, f"{ticket.id}\n")
    goal = f'{origin.actor} asked on {origin.thread_id}: "{_one_line(origin.text)}"'
    _write_atomic(mandate_path, _template(hub_root, "super-worker-mandate.md").format_map({
        "ticket_id": ticket.id, "slug": ticket.slug, "thread": ticket.thread_id,
        "strength": mandate.strength, "basis": _basis(store, origin), "scope": mandate.scope,
        "rules": ", ".join(mandate.rules) or "none", "policy_version": mandate.policy_version,
        "sender": mandate.sender or "-", "source": mandate.source,
        "created_at": mandate.created_at,
    }))
    _write_atomic(brief, brief_text(hub_root, {
        "clanker_skill": hub_root / "skills" / "clanker-mode" / "SKILL.md",
        "playbook": playbook,
        "mandate_path": mandate_path,
        "worktree": cwd,
        "branch": f"`{branch}`" if branch else "none, this scratch directory has no repository",
        "goal": goal,
        "inputs": "\n".join(f"- {entry.kind}: {entry.text}" for entry in inputs) or "- none",
        "assignment_id": assignment_id,
        "ticket_id": ticket.id,
        "resume_note": resume_note,
    }))
    if not resume_note.exists():
        _write_atomic(resume_note, _resume_note(ticket, goal, playbook, cwd, branch, brief))
    sid = str(uuid.uuid4())
    argv = [
        "claude", "-p", "--agent", "clanker-agent", "--session-id", sid, *SESSION_FLAGS,
        *_model(config),
        f"Read and execute, exactly, the handoff at {brief}. "
        "Return the artifact and your own account of it.",
    ]
    pid = _spawn(popen, argv, cwd, root, hub_root, _turn_log(where.log, assignment_id, 0))
    started = store.start_assignment(assignment_id, sid, pid, cwd)
    store.mark_delivered([entry.id for entry in inputs])
    return started


def _inputs_message(store, ticket_id, inputs):
    blocks = [f"# inputs for {ticket_id}"]
    for entry in inputs:
        if entry.kind is InputKind.trigger:
            trigger = _load(store, Trigger, entry.text)
            blocks.append(
                f"## {trigger.id} {trigger.source} {trigger.thread_id} {trigger.actor or '-'}\n"
                f"{trigger.text}"
            )
        else:
            blocks.append(f"## note\n{entry.text}")
    return "\n\n".join(blocks)


def _require_reaped(log_dir, assignment_id):
    turns = _turns(log_dir, assignment_id)
    if turns and not _marker(_turn_log(log_dir, assignment_id, turns - 1)).exists():
        raise SuperError(f"{assignment_id} finished a turn nobody reaped; run deez super-clanker reap first")
    return turns


def _start_turn(store, config, assignment, inputs, turn, hub_root, root, popen):
    argv = [
        "claude", "-p", "--resume", assignment.session_id, *SESSION_FLAGS, *_model(config),
        _inputs_message(store, assignment.ticket_id, inputs),
    ]
    pid = _spawn(
        popen, argv, assignment.worktree, root, hub_root,
        _turn_log(root / "log", assignment.id, turn),
    )
    started = store.start_assignment(assignment.id, assignment.session_id, pid, assignment.worktree)
    store.mark_delivered([entry.id for entry in inputs])
    return started


def resume(store, config, assignment_id, hub_root, root, popen=subprocess.Popen):
    root = Path(root)
    assignment = _load(store, Assignment, assignment_id)
    if assignment.state is not AssignmentState.running or alive(assignment.pid):
        return None
    inputs = store.undelivered_inputs(assignment.ticket_id)
    if not inputs:
        return None
    turns = _require_reaped(root / "log", assignment_id)
    return _start_turn(store, config, assignment, inputs, turns, hub_root, root, popen)


def revive(store, config, ticket_id, hub_root, root, popen=subprocess.Popen):
    root = Path(root)
    previous = store.assignment_for(ticket_id)
    if previous.state is not AssignmentState.ended or previous.session_id is None:
        return None
    if alive(previous.pid):
        return None
    inputs = store.undelivered_inputs(ticket_id)
    if not inputs:
        return None
    _require_reaped(root / "log", previous.id)
    running = len(store.running_assignments())
    limit = config.workers.max_running
    if running >= limit:
        raise SuperError(f"{running} of {limit} workers running; {ticket_id} waits for a slot")
    store.reopen(ticket_id)
    successor = store.succeed_assignment(ticket_id)
    return _start_turn(store, config, successor, inputs, 0, hub_root, root, popen)


def alive(pid, kill=os.kill):
    if pid is None:
        return False
    child = _children.get(pid)
    if child is not None:
        if child.poll() is None:
            return True
        del _children[pid]
        return False
    try:
        kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _final_report(output):
    try:
        outcome = json.loads(output.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    result = outcome.get("result") if isinstance(outcome, dict) else None
    found = REPORT_LINE.findall(result) if isinstance(result, str) else []
    if not found:
        return None
    kind, text = found[-1]
    return ReportKind(kind), text.strip()


def _no_report_text(err):
    try:
        tail = err.read_text(encoding="utf-8", errors="replace")[-ERR_TAIL_CHARS:].strip()
    except FileNotFoundError:
        tail = ""
    return f"{NO_REPORT}: {tail}" if tail else NO_REPORT


def _earlier_reports(log_dir, assignment_id, turns):
    markers = (_marker(_turn_log(log_dir, assignment_id, turn)) for turn in range(turns - 1))
    return {marker.read_text(encoding="utf-8").strip() for marker in markers if marker.exists()}


def _turn_report(store, assignment, output, earlier):
    recent = [
        report for report in _reports(store, assignment.id)
        if report.created_at >= assignment.started_at and report.id not in earlier
    ]
    said = _final_report(output)
    if said:
        same = next((r for r in reversed(recent) if (r.kind, r.text) == said), None)
        if same:
            return same
    if assignment.state is AssignmentState.ended:
        return recent[-1] if recent else None
    if said:
        kind, text = said
        return store.report(
            assignment.id, kind, text, question=text if kind is ReportKind.waiting else None
        )
    if recent:
        return recent[-1]
    return store.report(assignment.id, ReportKind.failed, _no_report_text(output.with_suffix(".err")))


def _report_trigger(assignment, report):
    ticket_id = assignment.ticket_id
    return Trigger(
        id=trigger_id("worker", report.id),
        source="worker",
        source_event_id=report.id,
        thread_id=f"worker:{ticket_id}",
        actor=f"worker:{ticket_id}",
        addressed=True,
        text=f"REPORT {report.kind} {report.text}",
        parent_id=None,
        received_at=utc_now(),
        meta={
            "ticket": ticket_id, "assignment": assignment.id, "report": report.id,
            "question": report.question,
            "evidence": list(report.evidence) if report.evidence else None,
        },
    )


def _reapable(store):
    running = store.running_assignments()
    seen = {assignment.id for assignment in running}
    finished = [store.assignment_for(row["ticket"]) for row in store.status()]
    return running + [
        assignment for assignment in finished
        if assignment.id not in seen and assignment.state is AssignmentState.ended
        and assignment.started_at is not None
    ]


def reap(store, root):
    log_dir = Path(root) / "log"
    emitted = []
    for assignment in _reapable(store):
        if alive(assignment.pid):
            continue
        turns = _turns(log_dir, assignment.id)
        output = _turn_log(log_dir, assignment.id, max(turns - 1, 0))
        marker = _marker(output)
        if marker.exists():
            continue
        report = _turn_report(
            store, assignment, output, _earlier_reports(log_dir, assignment.id, turns)
        )
        if report is None:
            _write_atomic(marker, "")
            continue
        if report.kind is ReportKind.dropped:
            store.end_ticket(assignment.ticket_id, "dropped")
        trigger = _report_trigger(assignment, report)
        stored = store.receive(trigger) == "stored"
        _write_atomic(marker, report.id)
        if stored:
            emitted.append(trigger)
    return emitted


def _signal(kill, pid, signum):
    for target in (-pid, pid):
        try:
            kill(target, signum)
            return
        except ProcessLookupError:
            continue


def stop(store, assignment_id, kill=os.kill, grace_seconds=5):
    assignment = _load(store, Assignment, assignment_id)
    if assignment.state is AssignmentState.ended:
        return None
    if alive(assignment.pid, kill):
        _signal(kill, assignment.pid, signal.SIGTERM)
        deadline = time.monotonic() + grace_seconds
        while alive(assignment.pid, kill) and time.monotonic() < deadline:
            time.sleep(0.05)
        if alive(assignment.pid, kill):
            _signal(kill, assignment.pid, signal.SIGKILL)
    return store.report(assignment_id, ReportKind.failed, "stopped by operator")
