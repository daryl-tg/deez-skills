import filecmp
from dataclasses import dataclass
from pathlib import Path

from deezlib import registry


@dataclass(frozen=True)
class Action:
    verb: str
    runtime: str
    kind: str
    name: str
    src: Path
    dest: Path
    reason: str


def _same_tree(left, right):
    comparison = filecmp.dircmp(str(left), str(right))
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(
        str(left), str(right), comparison.common_files, shallow=False
    )
    if mismatch or errors:
        return False
    return all(
        _same_tree(Path(left) / sub, Path(right) / sub)
        for sub in comparison.common_dirs
    )


def _classify(src, dest):
    if not src.is_dir() and not src.is_file():
        return "missing-source", f"no source at {src}"
    if dest.is_symlink():
        if dest.resolve() == src.resolve():
            return "ok", "already linked"
        return "relink", f"symlink points at {dest.resolve()}"
    if not dest.exists():
        return "link", "destination absent"
    if src.is_dir() and dest.is_dir() and _same_tree(src, dest):
        return "adopt", "real directory matches the repo"
    return "backup", "real path differs from the repo"


def compute(reg, repo_root, roots, profile):
    repo_root = Path(repo_root)
    actions = []
    for runtime in sorted(roots):
        for entry in registry.entries_for(reg, profile, runtime):
            root = roots[runtime].get(entry.kind)
            if root is None:
                continue
            src = repo_root / registry.source_dir(entry, runtime)
            dest = root / registry.install_filename(entry, runtime)
            verb, reason = _classify(src, dest)
            actions.append(
                Action(verb, runtime, entry.kind, entry.name, src, dest, reason)
            )
    return actions
