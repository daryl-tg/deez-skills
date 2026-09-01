import tomllib
from dataclasses import dataclass, field
from pathlib import Path

RUNTIMES = ("claude", "codex")
KIND_TABLES = {"skills": "skill", "commands": "command", "agents": "agent"}
KIND_DIRS = {"skill": "skills", "command": "commands", "agent": "agents"}
RUNTIME_KINDS = {"claude": ("skill", "command", "agent"), "codex": ("skill",)}
ALL = "*"


class RegistryError(Exception):
    """registry.toml is malformed or internally inconsistent."""


@dataclass(frozen=True)
class Entry:
    kind: str
    name: str
    category: str
    runtimes: tuple = ()
    install_as: dict = field(default_factory=dict)
    variant: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Registry:
    version: int
    default_profile: str
    categories: dict
    profiles: dict
    entries: tuple


def install_name(entry, runtime):
    return entry.install_as.get(runtime, entry.name)


def source_dir(entry, runtime):
    return entry.variant.get(runtime, f"{KIND_DIRS[entry.kind]}/{entry.name}")


def _parse_entries(data, categories):
    entries = []
    for table, kind in KIND_TABLES.items():
        for name, body in (data.get(table) or {}).items():
            category = body.get("category")
            if category not in categories:
                raise RegistryError(f"{table}.{name}: unknown category {category!r}")
            runtimes = tuple(body.get("runtimes") or ())
            if not runtimes:
                raise RegistryError(f"{table}.{name}: runtimes must not be empty")
            for runtime in runtimes:
                if runtime not in RUNTIMES:
                    raise RegistryError(f"{table}.{name}: unknown runtime {runtime!r}")
                if kind not in RUNTIME_KINDS[runtime]:
                    raise RegistryError(
                        f"{table}.{name}: runtime {runtime!r} does not support {kind}s"
                    )
            entries.append(
                Entry(
                    kind=kind,
                    name=name,
                    category=category,
                    runtimes=runtimes,
                    install_as=dict(body.get("install_as") or {}),
                    variant=dict(body.get("variant") or {}),
                )
            )
    return tuple(entries)


def _check_collisions(entries):
    seen = {}
    for entry in entries:
        for runtime in entry.runtimes:
            key = (runtime, entry.kind, install_name(entry, runtime))
            if key in seen:
                raise RegistryError(
                    f"{entry.name} and {seen[key]} both install as "
                    f"{key[2]!r} for {runtime}"
                )
            seen[key] = entry.name


def load(path):
    path = Path(path)
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except FileNotFoundError as exc:
        raise RegistryError(f"no registry at {path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise RegistryError(f"{path}: {exc}") from exc

    meta = data.get("meta") or {}
    version = meta.get("version")
    if version != 1:
        raise RegistryError(f"unsupported registry version {version!r}")

    categories = dict(data.get("categories") or {})
    profiles = {}
    for name, members in (data.get("profiles") or {}).items():
        members = tuple(members)
        for member in members:
            if member != ALL and member not in categories:
                raise RegistryError(f"profile {name!r}: unknown category {member!r}")
        profiles[name] = members

    default_profile = meta.get("default_profile", "full")
    if default_profile not in profiles:
        raise RegistryError(f"default_profile {default_profile!r} is not defined")

    entries = _parse_entries(data, categories)
    _check_collisions(entries)
    return Registry(version, default_profile, categories, profiles, entries)


def entries_for(registry, profile, runtime):
    if profile not in registry.profiles:
        raise RegistryError(f"unknown profile {profile!r}")
    if runtime not in RUNTIMES:
        raise RegistryError(f"unknown runtime {runtime!r}")
    members = registry.profiles[profile]
    everything = ALL in members
    return [
        entry
        for entry in registry.entries
        if runtime in entry.runtimes and (everything or entry.category in members)
    ]
