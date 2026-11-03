import subprocess
from dataclasses import dataclass

PS_ARGV = ["ps", "-axo", "pid=,ppid=,uid=,rss=,command="]
PS_TIMEOUT_SECONDS = 5


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
