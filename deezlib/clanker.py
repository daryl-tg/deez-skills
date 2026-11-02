"""Persistent, session-scoped Clanker hook state and hook installation."""

import fcntl
import hashlib
import json
import os
import shlex
import tempfile
from contextlib import contextmanager
from pathlib import Path


class ClankerError(Exception):
    """Clanker state or hook configuration is unsafe or invalid."""


_VERSION = 1
_STATE_KEYS = {
    "version",
    "runtime",
    "session_id",
    "active",
    "tool_count",
    "playbook",
    "checkpoint",
}
_EVENTS = ("UserPromptSubmit", "SessionStart", "PreToolUse")
_OPT_OUT = {"off", "stop", "disable", "exit", "opt-out", "optout"}
_MAX_SESSION_ID = 256
_MAX_PATH = 4096
_MAX_CORE_REMINDER = 2500
_MAX_ADDITIONAL_CONTEXT = 4800


def state_root(env, home):
    """Return the private Clanker state root."""
    override = env.get("DEEZ_CLANKER_STATE")
    if override:
        return Path(override)
    return Path(home) / ".local" / "state" / "deez-skills" / "clanker"


def _within(path, parent):
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _event_name(payload):
    return payload.get("hook_event_name") or payload.get("hookEventName")


def _session_id(payload):
    value = payload.get("session_id") or payload.get("sessionId")
    if not isinstance(value, str):
        return ""
    value = value.strip()
    if (
        not value
        or len(value) > _MAX_SESSION_ID
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        return ""
    return value


def _paths(state_home, runtime, session_id):
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    directory = Path(state_home) / runtime
    return directory / f"{digest}.json", directory / f"{digest}.lock"


def _ensure_private_directory(path):
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(str(path), 0o700)


@contextmanager
def _locked(lock_path, create):
    if create:
        _ensure_private_directory(lock_path.parent.parent)
        _ensure_private_directory(lock_path.parent)
    try:
        descriptor = os.open(str(lock_path), os.O_RDWR | (os.O_CREAT if create else 0), 0o600)
    except FileNotFoundError:
        yield False
        return
    try:
        os.fchmod(descriptor, 0o600)
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield True
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _validate_state(value, runtime, session_id):
    def safe_path(raw):
        return (
            raw is None
            or (
                isinstance(raw, str)
                and 0 < len(raw) <= _MAX_PATH
                and Path(raw).is_absolute()
                and not any(ord(character) < 32 or ord(character) == 127 for character in raw)
            )
        )

    valid = (
        isinstance(value, dict)
        and set(value) == _STATE_KEYS
        and value.get("version") == _VERSION
        and value.get("runtime") == runtime
        and value.get("session_id") == session_id
        and value.get("active") is True
        and isinstance(value.get("tool_count"), int)
        and not isinstance(value.get("tool_count"), bool)
        and value.get("tool_count") >= 0
        and safe_path(value.get("playbook"))
        and safe_path(value.get("checkpoint"))
    )
    if not valid:
        raise ClankerError("Clanker session state has an invalid schema")
    return value


def _read_state(path, runtime, session_id):
    try:
        raw = path.read_text(encoding="utf-8")
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ClankerError(f"cannot read Clanker session state: {path}") from exc
    return _validate_state(value, runtime, session_id)


def _write_atomic(path, value, mode=0o600):
    _ensure_private_directory(path.parent)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        os.chmod(str(path), mode)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _new_state(runtime, session_id):
    return {
        "version": _VERSION,
        "runtime": runtime,
        "session_id": session_id,
        "active": True,
        "tool_count": 0,
        "playbook": None,
        "checkpoint": None,
    }


def _activation(prompt):
    if not isinstance(prompt, str):
        return False
    text = prompt.lstrip()
    lowered = text.lower()
    for token in ("$clanker-mode", "/clanker-mode"):
        if lowered == token or (
            lowered.startswith(token) and lowered[len(token):len(token) + 1].isspace()
        ):
            arguments = lowered[len(token):].strip().split()
            return not arguments or arguments[0] not in _OPT_OUT
    words = lowered.split()
    if words[:1] == ["please"]:
        words = words[1:]
    if words[:1] in (["use"], ["enable"], ["enter"]):
        words = words[1:]
    elif words[:2] == ["turn", "on"]:
        words = words[2:]
    else:
        return False
    return bool(words) and words[0] in ("clanker-mode", "clanker", "clanker mode") and (
        words[0] == "clanker-mode" or words[:2] == ["clanker", "mode"]
    )


def _deactivation(prompt):
    if not isinstance(prompt, str):
        return False
    lowered = prompt.lstrip().lower()
    for token in ("$clanker-mode", "/clanker-mode"):
        if lowered.startswith(token) and lowered[len(token):len(token) + 1].isspace():
            arguments = lowered[len(token):].strip().split()
            return bool(arguments) and arguments[0] in _OPT_OUT
    words = lowered.split()
    if words[:1] == ["please"]:
        words = words[1:]
    if words[:2] == ["normal", "mode"]:
        return True
    prefixes = (("stop",), ("disable",), ("exit",), ("turn", "off"))
    for prefix in prefixes:
        if tuple(words[:len(prefix)]) == prefix:
            rest = words[len(prefix):]
            return rest[:1] == ["clanker-mode"] or rest[:2] == ["clanker", "mode"]
    return False


def _expansion_action(payload):
    command = payload.get("command_name") or payload.get("commandName")
    if command != "clanker-mode":
        return None
    arguments = (
        payload.get("command_args")
        if "command_args" in payload
        else payload.get("args", "")
    )
    if isinstance(arguments, list):
        words = [str(item).lower() for item in arguments]
    elif isinstance(arguments, str):
        words = arguments.lower().split()
    else:
        words = []
    return "disable" if words and words[0] in _OPT_OUT else "activate"


def _reminder(repo, runtime, session_id, state, event, full):
    source = repo / "skills" / "clanker-mode" / "references" / "session-reminder.md"
    try:
        core = source.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise ClankerError(f"cannot read Clanker reminder: {source}") from exc
    if len(core) > _MAX_CORE_REMINDER:
        raise ClankerError("Clanker core session reminder exceeds 2500 characters")
    skill = (repo / "skills" / "clanker-mode" / "SKILL.md").resolve()
    deez = (repo / "bin" / "deez").resolve()
    checkpoint_parts = [
        str(deez),
        "clanker-checkpoint",
        "--runtime",
        runtime,
        "--session",
        session_id,
        "--playbook",
        state["playbook"] or "<absolute-playbook.md>",
        "--resume-note",
        state["checkpoint"] or "<absolute-external-resume-note.md>",
    ]
    lines = [
        f"Clanker session: runtime={runtime}; session={session_id}.",
        f"Checkpoint command: {shlex.join(checkpoint_parts)}.",
    ]
    if state["playbook"]:
        lines.append(f"Selected playbook: {state['playbook']}.")
    if state["checkpoint"]:
        lines.append(f"Resume checkpoint: {state['checkpoint']}.")
    if full:
        lines.append(f"Reread the full Clanker skill at {skill}.")
        if state["playbook"]:
            lines.append(f"Reread the selected playbook at {state['playbook']}.")
        if state["checkpoint"]:
            lines.append(f"Reread the checkpoint pointer at {state['checkpoint']}.")
        lines.append("Continue the existing checklist from its current state; do not restart it.")
    lines.append(core)
    context = "\n".join(lines)
    if len(context) > _MAX_ADDITIONAL_CONTEXT:
        raise ClankerError("Clanker additional context exceeds 4800 characters")
    return {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": context,
        }
    }


def handle_event(repo: Path, runtime: str, payload: dict, state_home: Path):
    """Handle one hook event, returning optional hook-specific context."""
    if runtime not in ("claude", "codex") or not isinstance(payload, dict):
        return None
    event = _event_name(payload)
    session_id = _session_id(payload)
    if event not in (*_EVENTS, "UserPromptExpansion") or not session_id:
        return None
    repo = Path(repo).resolve()
    state_path, lock_path = _paths(state_home, runtime, session_id)

    action = None
    if event == "UserPromptSubmit":
        prompt = payload.get("prompt")
        if _deactivation(prompt):
            action = "disable"
        elif _activation(prompt):
            action = "activate"
    elif event == "UserPromptExpansion" and runtime == "claude":
        action = _expansion_action(payload)
    elif event == "SessionStart" and payload.get("source") == "clear":
        action = "disable"

    exists = state_path.exists()
    if not exists and action != "activate":
        return None
    with _locked(lock_path, create=exists or action == "activate") as locked:
        if not locked:
            return None
        exists = state_path.exists()
        if action == "disable":
            if exists:
                state_path.unlink()
            return None
        if exists:
            state = _read_state(state_path, runtime, session_id)
        elif action == "activate":
            state = _new_state(runtime, session_id)
        else:
            return None

        full = action == "activate"
        emit = False
        if event in ("UserPromptSubmit", "UserPromptExpansion"):
            emit = True
        elif event == "SessionStart":
            source = payload.get("source")
            emit = source in ("compact", "resume", "startup")
            if source in ("compact", "resume"):
                state["tool_count"] = 0
                full = True
        elif event == "PreToolUse":
            state["tool_count"] += 1
            emit = state["tool_count"] % 20 == 0
            full = emit

        _write_atomic(state_path, state)
        return _reminder(repo, runtime, session_id, state, event, full) if emit else None


def _resolve_playbook(repo, playbook):
    root = (repo / "skills" / "clanker-mode" / "playbooks").resolve(strict=True)
    supplied = Path(playbook)
    candidate = supplied if supplied.is_absolute() else root / supplied
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ClankerError(f"Clanker playbook does not exist: {candidate}") from exc
    if resolved.suffix != ".md" or resolved.parent != root or not resolved.is_file():
        raise ClankerError("Clanker playbook must be a direct .md file in the playbooks directory")
    if len(str(resolved)) > _MAX_PATH or any(
        ord(character) < 32 or ord(character) == 127 for character in str(resolved)
    ):
        raise ClankerError("Clanker playbook path is unsafe or too long")
    return resolved


def checkpoint(repo: Path, runtime: str, session_id: str, playbook: str,
               resume_note: Path, state_home: Path) -> str:
    """Update the playbook and external resume-note pointers for an active session."""
    repo = Path(repo).resolve()
    if runtime not in ("claude", "codex"):
        raise ClankerError(f"unsupported runtime: {runtime!r}")
    normalized_session = _session_id({"session_id": session_id})
    if not normalized_session:
        raise ClankerError("checkpoint requires a non-blank session ID")
    selected = _resolve_playbook(repo, playbook)
    note = Path(resume_note)
    if not note.is_absolute():
        raise ClankerError("resume note must be an absolute path")
    try:
        note = note.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ClankerError(f"resume note does not exist: {note}") from exc
    if not note.is_file() or not os.access(str(note), os.R_OK):
        raise ClankerError("resume note must be a readable file")
    if len(str(note)) > _MAX_PATH or any(
        ord(character) < 32 or ord(character) == 127 for character in str(note)
    ):
        raise ClankerError("resume note path is unsafe or too long")
    if _within(note, repo):
        raise ClankerError("resume note must be outside the deez-skills repository")

    state_path, lock_path = _paths(state_home, runtime, normalized_session)
    if not state_path.exists():
        raise ClankerError("checkpoint requires a registered active Clanker session")
    with _locked(lock_path, create=False) as locked:
        if not locked or not state_path.exists():
            raise ClankerError("checkpoint requires a registered active Clanker session")
        state = _read_state(state_path, runtime, normalized_session)
        state["playbook"] = str(selected)
        state["checkpoint"] = str(note)
        _write_atomic(state_path, state)
    return f"clanker checkpoint updated: {runtime}/{normalized_session} -> {selected.name}"


def _load_config(path):
    if not path.exists():
        return {}, None
    try:
        raw = path.read_bytes()
        document = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ClankerError(f"malformed hook configuration: {path}") from exc
    if not isinstance(document, dict):
        raise ClankerError(f"hook configuration must contain a JSON object: {path}")
    return document, raw


def _is_own_handler(handler, command_parts):
    if not isinstance(handler, dict) or handler.get("type") != "command":
        return False
    command = handler.get("command")
    if not isinstance(command, str):
        return False
    try:
        return shlex.split(command) == command_parts
    except ValueError:
        return False


def _install_event(document, event, command_parts, runtime, matcher=None):
    hooks = document.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ClankerError("hook configuration field 'hooks' must be an object")
    entries = hooks.setdefault(event, [])
    if not isinstance(entries, list):
        raise ClankerError(f"hook event {event!r} must contain a list")
    handler = {
        "type": "command",
        "command": shlex.join(command_parts),
        "timeout": 10,
    }
    if runtime == "codex":
        handler["additionalContextLimit"] = 1200
    found = False
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        handlers = entry.get("hooks")
        if not isinstance(handlers, list):
            continue
        for index, existing in enumerate(handlers):
            if _is_own_handler(existing, command_parts):
                handlers[index] = dict(handler)
                if len(handlers) == 1:
                    if matcher is None:
                        entry.pop("matcher", None)
                    else:
                        entry["matcher"] = matcher
                found = True
    if not found:
        entry = {"hooks": [handler]}
        if matcher is not None:
            entry["matcher"] = matcher
        entries.append(entry)


def _updated_config(document, repo, runtime):
    updated = json.loads(json.dumps(document))
    command_parts = [str((repo / "bin" / "deez").resolve()), "clanker-hook", "--runtime", runtime]
    for event in _EVENTS:
        _install_event(updated, event, command_parts, runtime)
    if runtime == "claude":
        _install_event(
            updated, "UserPromptExpansion", command_parts, runtime, matcher="^clanker-mode$"
        )
    return updated


def _config_bytes(document):
    return (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _write_bytes_atomic(path, content, mode):
    if path.parent.exists():
        if not path.parent.is_dir():
            raise ClankerError(f"hook configuration parent is not a directory: {path.parent}")
    else:
        path.parent.mkdir(parents=True, mode=0o700)
        os.chmod(str(path.parent), 0o700)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        os.chmod(str(path), mode)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def install(repo: Path, roots: dict, apply: bool) -> list[str]:
    """Plan or install Clanker's session hooks without disturbing other handlers."""
    repo = Path(repo).resolve()
    targets = {}
    filenames = {"claude": "settings.json", "codex": "hooks.json"}
    for runtime in ("claude", "codex"):
        if runtime not in roots:
            continue
        runtime_roots = roots[runtime]
        if not isinstance(runtime_roots, dict) or "skill" not in runtime_roots:
            raise ClankerError(f"runtime roots for {runtime!r} have no skill directory")
        targets[runtime] = Path(runtime_roots["skill"]).parent / filenames[runtime]
    prepared = []
    for runtime, path in targets.items():
        document, original = _load_config(path)
        updated = _updated_config(document, repo, runtime)
        content = _config_bytes(updated)
        current = original == content
        prepared.append((runtime, path, original, content, current))

    if not apply:
        return [
            f"plan clanker hooks: {runtime} {path} ({'current' if current else 'update'})"
            for runtime, path, _original, _content, current in prepared
        ]

    results = []
    for runtime, path, original, content, current in prepared:
        if current:
            results.append(f"clanker hooks current: {runtime} {path}")
            continue
        mode = stat_mode = 0o600
        if path.exists():
            stat_mode = path.stat().st_mode & 0o777
            mode = stat_mode
            backup = path.with_suffix(path.suffix + ".bak")
            _write_bytes_atomic(backup, original, stat_mode)
        _write_bytes_atomic(path, content, mode)
        results.append(f"clanker hooks updated: {runtime} {path}")
    return results
