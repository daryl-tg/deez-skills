"""Check a multi-phase plan against the skeleton its playbook publishes.

Adapted from pstack's `check-plan.mjs`. The rules that survived are the ones
that make a plan auditable by someone who did not write it: every unit carries
the same sub-blocks in the same order, every verification block restates the
rule so a reader who jumped into the middle still sees it, and every
real-surface box names its screenshot and its pass predicate.

The pstack original also enforced ten cloud lanes, a perf block, and a merge
block. Those describe a delivery model this hub does not use, so they are gone.

Plans live in dev-notes, outside every repository, so `bin/doctor` can never
reach one. This runs by path instead, from the playbook's own step.
"""

import re
from dataclasses import dataclass

RULE = (
    "Tests alone are not sufficient. A unit is verified when its unit box "
    "and its real-surface box are both checked."
)

SUB_BLOCKS = (
    "Depends on.",
    "Files.",
    "Build.",
    "You see.",
    "Verify, unit.",
    "Verify, real surface.",
    "Review gate.",
)
NEEDS_A_BOX = ("Files.", "Build.", "You see.", "Verify, unit.", "Verify, real surface.")
CARRIES_THE_RULE = ("Verify, unit.", "Verify, real surface.")
HOW_TO_READ_MARKERS = (
    "One box is one unit of work",
    "names the evidence",
    "Check a box only when",
    RULE,
)
INTRO_LIMIT = 10

BOX = re.compile(r"^\s*- \[[ x]\] (.*)$")
HEAD = re.compile(r"^\*\*([^*]+)\*\*(.*)$")
CODE_SPAN = re.compile(r"`[^`]*`")
LINK_TAIL = re.compile(r"\]\([^)]*\)")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
SKELETON = re.compile(r"^`{3,}markdown\n(.*?)\n`{3,}$", re.DOTALL | re.MULTILINE)


@dataclass(frozen=True)
class Problem:
    line: int
    message: str


@dataclass
class Line:
    n: int
    text: str
    code: bool


@dataclass
class Block:
    name: str
    n: int
    rest: str
    lines: list


def skeleton(playbook_text):
    """Return the fenced markdown skeleton a playbook publishes, or None."""
    match = SKELETON.search(playbook_text)
    return match.group(1) if match else None


def _collapse(text):
    return " ".join(text.split())


def _lines(text):
    raw = text.replace("\r\n", "\n").split("\n")
    start = 0
    if raw and raw[0] == "---" and "---" in raw[1:]:
        start = raw.index("---", 1) + 1
    out, fence = [], False
    for i in range(start, len(raw)):
        if raw[i].startswith("```"):
            fence = not fence
            out.append(Line(i + 1, raw[i], True))
            continue
        out.append(Line(i + 1, raw[i], fence))
    return out


def _prose(text):
    return LINK_TAIL.sub("]", IMAGE.sub("", CODE_SPAN.sub("`", text)))


def _punctuation(lines):
    found = []
    for line in lines:
        if line.code:
            continue
        prose = _prose(line.text)
        if re.search(r"[–—]", prose):
            found.append(Problem(line.n, "long dash"))
        if re.search(r"[‘’“”]", prose):
            found.append(Problem(line.n, "curly quote"))
        if re.search(r": \S", prose):
            found.append(Problem(line.n, "mid-sentence colon"))
    return found


def _sections(lines):
    sections = []
    for line in lines:
        if not line.code and line.text.startswith("## "):
            sections.append({"title": line.text[3:].strip(), "n": line.n, "body": []})
        elif sections:
            sections[-1]["body"].append(line)
    return sections


def _boxes(lines):
    """Boxes with their wrapped continuation lines folded in."""
    out = []
    for line in lines:
        if line.code:
            continue
        match = BOX.match(line.text)
        if match:
            out.append(Problem(line.n, match.group(1)))
        elif out and line.text.startswith(("  ", "\t")) and line.text.strip():
            last = out[-1]
            out[-1] = Problem(last.line, f"{last.message} {line.text.strip()}")
    return out


def _blocks(body):
    blocks = []
    for line in body:
        if line.code:
            continue
        match = HEAD.match(line.text)
        if match and match.group(1) in SUB_BLOCKS:
            blocks.append(Block(match.group(1), line.n, match.group(2).strip(), []))
        elif blocks:
            blocks[-1].lines.append(line)
    return blocks


def _opener(block):
    """The block's prose before its first box, unwrapped."""
    prose = [block.rest]
    for line in block.lines:
        if BOX.match(line.text):
            break
        prose.append(line.text)
    return _collapse(" ".join(prose))


def _check_unit(unit, found):
    title = unit["title"]
    blocks = _blocks(unit["body"])
    names = [b.name for b in blocks]
    if names != list(SUB_BLOCKS):
        found.append(
            Problem(
                unit["n"],
                f"{title}: sub-blocks are [{', '.join(names)}], "
                f"expected [{', '.join(SUB_BLOCKS)}]",
            )
        )
    by_name = {b.name: b for b in blocks}

    depends = by_name.get("Depends on.")
    if depends and not depends.rest:
        found.append(Problem(depends.n, f"{title}: Depends on names nothing"))

    for name in NEEDS_A_BOX:
        block = by_name.get(name)
        if block and not _boxes(block.lines):
            found.append(Problem(block.n, f"{title}: {name} has no box"))

    for name in CARRIES_THE_RULE:
        block = by_name.get(name)
        if block and not _opener(block).startswith(RULE):
            found.append(Problem(block.n, f"{title}: {name} does not open with the rule"))

    surface = by_name.get("Verify, real surface.")
    if surface:
        for box in _boxes(surface.lines):
            if not re.search(r"Saves `[^`]+`", box.message):
                found.append(Problem(box.line, f"{title}: real-surface box names no screenshot"))
            elif "Passes when" not in box.message:
                found.append(Problem(box.line, f"{title}: real-surface box has no pass predicate"))

    gate = by_name.get("Review gate.")
    if gate:
        gate_boxes = _boxes(gate.lines)
        if gate.rest.startswith("None."):
            if gate_boxes:
                found.append(Problem(gate.n, f"{title}: Review gate says None but has boxes"))
        else:
            text = _collapse(gate.rest + " " + " ".join(l.text for l in gate.lines))
            if not gate_boxes:
                found.append(Problem(gate.n, f"{title}: Review gate has no box"))
            for word in ("operator", "evidence"):
                if word not in text:
                    found.append(Problem(gate.n, f'{title}: Review gate lacks "{word}"'))


def _units(sections):
    """The unit sections, which sit between How to read this and Close."""
    titles = [s["title"] for s in sections]
    if "How to read this" not in titles or "Close" not in titles:
        return []
    return sections[titles.index("How to read this") + 1 : titles.index("Close")]


def problems(text):
    """Every rule the plan breaks, in line order."""
    lines = _lines(text)
    found = _punctuation(lines)
    sections = _sections(lines)
    titles = [s["title"] for s in sections]

    heading = next((l for l in lines if not l.code and l.text.startswith("# ")), None)
    if heading is None:
        found.append(Problem(1, "no H1 title"))

    how_to_read = next((s for s in sections if s["title"] == "How to read this"), None)
    if how_to_read is None:
        found.append(Problem(1, 'no "## How to read this" section'))
    else:
        if heading is not None:
            intro = [
                l
                for l in lines
                if heading.n < l.n < how_to_read["n"] and l.text.strip()
            ]
            if len(intro) >= INTRO_LIMIT:
                found.append(
                    Problem(heading.n, f"intro is {len(intro)} lines, under ten required")
                )
        body = _collapse(" ".join(l.text for l in how_to_read["body"]))
        for marker in HOW_TO_READ_MARKERS:
            if marker not in body:
                found.append(
                    Problem(how_to_read["n"], f'How to read this lacks "{marker}"')
                )

    close = next((s for s in sections if s["title"] == "Close"), None)
    if close is None:
        found.append(Problem(1, 'no "## Close" section'))

    units = _units(sections)
    if not units:
        found.append(Problem(1, "no unit sections between How to read this and Close"))
    for unit in units:
        _check_unit(unit, found)

    if close is not None:
        tail = sections[titles.index("Close") + 1 :]
        for section in tail:
            if not section["title"].startswith("Appendix"):
                found.append(
                    Problem(section["n"], f'"## {section["title"]}" after Close is not an appendix')
                )
        if not any("What the prototypes proved" in s["title"] for s in tail):
            found.append(
                Problem(close["n"], 'no "## Appendix ... What the prototypes proved" section')
            )

    return sorted(found, key=lambda p: (p.line, p.message))


def summary(text):
    """One line per unit, with its box counts, for the reply."""
    units = _units(_sections(_lines(text)))
    out = []
    for unit in units:
        blocks = {b.name: b for b in _blocks(unit["body"])}
        counts = " ".join(
            f"{name.rstrip('.').replace(', ', '-').replace(' ', '-').lower()}="
            f"{len(_boxes(blocks[name].lines)) if name in blocks else 0}"
            for name in SUB_BLOCKS
            if name != "Depends on."
        )
        total = len(_boxes(unit["body"]))
        out.append(f"{unit['title']}  boxes={total}  {counts}")
    return out
