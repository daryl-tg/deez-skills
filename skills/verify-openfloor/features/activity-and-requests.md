# Activity and requests

The notifications bell in the Chats header opens the Activity screen: mentions
and friend activity under an **All** tab, replies addressed to this account
under a **Replies** tab, and the friend requests sent and received. It is where
a request is accepted, declined or cancelled.

## Sub-features

- `activity-all` lists mentions and friend activity, grouped by day.
- `activity-replies` lists replies to this account.
- `activity-expand` expands one notification to its full text.
- `activity-requests` lists incoming friend requests.
- `activity-sent` expands the sent-requests group.
- `activity-accept` / `activity-decline` / `activity-cancel` action a request.
- `activity-mark-read` marks every reply read.
- `activity-more` loads older notifications.

## How to get to it (user POV)

- Tap the bell in the Chats header, right of the alerts beacon.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero, start from the Chats root.
- **Accepting, declining, cancelling and marking read are production writes**,
  and two of them are irreversible from here. Read the surface; action nothing.
  `activity-accept`, `activity-decline`, `activity-cancel` and
  `activity-mark-read` are the operator's call, not an agent's.

Stable handles:

| Handle | What it is |
|---|---|
| `label="Open notifications and requests"` | the bell, on the Chats header |
| `label="Back to chats"` | back — **ambiguous, needs `role=button`** |
| `label="Notifications"` | the screen title |
| `label="All"` | the mentions tab; the active tab carries `[selected]` |
| `label="Replies, <n>"` | the replies tab; **the count is live** |
| `label="Expand notification from <handle>"` / `label="Collapse notification from <handle>"` | one row, two labels |
| `label="Mark all replies read"` | a production write |
| `label="Load more notifications"` | paging |
| `label="Expand sent requests"` / `label="Collapse sent requests"` | the sent group |
| `label="Accept friend request from <name>"` | production write |
| `label="Decline friend request from <name>"` | production write |
| `label="Cancel friend request to <name>"` | production write |

Row shapes, both composites that inline the whole message body:

- mention: `"<initial>, <handle> mentioned you in #<roomId>, <body>, Expand notification from <handle>"`
- reply: `"<handle> replied to you in <where>, unread"`
- friend: `"You are now friends with <name>"`

- **Open it.** `./control-openfloor device press 'label="Open notifications and requests"' --settle`.
  The settled diff carries `Notifications`, `OPENMARKET ACTIVITY`, the two tabs
  and the day-grouped rows (`TODAY`, `YESTERDAY`, `THIS WEEK`).
- **Switch to replies.** Match on the stable half — the tab embeds a count:
  `./control-openfloor device find "Replies"`.
- **Expand one notification.**
  `press 'label="Expand notification from RyanNG0611" ' --settle` and assert the
  fuller text in the diff, then press the `Collapse …` twin.
- **Leave.** This route hides the dock, so use
  `press 'role=button label="Back to chats"'`.
- **Proof.** The `--settle` diff plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/activity.png" --normalize-status-bar`.

## Gotchas

- **`label="Back to chats"` is ambiguous** — `[other]` and `[button]` both
  match and a bare `press` fails with `AMBIGUOUS_MATCH`. Use
  `role=button label="Back to chats"`. Same shape as `Appearance`,
  `Back to settings` and the Alerts board's `Back`.
- **`Replies, <n>` embeds a live count.** Never exact-match it; `find "Replies"`.
- **Mention rows name the room by id, not by channel.** A row reads
  `mentioned you in #edfe132d4117`, not `#dev-forums`. That is what the app
  renders today — do not "correct" it in a caption, and do not build a selector
  on a channel name that is not there. Reply rows have the mirror problem and
  fall back to a generic `in chat`. Both are reported to the operator as
  product gaps, not doc drift.
- **Row labels inline the entire message body**, including mentions, code and
  URLs. Match a short leading substring with `find`, never the full label.
- **The accept and decline controls sit inside the row you are reading.** They
  are labelled clearly and they are one press from a real friendship. Snapshot
  the surface; do not press them to make a screenshot livelier.
- Verified live 2026-09-03 on `f2c3f88` (iPhone 17 Pro, iOS 26.5).
