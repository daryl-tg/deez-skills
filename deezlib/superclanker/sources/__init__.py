import json
import subprocess
from datetime import datetime

from deezlib.superclanker.sources import github, gitlab, omchat

COMMAND_TIMEOUT_SECONDS = 60
ERROR_TAIL_CHARS = 500
LAST_POLL = "last_poll"
LAST_ERROR = "last_error"

POLLERS = {"github": github.poll, "gitlab": gitlab.poll, "omchat": omchat.poll}


class PollFailed(Exception):
    pass


def due(store, policy, now):
    last = store.cursor(policy.name, LAST_POLL)
    if last is None:
        return True
    elapsed = datetime.fromisoformat(now()) - datetime.fromisoformat(last)
    return elapsed.total_seconds() >= policy.poll_seconds


def read_json(run, argv):
    try:
        completed = run(argv, capture_output=True, text=True, check=False,
                        timeout=COMMAND_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PollFailed(f"{argv[0]}: {exc}") from None
    if completed.returncode != 0:
        said = (completed.stderr or completed.stdout).strip()[-ERROR_TAIL_CHARS:]
        raise PollFailed(f"{' '.join(argv[:3])} exited {completed.returncode}: {said}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise PollFailed(f"{' '.join(argv[:3])} printed invalid JSON: {exc}") from None


def operator(policy):
    return policy.senders[0] if policy.senders else None


def mentions(policy, body):
    return any(handle in body for handle in policy.mentions)


def record(store, policy, now, read):
    stamp = now()
    try:
        found = read()
    except PollFailed as exc:
        failure = str(exc)
    except (LookupError, TypeError, ValueError) as exc:
        failure = f"unexpected reply: {exc!r}"
    else:
        failure = ""
    store.set_cursor(policy.name, LAST_POLL, stamp)
    store.set_cursor(policy.name, LAST_ERROR, failure)
    if failure:
        return []
    me = operator(policy)
    return [
        trigger for trigger in found
        if not (me and trigger.actor == me) and store.receive(trigger) == "stored"
    ]
