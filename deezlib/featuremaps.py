"""Publish explicitly selected project feature maps without broad Git changes."""

import subprocess
import tomllib
from pathlib import Path, PurePosixPath


class FeatureMapError(Exception):
    """A feature-map publication cannot proceed safely."""


def _git(repo, *args, check=True):
    command = ["git", "-C", str(repo), *args]
    try:
        return subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
            errors="surrogateescape",
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


def _assert_unpushed_history_is_maps(repo, feature_prefix):
    commits = _git(repo, "rev-list", "--reverse", "origin/main..HEAD").stdout.splitlines()
    allowed_parent = PurePosixPath(feature_prefix)
    for commit in commits:
        changed = _git(
            repo,
            "diff-tree", "--root", "-m", "--no-commit-id", "--name-only",
            "-r", "-z", commit,
        ).stdout.split("\0")
        for raw_path in changed:
            if not raw_path:
                continue
            path = PurePosixPath(raw_path)
            if path.parent != allowed_parent or path.suffix != ".md":
                raise FeatureMapError(
                    "unpushed history contains unrelated path "
                    f"{path.as_posix()!r}; synchronize unrelated commits separately"
                )
    return commits


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
    _git(
        repo,
        "fetch",
        "--quiet",
        "--no-tags",
        "origin",
        "+refs/heads/main:refs/remotes/origin/main",
    )
    _assert_remote_baseline(repo, project, skill)
    ancestor = _git(repo, "merge-base", "--is-ancestor", "origin/main", "HEAD", check=False)
    if ancestor.returncode != 0:
        raise FeatureMapError(
            "origin/main is not an ancestor of local main; synchronize the repository "
            "separately before publishing feature maps"
        )

    prefix = f"projects/{project}/skills/{skill}/features"
    before_commits = _assert_unpushed_history_is_maps(repo, prefix)
    changed = [
        path
        for path in selected
        if _git(repo, "status", "--porcelain=v1", "--untracked-files=all", "--", path).stdout
    ]
    for path in changed:
        tracked = _git(repo, "ls-files", "--error-unmatch", "--", path, check=False)
        if tracked.returncode != 0 and _git(repo, "check-ignore", "-q", "--", path, check=False).returncode == 0:
            raise FeatureMapError(f"feature map is ignored by Git: {path}")

    committed = False
    if changed:
        _git(repo, "add", "--", *changed)
        _git(
            repo,
            "commit",
            "--quiet",
            "--only",
            "-m",
            f"feature maps: update {project}/{skill}",
            "--",
            *changed,
        )
        committed = True

    after_commits = _assert_unpushed_history_is_maps(repo, prefix)
    if not after_commits:
        return "feature maps: already current"

    _git(repo, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    if committed:
        count = len(changed)
        noun = "file" if count == 1 else "files"
        return f"feature maps: committed and pushed {count} {noun}"
    if before_commits:
        return "feature maps: pushed existing commit"
    return "feature maps: already current"
