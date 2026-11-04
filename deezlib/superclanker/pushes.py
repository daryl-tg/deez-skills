import os
import tempfile
import time
from pathlib import Path

from deezlib.superclanker.domain import Assignment, ReportKind, Trigger, trigger_id, utc_now


def nudge_path(root):
    return Path(root) / "nudge"


def nudge(root):
    path = nudge_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(f"{time.time_ns()} {os.getpid()}\n")
    os.replace(temp, path)


def nudge_mark(root):
    try:
        return nudge_path(root).read_text(encoding="utf-8")
    except OSError:
        return ""


def report_trigger(assignment, report):
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


def push_report(store, assignment_id, report):
    if report.kind is ReportKind.progress:
        return None
    shown = store.show(assignment_id)
    shown.pop("related")
    trigger = report_trigger(Assignment(**shown), report)
    return trigger if store.receive(trigger) == "stored" else None
