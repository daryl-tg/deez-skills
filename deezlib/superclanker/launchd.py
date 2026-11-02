import os
import plistlib
import subprocess
import tempfile
import time
from pathlib import Path

from deezlib.superclanker import config

LABEL = "com.dboon.super-clanker"
WATCHDOG_LABEL = "com.dboon.super-watchdog"
SYSTEM_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"


def _agents(home, agents_dir):
    return Path(agents_dir) if agents_dir else Path(home) / "Library" / "LaunchAgents"


def _target(home, agents_dir, label=LABEL):
    return _agents(home, agents_dir) / f"{label}.plist"


def _job(label, verb, log_name, hub_root, root, home):
    root, home = Path(root), Path(home)
    return {
        "Label": label,
        "ProgramArguments": [str(Path(hub_root) / "bin" / "deez"), "super", verb],
        "WorkingDirectory": str(root),
        "StandardOutPath": str(root / "log" / f"{log_name}.out.log"),
        "StandardErrorPath": str(root / "log" / f"{log_name}.err.log"),
        "EnvironmentVariables": {
            "PATH": f"{home / '.local' / 'bin'}:{SYSTEM_PATH}",
            "HOME": str(home),
            "DEEZ_SUPER_STATE": str(root),
        },
    }


def plist(hub_root, root, home):
    job = _job(LABEL, "daemon", "launchd", hub_root, root, home)
    return plistlib.dumps({**job, "RunAtLoad": True, "KeepAlive": True}).decode("utf-8")


def watchdog_plist(hub_root, root, home):
    job = _job(WATCHDOG_LABEL, "watchdog", "watchdog", hub_root, root, home)
    interval = config.load(root).watchdog.interval_seconds
    return plistlib.dumps({**job, "StartInterval": interval, "RunAtLoad": False}).decode("utf-8")


def _plists(hub_root, root, home, agents_dir):
    return [
        (LABEL, _target(home, agents_dir), plist(hub_root, root, home)),
        (WATCHDOG_LABEL, _target(home, agents_dir, WATCHDOG_LABEL),
         watchdog_plist(hub_root, root, home)),
    ]


def _planned(path, wanted):
    try:
        current = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"would create {path}"
    return f"would replace {path} ({'unchanged' if current == wanted else 'changed'})"


def plan(hub_root, root, home, agents_dir=None):
    deez = Path(hub_root) / "bin" / "deez"
    interval = config.load(root).watchdog.interval_seconds
    return [
        *(_planned(path, wanted) for _label, path, wanted in _plists(hub_root, root, home, agents_dir)),
        f"daemon {deez} super daemon, state {Path(root)}",
        f"watchdog {deez} super watchdog every {interval}s, state {Path(root)}",
    ]


def _launchctl(run, *args):
    completed = run(["launchctl", *args], capture_output=True, text=True)
    return f"launchctl {' '.join(args)} exit {completed.returncode}"


def _domain():
    return f"gui/{os.getuid()}"


def _write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(text)
    os.chmod(temp, 0o644)
    os.replace(temp, path)


BOOTOUT_POLLS = 8
BOOTOUT_POLL_SECONDS = 0.25


def _loaded(run, label):
    completed = run(["launchctl", "print", f"{_domain()}/{label}"], capture_output=True, text=True)
    return completed.returncode == 0


def _current(path):
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def install(hub_root, root, home, agents_dir=None, apply=False, run=subprocess.run,
            sleep=time.sleep):
    if not apply:
        return plan(hub_root, root, home, agents_dir)
    (Path(root) / "log").mkdir(parents=True, exist_ok=True, mode=0o700)
    lines = []
    for label, path, wanted in _plists(hub_root, root, home, agents_dir):
        loaded = _loaded(run, label)
        if loaded and _current(path) == wanted:
            lines.append(f"kept {path}")
            if label == LABEL:
                lines.append(_launchctl(run, "kickstart", "-k", f"{_domain()}/{label}"))
            continue
        _write_atomic(path, wanted)
        lines.append(f"wrote {path}")
        if loaded:
            lines.append(_launchctl(run, "bootout", f"{_domain()}/{label}"))
            for _attempt in range(BOOTOUT_POLLS):
                if not _loaded(run, label):
                    break
                sleep(BOOTOUT_POLL_SECONDS)
        lines.append(_launchctl(run, "bootstrap", _domain(), str(path)))
        if label == LABEL:
            lines.append(_launchctl(run, "kickstart", "-k", f"{_domain()}/{label}"))
    return lines


def uninstall(home, agents_dir=None, apply=False, run=subprocess.run):
    lines = []
    for label in (LABEL, WATCHDOG_LABEL):
        path = _target(home, agents_dir, label)
        if not apply:
            lines.append(f"would boot out {label} and remove {path}")
            continue
        lines.append(_launchctl(run, "bootout", f"{_domain()}/{label}"))
        path.unlink(missing_ok=True)
        lines.append(f"removed {path}")
    return lines
