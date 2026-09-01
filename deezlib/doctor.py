import re
from dataclasses import dataclass
from pathlib import Path

from deezlib import frontmatter, linkplan, registry

# A local merge onto main. The delivery rule is rebase, PR, squash, so any skill
# that tells an agent to merge locally contradicts it. Matched on the command,
# not the word, so prose like "never merge locally" stays clean.
_LOCAL_MERGE = re.compile(
    r"git\s+merge\b|git\s+pull\b(?!\s+--rebase)|merge\s+--ff-only", re.I
)

# Roles a playbook step may route to, written as **role-name** in skill bodies.
_ROLE_REF = re.compile(r"\*\*([a-z][a-z0-9-]{2,})\*\*\s+role")


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    detail: str


def _fail(code, detail):
    return Finding("fail", code, detail)


def _warn(code, detail):
    return Finding("warn", code, detail)


def _registered_folders(reg):
    folders = set()
    for entry in reg.entries:
        for runtime in entry.runtimes:
            folders.add(registry.source_dir(entry, runtime))
    return folders


def _check_unregistered(reg, repo_root):
    findings = []
    registered = _registered_folders(reg)
    for kind_dir in ("skills", "commands", "agents"):
        base = Path(repo_root) / kind_dir
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if f"{kind_dir}/{child.name}" not in registered:
                findings.append(
                    _fail("unregistered", f"{kind_dir}/{child.name} has no registry entry")
                )
    return findings


def _check_flags(reg, repo_root):
    """A routed layer that stays model-invocable can fire on a description."""
    findings = []
    for entry in reg.entries:
        if not registry.requires_flag(entry.layer):
            continue
        for runtime in entry.runtimes:
            skill_md = Path(repo_root) / registry.source_dir(entry, runtime) / "SKILL.md"
            if not skill_md.is_file():
                continue
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            head = text.split("---")[1] if text.startswith("---") else ""
            if "disable-model-invocation: true" not in head:
                findings.append(
                    _fail(
                        "missing-flag",
                        f"{entry.name}: layer {entry.layer!r} must carry "
                        f"disable-model-invocation: true",
                    )
                )
            break
    return findings


def _check_local_merge(reg, repo_root):
    """No skill may instruct a local merge to main. Rebase, PR, squash."""
    findings = []
    for entry in reg.entries:
        for runtime in entry.runtimes:
            skill_md = Path(repo_root) / registry.source_dir(entry, runtime) / "SKILL.md"
            if not skill_md.is_file():
                continue
            for n, line in enumerate(
                skill_md.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                if _LOCAL_MERGE.search(line):
                    findings.append(
                        _fail(
                            "local-merge",
                            f"{entry.name}:{n} instructs a local merge. "
                            f"Landing is rebase, PR, squash",
                        )
                    )
            break
    return findings


def check_roles(reg, repo_root, known_roles):
    """A step routing to a role no runtime defines fails at dispatch."""
    findings = []
    for entry in reg.entries:
        for runtime in entry.runtimes:
            base = Path(repo_root) / registry.source_dir(entry, runtime)
            for md in sorted(base.rglob("*.md")):
                for role in set(_ROLE_REF.findall(md.read_text(
                    encoding="utf-8", errors="replace"
                ))):
                    if role not in known_roles:
                        findings.append(
                            _fail(
                                "unknown-role",
                                f"{md.relative_to(repo_root)} routes to "
                                f"{role!r}, absent from agent-matrix.tsv",
                            )
                        )
            break
    return findings


def _check_frontmatter(reg, repo_root):
    findings = []
    for entry in reg.entries:
        if entry.kind != "skill":
            continue
        for runtime in entry.runtimes:
            folder = Path(repo_root) / registry.source_dir(entry, runtime)
            skill_md = folder / "SKILL.md"
            if not skill_md.is_file():
                continue
            try:
                fields = frontmatter.parse(skill_md)
            except frontmatter.FrontmatterError as exc:
                findings.append(_fail("name-mismatch", str(exc)))
                continue
            expected = registry.install_name(entry, runtime)
            if fields["name"] != expected:
                findings.append(
                    _fail(
                        "name-mismatch",
                        f"{skill_md}: frontmatter name {fields['name']!r} != "
                        f"install name {expected!r} for {runtime}",
                    )
                )
            size = len(fields["description"])
            if size > frontmatter.DESCRIPTION_FAIL:
                findings.append(
                    _fail(
                        "description-too-long",
                        f"{entry.name}: description is {size} chars "
                        f"(limit {frontmatter.DESCRIPTION_FAIL})",
                    )
                )
            elif size > frontmatter.DESCRIPTION_WARN:
                findings.append(
                    _warn(
                        "description-long",
                        f"{entry.name}: description is {size} chars "
                        f"(soft limit {frontmatter.DESCRIPTION_WARN})",
                    )
                )
    return findings


_VERB_CODES = {
    "missing-source": "missing-source",
    "link": "not-linked",
    "adopt": "not-symlink",
    "backup": "not-symlink",
    "relink": "wrong-target",
}


def check(reg, repo_root, roots, profile):
    findings = []
    findings.extend(_check_unregistered(reg, repo_root))
    findings.extend(_check_frontmatter(reg, repo_root))
    findings.extend(_check_flags(reg, repo_root))
    findings.extend(_check_local_merge(reg, repo_root))
    actions = linkplan.compute(reg, repo_root, roots, profile)

    # Before migration the hub is deliberately unlinked. Nothing linked at all
    # is that state, not drift. Some linked and some not is drift.
    linkable = [a for a in actions if a.verb != "missing-source"]
    if linkable and all(a.verb == "link" for a in linkable):
        findings.append(
            Finding(
                "info",
                "unlinked",
                f"{len(linkable)} entries, none linked. Pre-migration state; "
                f"run bin/link --apply to install",
            )
        )
        actions = [a for a in actions if a.verb == "missing-source"]

    for act in actions:
        code = _VERB_CODES.get(act.verb)
        if code:
            findings.append(_fail(code, f"{act.runtime} {act.name}: {act.reason}"))

    from deezlib import index

    readme = Path(repo_root) / "README.md"
    if readme.is_file() and index.MARKER in readme.read_text(encoding="utf-8"):
        if index.is_stale(reg, repo_root, readme):
            findings.append(
                _fail("readme-stale", "README index is stale — run bin/index")
            )

    seen, unique = set(), []
    for finding in findings:
        key = (finding.code, finding.detail)
        if key not in seen:
            seen.add(key)
            unique.append(finding)
    return unique


def orphans(roots, reg):
    managed = set()
    for entry in reg.entries:
        for runtime in entry.runtimes:
            managed.add((runtime, registry.install_name(entry, runtime)))
    findings = []
    for runtime in sorted(roots):
        root = roots[runtime].get("skill")
        if root is None or not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if child.is_symlink() or not child.is_dir():
                continue
            if child.name.startswith("."):
                continue
            if (runtime, child.name) in managed:
                continue
            findings.append(
                _warn("orphan", f"{runtime}: {child.name} is unadopted (no source repo)")
            )
    return findings
