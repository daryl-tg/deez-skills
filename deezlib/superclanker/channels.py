import subprocess
import urllib.parse

from deezlib.superclanker.sources import COMMAND_TIMEOUT_SECONDS, ERROR_TAIL_CHARS


def _github(address, text):
    repo, number = address.rsplit("#", 1)
    return ["gh", "pr", "comment", number, "--repo", repo, "--body", text]


def _gitlab(address, text):
    project, iid = address.rsplit("!", 1)
    path = urllib.parse.quote(project, safe="")
    return ["glab", "api", f"projects/{path}/merge_requests/{iid}/notes", "-f", f"body={text}"]


WRITERS = {"gh": _github, "gl": _gitlab}
UNWRITTEN = {"om": "om channel not implemented"}


def _post(run, argv):
    try:
        completed = run(argv, capture_output=True, text=True, check=False,
                        timeout=COMMAND_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return str(exc)
    if completed.returncode != 0:
        return (completed.stderr or completed.stdout).strip()[-ERROR_TAIL_CHARS:]
    return None


def deliver(store, config, run=subprocess.run):
    lines = []
    for reply in store.unsent_replies():
        channel, _colon, address = reply.thread_id.partition(":")
        if channel in UNWRITTEN:
            lines.append(f"{reply.id}: {UNWRITTEN[channel]}")
            continue
        if channel not in WRITERS:
            continue
        failure = _post(run, WRITERS[channel](address, reply.text))
        if failure is None:
            store.mark_sent(reply.id)
        else:
            lines.append(f"{reply.id}: {failure}")
    return lines
