import os
import shutil
import signal
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from itertools import takewhile
from pathlib import Path

from deezlib.superclanker import channels, compose, config, router, sources, workers
from deezlib.superclanker.domain import Strength, utc_now
from deezlib.superclanker.store import Store, SuperError

TERMINAL_PREFIX = "terminal:"
BACKOFF = "backoff"
BACKOFF_FIRST_SECONDS = 30
BACKOFF_CEILING_SECONDS = 600


@dataclass(frozen=True)
class PassResult:
    fanned_out: int
    launched: int
    resumed: int
    reaped: int
    wake_id: str | None
    replies_sent: int
    errors: tuple
    polled: int = 0

    @property
    def eventful(self):
        counts = (
            self.polled, self.fanned_out, self.launched, self.resumed, self.reaped,
            self.replies_sent,
        )
        return any(counts) or self.wake_id not in (None, BACKOFF) or bool(self.errors)

    def line(self, at):
        polled = f" polled={self.polled}" if self.polled else ""
        return (
            f"{at}  fanout={self.fanned_out} reaped={self.reaped} resumed={self.resumed} "
            f"launched={self.launched} wake={self.wake_id or '-'} replies={self.replies_sent} "
            f"errors={len(self.errors)}{polled}"
        )


def heartbeat_path(root):
    return Path(root) / "daemon.heartbeat"


def inbox_path(root, thread_id):
    return Path(root) / "inbox" / f"{thread_id.replace(':', '-')}.log"


def _append_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        existing = ""
    handle, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(existing + text)
    os.replace(temp, path)


def _fan_out(store, settings):
    fanned = 0
    for trigger in store.queued():
        if router.admission(store, settings, trigger).strength is Strength.not_admitted:
            continue
        router_batch, fanout = compose.partition([trigger], store)
        if router_batch:
            continue
        for ticket_id in fanout:
            store.record_fanout(trigger.id, [ticket_id])
            store.add_input(ticket_id, "trigger", trigger.id)
            fanned += 1
    return fanned


def _seconds_since(stamp, now):
    return (datetime.fromisoformat(now()) - datetime.fromisoformat(stamp)).total_seconds()


def _wake_is_stuck(wake, now):
    return _seconds_since(wake.started_at, now) >= router.WAKE_TIMEOUT_SECONDS


def _backing_off(store, now):
    wakes = store.recent_wakes()
    failures = len(list(takewhile(lambda wake: wake.exit_code != 0, wakes)))
    if not failures:
        return False
    delay = min(BACKOFF_CEILING_SECONDS, BACKOFF_FIRST_SECONDS * 2 ** (failures - 1))
    return _seconds_since(wakes[0].ended_at, now) < delay


def _poll_due_sources(store, settings, now):
    return sum(
        len(sources.POLLERS[name](store, policy, now=now))
        for name, policy in settings.sources.items()
        if policy.enabled and name in sources.POLLERS and sources.due(store, policy, now)
    )


def _send_forge_replies(store, settings):
    waiting = {reply.id for reply in store.unsent_replies()}
    lines = channels.deliver(store, settings)
    still_waiting = {reply.id for reply in store.unsent_replies()}
    return len(waiting - still_waiting), lines


def _send_terminal_replies(store, root):
    sent = 0
    for reply in store.unsent_replies():
        if not reply.thread_id.startswith(TERMINAL_PREFIX):
            continue
        _append_atomic(inbox_path(root, reply.thread_id), f"{reply.created_at}  {reply.text}\n")
        store.mark_sent(reply.id)
        sent += 1
    return sent


def one_pass(store, config, root, hub_root, wake=router.wake, launch=workers.launch,
             resume=workers.resume, revive=workers.revive, reap=workers.reap, now=utc_now):
    errors = []

    def attempt(step, *args):
        try:
            return step(*args)
        except SuperError as exc:
            errors.append(str(exc))
            return None

    polled = _poll_due_sources(store, config, now)
    fanned_out = attempt(_fan_out, store, config) or 0
    reaped = len(attempt(reap, store, root) or [])
    resumed = 0
    for assignment in store.running_assignments():
        if workers.alive(assignment.pid) or not store.undelivered_inputs(assignment.ticket_id):
            continue
        if attempt(resume, store, config, assignment.id, hub_root, root) is not None:
            resumed += 1
    for ticket_id in store.revivable():
        if len(store.running_assignments()) >= config.workers.max_running:
            break
        if attempt(revive, store, config, ticket_id, hub_root, root) is not None:
            resumed += 1
    launched = 0
    running = len(store.running_assignments())
    for assignment in store.pending_assignments():
        if running >= config.workers.max_running:
            break
        if attempt(launch, store, config, assignment.id, hub_root, root) is not None:
            launched += 1
            running += 1
    wake_id = None
    plan = router.triage(store, config)
    for trigger, verdict in plan.refused:
        attempt(store.ignore, trigger.id, f"not admitted: {verdict.basis}")
    if plan.router_items:
        inflight = store.inflight_wake()
        if inflight is not None and _wake_is_stuck(inflight, now):
            store.expire_wake(inflight.id)
            inflight = None
        if inflight is None and _backing_off(store, now):
            wake_id = BACKOFF
        elif inflight is None:
            woken = attempt(wake, store, config, root, hub_root)
            wake_id = woken and woken.wake_id
    replies_sent = _send_terminal_replies(store, root)
    forge_sent, undelivered = _send_forge_replies(store, config)
    errors.extend(undelivered)
    workers._write_atomic(heartbeat_path(root), now() + "\n")
    return PassResult(
        fanned_out, launched, resumed, reaped, wake_id, replies_sent + forge_sent, tuple(errors),
        polled,
    )


def log_pass(root, result):
    line = result.line(utc_now())
    if result.eventful:
        log = Path(root) / "log" / "daemon.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
    return line


def _lock_owner(lock):
    try:
        return int((lock / "pid").read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError):
        return None


def _take_lock(lock):
    try:
        lock.mkdir()
    except FileExistsError:
        owner = _lock_owner(lock)
        if workers.alive(owner):
            return owner
        shutil.rmtree(lock, ignore_errors=True)
        try:
            lock.mkdir()
        except FileExistsError:
            return _lock_owner(lock) or 0
    handle, temp = tempfile.mkstemp(dir=lock, prefix=".pid.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    os.replace(temp, lock / "pid")
    return None


def run(root, hub_root, interval_seconds=5, passes=None, sleep=time.sleep,
        load_config=config.load):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = root / "daemon.lock.d"
    owner = _take_lock(lock)
    if owner is not None:
        print(f"daemon already running as {owner}")
        return 0
    stopping = []
    previous = {
        signum: signal.signal(signum, lambda *_frame: stopping.append(True))
        for signum in (signal.SIGTERM, signal.SIGINT)
    }
    try:
        store = Store.open(root)
        try:
            done = 0
            while True:
                try:
                    result = one_pass(store, load_config(root), root, hub_root)
                except SuperError as exc:
                    result = PassResult(0, 0, 0, 0, None, 0, (str(exc),))
                for error in result.errors:
                    print(f"daemon: {error}", file=sys.stderr)
                log_pass(root, result)
                done += 1
                if stopping or (passes is not None and done >= passes):
                    break
                sleep(interval_seconds)
                if stopping:
                    break
        finally:
            store.close()
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
        shutil.rmtree(lock, ignore_errors=True)
    return 0
