from pathlib import Path

LAYOUT = {
    "claude": {"skill": "skills", "command": "commands", "agent": "agents"},
    "codex": {"skill": "skills"},
}
HOME_ENV = {"claude": "DEEZ_CLAUDE_HOME", "codex": "DEEZ_CODEX_HOME"}
HOME_DEFAULT = {"claude": ".claude", "codex": ".codex"}


def roots(env, home):
    resolved = {}
    for runtime, kinds in LAYOUT.items():
        override = env.get(HOME_ENV[runtime])
        base = Path(override) if override else Path(home) / HOME_DEFAULT[runtime]
        resolved[runtime] = {kind: base / sub for kind, sub in kinds.items()}
    return resolved
