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
# A line that forbids rather than instructs. Either the negation sits inline
# before the command, or the line is a bullet under a "Never:" style header.
_NEGATION = re.compile(r"\b(never|not|no|don't|do not|avoid|forbidden|without)\b", re.I)
_PROHIBITION_HEADER = re.compile(r"^\s*\**\s*(never|do not|don't|forbidden)\b.*:\s*\**\s*$", re.I)
_BULLET = re.compile(r"^\s*[-*+]\s")


def _prohibits(line, in_prohibition_block):
    """True when this line forbids the command rather than instructing it."""
    match = _LOCAL_MERGE.search(line)
    if match and _NEGATION.search(line[: match.start()]):
        return True
    return bool(in_prohibition_block and _BULLET.match(line))

# Roles a playbook step may route to, written as **role-name** in skill bodies.
_ROLE_REF = re.compile(r"\*\*([a-z][a-z0-9-]{2,})\*\*\s+role")

# A skill cited in bold. Dangling only when neither the registry nor vendor.toml
# knows the name: a vendored skill is legitimately cited and legitimately absent
# from skills/, because its fetcher owns the copy.
_PRINCIPLE_REF = re.compile(r"\*\*(principle-[a-z0-9-]+)\*\*")
_VENDOR_ENTRY = re.compile(r"^\[vendor\.([a-z0-9-]+)\]", re.M)


# Skill-name shaped: lowercase with at least one hyphen. A heuristic, so it
# only ever warns — the corpus also contains hostnames ("dboons-mac-mini"),
# adjectives ("read-only") and repo names in bold, and failing on those would
# make the check noise.
_SKILLISH_REF = re.compile(r"\*\*([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\*\*")


def _vendored(repo_root):
    path = Path(repo_root) / "vendor.toml"
    if not path.is_file():
        return set()
    return set(_VENDOR_ENTRY.findall(path.read_text(encoding="utf-8")))


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


def check_gates(reg, repo_root):
    """A routed layer must be gated on every runtime it installs to.

    Claude reads `disable-model-invocation` in the frontmatter and ignores
    agents/openai.yaml. Codex does the reverse. A skill carrying only one gate
    behaves correctly on one runtime and leaks into description-matching on the
    other, which is invisible until it fires.
    """
    findings = []
    for entry in reg.entries:
        base = Path(repo_root) / registry.source_dir(entry, entry.runtimes[0])
        skill_md = base / "SKILL.md"
        if not skill_md.is_file():
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")
        head = text.split("---")[1] if text.startswith("---") else ""
        claude_gated = "disable-model-invocation: true" in head

        if registry.requires_flag(entry.layer) and not claude_gated:
            findings.append(
                _fail("missing-flag",
                      f"{entry.name}: layer {entry.layer!r} needs "
                      f"disable-model-invocation: true for Claude")
            )
            claude_gated = True  # report the Codex side too, not just this

        # Gating is the author's decision, not the layer's. Whatever the layer,
        # a skill gated on one runtime must be gated on every runtime it
        # installs to, or it behaves differently depending which CLI you opened.
        if not claude_gated or "codex" not in entry.runtimes:
            continue
        yaml = base / "agents" / "openai.yaml"
        gated = (
            yaml.is_file()
            and "allow_implicit_invocation: false"
            in yaml.read_text(encoding="utf-8", errors="replace")
        )
        if not gated:
            findings.append(
                _fail("missing-codex-gate",
                      f"{entry.name}: layer {entry.layer!r} installs to Codex, "
                      f"so agents/openai.yaml needs "
                      f"policy.allow_implicit_invocation: false")
            )
    return findings


def _check_local_merge(reg, repo_root):
    """No skill may instruct a local merge to main. Rebase, PR, squash."""
    findings = []
    for entry in reg.entries:
        for runtime in entry.runtimes:
            skill_md = Path(repo_root) / registry.source_dir(entry, runtime) / "SKILL.md"
            if not skill_md.is_file():
                continue
            in_block = False
            for n, line in enumerate(
                skill_md.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                if _PROHIBITION_HEADER.match(line):
                    in_block = True
                elif line.strip() and not _BULLET.match(line):
                    in_block = False
                if _LOCAL_MERGE.search(line) and not _prohibits(line, in_block):
                    findings.append(
                        _fail(
                            "local-merge",
                            f"{entry.name}:{n} instructs a local merge. "
                            f"Landing is rebase, PR, squash",
                        )
                    )
            break
    return findings


def budget(reg, repo_root):
    """Report what skill metadata costs per runtime.

    There is no per-skill limit. A single long description is not a problem; a
    runtime truncating the whole catalogue is. The aggregate is the number that
    predicts that, so it gets reported rather than gated. Structure is what
    keeps it down: a routed layer costs nothing on a runtime that honours the
    flag, and a well-decomposed skill needs a short description anyway.
    """
    per_runtime = {}
    for entry in reg.entries:
        for runtime in entry.runtimes:
            folder = Path(repo_root) / registry.source_dir(entry, runtime)
            skill_md = folder / "SKILL.md" if folder.is_dir() else folder
            if not skill_md.is_file():
                continue
            try:
                fields = frontmatter.parse(skill_md)
            except frontmatter.FrontmatterError:
                continue
            cost = len(fields["description"]) + len(entry.name)
            # Each runtime reads its own gate: Claude the frontmatter flag,
            # Codex agents/openai.yaml.
            if runtime == "claude":
                routed = ("disable-model-invocation: true"
                          in skill_md.read_text(encoding="utf-8", errors="replace"))
            else:
                y = skill_md.parent / "agents" / "openai.yaml"
                routed = (y.is_file() and "allow_implicit_invocation: false"
                          in y.read_text(encoding="utf-8", errors="replace"))
            slot = per_runtime.setdefault(runtime, {"visible": 0, "routed": 0,
                                                    "n_vis": 0, "n_rt": 0})
            if routed:
                slot["routed"] += cost
                slot["n_rt"] += 1
            else:
                slot["visible"] += cost
                slot["n_vis"] += 1

    findings = []
    for runtime in sorted(per_runtime):
        s = per_runtime[runtime]
        detail = (
            f"{runtime}: {s['n_vis']} visible ~{s['visible'] // 4} tok "
            f"every session"
        )
        if s["n_rt"]:
            detail += f", {s['n_rt']} routed ~{s['routed'] // 4} tok not paid"
        findings.append(Finding("info", "budget", detail))
    return findings


def check_citations(reg, repo_root):
    """Every **principle-x** cited anywhere must be a registered entry."""
    known = {e.name for e in reg.entries} | _vendored(repo_root)
    findings, seen = [], set()
    for entry in reg.entries:
        for runtime in entry.runtimes:
            base = Path(repo_root) / registry.source_dir(entry, runtime)
            for md in sorted(base.rglob("*.md")):
                text = md.read_text(encoding="utf-8", errors="replace")
                for cited in sorted(set(_PRINCIPLE_REF.findall(text))):
                    if cited in known:
                        continue
                    key = (str(md), cited)
                    if key in seen:
                        continue
                    seen.add(key)
                    findings.append(
                        _fail(
                            "dangling-citation",
                            f"{md.relative_to(repo_root)} cites {cited}, "
                            f"which is in neither registry.toml nor vendor.toml",
                        )
                    )
            break
    return findings


def check_skill_references(reg, repo_root, extra_known=()):
    """Warn on a bold skill-shaped name nothing in the hub or vendor.toml knows.

    Heuristic by design. It caught four real citation bugs on first run — a
    principle cited without its prefix, a vendored skill nobody had recorded,
    and two skills cited but never migrated — at the cost of a handful of
    false positives it deliberately does not fail on.
    """
    known = {e.name for e in reg.entries} | _vendored(repo_root) | set(extra_known)
    findings, seen = [], set()
    for entry in reg.entries:
        for runtime in entry.runtimes:
            base = Path(repo_root) / registry.source_dir(entry, runtime)
            if not base.is_dir():
                continue
            for md in sorted(base.rglob("*.md")):
                text = md.read_text(encoding="utf-8", errors="replace")
                for cited in sorted(set(_SKILLISH_REF.findall(text))):
                    if cited in known or cited.startswith("principle-"):
                        continue
                    key = (str(md), cited)
                    if key in seen:
                        continue
                    seen.add(key)
                    findings.append(
                        _warn(
                            "unknown-reference",
                            f"{md.relative_to(repo_root)} mentions **{cited}**, "
                            f"which is not a hub skill, a vendor entry, or a role",
                        )
                    )
            break
    return findings


def check_runtime_neutrality(reg, repo_root):
    """Playbook steps must name a role, not a runtime's dispatch mechanism.

    The same playbooks run on Claude and on Codex, so a step saying
    `Agent(subagent_type: ...)` is unreadable in Codex and `agent_type:` is
    unreadable in Claude. Naming the role keeps one text correct on both.

    Replaces an earlier routing-drift check that compared registry.toml's
    default_lane against the mode skill's prose. That comparison described a
    cross-runtime dispatch that no longer exists.
    """
    mechanisms = ("agent(subagent_type:", "agent_type:", "codex:codex-rescue")
    findings = []
    for entry in reg.entries:
        if entry.layer not in ("mode", "playbook-host"):
            continue
        base = Path(repo_root) / registry.source_dir(entry, entry.runtimes[0])
        pb = base / "playbooks"
        if not pb.is_dir():
            continue
        for md in sorted(pb.glob("*.md")):
            low = md.read_text(encoding="utf-8", errors="replace").lower()
            for mech in mechanisms:
                if mech in low:
                    findings.append(
                        _fail(
                            "runtime-specific-dispatch",
                            f"{md.relative_to(repo_root)} names {mech!r}. "
                            f"Playbooks name a role; the runtime resolves it",
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
    findings.extend(check_gates(reg, repo_root))
    findings.extend(_check_local_merge(reg, repo_root))
    findings.extend(check_citations(reg, repo_root))
    findings.extend(check_runtime_neutrality(reg, repo_root))
    actions = linkplan.compute(reg, repo_root, roots, profile)

    # Before migration the hub is deliberately unlinked. Nothing linked at all
    # is that state, not drift. Some linked and some not is drift.
    # The hub is "unlinked" when nothing resolves into it yet. Destinations may
    # be absent, or may still point at whatever source owned them before
    # migration; either way this repo is not installed. Drift begins once at
    # least one entry does resolve here and others do not.
    linkable = [a for a in actions if a.verb != "missing-source"]
    if linkable and not any(a.verb == "ok" for a in linkable):
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


def orphans(roots, reg, repo_root=None):
    """Real directories nobody owns. A vendor.toml entry counts as owned:
    its fetcher installs it, so it is managed, just not by this repo."""
    managed = set()
    vendored = _vendored(repo_root) if repo_root else set()
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
            if (runtime, child.name) in managed or child.name in vendored:
                continue
            findings.append(
                _warn("orphan", f"{runtime}: {child.name} is unadopted (no source repo)")
            )
    return findings
