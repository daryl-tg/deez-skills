from deezlib.superclanker import procs

KB_PER_GB = 1024 * 1024


def gb(kb):
    return f"{kb / KB_PER_GB:.1f}"


def _age(seconds):
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if seconds >= size:
            return f"{seconds // size}{unit}"
    return f"{seconds}s"


def _tree_kb(snap, groups):
    return sum(procs.tree_rss_kb(snap.table, pids) for pids in groups)


def header_text(snap):
    if not snap.initialised:
        return "daemon not initialised"
    health = snap.health
    if health is None:
        daemon = "daemon ?"
    elif health.alive and health.heartbeat_age_s is not None:
        daemon = f"daemon ok {health.heartbeat_age_s}s"
    else:
        daemon = "daemon DOWN"
    free = "?" if snap.free_pct is None else f"{snap.free_pct}%"
    spend = "?" if snap.spend_today is None else f"${snap.spend_today:.2f}"
    anomalies = sum(len(items) for _kind, items in snap.anomalies)
    stale = f"  STALE ({snap.error})" if snap.stale else ""
    attribution = snap.attribution
    workers = attribution.workers if attribution else {}
    peers = attribution.peers if attribution else {}
    other = attribution.other if attribution else set()
    return "\n".join([
        f"mem {free} free · held: {'no' if snap.held is None else 'yes'} · {daemon} · "
        f"watchdog {anomalies} · today {spend}{stale}",
        f"workers {len(workers)}/{snap.max_running} · {gb(_tree_kb(snap, workers.values()))} GB   "
        f"claude peers {len(peers)} · {gb(_tree_kb(snap, peers.values()))} GB   "
        f"other {gb(_tree_kb(snap, [other]))} GB",
    ])


def ticket_label(row):
    size = "-" if row.rss_kb is None else f"{gb(row.rss_kb)} GB"
    ask = f'  "{row.question}"' if row.question else ""
    return (
        f"{row.ticket_id}  {row.state}  {row.worker_state or '-'}  {row.repo}  {row.slug}  "
        f"{row.last_report or '-'}  {size}  {_age(row.age_s)}{ask}"
    )


def report_text(row):
    return "\n".join([
        f"{row.ticket_id}  {row.slug}  {row.state}", f"repo {row.repo}  worker {row.worker_state or '-'}",
        f"last report: {row.last_report or '-'}", f"question: {row.question or '-'}",
    ])


def sessions_text(snap):
    if not snap.peers:
        return "no peer sessions"
    groups = snap.attribution.peers if snap.attribution else {}
    lines = []
    for peer in snap.peers:
        pids = groups.get(peer.name)
        size = "-" if pids is None else f"{gb(procs.tree_rss_kb(snap.table, pids))} GB"
        lines.append(f"{peer.name}  {peer.pid}  {peer.status}  {size}  {peer.cwd}")
    return "\n".join(lines)
