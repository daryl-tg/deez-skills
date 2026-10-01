import tomllib
from dataclasses import dataclass, field
from pathlib import Path

RUNTIMES = ("claude", "codex")
KIND_TABLES = {"skills": "skill", "commands": "command", "agents": "agent"}
KIND_DIRS = {"skill": "skills", "command": "commands", "agent": "agents"}
RUNTIME_KINDS = {"claude": ("skill", "command", "agent"), "codex": ("skill",)}
ALL = "*"

# A layer says what a skill is for, which determines how it may be invoked.
#   mode          the router. Sticky, routed to explicitly, never matched.
#   principle     one rule. Cited by playbooks, must exist on both runtimes so
#                 a handoff citation resolves on either side.
#   playbook-host a skill owning a playbooks/ directory.
#   workflow      everything else. May stay model-invocable.
LAYERS = ("mode", "principle", "playbook-host", "workflow")
DEFAULT_LAYER = "workflow"

# Layers that must ship `disable-model-invocation: true`. These are reached by
# explicit routing; description-matching them is the failure this prevents.
FLAGGED_LAYERS = ("mode", "principle", "playbook-host")

# Nothing is Claude-only any more. Codex gates invocation through
# agents/openai.yaml (`policy.allow_implicit_invocation: false`), verified
# 2026-09-02 with two probe skills differing only in that field: Codex listed
# the open one and not the gated one. The earlier restriction assumed Codex had
# no gate at all, which was a wrong conclusion drawn from looking in
# config.toml rather than at the skill.
CLAUDE_ONLY_LAYERS = ()

# Layers that must be installed everywhere, or a cited rule goes missing.
BOTH_RUNTIME_LAYERS = ("principle",)

# Where each kind of work runs. The reserved four are non-dispatchable per the
# operator's CLAUDE.md, whatever default_lane says.
ROUTING_DEFAULTS = {
    "default_lane": "codex",
    "planning": "claude",
    "review": "claude",
    "verification": "claude",
    "git_mutations": "claude",
}
RESERVED_LANES = ("planning", "review", "verification", "git_mutations")


def requires_flag(layer):
    """True when a layer must carry disable-model-invocation."""
    return layer in FLAGGED_LAYERS


class RegistryError(Exception):
    """registry.toml is malformed or internally inconsistent."""


@dataclass(frozen=True)
class Entry:
    kind: str
    name: str
    category: str
    layer: str = DEFAULT_LAYER
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
    routing: dict = field(default_factory=dict)


def install_name(entry, runtime):
    return entry.install_as.get(runtime, entry.name)


# Skills are directories. Commands and agents are single markdown files, so
# their paths carry the extension both in the repo and at the install site.
FILE_KINDS = ("command", "agent")


def _suffix(kind):
    return ".md" if kind in FILE_KINDS else ""


def source_dir(entry, runtime):
    default = f"{KIND_DIRS[entry.kind]}/{entry.name}{_suffix(entry.kind)}"
    return entry.variant.get(runtime, default)


def install_filename(entry, runtime):
    """The basename to create at the install root."""
    return f"{install_name(entry, runtime)}{_suffix(entry.kind)}"


def _parse_entries(data, categories):
    entries = []
    for table, kind in KIND_TABLES.items():
        for name, body in (data.get(table) or {}).items():
            category = body.get("category")
            if category not in categories:
                raise RegistryError(f"{table}.{name}: unknown category {category!r}")
            layer = body.get("layer", DEFAULT_LAYER)
            if layer not in LAYERS:
                raise RegistryError(
                    f"{table}.{name}: unknown layer {layer!r}; "
                    f"known: {', '.join(LAYERS)}"
                )
            runtimes = tuple(body.get("runtimes") or ())
            if not runtimes:
                raise RegistryError(f"{table}.{name}: runtimes must not be empty")
            if layer in CLAUDE_ONLY_LAYERS and tuple(runtimes) != ("claude",):
                raise RegistryError(
                    f"{table}.{name}: layer {layer!r} must be claude only. "
                    f"Codex ignores disable-model-invocation, so a router there "
                    f"fires on description matches"
                )
            if layer in BOTH_RUNTIME_LAYERS and set(runtimes) != set(RUNTIMES):
                raise RegistryError(
                    f"{table}.{name}: layer {layer!r} must be installed on both "
                    f"runtimes, or a handoff citing it fails to resolve on Codex"
                )
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
                    layer=layer,
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

    routing = dict(ROUTING_DEFAULTS)
    for key, value in (data.get("routing") or {}).items():
        if key not in ROUTING_DEFAULTS:
            raise RegistryError(f"routing: unknown key {key!r}")
        if value not in RUNTIMES:
            raise RegistryError(f"routing.{key}: unknown lane {value!r}")
        if key in RESERVED_LANES and value != "claude":
            raise RegistryError(
                f"routing.{key} must stay 'claude'. Design, review, "
                f"verification, and git mutations are not dispatchable"
            )
        routing[key] = value

    entries = _parse_entries(data, categories)
    _check_collisions(entries)
    return Registry(
        version, default_profile, categories, profiles, entries, routing
    )


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
