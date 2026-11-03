import os
import signal
import subprocess
import time
from pathlib import Path

LSOF_TIMEOUT_SECONDS = 10
POLL_SECONDS = 0.05


def _inside(root_parts, path):
    try:
        return Path(path).resolve().parts[:len(root_parts)] == root_parts
    except (OSError, RuntimeError, ValueError):
        return False


def _cwd_listing(run):
    try:
        listing = run(
            ["lsof", "-a", "-d", "cwd", "-Fpn"], capture_output=True, text=True,
            timeout=LSOF_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return listing.stdout if listing.returncode == 0 else ""


def leftovers(worktree, run=subprocess.run):
    root_parts = Path(worktree).resolve().parts
    found = []
    pid = None
    for line in _cwd_listing(run).splitlines():
        if line.startswith("p") and line[1:].isdigit():
            pid = int(line[1:])
        elif line.startswith("n") and pid is not None and pid != os.getpid():
            if _inside(root_parts, line[1:]):
                found.append(pid)
    return found


def _alive(kill, pid):
    try:
        kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _send(kill, pid, signum):
    try:
        kill(pid, signum)
    except ProcessLookupError:
        pass
    except OSError:
        return False
    return True


def sweep(worktree, run=subprocess.run, kill=os.kill, grace_seconds=3):
    pids = [
        pid for pid in leftovers(worktree, run) if _send(kill, pid, signal.SIGTERM)
    ]
    deadline = time.monotonic() + grace_seconds
    survivors = [pid for pid in pids if _alive(kill, pid)]
    while survivors and time.monotonic() < deadline:
        time.sleep(POLL_SECONDS)
        survivors = [pid for pid in survivors if _alive(kill, pid)]
    for pid in survivors:
        _send(kill, pid, signal.SIGKILL)
    return pids
