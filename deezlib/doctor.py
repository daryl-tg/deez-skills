import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from deezlib import frontmatter, index, linkplan, plancheck, registry

# A local merge onto main. The delivery rule is rebase, PR, squash, so any skill
# that tells an agent to merge locally contradicts it. Matched on the command,
# not the word, so prose like "never merge locally" stays clean.
#
# What separates a landing from a sync is the ref being merged, not the flag:
#
#   git merge-base / -tree / -file / -head   read-only plumbing. `\b` after
#       "merge" matches before a hyphen, so these need an explicit exclusion.
#   a merge naming origin/* or upstream/*    a branch catching up to its own
#       remote, or a vendored fork syncing from the project it forked. Neither
#       lands work, and rebasing a published fork rewrites history.
#
# A merge naming no such ref is a landing, whatever flags it carries — which is
# why `git merge --ff-only` onto main is still a failure.
_MERGE_PLUMBING = r"(?!-base|-tree|-file|-head)"
_SYNC_REF = r"(?!.*\b(?:origin|upstream)/)"
_LOCAL_MERGE = re.compile(
    rf"git\s+merge{_MERGE_PLUMBING}\b{_SYNC_REF}"
    rf"|git\s+pull\b(?!\s+--rebase|\s+--ff-only)"
    rf"|(?<!git )\bmerge\s+--ff-only{_SYNC_REF}",
    re.I,
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
# The five roles a playbook step may route to. Both runtimes define all five as
# agent definitions; the hub does not version them yet.
ROLES = ("explore", "executor", "test-engineer", "code-reviewer", "verifier")
# A step that says `playbooks/x.md` dead-ends unless x.md sits next to it.
_PLAYBOOK_REF = re.compile(r"playbooks/([a-z0-9][a-z0-9-]*\.md)")

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
    repo_root = Path(repo_root)
    registered = _registered_folders(reg)
    registered_targets = {(repo_root / folder).resolve() for folder in registered}
    bases = [repo_root / kind for kind in ("skills", "commands", "agents")]
    bases.extend(sorted((repo_root / "projects").glob("*/skills")))
    for base in bases:
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            relative = child.relative_to(repo_root).as_posix()
            if relative not in registered and child.resolve() not in registered_targets:
                findings.append(
                    _fail("unregistered", f"{relative} has no registry entry")
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
    findings = _claude_only_tools(reg, repo_root)
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


# Claude Code tools Codex does not have. A skill installed on Codex that tells
# the agent to call one sends it looking for a tool that is not there. A table
# row is exempt, because a row mapping the tool to its Codex equivalent is how a
# skill stays correct on both runtimes.
_CLAUDE_ONLY_TOOL = re.compile(r"\b(AskUserQuestion|TodoWrite)\b|\b(Agent)\(")


def _claude_only_tools(reg, repo_root):
    """Warn when a Codex-installed skill names a Claude-only tool in prose.

    A warning, not a failure: the name is sometimes fine in context, and the
    fix is a rewording an author should choose, not a mechanical edit.
    """
    findings = []
    for entry in reg.entries:
        if entry.kind != "skill" or "codex" not in entry.runtimes:
            continue
        base = Path(repo_root) / registry.source_dir(entry, "codex")
        if not base.is_dir():
            continue
        for md in sorted(base.rglob("*.md")):
            text = md.read_text(encoding="utf-8", errors="replace")
            for n, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith("|"):
                    continue
                for match in _CLAUDE_ONLY_TOOL.finditer(line):
                    tool = match.group(1) or f"{match.group(2)}("
                    findings.append(
                        _warn(
                            "runtime-specific-tool",
                            f"{md.relative_to(repo_root)}:{n} names {tool}, "
                            f"which Codex does not have. Name the action, or "
                            f"map the tool per runtime in a table row",
                        )
                    )
    return findings


def check_gate_tracking(reg, repo_root):
    """A gate file that was written but never added breaks the next clone.

    The gates are marked generated in .gitattributes so they stay out of review
    diffs, which is the same property that lets an untracked one sit unnoticed
    in `git status` behind a wall of other noise. Git is the authority here, so
    ask it. Outside a work tree there is nothing to ask, and the check is silent.
    """
    import subprocess

    root = Path(repo_root)
    try:
        listed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", "*/agents/openai.yaml"],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    tracked = {line.strip() for line in listed.stdout.splitlines() if line.strip()}
    findings = []
    for entry in reg.entries:
        base = root / registry.source_dir(entry, entry.runtimes[0])
        gate = base / "agents" / "openai.yaml"
        if not gate.is_file():
            continue
        relative = gate.relative_to(root).as_posix()
        if relative not in tracked:
            findings.append(
                _fail(
                    "untracked-gate",
                    f"{relative} exists but git does not track it. "
                    f"A clone would fail the Codex gate check",
                )
            )
    return findings


def check_playbook_links(reg, repo_root):
    """A step citing `playbooks/x.md` must land on a file that exists.

    Nothing checked this before, so a playbook could route to a sibling that
    was renamed, never written, or deliberately not adopted. The reader only
    finds out mid-task, which is the worst moment to discover it.
    """
    findings, seen = [], set()
    for entry in reg.entries:
        if entry.layer not in ("mode", "playbook-host"):
            continue
        base = Path(repo_root) / registry.source_dir(entry, entry.runtimes[0])
        pb = base / "playbooks"
        if not pb.is_dir():
            continue
        for md in sorted(base.rglob("*.md")):
            text = md.read_text(encoding="utf-8", errors="replace")
            for name in sorted(set(_PLAYBOOK_REF.findall(text))):
                if (pb / name).is_file():
                    continue
                key = (str(md), name)
                if key in seen:
                    continue
                seen.add(key)
                findings.append(
                    _fail(
                        "dangling-playbook",
                        f"{md.relative_to(repo_root)} routes to "
                        f"playbooks/{name}, which does not exist",
                    )
                )
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
                                f"{role!r}, which no runtime defines",
                            )
                        )
            break
    return findings


# What both runtimes accept as a name, and the longest they accept.
_NAME_SHAPE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_NAME_LIMIT = 64


def _check_file_frontmatter(entry, repo_root):
    """An agent or command is one file, so its name is the file stem.

    An agent must say so in `name:`, which Claude reads as the agent type. A
    command may leave `name:` out, since the stem names it, but one that sets
    it must not disagree.
    """
    path = Path(repo_root) / registry.source_dir(entry, entry.runtimes[0])
    if not path.is_file():
        return []
    relative = path.relative_to(repo_root)
    try:
        name = frontmatter.fields(path).get("name")
    except frontmatter.FrontmatterError as exc:
        return [_fail("name-mismatch", str(exc))] if entry.kind == "agent" else []

    findings = []
    if name is None and entry.kind == "command":
        name = path.stem
    elif name is None:
        findings.append(
            _fail("name-mismatch",
                  f"{relative}: missing name:. An agent needs one equal to "
                  f"its file stem {path.stem!r}")
        )
    elif name != path.stem:
        findings.append(
            _fail("name-mismatch",
                  f"{relative}: frontmatter name {name!r} != file stem {path.stem!r}")
        )
    if name and (not _NAME_SHAPE.match(name) or len(name) > _NAME_LIMIT):
        findings.append(
            _fail("invalid-name",
                  f"{relative}: name {name!r} must be lowercase words joined by "
                  f"hyphens, at most {_NAME_LIMIT} characters")
        )
    return findings


def _check_frontmatter(reg, repo_root):
    findings = []
    for entry in reg.entries:
        if entry.kind in registry.FILE_KINDS:
            findings.extend(_check_file_frontmatter(entry, repo_root))
            continue
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


# --- Docs against the tree --------------------------------------------------
# The README and the guide describe the tree in prose: how many principles,
# which playbooks, where a link goes. Nothing generated that prose, so nothing
# kept it true. These checks read it back against the tree.

_COUNTS_OK = "<!-- deez:counts-ok -->"
_COUNT_NOUNS = ("skills", "principles", "playbooks", "agents")
_COUNT_CLAIM = re.compile(
    r"(?<![\w.-])(\d+|[a-z]+(?:-[a-z]+)?) (" + "|".join(_COUNT_NOUNS) + r")\b", re.I
)
_SMALL = ("zero one two three four five six seven eight nine ten eleven twelve "
          "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = ("", "", "twenty", "thirty", "forty", "fifty",
         "sixty", "seventy", "eighty", "ninety")

_LINK = re.compile(r"\]\(<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\)")
_CODE_SPAN = re.compile(r"`[^`]*`")
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
_HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.*?)\s*$")

_PRINCIPLE_TABLE = re.compile(r"^\|\s*principle\s*\|", re.I)
_PRINCIPLE_ROW = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|")


def _number(word):
    """A whole number written as digits or as words up to ninety-nine."""
    word = word.lower()
    if word.isdigit():
        return int(word)
    if word in _SMALL:
        return _SMALL.index(word)
    tens, _, unit = word.partition("-")
    if tens in _TENS[2:] and (not unit or unit in _SMALL[1:10]):
        return _TENS.index(tens) * 10 + (_SMALL.index(unit) if unit else 0)
    return None


def _prose_lines(text):
    """Yield (line number, line) for every line outside a fenced code block."""
    fence = None
    for n, row in enumerate(text.split("\n"), 1):
        if fence is None:
            fence = plancheck.opening_fence(row)
            if fence is None:
                yield n, row
        elif plancheck.closes_fence(row, fence):
            fence = None


def _readme_head(repo_root):
    """The hand-written README, above the generated index. None when absent."""
    readme = Path(repo_root) / "README.md"
    if not readme.is_file():
        return None
    return readme.read_text(encoding="utf-8").partition(index.MARKER)[0]


def _markdown_under(repo_root, *folders):
    root = Path(repo_root)
    found = []
    for folder in folders:
        if (root / folder).is_dir():
            found.extend(sorted((root / folder).rglob("*.md")))
    return found


def _playbook_dirs(reg, repo_root):
    """The router's playbooks/ folders, with the source path each sits under."""
    for entry in reg.entries:
        if entry.layer != "mode":
            continue
        source = registry.source_dir(entry, entry.runtimes[0])
        folder = Path(repo_root) / source / "playbooks"
        if folder.is_dir():
            yield source, folder


def _tree_counts(reg, repo_root):
    skills = [e.name for e in reg.entries if e.kind == "skill"]
    return {
        "skills": len(skills),
        "principles": sum(name.startswith("principle-") for name in skills),
        "playbooks": sum(len(list(folder.glob("*.md")))
                         for _, folder in _playbook_dirs(reg, repo_root)),
        "agents": sum(e.kind == "agent" for e in reg.entries),
    }


def check_count_claims(reg, repo_root):
    """A number written before skills, principles, playbooks or agents is a
    claim about the tree, so it must match the tree.

    Read from README.md above the generated index and from docs/**. Fenced code
    is skipped. Skills counts every registered skill, principles the
    registered principle-* skills, playbooks the router's playbooks/*.md, and
    agents the registered agents.

    Some numbers are not claims about the whole set: a subset ("three skills
    fire on their own") or history ("adopted 59 skills"). Mark those with
    `<!-- deez:counts-ok -->` at the end of the line, or alone on the line
    directly above. The marker is invisible when rendered and exempts that one
    line, so a stale count elsewhere in the paragraph still fails.

    Table cells rarely match: `| Skills | 45 |` puts no number directly before
    the noun. A row that does write `45 skills` needs the marker too.
    """
    counts = _tree_counts(reg, repo_root)
    head = _readme_head(repo_root)
    docs = [("README.md", head)] if head is not None else []
    for path in _markdown_under(repo_root, "docs"):
        docs.append((path.relative_to(repo_root).as_posix(),
                     path.read_text(encoding="utf-8", errors="replace")))

    findings = []
    for relative, text in docs:
        lines = text.split("\n")
        for n, line in _prose_lines(text):
            if _COUNTS_OK in line or (n > 1 and lines[n - 2].strip() == _COUNTS_OK):
                continue
            for match in _COUNT_CLAIM.finditer(line):
                claimed, noun = _number(match.group(1)), match.group(2).lower()
                if claimed is None or claimed == counts[noun]:
                    continue
                findings.append(
                    _fail("count-claim",
                          f'{relative}:{n} says "{match.group(0)}", but the '
                          f"tree has {counts[noun]}")
                )
    return findings


def check_readme_lists(reg, repo_root):
    """Every playbook and every principle has a row in the README.

    Playbooks are matched by their link, `(./skills/<router>/playbooks/x.md)`.
    Principles are matched by a `| `name` |` row, without the prefix, inside a
    table whose header starts `| principle |`. A row naming a principle that is
    not registered fails too: that is a retired rule still advertised. The
    generated index does not count, since it lists everything by construction.
    """
    head = _readme_head(repo_root)
    if head is None:
        return []
    findings = []
    for source, folder in _playbook_dirs(reg, repo_root):
        for md in sorted(folder.glob("*.md")):
            if f"(./{source}/playbooks/{md.name})" not in head:
                findings.append(
                    _fail("unlisted-playbook",
                          f"README.md does not list playbook {md.stem}. Add a "
                          f"row linking ./{source}/playbooks/{md.name}")
                )

    listed, in_table = set(), False
    for _, line in _prose_lines(head):
        row = line.strip()
        if _PRINCIPLE_TABLE.match(row):
            in_table = True
        elif not row.startswith("|"):
            in_table = False
        elif in_table and (match := _PRINCIPLE_ROW.match(row)):
            listed.add(match.group(1))

    registered = {e.name.removeprefix("principle-") for e in reg.entries
                  if e.kind == "skill" and e.name.startswith("principle-")}
    for name in sorted(registered - listed):
        findings.append(
            _fail("unlisted-principle",
                  f"README.md does not list principle-{name} in a principle table")
        )
    for name in sorted(listed - registered):
        findings.append(
            _fail("unknown-principle",
                  f"README.md lists principle {name!r}, which is not registered")
        )
    return findings


def _slug(heading):
    """GitHub's anchor for a heading: lowercase, punctuation dropped, spaces
    to hyphens. Link text and code ticks count as plain text."""
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    plain = re.sub(r"\s+#+$", "", plain)
    plain = re.sub(r"[`*]", "", plain).strip().lower()
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", plain))


def _anchors(path):
    found, seen = set(), {}
    text = path.read_text(encoding="utf-8", errors="replace")
    for _, line in _prose_lines(text):
        match = _HEADING.match(line)
        if not match:
            continue
        slug = _slug(match.group(1))
        repeat = seen.get(slug, 0)
        seen[slug] = repeat + 1
        found.add(f"{slug}-{repeat}" if repeat else slug)
    return found


def check_doc_links(reg, repo_root):
    """Every relative link in README.md, docs/** and agents/** resolves.

    The target must exist. A `#anchor`, on its own or after a .md path, must
    match a GitHub-style heading slug in the target. Links in fenced code or in
    code spans are examples, not links, and are skipped, as are links with a
    scheme (http, https, mailto).
    """
    root = Path(repo_root)
    docs = [root / "README.md"] if (root / "README.md").is_file() else []
    docs += _markdown_under(root, "docs", "agents")
    anchors, findings = {}, []
    for doc in docs:
        relative = doc.relative_to(root).as_posix()
        text = doc.read_text(encoding="utf-8", errors="replace")
        for n, line in _prose_lines(text):
            for match in _LINK.finditer(_CODE_SPAN.sub("", line)):
                href = match.group(1)
                if _SCHEME.match(href):
                    continue
                target, _, anchor = href.partition("#")
                if not target:
                    path = doc
                elif target.startswith("/"):
                    path = root / unquote(target).lstrip("/")
                else:
                    path = doc.parent / unquote(target)
                if not path.exists():
                    findings.append(
                        _fail("broken-link",
                              f"{relative}:{n} links to {href}, which does not exist")
                    )
                    continue
                if not anchor or path.suffix != ".md":
                    continue
                key = path.resolve()
                if key not in anchors:
                    anchors[key] = _anchors(path)
                if anchor not in anchors[key]:
                    findings.append(
                        _fail("broken-anchor",
                              f"{relative}:{n} links to {href}, but no heading "
                              f"in {path.name} has that anchor")
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
    findings.extend(check_playbook_links(reg, repo_root))
    findings.extend(check_gate_tracking(reg, repo_root))
    findings.extend(check_roles(reg, repo_root, ROLES))
    findings.extend(check_count_claims(reg, repo_root))
    findings.extend(check_readme_lists(reg, repo_root))
    findings.extend(check_doc_links(reg, repo_root))
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
