import os
import subprocess
from pathlib import Path

from deezlib.superclanker.store import SuperError

TEXTUAL_PIN = "8.2.8"
VENV = Path.home() / ".local/share/deez-skills/venvs/ui"
BASE_PYTHON = "/opt/homebrew/bin/python3"
SESSION = "clanker"
REPO_ROOT = Path(__file__).resolve().parents[2]


def _step(run, argv):
    completed = run([str(part) for part in argv], capture_output=True, text=True)
    if completed.returncode != 0:
        tail = "\n".join((completed.stderr or "").splitlines()[-5:])
        raise SuperError(f"{' '.join(str(part) for part in argv)} failed: {tail}")


def ensure_venv(venv=VENV, run=subprocess.run):
    python = Path(venv) / "bin" / "python"
    probe = [str(python), "-c", f"import textual,sys; sys.exit(textual.__version__ != {TEXTUAL_PIN!r})"]
    if run(probe, capture_output=True, text=True).returncode == 0:
        return python
    _step(run, [BASE_PYTHON, "-m", "venv", venv])
    _step(run, [Path(venv) / "bin" / "pip", "install", "--quiet", f"textual=={TEXTUAL_PIN}"])
    return python


def _state_args(state):
    return ["--state", str(state)] if state else []


def tmux_plan(env, has_session, deez, state):
    if "TMUX" in env:
        return []
    plan = []
    if not has_session:
        plan.append([
            "tmux", "new-session", "-d", "-s", SESSION, "-n", "board",
            str(deez), "super-clanker", "ui", "--no-tmux", *_state_args(state),
        ])
        plan.append([
            "tmux", "new-window", "-t", SESSION, "-n", "main", "-c", str(Path.home()),
            "sh", "-c", "claude --continue || claude",
        ])
    plan.append(["tmux", "attach", "-t", SESSION])
    return plan


def app_argv(python, state):
    return [str(python), "-m", "deezlib.superclanker.ui_app", *_state_args(state)]


def launch(args, env, run=subprocess.run, execve=os.execve, deez=REPO_ROOT / "bin/deez"):
    python = ensure_venv(run=run)
    state = getattr(args, "state", None)
    if not args.no_tmux and "TMUX" not in env:
        has_session = run(["tmux", "has-session", "-t", SESSION], capture_output=True).returncode == 0
        plan = tmux_plan(env, has_session, deez, state)
        for step in plan[:-1]:
            _step(run, step)
        execve("/usr/bin/env", ["tmux", *plan[-1][1:]], dict(env))
        return 0
    child_env = {**env, "PYTHONPATH": str(Path(deez).parents[1])}
    argv = app_argv(python, state)
    execve(argv[0], argv, child_env)
    return 0
