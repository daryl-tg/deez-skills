import os
import shutil
import subprocess
from pathlib import Path

from deezlib.superclanker.store import SuperError

TEXTUAL_PIN = "8.2.8"
VENV = Path.home() / ".local/share/deez-skills/venvs/ui"
BASE_PYTHON = "/opt/homebrew/bin/python3"
SESSION = "clanker"
REPO_ROOT = Path(__file__).resolve().parents[2]


def _describe(argv):
    return " ".join(str(part) for part in argv)


def _run(run, argv, env):
    try:
        return run([str(part) for part in argv], capture_output=True, text=True, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SuperError(f"{_describe(argv)} failed: {exc}") from exc


def _step(run, argv, env):
    completed = _run(run, argv, env)
    if completed.returncode != 0:
        tail = "\n".join((completed.stderr or "").splitlines()[-5:])
        raise SuperError(f"{_describe(argv)} failed: {tail}")


def ensure_venv(venv=VENV, run=subprocess.run, env=None):
    python = Path(venv) / "bin" / "python"
    probe = [str(python), "-c", f"import textual,sys; sys.exit(textual.__version__ != {TEXTUAL_PIN!r})"]
    try:
        installed = run(probe, capture_output=True, text=True, env=env).returncode == 0
    except (OSError, subprocess.SubprocessError):
        installed = False
    if installed:
        return python
    _step(run, [BASE_PYTHON, "-m", "venv", venv], env)
    _step(run, [Path(venv) / "bin" / "pip", "install", "--quiet", f"textual=={TEXTUAL_PIN}"], env)
    return python


def child_env(env):
    wanted = ["/opt/homebrew/bin", str(Path.home() / ".local/bin")]
    existing = [part for part in env.get("PATH", "").split(os.pathsep) if part]
    path = []
    for part in [*wanted, *existing]:
        if part not in path:
            path.append(part)
    return {**env, "PATH": os.pathsep.join(path)}


def _state_args(state):
    return ["--state", str(state)] if state else []


def _board_command(deez, state):
    return [str(deez), "super-clanker", "ui", "--no-tmux", *_state_args(state)]


def _main_command(env):
    path = env.get("PATH", os.defpath)
    return ["env", f"PATH={path}", "sh", "-c", "claude --continue || claude"]


def _window_named(windows, name):
    return next((window for window in windows if window.startswith(name)), None)


def tmux_plan(env, has_session, deez, state, windows=()):
    if "TMUX" in env:
        return []
    plan = []
    if not has_session:
        plan.append(["tmux", "new-session", "-d", "-s", SESSION, "-n", "board", *_board_command(deez, state)])
        plan.append(["tmux", "new-window", "-t", SESSION, "-n", "main", "-c", str(Path.home()), *_main_command(env)])
        board = "board"
    else:
        board = _window_named(windows, "board")
        if board is None:
            plan.append(["tmux", "new-window", "-t", SESSION, "-n", "board", *_board_command(deez, state)])
            board = "board"
        if _window_named(windows, "main") is None:
            plan.append(["tmux", "new-window", "-t", SESSION, "-n", "main", "-c", str(Path.home()), *_main_command(env)])
    plan.append(["tmux", "select-window", "-t", f"{SESSION}:{board}"])
    plan.append(["tmux", "attach", "-t", SESSION])
    return plan


def _window_names(run, env):
    listing = _run(run, ["tmux", "list-windows", "-t", SESSION, "-F", "#{window_name}"], env)
    if listing.returncode != 0:
        raise SuperError(f"tmux list-windows -t {SESSION} failed: {(listing.stderr or '').strip()}")
    return (listing.stdout or "").splitlines()


def app_argv(python, state):
    return [str(python), "-m", "deezlib.superclanker.ui_app", *_state_args(state)]


def launch(args, env, run=subprocess.run, execve=os.execve, deez=REPO_ROOT / "bin/deez", which=shutil.which):
    env = child_env(env)
    python = ensure_venv(run=run, env=env)
    state = getattr(args, "state", None)
    if not args.no_tmux and "TMUX" not in env:
        tmux = which("tmux", path=env["PATH"])
        if not tmux:
            raise SuperError(f"tmux not found on PATH {env['PATH']}")
        has_session = _run(run, ["tmux", "has-session", "-t", SESSION], env).returncode == 0
        windows = _window_names(run, env) if has_session else ()
        plan = tmux_plan(env, has_session, deez, state, windows)
        for step in plan[:-1]:
            _step(run, step, env)
        execve(tmux, plan[-1], env)
        return 0
    existing = env.get("PYTHONPATH")
    hub = str(Path(deez).parents[1])
    env = {**env, "PYTHONPATH": f"{hub}{os.pathsep}{existing}" if existing else hub}
    argv = app_argv(python, state)
    execve(argv[0], argv, env)
    return 0
