# Search and filters

Finding a message. A combobox in the channel header takes a query in Discord's
filter grammar (`from:`, `in:`, `mentions:`, `has:`, `is:`), completes each
filter's operand from a typeahead, and puts the hits in a right-slot results
panel. Landed in #703; `src/components/SearchPanel.tsx` is the panel.

The header cluster and the results panel are **two different things**, and the
fixture wires them to different degrees. Read the gotchas before planning a
proof: the grammar is fully driveable, but executing a search is not.

## Sub-features

- The header search combobox, whose accessible name carries the current scope
  and retargets with navigation (`Search #ops` → `Search this topic: CPI print
  — Aug` → `Search @ana`).
- The filter dropdown: a `listbox` named **"Search filters"** offering the six
  grammar entries, each labelled with its purpose *and* its token.
- Operand typeahead — choosing `from:` replaces the option list with the
  roster, and choosing a person composes the token (`from:@ana `).
- The results panel: a result count and the hit rows.
- The search-unavailable error state.
- The two other header search affordances, "Open search in #ops" and
  "Open search panel".

## How to get to it (user POV)

You are in `#ops` and you want the message where someone explained the dedupe
window. You click the search box in the channel header. A menu drops down
offering the ways to narrow — from a person, in a channel, mentioning someone,
by attachment type. You pick **From a specific user**, the box fills in `from:`
and now lists your people; you pick `@ana` and it reads `from:@ana `. You add a
word and the results appear in a panel down the right.

## Driving it with control-om-chat

The grammar drives entirely by role and name:

```bash
agent-browser open "$(./control-om-chat url \
  'tools/visual/shell-fixture.html?view=room&alerts=quiet')"

agent-browser find role combobox click --name "Search #ops"
agent-browser find role option   click --name "From a specific user from: user"
agent-browser find role option   click --name "@ana ana (ops)"
agent-browser eval '(()=>document.querySelector("input[placeholder*=\"Search\"]").value)()'
#   "from:@ana "
```

The six filter options, by their full accessible names:

| Option name | Token |
|---|---|
| `From a specific user from: user` | `from:` |
| `Sent in a specific channel in: channel` | `in:` |
| `Mentions a specific user mentions: user` | `mentions:` |
| `Includes a specific type of data has: image, file, attachment or link` | `has:` |
| `Sent by a person or an agent is: agent or human` | `is:` |
| `More filters dates, author type, and more` | — |

The **results panel has its own route**, because typing a query and pressing
Enter does not run one here (see Gotchas). `?panel=search` seeds a canned run —
the query `dedupe`, scoped to `#ops`:

| Route | State |
|---|---|
| `shell-fixture.html?view=room&alerts=quiet&panel=search` | Results panel, one hit, heading `1 results` |
| `shell-fixture.html?view=room&alerts=quiet&panel=search&searchState=error` | The same run, plus *"The search service is unavailable"* |

Scope retargeting is the cheap second observation, and it is the one worth
capturing — it proves the search box followed the navigation, not just the
pane:

```bash
agent-browser snapshot -c | grep -i combobox
#   "Search #ops"  ->  "Search this topic: CPI print — Aug"  ->  "Search @ana"
```

## Gotchas

- **Enter does not execute a search in the fixture.** The grammar composes, the
  typeahead resolves, and then nothing happens: no results panel, no route
  change. Use `?panel=search` for a run you can photograph. A proof that
  types a query and screenshots the unchanged pane is evidence of nothing.
- **`?searchState=error` alone renders nothing.** The message only exists
  inside the panel, so it needs `panel=search` beside it. On its own the
  parameter looks dead.
- **Only the combobox is wired.** Its two neighbours are not: "Open search in
  #ops" leaves focus on the button with the combobox still collapsed, and
  "Open search panel" opens no panel. **"More filters"** closes the dropdown
  and inserts no token. None of the three is a regression to report from this
  lane — the fixture simply does not seed them — but do not build a proof on
  any of them. Reach the panel by route instead.
- **The sidebar's "Search or jump to…" is a different control** and is also
  inert (see [channel-and-topic-navigation.md](channel-and-topic-navigation.md)).
  Do not confuse the two: the header combobox is the one that works.
- The filter options' accessible names are the label **and** the token run
  together (`From a specific user from: user`). An `--exact` match on either
  half alone finds nothing.
- The result count is not pluralised — a single hit reads **`1 results`**
  (`SearchPanel.tsx:1230`, `:1238`). That is the product string, not a fixture
  artefact; caption a screenshot around it rather than quietly "fixing" it in
  the caption.
