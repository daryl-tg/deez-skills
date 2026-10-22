import re
from pathlib import Path

_BLOCK = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_KEY = re.compile(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$")


class FrontmatterError(Exception):
    """A SKILL.md is missing or has unusable frontmatter."""


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_block(block):
    fields = {}
    lines = block.split("\n")
    index = 0
    while index < len(lines):
        match = _KEY.match(lines[index])
        index += 1
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value in (">", "|", ">-", "|-"):
            collected = []
            while index < len(lines) and (
                lines[index].startswith((" ", "\t")) or not lines[index].strip()
            ):
                collected.append(lines[index].strip())
                index += 1
            value = " ".join(part for part in collected if part)
        fields[key] = _unquote(value).strip()
    return fields


def fields(path):
    """Every top-level key in the frontmatter, with nothing required.

    A command file carries no `name:` (its stem is the name), so callers that
    read commands and agents need the block without parse's requirements.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise FrontmatterError(f"cannot read {path}: {exc}") from exc

    match = _BLOCK.match(text)
    if not match:
        raise FrontmatterError(f"{path}: no YAML frontmatter block")
    return _parse_block(match.group(1))


def parse(path):
    path = Path(path)
    found = fields(path)
    for required in ("name", "description"):
        if not found.get(required):
            raise FrontmatterError(f"{path}: frontmatter is missing {required!r}")
    return {"name": found["name"], "description": found["description"]}
