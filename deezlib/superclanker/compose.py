from deezlib.superclanker.store import SuperError

SHRUNK_TEXT_CHARS = 50
REPORT_CHARS = 60
VERBS = (
    "deez super dispatch <trigger> --slug <kebab> --playbook <clanker playbook file>"
    " [--scope <text>]",
    "deez super attach <trigger> <ticket>",
    "deez super ignore <trigger> --reason <text>",
    "deez super stop <ticket> --reason <text>",
    "deez super reply <thread> --text <text>",
    "deez super note <ticket> --text <text>",
)


def is_stop(trigger):
    said = trigger.text.lower().strip()
    return said == "stop" or said.startswith("stop ")


def partition(triggers, store):
    router_batch, fanout = [], {}
    for trigger in triggers:
        targets = store.fanout_targets(trigger.thread_id)
        for ticket_id in targets:
            fanout.setdefault(ticket_id, []).append(trigger)
        if not targets or is_stop(trigger):
            router_batch.append(trigger)
    return router_batch, fanout


def thread_tickets(store, thread_id):
    related = store.show(thread_id)["related"]
    return list(dict.fromkeys(i for i, _summary in related if i.startswith("k_")))


def _one_line(text):
    return " ".join(text.splitlines())


def _spill(text, chars):
    shown = _one_line(text[:chars])
    remaining = len(text) - chars
    return f"{shown} …[+{remaining} chars]" if remaining > 0 else shown


def _clip(text, chars):
    return _one_line(text[:chars]) + ("…" if len(text) > chars else "")


def _parent(trigger, chars, store):
    if trigger.parent_id is None:
        return "(none)"
    try:
        return _spill(store.show(trigger.parent_id)["text"], chars)
    except SuperError:
        return f"{trigger.parent_id} (not stored)"


def _ticket(ticket_id, store):
    shown = store.show(ticket_id)
    report_id = next((i for i, _summary in shown["related"] if i.startswith("r_")), None)
    if report_id is None:
        return f"{ticket_id} {shown['state']} · last report: (none)"
    report = store.show(report_id)
    summary = _clip(report["text"], REPORT_CHARS)
    return f'{ticket_id} {shown["state"]} · last report: {report["kind"]} "{summary}"'


def _recall(trigger, config, store):
    tickets = [_ticket(ticket_id, store) for ticket_id in thread_tickets(store, trigger.thread_id)]
    return (
        f"parent: {_parent(trigger, config.router.inline_chars, store)}",
        f"tickets on thread: {'; '.join(tickets) or '(none)'}",
    )


def _block(trigger, admission, recall, text_chars):
    addressed = "addressed" if trigger.addressed else "unaddressed"
    return "\n".join([
        f"## {trigger.id}  {trigger.source}  {trigger.thread_id}  {trigger.actor or '-'}  "
        f"{addressed}  {admission.strength}/{admission.basis}",
        f"text: {_spill(trigger.text, text_chars)}",
        *recall,
        f"more: deez super show {trigger.id}",
    ])


def _header(config, count):
    rules = ", ".join(config.rules) or "(none)"
    return "\n".join([
        "# super-clanker wake",
        f"accept mode: {config.accept.mode} · policy version: {config.accept.policy_version} "
        f"· rules: {rules}",
        f"batch: {count} trigger{'' if count == 1 else 's'}",
    ])


def wake_prompt(items, config, store):
    header = _header(config, len(items))
    entries = [
        (trigger, admission, _recall(trigger, config, store)) for trigger, admission in items
    ]

    def render(text_chars, kept):
        sections = [header, *(_block(t, a, recall, text_chars) for t, a, recall in entries[:kept])]
        sections.append("\n".join(["## verbs", *VERBS]))
        spilled = [f"{t.id} {t.source} {t.thread_id}" for t, _a, _recall in entries[kept:]]
        if spilled:
            sections.append("\n".join(["## also queued", *spilled]))
        return "\n\n".join(sections)

    cap = config.router.wake_cap_chars
    prompt = render(config.router.inline_chars, len(entries))
    if len(prompt) <= cap:
        return prompt
    shrunk = min(config.router.inline_chars, SHRUNK_TEXT_CHARS)
    kept = 0
    while kept < len(entries) and len(render(shrunk, kept + 1)) <= cap:
        kept += 1
    return render(shrunk, kept)
