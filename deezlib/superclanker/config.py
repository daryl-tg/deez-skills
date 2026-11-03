import os
import tomllib
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path

from deezlib.superclanker.store import SuperError


class AcceptMode(StrEnum):
    off = "off"
    observe = "observe"
    auto = "auto"


class SourceMode(StrEnum):
    explicit_only = "explicit-only"
    candidates = "candidates"
    ignore = "ignore"


@dataclass(frozen=True)
class AcceptPolicy:
    mode: AcceptMode = AcceptMode.observe
    policy_version: str = "unset"


@dataclass(frozen=True)
class RouterConfig:
    model: str = "sonnet"
    wake_cap_chars: int = 12000
    inline_chars: int = 200
    im_reply_words: int = 100


@dataclass(frozen=True)
class WorkersConfig:
    model: str | None = None
    max_running: int = 3
    turn_limit_minutes: int = 120
    min_free_pct: int = 30


@dataclass(frozen=True)
class WatchdogConfig:
    model: str = "sonnet"
    interval_seconds: int = 1800
    max_turn_minutes: int = 90
    attention_hours: int = 1
    heartbeat_stale_seconds: int = 120


@dataclass(frozen=True)
class SourcePolicy:
    name: str
    enabled: bool = False
    mode: SourceMode = SourceMode.explicit_only
    senders: tuple = ()
    bots: tuple = ()
    scopes: tuple = ()
    mentions: tuple = ()
    poll_seconds: int = 120


def default_policy(name):
    if name == "terminal":
        operator = os.environ.get("USER", "operator")
        return SourcePolicy(name, True, SourceMode.explicit_only, (operator,))
    return SourcePolicy(name)


@dataclass(frozen=True)
class Config:
    accept: AcceptPolicy
    router: RouterConfig
    sources: dict
    rules: list
    workers: WorkersConfig = WorkersConfig()
    watchdog: WatchdogConfig = WatchdogConfig()

    def policy(self, source):
        return self.sources.get(source) or default_policy(source)


def _text(value):
    if not isinstance(value, str):
        raise ValueError("a string")
    return value


def _flag(value):
    if not isinstance(value, bool):
        raise ValueError("true or false")
    return value


def _count(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("a positive integer")
    return value


def _names(value):
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("a list of strings")
    return tuple(value)


def _choice(kind):
    def parse(value):
        try:
            return kind(value)
        except ValueError:
            raise ValueError("one of " + ", ".join(member.value for member in kind)) from None
    return parse


_ACCEPT = {"mode": _choice(AcceptMode), "policy_version": _text}
_ROUTER = {
    "model": _text, "wake_cap_chars": _count, "inline_chars": _count, "im_reply_words": _count,
}
_WORKERS = {
    "model": _text, "max_running": _count, "turn_limit_minutes": _count, "min_free_pct": _count,
}
_WATCHDOG = {
    "model": _text, "interval_seconds": _count, "max_turn_minutes": _count,
    "attention_hours": _count, "heartbeat_stale_seconds": _count,
}
_SOURCE = {
    "enabled": _flag, "mode": _choice(SourceMode), "senders": _names, "bots": _names,
    "scopes": _names, "mentions": _names, "poll_seconds": _count,
}


def _table(key, value):
    if not isinstance(value, dict):
        raise SuperError(f"sources.toml: {key} must be a table")
    return value


def _section(key, value, schema):
    parsed = {}
    for name, raw in _table(key, value).items():
        if name not in schema:
            raise SuperError(f"sources.toml: unknown key {key}.{name}")
        try:
            parsed[name] = schema[name](raw)
        except ValueError as exc:
            raise SuperError(f"sources.toml: {key}.{name} must be {exc}, not {raw!r}") from None
    return parsed


def _read(path):
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except FileNotFoundError:
        return {}
    except tomllib.TOMLDecodeError as exc:
        raise SuperError(f"{path}: {exc}") from None


def load(root):
    root = Path(root)
    raw = _read(root / "sources.toml")
    unknown = sorted(raw.keys() - {"accept", "router", "workers", "watchdog", "sources"})
    if unknown:
        raise SuperError(f"sources.toml: unknown key {', '.join(unknown)}")
    sources = {"terminal": default_policy("terminal")}
    for name, table in _table("sources", raw.get("sources", {})).items():
        sources[name] = replace(default_policy(name), **_section(f"sources.{name}", table, _SOURCE))
    return Config(
        accept=AcceptPolicy(**_section("accept", raw.get("accept", {}), _ACCEPT)),
        router=RouterConfig(**_section("router", raw.get("router", {}), _ROUTER)),
        sources=sources,
        workers=WorkersConfig(**_section("workers", raw.get("workers", {}), _WORKERS)),
        watchdog=WatchdogConfig(**_section("watchdog", raw.get("watchdog", {}), _WATCHDOG)),
        rules=sorted(
            path.stem for path in (root / "policy" / "rules").glob("*.md") if path.is_file()
        ),
    )
