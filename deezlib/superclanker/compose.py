from deezlib.superclanker.store import SuperError

SHRUNK_TEXT_CHARS = 50
REPORT_CHARS = 60
CONVERSATION_MESSAGES = 8
MESSAGE_CHARS = 200
VERBS = (
    "deez super-clanker dispatch <trigger> --slug <kebab> [--playbook <name, only when a person"
    " named one>] [--scope <text>] [--rule <name>]",
    "deez super-clanker attach <trigger> <ticket>",
    "deez super-clanker ignore <trigger> --reason <text>",
    "deez super-clanker stop <ticket> --reason <text>",
    "deez super-clanker reply <thread> --text <text>",
    "deez super-clanker note <ticket> --text <text>",
    "deez super-clanker route <<'ROUTE' … ROUTE, one of the verbs above per line, for several decisions in one call",
)


def is_stop(trigger):
    said = trigger.text.lower().strip()
    return said == "stop" or said.startswith("stop ")


def partition(triggers, store):
    router_batch, fanout = [], {}
    for trigger in triggers:
        targets = [] if trigger.source == "terminal" else store.fanout_targets(trigger.thread_id)
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
        f"more: deez super-clanker show {trigger.id}",
    ])


def _header(config, count):
    rules = ", ".join(config.rules) or "(none)"
    return "\n".join([
        "# super-clanker wake",
        f"accept mode: {config.accept.mode} · policy version: {config.accept.policy_version} "
        f"· rules: {rules}",
        f"batch: {count} trigger{'' if count == 1 else 's'}",
    ])


def _open_ticket(row, store):
    line = f"{row['ticket']} {row['slug']} · worker {row['assignment']}"
    report = store.last_report(row["ticket"])
    if report is None:
        return f"- {line} · no report yet"
    line += f' · {report.kind} "{_clip(report.text, REPORT_CHARS)}"'
    if report.question and row["attention"]:
        line += f" · asks: {_clip(report.question, MESSAGE_CHARS)}"
    return f"- {line}"


def _open_tickets(store):
    lines = [_open_ticket(row, store) for row in store.status() if row["state"] == "open"]
    return "\n".join(["## open tickets", *(lines or ["- none"])])


def _conversation(thread_id, batch_ids, store):
    messages = [
        f"- {who}: {_clip(text, MESSAGE_CHARS)}"
        for _at, who, text, message_id in store.thread_messages(thread_id, CONVERSATION_MESSAGES + len(batch_ids))
        if message_id not in batch_ids
    ][-CONVERSATION_MESSAGES:]
    return "\n".join([f"## recent conversation on {thread_id}", *(messages or ["- none"])])


def _state(items, store):
    batch_ids = {trigger.id for trigger, _admission in items}
    threads = dict.fromkeys(t.thread_id for t, _a in items if t.source == "terminal")
    return [_open_tickets(store), *(_conversation(thread, batch_ids, store) for thread in threads)]


def wake_prompt(items, config, store):
    header = "\n\n".join([_header(config, len(items)), *_state(items, store)])
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
