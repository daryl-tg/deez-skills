import os
import plistlib
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List

CRITICAL_FREE_PCT = int(os.environ.get("MEMGUARD_CRIT_PCT", "15"))
MAX_AGE_S = int(os.environ.get("MEMGUARD_MAX_AGE_MIN", "45")) * 60
MIN_JOB_MB = int(os.environ.get("MEMGUARD_MIN_MB", "300"))
LOG_PATH = os.path.expanduser("~/Library/Logs/memguard.log")
LABEL = "com.dboon.memguard"
PLIST_PATH = os.path.expanduser(f"~/Library/LaunchAgents/{LABEL}.plist")

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
class Kill:
    root: int
    reason: str
    mem_mb: float
    age_s: int
    args: str
    pids: List[int] = field(default_factory=list)


def is_heavy(proc: Proc) -> bool:
    return bool(HEAVY.search(proc.args))


def jobs(procs: List[Proc]) -> List[Kill]:
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

    roots = {heavy_root(p).pid for p in procs if is_heavy(p)}
    found = []
    for root_pid in roots:
        root = by_pid[root_pid]
        pids = subtree(root_pid)
        mem = sum(by_pid[x].mem_mb for x in pids)
        found.append(Kill(root_pid, "", mem, root.age_s, root.args, pids))
    return [j for j in found if j.mem_mb >= MIN_JOB_MB]


def plan(procs: List[Proc], free_pct: int) -> List[Kill]:
    kills = []
    remaining = []
    for job in jobs(procs):
        root_ppid = next(p.ppid for p in procs if p.pid == job.root)
        if root_ppid == 1:
            job.reason = "orphaned"
            kills.append(job)
        elif job.age_s > MAX_AGE_S:
            job.reason = "over-age"
            kills.append(job)
        else:
            remaining.append(job)
    if free_pct < CRITICAL_FREE_PCT and remaining:
        newest = min(remaining, key=lambda j: j.age_s)
        newest.reason = "memory-critical"
        kills.append(newest)
    return kills


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
        pid, ppid = int(parts[0]), int(parts[1])
        procs.append(Proc(pid, ppid, parse_etime(parts[2]), mem.get(pid, 0.0), parts[3]))
    return procs


def free_pct() -> int:
    return parse_free_pct(subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout)


def log(message: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")


def notify(message: str) -> None:
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "memguard"'],
                   capture_output=True)


def execute(kill: Kill) -> None:
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for pid in reversed(kill.pids):
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass
        if sig == signal.SIGTERM:
            time.sleep(3)
    summary = f"killed {kill.reason} job pid {kill.root} ({kill.mem_mb / 1024:.1f} GB, {kill.age_s // 60} min): {kill.args[:160]}"
    log(summary)
    notify(f"{kill.reason}: killed {kill.mem_mb / 1024:.1f} GB job pid {kill.root}")


def launch_agent_plist(repo: str) -> str:
    return plistlib.dumps({
        "Label": LABEL,
        "ProgramArguments": [os.path.join(repo, "bin", "memguard")],
        "StartInterval": 30,
        "RunAtLoad": True,
        "ProcessType": "Interactive",
        "StandardErrorPath": os.path.expanduser("~/Library/Logs/memguard.err.log"),
    }).decode()


def install(repo: str) -> int:
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", f"{domain}/{LABEL}"], capture_output=True)
    with open(PLIST_PATH, "w") as fh:
        fh.write(launch_agent_plist(repo))
    result = subprocess.run(["launchctl", "bootstrap", domain, PLIST_PATH])
    print(f"memguard: installed {PLIST_PATH} -> {repo}/bin/memguard every 30s")
    return result.returncode


def main(argv: List[str]) -> int:
    if argv[:1] == ["install"]:
        return install(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dry_run = "--dry-run" in argv
    pct = free_pct()
    kills = plan(snapshot(), pct)
    if dry_run:
        print(f"free {pct}%")
        for k in kills:
            print(f"would kill {k.reason} root {k.root} {k.mem_mb:.0f} MB {k.age_s // 60} min: {k.args[:140]}")
        return 0
    for k in kills:
        execute(k)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
