import json
import re
import subprocess
from datetime import datetime, timezone

REVIEW_URL = re.compile(r"https?://[^\s)\]>'\"`]+/(?:pull|merge_requests)/\d+")
CHECK_SECONDS = 120
FORGE_TIMEOUT_SECONDS = 20
CURSOR = ("reviews", "checked_at")


def find_review_url(texts):
    for text in texts:
        found = REVIEW_URL.search(text or "")
        if found:
            return found.group(0)
    return None


def ticket_review_url(store, ticket_id):
    texts = []
    for report in store.ticket_reports(ticket_id):
        texts += [*(report.evidence or ()), report.text]
    return find_review_url(texts)


def _command(url):
    if "/merge_requests/" in url:
        return ["glab", "mr", "view", url, "-F", "json"]
    return ["gh", "pr", "view", url, "--json", "state,headRefOid", "-q", '.state + " " + .headRefOid']


def review_status(url, run=subprocess.run):
    argv = _command(url)
    try:
        done = run(argv, capture_output=True, text=True, timeout=FORGE_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReviewError(f"{url}: {argv[0]} failed: {exc}") from exc
    if done.returncode != 0:
        raise ReviewError(f"{url}: {argv[0]} exit {done.returncode}: {(done.stderr or '').strip()[-200:]}")
    raw = (done.stdout or "").strip()
    if argv[0] == "glab":
        try:
            found = json.loads(raw)
            return str(found.get("state", "")).lower(), found.get("sha") or None
        except (ValueError, AttributeError) as exc:
            raise ReviewError(f"{url}: glab gave no state") from exc
    state, _, head = raw.partition(" ")
    return state.lower(), head.strip() or None


class ReviewError(Exception):
    pass


def merge(url, auto=False, run=None):
    run = run or subprocess.run
    if "/merge_requests/" in url:
        argv = ["glab", "mr", "merge", url, "--squash", "--yes", "--auto-merge" if auto else "--auto-merge=false"]
    else:
        argv = ["gh", "pr", "merge", url, "--squash", *(["--auto"] if auto else [])]
    try:
        done = run(argv, capture_output=True, text=True, timeout=FORGE_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReviewError(f"{url}: {argv[0]} failed: {exc}") from exc
    if done.returncode != 0:
        raise ReviewError(f"{url}: {argv[0]} exit {done.returncode}: {(done.stderr or '').strip()[-300:]}")


def _due(store, now):
    last = store.cursor(*CURSOR)
    if last:
        try:
            if (now - datetime.fromisoformat(last)).total_seconds() < CHECK_SECONDS:
                return False
        except ValueError:
            pass
    store.set_cursor(*CURSOR, now.isoformat())
    return True


def close_merged(store, now=None, run=subprocess.run):
    now = now or datetime.now(timezone.utc)
    if not _due(store, now):
        return [], []
    closed, errors = [], []
    for row in store.status():
        if row["state"] != "open":
            continue
        url = ticket_review_url(store, row["ticket"])
        if url is None or store.worker_running(row["ticket"]):
            continue
        try:
            state, head = review_status(url, run)
        except ReviewError as exc:
            errors.append(str(exc))
            continue
        if state != "merged":
            continue
        ticket = store.close_merged(row["ticket"], url, head)
        closed.append(ticket.id)
        if ticket.thread_id.startswith("terminal:"):
            store.reply(ticket.thread_id, f"{ticket.slug}: {url} merged. Closed the ticket; its workspace is removed next.")
    return closed, errors
