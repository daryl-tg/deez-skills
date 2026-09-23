# Search and filters

Finding a message. A combobox in the channel header takes a query in Discord's
filter grammar (`from:`, `in:`, `mentions:`, `has:`, `is:`), completes each
filter's operand from a typeahead, and puts the hits in a right-slot results
panel. Landed in #703; `packages/chat-ui/src/components/SearchPanel.tsx` is the panel.

The header and results panel share the search seam. The default fixture uses
canned results. `#971` added `?search=live`, which runs the real seam against
deterministic fixture responses, to **both** fixtures —
`tools/visual/shell-fixture.tsx` for `/rooms/` and
`apps/cloud/tools/visual/shell-fixture.tsx` for `/chat/`. With it, pressing
Enter in the combobox really runs a search: the panel opens and
`document.documentElement.dataset.fixtureSearchRequest` records
`<room>:<topic>:<query>`. The recipe below was re-driven end to end on both
hosts at `41a57adc`.

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

The results panel also has a seeded route. `?panel=search` seeds a canned run
with the query `dedupe`, scoped to `#ops`:

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

To reproduce the thread-navigation case on the candidate:

1. Open `tools/visual/shell-fixture.html?view=topic&topic=cpi-print-aug&alerts=quiet&search=live`
   under `/rooms/`. For `/chat/`, start the cloud host on its own agent port
   (see "The /chat/ host" in SKILL.md) and use a fresh browser session.
2. Fill and click the combobox `Search this topic: CPI print — Aug`, then press
   Enter with `primary`. There are no matching messages in that topic.
3. Snapshot, then click the `ETF flows, week of the 28th, 1 mention, 2 unread`
   treeitem beneath **ops**. The same accessible name exists under other rooms,
   so use the current snapshot ref for the ops row.
4. The visible message begins `primary market`. The panel must now show that
   result and the ETF topic breadcrumb without closing or reopening search.
5. Check `document.documentElement.dataset.fixtureSearchRequest`. It must be
   `ops:etf-flows-week:primary`. Change the panel query to `secondary` and click
   the exact `Search` button. Expect the same message and the new query in that
   request marker.

The fixture runs real search UI, query parsing and request construction. Its
transport searches seeded text by case-insensitive substring. It does not prove
production full-text ranking, permissions or backend coverage. The existing
partial-window warning remains visible.

## Gotchas

- Default fixture results are canned. Use `?search=live` to prove query and
  thread scoping. A canned hit is not evidence that text search matched.
- Before `#971`, `fixtureSearchSeam.run` referenced `sessionState` and `emit`
  outside their scope, so Enter threw a ReferenceError. `#971` moved the seam
  inside the fixture session. On an older checkout, Enter rendering nothing is
  that bug, not the product.
- The cloud fixture stubs less than the root one — alert, Composer and
  closed-dialog state were thin before `#971`. If the page crashes or a search
  control is covered, read the console and look for the missing stub: a truthy
  `INERT` predicate can hold a dialog open over the thing you meant to click.
  (It cannot pose as a Promise: both fixtures' `INERT` answers `then` with
  `undefined`, and has since each entered this repo.)
- **The sidebar's "Search or jump to…" is a different control** and is also
  inert (see [channel-and-topic-navigation.md](channel-and-topic-navigation.md)).
  Do not confuse the two: the header combobox is the one that works.
- The filter options' accessible names are the label **and** the token run
  together (`From a specific user from: user`). An `--exact` match on either
  half alone finds nothing.
- The result count is not pluralised — a single hit reads **`1 results`**
  (`SearchPanel.tsx:1287`, `:1295`). That is the product string, not a fixture
  artefact; caption a screenshot around it rather than quietly "fixing" it in
  the caption.
