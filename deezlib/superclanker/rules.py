import re
from dataclasses import dataclass
from pathlib import Path

from deezlib.superclanker.config import AcceptMode
from deezlib.superclanker.store import SuperError
from deezlib.superclanker.workers import _write_atomic

MODE_LINE = re.compile(r"^mode:\s*(\S*)\s*$")
TITLE_PREFIX = "# "


@dataclass(frozen=True)
class Rule:
    name: str
    title: str
    mode: AcceptMode
    text: str


def rules_dir(root):
    return Path(root) / "policy" / "rules"


def _mode(name, value):
    try:
        return AcceptMode(value)
    except ValueError:
        choices = ", ".join(member.value for member in AcceptMode)
        raise SuperError(f"rule {name} mode {value} is not one of {choices}") from None


def _mode_line(lines):
    return next(
        (index for index, line in enumerate(lines) if index and MODE_LINE.match(line.strip())),
        None,
    )


def _parse(name, content):
    lines = content.splitlines()
    head = lines[0] if lines else ""
    title = head.removeprefix(TITLE_PREFIX).strip() if head.startswith(TITLE_PREFIX) else name
    at = _mode_line(lines)
    mode = AcceptMode.observe if at is None else _mode(name, MODE_LINE.match(lines[at].strip())[1])
    body = [line for index, line in enumerate(lines) if index and index != at]
    return Rule(name, title, mode, "\n".join(body).strip())


def load(root):
    return {
        path.stem: _parse(path.stem, path.read_text(encoding="utf-8"))
        for path in sorted(rules_dir(root).glob("*.md")) if path.is_file()
    }


def require(root, names):
    known = load(root)
    for name in names:
        if name not in known:
            raise SuperError(f"no rule {name}")
    return [known[name] for name in names]


def set_mode(root, name, mode):
    path = rules_dir(root) / f"{name}.md"
    if not path.is_file():
        raise SuperError(f"no rule {name}")
    mode = _mode(name, mode)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    at = _mode_line(lines)
    if at is None:
        lines.insert(1, f"mode: {mode}\n")
    else:
        lines[at] = f"mode: {mode}\n"
    _write_atomic(path, "".join(lines))
    return _parse(name, "".join(lines))
