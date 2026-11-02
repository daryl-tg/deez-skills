from dataclasses import dataclass
from enum import StrEnum

from deezlib.superclanker.config import AcceptMode, SourceMode
from deezlib.superclanker.domain import Strength


class Basis(StrEnum):
    source = "source"
    addressed = "addressed"
    followup = "followup"
    admission = "admission"
    bot = "bot"
    off = "off"


@dataclass(frozen=True)
class Admission:
    strength: Strength
    basis: Basis
    reason: str


def _fast_path(trigger, policy, thread_has_tickets):
    actor = trigger.actor
    candidates = policy.mode == SourceMode.candidates
    if not policy.enabled:
        return Admission(Strength.not_admitted, Basis.source, f"{policy.name} is disabled")
    if policy.mode == SourceMode.ignore:
        return Admission(Strength.not_admitted, Basis.source, f"{policy.name} is ignored")
    if actor in policy.bots:
        if trigger.addressed:
            return Admission(Strength.inferred, Basis.bot, f"bot {actor} addressed the agent")
        if candidates:
            return Admission(Strength.inferred, Basis.bot, f"bot {actor} on a candidates source")
        return Admission(Strength.not_admitted, Basis.bot, f"bot {actor} did not address the agent")
    listed = actor in policy.senders
    who = f"listed sender {actor}" if listed else f"unlisted actor {actor}"
    if listed and trigger.addressed:
        return Admission(Strength.explicit, Basis.addressed, f"{who} addressed the agent")
    if thread_has_tickets:
        strength = Strength.explicit if listed else Strength.inferred
        return Admission(strength, Basis.followup, f"{who} followed up on a ticketed thread")
    if candidates:
        return Admission(Strength.inferred, Basis.admission, f"{who} on a candidates source")
    return Admission(
        Strength.not_admitted, Basis.source, f"{who} not admitted by {policy.name} {policy.mode}"
    )


def admit(trigger, policy, accept_mode, thread_has_tickets):
    admission = _fast_path(trigger, policy, thread_has_tickets)
    if admission.strength is Strength.inferred and accept_mode == AcceptMode.off:
        return Admission(Strength.not_admitted, Basis.off, f"accept mode off: {admission.reason}")
    return admission
