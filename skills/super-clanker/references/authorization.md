# Authorization

## The gate

Python gates each queued Trigger before any model runs. The first match decides.

1. A `worker` report is explicit.
2. A disabled source, or one in mode `ignore`, admits nothing.
3. A listed bot is inferred if it addresses the agent or the source is in
   `candidates` mode, else not admitted.
4. A sender-less event is inferred on a Thread with Tickets, else not admitted.
5. A listed sender addressing the agent is explicit.
6. A follow-up on a Thread with Tickets is explicit from a listed sender,
   inferred from anyone else.
7. Any sender on a `candidates` source is inferred.
8. Nothing else is admitted.

## Strength

| Strength | What happens |
|---|---|
| explicit | `dispatch` starts work at once. Modes do not apply. |
| inferred | `dispatch` obeys the accept mode and the cited rules' modes. |
| not_admitted | Ignored with the gate's reason, unseen by the Router. |

## Modes

`accept.mode` is the default for inferred work.

- `off` makes inferred work not admitted at the gate.
- `observe`, the default, records an inferred `dispatch` as an ignore decision
  reading `would accept: <slug> via <rules>`. Nothing starts.
- `auto` accepts inferred work.

A rule's `mode:` line overrides it for a dispatch citing `--rule <name>`. A
cited rule in `off` refuses the dispatch. A cited rule in `auto` accepts it
even under `observe`. Accepted inferred work still stops at a verified local
candidate.

## A Worker's question

1. A Worker at a gate only the operator can pass reports `waiting` with one
   question and stops.
2. `reap` turns the report into a Trigger on `worker:<ticket>`, which wakes
   the Router.
3. The Router relays it with `deez super reply` on the request's Thread,
   then ignores the report.
4. The daemon delivers it, and `status` flags the Ticket for attention.
5. The operator answers on that Thread. The Ticket is subscribed, so the
   answer fans out to it without waking the Router, unless it is a stop.
6. The daemon resumes the Worker's session with the answer as input.
