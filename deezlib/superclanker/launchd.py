import os
import plistlib
import subprocess
import tempfile
from pathlib import Path

LABEL = "com.dboon.super-clanker"
SYSTEM_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"


def _agents(home, agents_dir):
    return Path(agents_dir) if agents_dir else Path(home) / "Library" / "LaunchAgents"


def _target(home, agents_dir):
    return _agents(home, agents_dir) / f"{LABEL}.plist"


def plist(hub_root, root, home):
    root, home = Path(root), Path(home)
    return plistlib.dumps({
        "Label": LABEL,
        "ProgramArguments": [str(Path(hub_root) / "bin" / "deez"), "super", "daemon"],
        "RunAtLoad": True,
        "KeepAlive": True,
        "WorkingDirectory": str(root),
        "StandardOutPath": str(root / "log" / "launchd.out.log"),
        "StandardErrorPath": str(root / "log" / "launchd.err.log"),
        "EnvironmentVariables": {
            "PATH": f"{home / '.local' / 'bin'}:{SYSTEM_PATH}",
            "HOME": str(home),
            "DEEZ_SUPER_STATE": str(root),
        },
    }).decode("utf-8")


def plan(hub_root, root, home, agents_dir=None):
    path = _target(home, agents_dir)
    wanted = plist(hub_root, root, home)
    try:
        current = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        current = None
    if current is None:
        action = f"would create {path}"
    else:
        action = f"would replace {path} ({'unchanged' if current == wanted else 'changed'})"
    return [action, f"daemon {Path(hub_root) / 'bin' / 'deez'} super daemon, state {Path(root)}"]


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


def install(hub_root, root, home, agents_dir=None, apply=False, run=subprocess.run):
    if not apply:
        return plan(hub_root, root, home, agents_dir)
    path = _target(home, agents_dir)
    (Path(root) / "log").mkdir(parents=True, exist_ok=True, mode=0o700)
    _write_atomic(path, plist(hub_root, root, home))
    return [
        f"wrote {path}",
        _launchctl(run, "bootout", f"{_domain()}/{LABEL}"),
        _launchctl(run, "bootstrap", _domain(), str(path)),
        _launchctl(run, "kickstart", "-k", f"{_domain()}/{LABEL}"),
    ]


def uninstall(home, agents_dir=None, apply=False, run=subprocess.run):
    path = _target(home, agents_dir)
    if not apply:
        return [f"would boot out {LABEL} and remove {path}"]
    booted_out = _launchctl(run, "bootout", f"{_domain()}/{LABEL}")
    path.unlink(missing_ok=True)
    return [booted_out, f"removed {path}"]
