import json
import os
import plistlib
import re
import signal
import subprocess
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional

PAUSE_BELOW_PCT = int(os.environ.get("MEMGUARD_PAUSE_PCT", "15"))
RESUME_AT_PCT = int(os.environ.get("MEMGUARD_RESUME_PCT", "30"))
LAST_RESORT_PCT = int(os.environ.get("MEMGUARD_LAST_RESORT_PCT", "5"))
MIN_JOB_MB = int(os.environ.get("MEMGUARD_MIN_MB", "300"))
WEEK_S = 7 * 86400
KEEP_EVENTS_S = 35 * 86400
TICK_S = 30

LOG_PATH = os.path.expanduser("~/Library/Logs/memguard.log")
EVENTS_PATH = os.path.expanduser("~/Library/Logs/memguard.jsonl")
STATE_PATH = os.path.expanduser("~/.local/state/memguard/paused.json")
REPORT_DIR = os.path.expanduser("~/Documents/dev-notes/memguard")
LABEL = "com.dboon.memguard"
WEEKLY_LABEL = "com.dboon.memguard.weekly"
AGENTS_DIR = os.path.expanduser("~/Library/LaunchAgents")

HEAVY = re.compile(
    r"typescript/bin/tsc|(^|[\s/])tsc\s|typecheck|\bbun test\b|vitest|\bjest\b|playwright test"
    r"|om-chat-gate|test-fast|\b(next|vite|turbo) build\b|verify:cloud"
)


@dataclass
class Proc:
    pid: int
    ppid: int
    age_s: int
    mem_mb: float
    args: str


@dataclass
class Job:
    root: int
    ppid: int
    mem_mb: float
    age_s: int
    args: str
    pids: List[int]


@dataclass
class Paused:
    root: int
    pids: List[int]
    paused_at: int
    args: str
    mem_mb: float


@dataclass
class Action:
    kind: str
    root: int
    reason: str
    pids: List[int] = field(default_factory=list)
    mem_mb: float = 0.0
    args: str = ""


def is_heavy(proc: Proc) -> bool:
    return bool(HEAVY.search(proc.args))


def jobs(procs: List[Proc]) -> Dict[int, Job]:
    by_pid = {p.pid: p for p in procs}
    children: Dict[int, List[int]] = {}
    for p in procs:
        children.setdefault(p.ppid, []).append(p.pid)

    def heavy_root(p: Proc) -> Proc:
        while p.ppid in by_pid and is_heavy(by_pid[p.ppid]):
            p = by_pid[p.ppid]
        return p

    def subtree(pid: int) -> List[int]:
        out = [pid]
        for child in children.get(pid, []):
            out += subtree(child)
        return out

    found = {}
    for root_pid in {heavy_root(p).pid for p in procs if is_heavy(p)}:
        root = by_pid[root_pid]
        pids = subtree(root_pid)
        mem = sum(by_pid[x].mem_mb for x in pids)
        if mem >= MIN_JOB_MB:
            found[root_pid] = Job(root_pid, root.ppid, mem, root.age_s, root.args, pids)
    return found


def plan(procs: List[Proc], free_pct: int, paused: Dict[int, Paused]) -> List[Action]:
    by_pid = {p.pid: p for p in procs}
    live = jobs(procs)
    actions = []

    still_paused = {}
    for root, job in paused.items():
        proc = by_pid.get(root)
        if proc is None or proc.args != job.args:
            actions.append(Action("forget", root, "gone", job.pids, job.mem_mb, job.args))
        else:
            still_paused[root] = job

    for root, job in sorted(live.items()):
        if job.ppid == 1:
            actions.append(Action("kill", root, "orphaned", job.pids, job.mem_mb, job.args))
            still_paused.pop(root, None)

    killed = {a.root for a in actions if a.kind == "kill"}
    running = [j for r, j in live.items() if r not in killed and r not in still_paused]

    if free_pct < PAUSE_BELOW_PCT:
        if running:
            newest = min(running, key=lambda j: j.age_s)
            actions.append(Action("pause", newest.root, "memory-critical", newest.pids, newest.mem_mb, newest.args))
        elif free_pct < LAST_RESORT_PCT and still_paused:
            newest = min(still_paused, key=lambda r: by_pid[r].age_s)
            job = live.get(newest)
            pids = job.pids if job else still_paused[newest].pids
            mem = job.mem_mb if job else still_paused[newest].mem_mb
            actions.append(Action("kill", newest, "last-resort", pids, mem, still_paused[newest].args))
    elif free_pct >= RESUME_AT_PCT and still_paused:
        first = min(still_paused.values(), key=lambda p: p.paused_at)
        job = live.get(first.root)
        pids = sorted(set(first.pids) | set(job.pids if job else []))
        actions.append(Action("resume", first.root, "memory-recovered", pids, first.mem_mb, first.args))
    return actions


def _signal(pid: int, sig: int) -> None:
    try:
        os.kill(pid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def _event(now: int, action: Action, **extra) -> dict:
    return {"ts": now, "event": action.kind, "root": action.root, "reason": action.reason,
            "mem_mb": round(action.mem_mb), "args": action.args[:300], **extra}


def _resume_all(state: Dict[int, Paused], now: int, send: Callable[[int, int], None], reason: str) -> List[dict]:
    events = []
    for root, job in list(state.items()):
        for pid in job.pids:
            send(pid, signal.SIGCONT)
        events.append(_event(now, Action("resume", root, reason, job.pids, job.mem_mb, job.args),
                             paused_s=now - job.paused_at))
        del state[root]
    return events


def safe_tick(procs: List[Proc], free_pct: int, state: Dict[int, Paused], now: int,
              send: Callable[[int, int], None] = _signal,
              planner: Callable[..., List[Action]] = plan,
              sleep: Callable[[float], None] = time.sleep) -> List[dict]:
    try:
        events = []
        for action in planner(procs, free_pct, state):
            if action.kind == "pause":
                for pid in action.pids:
                    send(pid, signal.SIGSTOP)
                state[action.root] = Paused(action.root, action.pids, now, action.args, action.mem_mb)
                events.append(_event(now, action, free=free_pct))
            elif action.kind == "resume":
                for pid in action.pids:
                    send(pid, signal.SIGCONT)
                paused_at = state.pop(action.root).paused_at
                events.append(_event(now, action, free=free_pct, paused_s=now - paused_at))
            elif action.kind == "kill":
                for pid in reversed(action.pids):
                    send(pid, signal.SIGTERM)
                    send(pid, signal.SIGCONT)
                sleep(3)
                for pid in reversed(action.pids):
                    send(pid, signal.SIGKILL)
                state.pop(action.root, None)
                events.append(_event(now, action, free=free_pct))
            elif action.kind == "forget":
                state.pop(action.root, None)
                events.append(_event(now, action))
        return events
    except Exception as exc:
        return [{"ts": now, "event": "error", "error": repr(exc)}] + _resume_all(state, now, send, "failsafe")


def _source(args: str) -> str:
    m = re.search(r"cd ([^ ;&']+)", args)
    if m:
        return os.path.basename(m.group(1).rstrip("/"))
    return args[:60]


def weekly_report(events: List[dict], now: int) -> str:
    week = [e for e in events if e["ts"] >= now - WEEK_S]
    samples = [e["free"] for e in week if e["event"] == "sample"]
    pauses = [e for e in week if e["event"] == "pause"]
    resumes = [e for e in week if e["event"] == "resume"]
    kills = [e for e in week if e["event"] == "kill"]
    errors = [e for e in week if e["event"] == "error"]
    start = time.strftime("%Y-%m-%d", time.localtime(now - WEEK_S))
    end = time.strftime("%Y-%m-%d", time.localtime(now))

    lines = [f"# memguard weekly report, {start} to {end}", ""]
    if not pauses and not kills:
        lines.append("Nothing paused or killed this week.")
        lines.append("")
    lines += [
        f"- Lowest free memory: {min(samples)}%" if samples else "- Lowest free memory: no samples",
        f"- Time under {PAUSE_BELOW_PCT}% free: about {sum(1 for s in samples if s < PAUSE_BELOW_PCT) * TICK_S // 60} min",
        f"- Paused: {len(pauses)}",
        f"- Resumed: {len(resumes)}",
        f"- Longest pause: {max((e.get('paused_s', 0) for e in resumes), default=0) // 60} min",
        f"- Killed: {len(kills)}",
        f"- Errors (everything resumed): {len(errors)}",
    ]
    if pauses:
        lines += ["", "## What caused the pauses", ""]
        for source, count in Counter(_source(e["args"]) for e in pauses).most_common(10):
            lines.append(f"- {source}: {count}")
    if kills:
        lines += ["", "## Kills", ""]
        for e in kills:
            when = time.strftime("%a %H:%M", time.localtime(e["ts"]))
            lines.append(f"- {when}, {e['reason']}, {e['mem_mb'] / 1024:.1f} GB: {_source(e['args'])}")
    return "\n".join(lines) + "\n"


def parse_free_pct(memory_pressure_output: str) -> int:
    return int(re.search(r"free percentage:\s*(\d+)%", memory_pressure_output).group(1))


UNIT_TO_MB = {"B": 1 / 1048576, "K": 1 / 1024, "M": 1, "G": 1024}


def parse_top(top_output: str) -> Dict[int, float]:
    mem = {}
    for line in top_output.splitlines():
        m = re.match(r"\s*(\d+)\s+([\d.]+)([BKMG])\+?\s*$", line)
        if m:
            mem[int(m.group(1))] = float(m.group(2)) * UNIT_TO_MB[m.group(3)]
    return mem


def parse_etime(etime: str) -> int:
    days, _, rest = etime.rpartition("-")
    parts = [int(x) for x in rest.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return (int(days) if days else 0) * 86400 + h * 3600 + m * 60 + s


def snapshot() -> List[Proc]:
    mem = parse_top(subprocess.run(["top", "-l", "1", "-n", "3000", "-stats", "pid,mem"],
                                   capture_output=True, text=True).stdout)
    out = subprocess.run(["ps", "-U", str(os.getuid()), "-o", "pid=,ppid=,etime=,args="],
                         capture_output=True, text=True).stdout
    procs = []
    for line in out.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 4 or int(parts[0]) == os.getpid():
            continue
        procs.append(Proc(int(parts[0]), int(parts[1]), parse_etime(parts[2]), mem.get(int(parts[0]), 0.0), parts[3]))
    return procs


def free_pct(timeout_seconds: float = 5) -> int:
    return parse_free_pct(subprocess.run(
        ["memory_pressure"], capture_output=True, text=True, timeout=timeout_seconds,
    ).stdout)


def load_state() -> Dict[int, Paused]:
    try:
        with open(STATE_PATH) as fh:
            return {int(k): Paused(**v) for k, v in json.load(fh).items()}
    except FileNotFoundError:
        return {}


def save_state(state: Dict[int, Paused]) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as fh:
        json.dump({str(k): asdict(v) for k, v in state.items()}, fh)
    os.replace(tmp, STATE_PATH)


def load_events() -> List[dict]:
    try:
        with open(EVENTS_PATH) as fh:
            return [json.loads(line) for line in fh if line.strip()]
    except FileNotFoundError:
        return []


def record(events: List[dict]) -> None:
    with open(EVENTS_PATH, "a") as fh:
        for e in events:
            fh.write(json.dumps(e) + "\n")
    with open(LOG_PATH, "a") as fh:
        for e in events:
            if e["event"] == "sample":
                continue
            stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e["ts"]))
            detail = e.get("error") or f"pid {e['root']} {e.get('mem_mb', 0) / 1024:.1f} GB {e.get('reason', '')}: {e.get('args', '')[:160]}"
            fh.write(f"{stamp} {e['event']} {detail}\n")


def notify(message: str) -> None:
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "memguard"'],
                   capture_output=True)


def tick(dry_run: bool) -> int:
    now = int(time.time())
    state = load_state()
    pct = free_pct()
    procs = snapshot()
    if dry_run:
        print(f"free {pct}%, paused {sorted(state)}")
        for a in plan(procs, pct, state):
            print(f"would {a.kind} ({a.reason}) root {a.root} {a.mem_mb:.0f} MB: {a.args[:140]}")
        return 0
    events = [{"ts": now, "event": "sample", "free": pct}] + safe_tick(procs, pct, state, now)
    save_state(state)
    record(events)
    for e in events:
        if e["event"] in ("kill", "error"):
            notify(f"{e['event']} {e.get('reason', '')}: pid {e.get('root', '')}")
    return 0


def resume_all() -> int:
    state = load_state()
    events = _resume_all(state, int(time.time()), _signal, "manual")
    save_state(state)
    record(events)
    print(f"memguard: resumed {len(events)} paused job(s)")
    return 0


def report() -> int:
    now = int(time.time())
    events = load_events()
    text = weekly_report(events, now)
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, f"{time.strftime('%Y-%m-%d', time.localtime(now))}-weekly.md")
    with open(path, "w") as fh:
        fh.write(text)
    kept = [e for e in events if e["ts"] >= now - KEEP_EVENTS_S]
    with open(EVENTS_PATH, "w") as fh:
        for e in kept:
            fh.write(json.dumps(e) + "\n")
    week = [e for e in events if e["ts"] >= now - WEEK_S]
    notify(f"weekly: {sum(e['event'] == 'pause' for e in week)} paused, "
           f"{sum(e['event'] == 'kill' for e in week)} killed. Report in dev-notes/memguard")
    print(path)
    return 0


def launch_agent_plist(repo: str) -> str:
    return plistlib.dumps({
        "Label": LABEL,
        "ProgramArguments": [os.path.join(repo, "bin", "memguard")],
        "StartInterval": TICK_S,
        "RunAtLoad": True,
        "ProcessType": "Interactive",
        "StandardErrorPath": os.path.expanduser("~/Library/Logs/memguard.err.log"),
    }).decode()


def weekly_plist(repo: str) -> str:
    return plistlib.dumps({
        "Label": WEEKLY_LABEL,
        "ProgramArguments": [os.path.join(repo, "bin", "memguard"), "report"],
        "StartCalendarInterval": {"Weekday": 1, "Hour": 9, "Minute": 0},
        "StandardErrorPath": os.path.expanduser("~/Library/Logs/memguard.err.log"),
    }).decode()


def _agents(repo: Optional[str]):
    yield LABEL, launch_agent_plist(repo) if repo else ""
    yield WEEKLY_LABEL, weekly_plist(repo) if repo else ""


def uninstall() -> int:
    domain = f"gui/{os.getuid()}"
    for label, _ in _agents(None):
        subprocess.run(["launchctl", "bootout", f"{domain}/{label}"], capture_output=True)
        path = os.path.join(AGENTS_DIR, f"{label}.plist")
        if os.path.exists(path):
            os.remove(path)
    return resume_all()


def install(repo: str) -> int:
    domain = f"gui/{os.getuid()}"
    code = 0
    for label, body in _agents(repo):
        path = os.path.join(AGENTS_DIR, f"{label}.plist")
        subprocess.run(["launchctl", "bootout", f"{domain}/{label}"], capture_output=True)
        with open(path, "w") as fh:
            fh.write(body)
        code |= subprocess.run(["launchctl", "bootstrap", domain, path]).returncode
        print(f"memguard: loaded {path}")
    return code


def main(argv: List[str]) -> int:
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    command = argv[0] if argv else ""
    if command == "install":
        return install(repo)
    if command == "uninstall":
        return uninstall()
    if command == "resume-all":
        return resume_all()
    if command == "report":
        return report()
    return tick(dry_run=command == "--dry-run")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
