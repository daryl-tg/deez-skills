import os
import uuid

from deezlib.superclanker.domain import Trigger, trigger_id, utc_now


def ask(store, text, thread_name="default", actor=None):
    event_id = str(uuid.uuid4())
    trigger = Trigger(
        id=trigger_id("terminal", event_id),
        source="terminal",
        source_event_id=event_id,
        thread_id=f"terminal:{thread_name}",
        actor=actor or os.environ.get("USER", "operator"),
        addressed=True,
        text=text,
        parent_id=None,
        received_at=utc_now(),
        meta={},
    )
    return trigger, store.receive(trigger)
