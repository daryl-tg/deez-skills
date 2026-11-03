import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from deezlib.superclanker import daemon, workers

LOCK_DIR = "daemon.lock.d"


@dataclass(frozen=True)
class Peer:
    name: str
    pid: int
    cwd: str
    status: str
    session_id: str


@dataclass(frozen=True)
class DaemonHealth:
    pid: int | None
    alive: bool
    heartbeat_age_s: int | None


def _peer(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("kind") != "interactive" or not isinstance(data.get("pid"), int):
            return None
        return Peer(
            str(data.get("name") or path.stem), data["pid"], str(data.get("cwd") or ""),
            str(data.get("status") or ""), str(data.get("sessionId") or ""),
        )
    except (OSError, ValueError, AttributeError):
        return None


def read_peers(sessions_dir, alive=workers.alive):
    found = (_peer(path) for path in Path(sessions_dir).glob("*.json"))
    return sorted((peer for peer in found if peer and alive(peer.pid)), key=lambda peer: peer.name)


def read_inbox(path, offset):
    try:
        with open(path, "rb") as stream:
            size = stream.seek(0, 2)
            start = offset if offset <= size else 0
            stream.seek(start)
            return stream.read().decode("utf-8", errors="replace"), size
    except FileNotFoundError:
        return "", 0


def _heartbeat_age(root, now):
    try:
        beat = daemon.heartbeat_path(root).read_text(encoding="utf-8").strip()
        return int((now - datetime.fromisoformat(beat)).total_seconds())
    except (OSError, ValueError):
        return None


def read_daemon_health(root, now):
    pid = daemon._lock_owner(Path(root) / LOCK_DIR)
    return DaemonHealth(pid, workers.alive(pid), _heartbeat_age(root, now))


def read_held(root):
    try:
        return int(daemon.held_path(root).read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def repo_of(worktree, root):
    if not worktree:
        return "-"
    try:
        parts = Path(worktree).relative_to(Path(root) / "worktrees").parts
    except ValueError:
        return "-"
    return parts[0] if len(parts) >= 2 else "-"


def local_midnight_utc(now):
    local = now.astimezone()
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight.astimezone(timezone.utc).isoformat(timespec="seconds")
