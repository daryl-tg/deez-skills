"""Publish explicitly selected project feature maps without broad Git changes."""

import os
import subprocess
import tempfile
import tomllib
from pathlib import Path, PurePosixPath

PUSH_ATTEMPTS = 3


class FeatureMapError(Exception):
    """A feature-map publication cannot proceed safely."""


def _git(repo, *args, check=True, env=None):
    command = ["git", "-C", str(repo), *args]
    try:
        return subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
            errors="surrogateescape",
            env=env,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = ""
        if isinstance(exc, subprocess.CalledProcessError):
            detail = (exc.stderr or exc.stdout or "").strip()
        suffix = f": {detail}" if detail else ""
        raise FeatureMapError(f"git {' '.join(args)} failed{suffix}") from exc


def _registered_project(reg, project, skill):
    matches = [entry for entry in reg.entries if entry.kind == "skill" and entry.name == skill]
    if not matches:
        raise FeatureMapError(f"skill {skill!r} is not registered")
    if not any(entry.project == project for entry in matches):
        owner = matches[0].project or "the shared skills root"
        raise FeatureMapError(
            f"skill {skill!r} belongs to project {owner!r}, not {project!r}"
        )


def _selected_paths(repo, project, skill, files):
    names = list(files)
    if not names:
        raise FeatureMapError("at least one feature-map filename is required")

    feature_dir = repo / "projects" / project / "skills" / skill / "features"
    try:
        resolved_dir = feature_dir.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FeatureMapError(f"feature-map directory does not exist: {feature_dir}") from exc
    if not resolved_dir.is_dir() or not resolved_dir.is_relative_to(repo):
        raise FeatureMapError("feature-map directory resolves outside the deez-skills repository")

    selected = []
    seen = set()
    for value in names:
        name = str(value)
        candidate_name = Path(name)
        if (
            candidate_name.is_absolute()
            or len(candidate_name.parts) != 1
            or candidate_name.name != name
            or candidate_name.suffix != ".md"
        ):
            raise FeatureMapError(
                f"feature map {name!r} must be a direct-child .md filename"
            )
        path = feature_dir / name
        if path.is_symlink():
            raise FeatureMapError(f"feature map {name!r} must not be a symlink")
        relative = path.relative_to(repo).as_posix()
        try:
            resolved = path.resolve(strict=True)
        except FileNotFoundError as exc:
            tracked_type = _git(
                repo, "cat-file", "-t", f"HEAD:{relative}", check=False
            )
            if tracked_type.returncode != 0 or tracked_type.stdout.strip() != "blob":
                raise FeatureMapError(f"feature map does not exist: {name}") from exc
        else:
            if resolved.parent != resolved_dir or not resolved.is_file():
                raise FeatureMapError(f"feature map {name!r} is outside its feature directory")
        if relative not in seen:
            selected.append(relative)
            seen.add(relative)
    return selected


def _assert_repo(repo):
    result = _git(repo, "rev-parse", "--show-toplevel")
    top = Path(result.stdout.strip()).resolve()
    if top != repo:
        raise FeatureMapError(f"repository root must be {top}, got {repo}")


def _fetch_origin_main(repo):
    _git(
        repo,
        "fetch",
        "--quiet",
        "--no-tags",
        "origin",
        "+refs/heads/main:refs/remotes/origin/main",
    )
    return _git(repo, "rev-parse", "refs/remotes/origin/main").stdout.strip()


def _leftover_map_paths(repo, feature_prefix):
    allowed_parent = PurePosixPath(feature_prefix)
    commits = _git(repo, "rev-list", "origin/main..HEAD").stdout.split()
    found = []
    for commit in commits:
        changed = _git(
            repo, "diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "-r", "-z", commit,
        ).stdout.split("\0")
        for raw_path in changed:
            path = PurePosixPath(raw_path) if raw_path else None
            if path and path.parent == allowed_parent and path.suffix == ".md":
                found.append(path.as_posix())
    return found


def _assert_publishable(repo, base, paths):
    for path in paths:
        on_origin = _git(repo, "cat-file", "-e", f"{base}:{path}", check=False).returncode == 0
        if not on_origin and _git(repo, "check-ignore", "-q", "--", path, check=False).returncode == 0:
            raise FeatureMapError(f"feature map is ignored by Git: {path}")


def _write_blob(repo, blob, destination):
    content = _git(repo, "cat-file", "blob", blob).stdout if blob else ""
    destination.write_text(content, encoding="utf-8", errors="surrogateescape")
    return destination


def _merge_origin_edit(repo, fork, base, path, scratch):
    ancestor = _blob(repo, fork, path)
    theirs = _blob(repo, base, path)
    worktree = repo / path
    if theirs == ancestor or not worktree.is_file():
        return None
    ours = _git(repo, "hash-object", "--", path).stdout.strip()
    if ours == theirs:
        return None
    merged = _git(
        repo, "merge-file", "-p", "-L", "this checkout", "-L", "common", "-L", "origin/main",
        str(worktree),
        str(_write_blob(repo, ancestor, Path(scratch) / "ancestor")),
        str(_write_blob(repo, theirs, Path(scratch) / "theirs")),
        check=False,
    )
    if merged.returncode != 0:
        raise FeatureMapError(
            f"origin/main changed {path} since this checkout and the edits overlap; "
            "pull, resolve, and publish again"
        )
    return worktree, merged.stdout


def _commit_on(repo, base, paths, message):
    fork = _git(repo, "merge-base", "HEAD", base).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="feature-maps-") as scratch:
        merges = [_merge_origin_edit(repo, fork, base, path, scratch) for path in paths]
        for worktree, text in filter(None, merges):
            worktree.write_text(text, encoding="utf-8", errors="surrogateescape")
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(scratch) / "index")}
        _git(repo, "read-tree", base, env=env)
        for path in paths:
            if (repo / path).is_file():
                blob = _git(repo, "hash-object", "-w", "--", path).stdout.strip()
                _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
            else:
                _git(repo, "update-index", "--force-remove", "--", path, env=env)
        tree = _git(repo, "write-tree", env=env).stdout.strip()
    if tree == _git(repo, "rev-parse", f"{base}^{{tree}}").stdout.strip():
        return None, []
    changed = _git(repo, "diff-tree", "--name-only", "-r", "-z", base, tree).stdout.split("\0")
    commit = _git(repo, "commit-tree", tree, "-p", base, "-m", message).stdout.strip()
    return commit, [path for path in changed if path]


def _blob(repo, commit, path):
    found = _git(repo, "rev-parse", "--verify", "--quiet", f"{commit}:{path}", check=False)
    return found.stdout.strip() if found.returncode == 0 else None


def _contained(repo, head, commit):
    for local in _git(repo, "rev-list", f"{commit}..{head}").stdout.split():
        changed = _git(
            repo, "diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "-r", "-z", local,
        ).stdout.split("\0")
        if any(path and _blob(repo, head, path) != _blob(repo, commit, path) for path in changed):
            return False
    return True


def _reconcile(repo, commit, published):
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    if not _contained(repo, head, commit):
        return "; local main has unpublished commits, left as is"
    try:
        _git(repo, "add", "-A", "--", *published)
        _git(repo, "read-tree", "-m", "-u", head, commit)
        _git(repo, "update-ref", "-m", "feature maps: follow origin/main", "HEAD", commit, head)
    except FeatureMapError as exc:
        return f"; local main left behind origin/main ({exc})"
    return ""


def _assert_remote_baseline(repo, project, skill):
    registry_file = _git(
        repo, "show", "origin/main:registry.toml", check=False
    )
    if registry_file.returncode != 0:
        raise FeatureMapError(
            "origin/main has no readable registry.toml; ordinary verification-skill "
            "delivery must land first"
        )
    try:
        remote_registry = tomllib.loads(registry_file.stdout)
    except tomllib.TOMLDecodeError as exc:
        raise FeatureMapError(
            "origin/main registry.toml is invalid; ordinary verification-skill "
            "delivery must land first"
        ) from exc
    body = (remote_registry.get("skills") or {}).get(skill)
    if not isinstance(body, dict) or body.get("project") != project:
        raise FeatureMapError(
            f"origin/main does not register {skill!r} for project {project!r}; "
            "ordinary verification-skill delivery must land first"
        )

    skill_path = f"projects/{project}/skills/{skill}/SKILL.md"
    remote_type = _git(
        repo, "cat-file", "-t", f"origin/main:{skill_path}", check=False
    )
    if remote_type.returncode != 0 or remote_type.stdout.strip() != "blob":
        raise FeatureMapError(
            f"origin/main has no canonical {skill_path}; ordinary verification-skill "
            "delivery must land first"
        )


def publish(repo_root, reg, project, skill, files):
    """Commit and push only named maps for one registered project skill."""
    repo = Path(repo_root).resolve()
    _registered_project(reg, project, skill)
    _assert_repo(repo)
    selected = _selected_paths(repo, project, skill, files)

    if (repo / ".sync-hold").exists():
        return "feature maps: .sync-hold present; skipped"

    branch = _git(repo, "branch", "--show-current").stdout.strip()
    if branch not in ("", "main"):
        raise FeatureMapError(
            "feature maps can only publish from main or a detached worktree; "
            f"current branch is {branch!r}"
        )
    _git(repo, "remote", "get-url", "origin")
    prefix = f"projects/{project}/skills/{skill}/features"
    message = f"feature maps: update {project}/{skill}"

    for _attempt in range(PUSH_ATTEMPTS):
        base = _fetch_origin_main(repo)
        _assert_remote_baseline(repo, project, skill)
        paths = list(dict.fromkeys([*selected, *_leftover_map_paths(repo, prefix)]))
        _assert_publishable(repo, base, paths)
        commit, published = _commit_on(repo, base, paths, message)
        if commit is None:
            return "feature maps: already current"
        pushed = _git(repo, "push", "--quiet", "origin", f"{commit}:refs/heads/main", check=False)
        if pushed.returncode == 0:
            break
        if _fetch_origin_main(repo) == base:
            raise FeatureMapError(
                f"git push of feature maps failed: {(pushed.stderr or pushed.stdout).strip()}"
            )
    else:
        raise FeatureMapError(
            f"origin/main moved during each of {PUSH_ATTEMPTS} publication attempts; retry"
        )

    note = _reconcile(repo, commit, published)
    count = len(published)
    noun = "file" if count == 1 else "files"
    return f"feature maps: committed and pushed {count} {noun}{note}"
