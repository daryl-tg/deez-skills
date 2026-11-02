import json
import os
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path

from deezlib.superclanker import compose
from deezlib.superclanker.domain import Strength
from deezlib.superclanker.gate import admit
from deezlib.superclanker.store import SuperError

WAKE_TIMEOUT_SECONDS = 600
STDERR_TAIL_CHARS = 2000
ALLOWED_TOOLS = "Bash(deez super *)"


@dataclass(frozen=True)
class WakeResult:
    wake_id: str
    batch: int
    decided: int
    denials: int
    cost_usd: float | None
    result: str | None


@dataclass(frozen=True)
class Triage:
    refused: list
    router_items: list


def session_id(root):
    path = Path(root) / "router.session"
    try:
        return path.read_text(encoding="utf-8").strip(), False
    except FileNotFoundError:
        pass
    sid = str(uuid.uuid4())
    handle, temp = tempfile.mkstemp(dir=root, prefix=".router.session.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(sid + "\n")
    os.chmod(temp, 0o600)
    os.replace(temp, path)
    return sid, True


def agent_prompt(hub_root):
    text = (Path(hub_root) / "agents" / "super-router.md").read_text(encoding="utf-8")
    _before, _frontmatter, body = text.split("---\n", 2)
    return body.strip()


def admission(store, config, trigger):
    return admit(
        trigger, config.policy(trigger.source), config.accept.mode,
        bool(compose.thread_tickets(store, trigger.thread_id)),
    )


def triage(store, config):
    admitted, refused = [], []
    for trigger in store.queued():
        verdict = admission(store, config, trigger)
        target = refused if verdict.strength is Strength.not_admitted else admitted
        target.append((trigger, verdict))
    router_batch, _fanout = compose.partition([trigger for trigger, _ in admitted], store)
    batch_ids = {trigger.id for trigger in router_batch}
    return Triage(refused, [item for item in admitted if item[0].id in batch_ids])


def _command(config, hub_root, sid, is_new, prompt):
    return [
        "claude", "-p", "--model", config.router.model, "--tools", "Bash",
        "--allowedTools", ALLOWED_TOOLS, "--permission-mode", "dontAsk",
        "--output-format", "json", "--strict-mcp-config", "--setting-sources", "project,local",
        "--append-system-prompt", agent_prompt(hub_root),
        "--session-id" if is_new else "--resume", sid, prompt,
    ]


def _environment(root, hub_root):
    env = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}
    env["DEEZ_SUPER_STATE"] = str(root)
    env["PATH"] = os.pathsep.join([str(Path(hub_root) / "bin"), env.get("PATH", "")])
    return env


def _outcome(completed):
    if completed.returncode != 0:
        return None
    try:
        outcome = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None
    return outcome if isinstance(outcome, dict) else None


def _denied_commands(outcome):
    return [
        str(denial.get("tool_input", {}).get("command", denial.get("tool_name")))
        for denial in outcome.get("permission_denials") or []
    ]


def wake(store, config, root, hub_root, runner=subprocess.run):
    plan = triage(store, config)
    for trigger, verdict in plan.refused:
        store.ignore(trigger.id, f"not admitted: {verdict.basis}")
    if not plan.router_items:
        return None
    ids = [trigger.id for trigger, _ in plan.router_items]
    prompt = compose.wake_prompt(plan.router_items, config, store)
    sid, is_new = session_id(root)
    wake_id = store.begin_wake(ids)
    try:
        completed = runner(
            _command(config, hub_root, sid, is_new, prompt), cwd=root,
            env=_environment(root, hub_root), capture_output=True, text=True,
            timeout=WAKE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        completed = subprocess.CompletedProcess([], None, "", str(exc))
    outcome = _outcome(completed)
    if outcome is None:
        store.end_wake(
            wake_id, completed.returncode, None, None, completed.stderr[-STDERR_TAIL_CHARS:]
        )
        if is_new:
            (Path(root) / "router.session").unlink(missing_ok=True)
        raise SuperError(f"router wake {wake_id} failed with exit {completed.returncode}")
    cost = outcome.get("total_cost_usd")
    result = outcome.get("result")
    denials = _denied_commands(outcome)
    store.end_wake(
        wake_id, completed.returncode, cost, outcome.get("session_id", sid), result, denials
    )
    left = store.undecided(ids)
    if left:
        store.mark_unavailable(left, f"router made no decision in {wake_id}")
    return WakeResult(wake_id, len(ids), len(ids) - len(left), len(denials), cost, result)
