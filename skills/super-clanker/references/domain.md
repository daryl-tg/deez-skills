# Domain

Source → Trigger → Thread → Decision. An accept creates a Ticket, its Mandate
and one Assignment. Subscriptions tie Tickets to Threads. A person is Trigger
metadata, never an object.

| Object | Id | Key rule |
|---|---|---|
| Trigger | `t_` | Immutable. Stored once. |
| Thread | its address, such as `terminal:default` | Holds subscriptions and decision history. |
| Decision | `d_` | accept, stop, ignore or unavailable, with strength and reason. |
| Mandate | `m_` | Policy version, scope, strength, rules, sender, source. Immutable. Only a person's stop withdraws it. |
| Ticket | `k_` | One piece of work. |
| Assignment | `a_` | One Worker process. |
| Report | `r_` | progress, waiting, ready, blocked, failed or dropped. `waiting` carries one question. |

Also: wake `w_`, reply `p_`, Worker input `i_`, Watchdog tick `x_`.
`deez super show <id>` prints any of them with its neighbours.

## Ticket

`open` → `ended`.

- A person's stop sets `ended_by`, withdraws the Mandate and ends every
  Assignment. `attach` refuses the Ticket afterwards, whoever ran the stop,
  because the Router stops only on a person's word.
- Work ends it with `ended_by` empty, as a `dropped` report does. A follow-up
  on a subscribed Thread still reaches it through fan-out, and `attach` accepts it.

## Assignment

`pending` → `running` → `ended`.

- The daemon launches `pending` work while fewer than `workers.max_running`
  Assignments run.
- `running` spans turns. A turn ends when the process exits. `reap` turns its
  last report into a `worker` Trigger. `progress`, `waiting` and `blocked` keep
  it running, and new inputs resume the same session.
- `ready`, `failed`, `dropped`, `kill`, `retry` and a stop end it. `retry` also
  queues a fresh `pending` Assignment.
