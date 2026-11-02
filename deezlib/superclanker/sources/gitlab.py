import subprocess

from deezlib.superclanker import sources
from deezlib.superclanker.domain import Trigger, trigger_id, utc_now

SOURCE = "gitlab"
FINISHED_PIPELINES = ("success", "failed", "canceled")
OPEN_MRS = "merge_requests?scope=created_by_me&state=opened&per_page=100"
NEWEST_NOTES = "notes?sort=desc&order_by=created_at&per_page=100"


def _trigger(policy, mr, event_id, actor, body, text, received_at):
    return Trigger(
        id=trigger_id(SOURCE, event_id),
        source=SOURCE,
        source_event_id=event_id,
        thread_id=f"gl:{mr['references']['full']}",
        actor=actor,
        addressed=sources.mentions(policy, body),
        text=text,
        parent_id=None,
        received_at=received_at,
        meta={"project_id": mr["project_id"], "iid": mr["iid"], "web_url": mr["web_url"]},
    )


def mr_triggers(policy, mr, notes, pipelines):
    found = [
        _trigger(
            policy, mr, f"note:{note['id']}", note["author"]["username"], note["body"],
            note["body"], note["created_at"],
        )
        for note in reversed(notes) if not note["system"]
    ]
    found += [
        _trigger(
            policy, mr, f"pipeline:{pipeline['id']}:{pipeline['status']}", None, "",
            f"CI pipeline {pipeline['status']} on {mr['source_branch']}", pipeline["updated_at"],
        )
        for pipeline in reversed(pipelines) if pipeline["status"] in FINISHED_PIPELINES
    ]
    return found


def _in_scope(policy, mr):
    project = mr["references"]["full"].rsplit("!", 1)[0]
    return not policy.scopes or project in policy.scopes


def _read(policy, run):
    found = []
    for mr in sources.read_json(run, ["glab", "api", OPEN_MRS]):
        if not _in_scope(policy, mr):
            continue
        base = f"projects/{mr['project_id']}/merge_requests/{mr['iid']}"
        notes = sources.read_json(run, ["glab", "api", f"{base}/{NEWEST_NOTES}"])
        pipelines = sources.read_json(run, ["glab", "api", f"{base}/pipelines"])
        found += mr_triggers(policy, mr, notes, pipelines)
    return found


def poll(store, policy, run=subprocess.run, now=utc_now):
    return sources.record(store, policy, now, lambda: _read(policy, run))
