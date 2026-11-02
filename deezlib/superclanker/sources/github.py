import subprocess

from deezlib.superclanker import sources
from deezlib.superclanker.domain import Trigger, trigger_id, utc_now

SOURCE = "github"
VIEW_FIELDS = "number,headRefName,reviewDecision,reviews,statusCheckRollup,comments"
UNFINISHED_STATES = ("PENDING", "EXPECTED")
REVIEW_THREADS_QUERY = (
    "query($owner:String!,$name:String!,$number:Int!){ repository(owner:$owner,name:$name){ "
    "pullRequest(number:$number){ reviewThreads(first:100){ nodes{ id isResolved "
    "comments(first:50){ nodes{ id databaseId author{login} body createdAt path url } } } } } } }"
)


def _login(author):
    return author["login"] if author else "ghost"


def _trigger(policy, scope, number, event_id, actor, body, text, received_at, meta,
             parent_id=None):
    return Trigger(
        id=trigger_id(SOURCE, event_id),
        source=SOURCE,
        source_event_id=event_id,
        thread_id=f"gh:{scope}#{number}",
        actor=actor,
        addressed=sources.mentions(policy, body),
        text=text,
        parent_id=parent_id,
        received_at=received_at,
        meta={"pr": number, "repo": scope, **meta},
    )


def _thread_triggers(policy, scope, number, thread):
    comments = thread["comments"]["nodes"]
    first = trigger_id(SOURCE, f"comment:{comments[0]['databaseId']}") if comments else None
    return [
        _trigger(
            policy, scope, number, f"comment:{comment['databaseId']}", _login(comment["author"]),
            comment["body"], f"[{comment['path']}] {comment['body']}", comment["createdAt"],
            {"url": comment["url"], "thread": thread["id"], "resolved": thread["isResolved"]},
            parent_id=None if index == 0 else first,
        )
        for index, comment in enumerate(comments)
    ]


def _verdict(check):
    if "status" in check:
        return (check.get("conclusion") or None) if check["status"] == "COMPLETED" else None
    return None if check["state"] in UNFINISHED_STATES else check["state"]


def _check_trigger(policy, scope, view, check, stamp):
    name = check.get("name") or check.get("context")
    conclusion = _verdict(check)
    completed_at = check.get("completedAt") or ""
    return _trigger(
        policy, scope, view["number"],
        f"check:{view['number']}:{name}:{conclusion}:{completed_at}", None, "",
        f"CI {name} {conclusion} on {view['headRefName']}", completed_at or stamp,
        {"url": check.get("detailsUrl") or check.get("targetUrl")},
    )


def pr_triggers(policy, scope, view, threads, stamp):
    number = view["number"]
    found = [
        trigger for thread in threads for trigger in _thread_triggers(policy, scope, number, thread)
    ]
    found += [
        _trigger(
            policy, scope, number, f"issuecomment:{comment['id']}", _login(comment["author"]),
            comment["body"], comment["body"], comment["createdAt"], {"url": comment["url"]},
        )
        for comment in view["comments"]
    ]
    found += [
        _trigger(
            policy, scope, number, f"review:{_login(review['author'])}:{review['submittedAt']}",
            _login(review["author"]), review["body"], f"review {review['state']}: {review['body']}",
            review["submittedAt"], {},
        )
        for review in view["reviews"] if review["state"] != "PENDING"
    ]
    found += [
        _check_trigger(policy, scope, view, check, stamp)
        for check in view["statusCheckRollup"] if _verdict(check)
    ]
    return found


def _read(policy, run, stamp):
    found = []
    for scope in policy.scopes:
        owner, name = scope.split("/", 1)
        listed = sources.read_json(run, [
            "gh", "pr", "list", "--repo", scope, "--author", "@me", "--state", "open",
            "--json", "number,headRefName,updatedAt",
        ])
        for pr in listed:
            number = str(pr["number"])
            view = sources.read_json(
                run, ["gh", "pr", "view", number, "--repo", scope, "--json", VIEW_FIELDS]
            )
            threads = sources.read_json(run, [
                "gh", "api", "graphql", "-F", f"owner={owner}", "-F", f"name={name}",
                "-F", f"number={number}", "-f", f"query={REVIEW_THREADS_QUERY}",
            ])["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
            found += pr_triggers(policy, scope, view, threads, stamp)
    return found


def poll(store, policy, run=subprocess.run, now=utc_now):
    stamp = now()
    return sources.record(store, policy, lambda: stamp, lambda: _read(policy, run, stamp))
