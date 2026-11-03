import os
import signal
import subprocess
import time
from dataclasses import dataclass

PS_ARGV = ["ps", "-axo", "pid=,ppid=,uid=,rss=,command="]
PS_TIMEOUT_SECONDS = 5
LSOF = "/usr/sbin/lsof"
LSOF_TIMEOUT_SECONDS = 5
TMUX_TIMEOUT_SECONDS = 5
PROTECTED_PORTS = (8097, 8098, 31337, 31338)
PROTECTED_COMMANDS = ("super-clanker daemon", "super-clanker watchdog")
MAIN_SESSION_TARGET = "clanker:main"
POLL_SECONDS = 0.05


@dataclass(frozen=True)
class Proc:
    pid: int
    ppid: int
    uid: int
    rss_kb: int
    command: str


@dataclass(frozen=True)
class Attribution:
    workers: dict
    peers: dict
    other: set


def _parse(line):
    fields = line.split(None, 4)
    if len(fields) < 5:
        return None
    try:
        pid, ppid, uid, rss = (int(field) for field in fields[:4])
    except ValueError:
        return None
    return Proc(pid, ppid, uid, rss, fields[4].strip())


def read_table(run=subprocess.run):
    try:
        listing = run(
            PS_ARGV, capture_output=True, text=True, timeout=PS_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return {}
    if listing.returncode != 0:
        return {}
    parsed = (_parse(line) for line in (listing.stdout or "").splitlines())
    return {proc.pid: proc for proc in parsed if proc is not None}


def _children(table):
    children = {}
    for proc in table.values():
        children.setdefault(proc.ppid, []).append(proc.pid)
    return children


def _descendants(children, pid):
    found = {pid}
    pending = [pid]
    while pending:
        for child in children.get(pending.pop(), ()):
            if child not in found:
                found.add(child)
                pending.append(child)
    return found


def subtree(table, pid):
    if pid not in table:
        return set()
    return _descendants(_children(table), pid)


def tree_rss_kb(table, pids):
    return sum(table[pid].rss_kb for pid in pids if pid in table)


def attribute(table, worker_roots, peer_roots):
    children = _children(table)
    claimed = set()
    workers = {}
    for ticket, roots in worker_roots.items():
        pids = set()
        for root in roots:
            if root in table:
                pids |= _descendants(children, root)
        pids -= claimed
        workers[ticket] = pids
        claimed |= pids
    peers = {}
    for name, root in peer_roots.items():
        pids = _descendants(children, root) - claimed if root in table else set()
        peers[name] = pids
        claimed |= pids
    return Attribution(workers, peers, set(table) - claimed)


def _ranked(table, children, pids):
    ranked = []
    for pid in pids:
        members = _descendants(children, pid)
        ranked.append((pid, tree_rss_kb(table, members), table[pid].command))
    ranked.sort(key=lambda entry: (-entry[1], entry[0]))
    return ranked


def child_trees(table, pid):
    children = _children(table)
    return _ranked(table, children, children.get(pid, ()))


def top_trees(table, n=20):
    children = _children(table)
    roots = [
        proc.pid for proc in table.values()
        if proc.pid > 1 and (proc.ppid == 1 or proc.ppid not in table)
    ]
    return _ranked(table, children, roots)[:n]


def _listener_pids(run, port):
    try:
        listing = run(
            [LSOF, "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t"],
            capture_output=True, text=True, timeout=LSOF_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if listing.returncode not in (0, 1):
        return None
    return {int(word) for word in (listing.stdout or "").split() if word.isdigit()}


def port_listeners(run=subprocess.run):
    found = set()
    for port in PROTECTED_PORTS:
        pids = _listener_pids(run, port)
        if pids is None:
            return None
        found |= pids
    return found


def main_session_pids(table, run=subprocess.run):
    try:
        listing = run(
            ["tmux", "list-panes", "-t", MAIN_SESSION_TARGET, "-F", "#{pane_pid}"],
            capture_output=True, text=True, timeout=TMUX_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return set()
    if listing.returncode != 0:
        return set()
    found = set()
    for word in (listing.stdout or "").split():
        if word.isdigit():
            found |= subtree(table, int(word))
    return found


def ancestors(table, pid):
    found = set()
    while pid in table and pid not in found:
        found.add(pid)
        pid = table[pid].ppid
    return found


def protected(table, own_pid, main_pids, listeners):
    if listeners is None:
        return None
    named = {
        proc.pid for proc in table.values()
        if any(marker in proc.command for marker in PROTECTED_COMMANDS)
    }
    return ancestors(table, own_pid) | set(main_pids) | set(listeners) | named


def kill_refusal(table, target, protected_pids, uid, worker_pids):
    if target <= 1:
        return "system process"
    if target not in table:
        return "not running"
    if protected_pids is None:
        return "protection unavailable"
    if table[target].uid != uid:
        return "another user's process"
    if target in worker_pids:
        return "Worker: use k"
    if subtree(table, target) & set(protected_pids):
        return "protected"
    return None


def _alive(kill, pid):
    try:
        kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True


def _signal(kill, pid, signum):
    try:
        kill(pid, signum)
    except ProcessLookupError:
        return True
    except OSError:
        return False
    return True


def _depth(table, pid, members):
    depth = 0
    while pid in members and table[pid].ppid in members:
        pid = table[pid].ppid
        depth += 1
    return depth


def kill_tree(target, read=read_table, kill=os.kill, sleep=time.sleep,
              clock=time.monotonic, grace_seconds=3):
    if target.pid <= 1:
        return []
    table = read()
    current = table.get(target.pid)
    if current is None or current.command != target.command or current.ppid != target.ppid:
        return []
    members = subtree(table, target.pid)
    ordered = sorted(members, key=lambda pid: -_depth(table, pid, members))
    signalled = [pid for pid in ordered if _signal(kill, pid, signal.SIGTERM)]
    deadline = clock() + grace_seconds
    survivors = [pid for pid in signalled if _alive(kill, pid)]
    while survivors and clock() < deadline:
        sleep(POLL_SECONDS)
        survivors = [pid for pid in survivors if _alive(kill, pid)]
    for pid in survivors:
        _signal(kill, pid, signal.SIGKILL)
    return signalled
