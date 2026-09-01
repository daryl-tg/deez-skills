import shutil
from pathlib import Path


class ApplyError(Exception):
    """A plan cannot be applied safely."""


def backup_root(stamp, state_home):
    return Path(state_home) / stamp


def _stash(action, stamp, state_home):
    target = backup_root(stamp, state_home) / action.runtime / action.kind / action.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(action.dest), str(target))
    return target


def _link(action):
    action.dest.parent.mkdir(parents=True, exist_ok=True)
    action.dest.symlink_to(action.src)


def execute(actions, state_home, stamp):
    broken = [a for a in actions if a.verb == "missing-source"]
    if broken:
        names = ", ".join(sorted(a.name for a in broken))
        raise ApplyError(f"refusing to apply: no source for {names}")

    unknown = sorted({a.verb for a in actions} - {
        "ok", "link", "relink", "adopt", "backup"
    })
    if unknown:
        raise ApplyError(f"unknown verb(s): {', '.join(unknown)}")

    results = []
    for act in actions:
        if act.verb == "ok":
            results.append(f"ok      {act.runtime:6} {act.name}")
        elif act.verb == "link":
            _link(act)
            results.append(f"linked  {act.runtime:6} {act.name}")
        elif act.verb == "relink":
            act.dest.unlink()
            _link(act)
            results.append(f"relink  {act.runtime:6} {act.name}")
        elif act.verb == "adopt":
            shutil.rmtree(act.dest)
            _link(act)
            results.append(f"adopted {act.runtime:6} {act.name}")
        elif act.verb == "backup":
            saved = _stash(act, stamp, state_home)
            _link(act)
            results.append(f"backup  {act.runtime:6} {act.name} -> {saved}")
    return results
