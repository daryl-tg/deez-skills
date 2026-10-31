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
`<room>:<topic>:<query>`. The earlier dual-host proof was run at GitHub
`41a57adc`, which reached this repo through sync commit `8b0ff076`. Since then,
the `/rooms/` fixture has changed; current `/rooms/` and `/chat/` fixture files
are not byte-identical. Source confirms both still implement `?search=live` with
deterministic fixture responses, but only `/rooms/` was re-driven in this pass.
Do not infer byte parity or current live behavior on `/chat/` from the older
proof.

## Sub-features

- The header search combobox, whose accessible name carries the current scope
  and retargets with navigation (`Search #ops` → `Search this topic: CPI print
  — Aug` → `Search @ana`).
- The filter dropdown: a `listbox` named **"Search filters"** offering the six
  grammar entries, each labelled with its purpose *and* its token.
- Operand typeahead — choosing `from:` replaces the option list with the
  roster, and choosing a person composes the token (`from:@ana `).
- The results panel: a result count and the hit rows.
- The results-scope picker. On room searches it offers **This thread** when
  inside a topic, **This channel**, **This server**, **Library**, and
  **Everywhere**; on a DM it offers **This DM**, **All DMs**, and
  **Everywhere** (options `SearchPanel.tsx:74-101`, the picker with trigger
  `Search in: <label>` and menu `Search in` at `:458-500`).
- Date filters from **More filters**: `before:`, `after:`, and `during:`
  (`search-query.ts:3-38`).
- The search-unavailable error state.
- The two other header search affordances, "Open search in #ops" and
  "Open search panel" / "Close search panel" (`SearchBar.tsx:561`). The toggle
  name follows the scope: `Open search in topic <name>` in a topic, and
  `Open search with @ana` (not "in") in a DM.
- Result counts read `${count}${partial ? "+" : ""} results`, so a partial
  window shows `1+ results` (`SearchPanel.tsx:1287`, `:1295`). Empty states:
  "No results in #ops." (`:1777`) and "No results in your conversation with
  @x." (`:2333`). Plus `Clear search`, `Clear search history` and the `Sort
  search results` menu.

## How to get to it (user POV)

You are in `#ops` and you want the message where someone explained the dedupe
window. You click the search box in the channel header. A menu drops down
offering the ways to narrow — from a person, in a channel, mentioning someone,
by attachment type. The results panel also lets you scope that search to this
thread, channel, server, the Library, or everywhere. In a DM, choose this
conversation or all DMs. You pick **From a specific user**, the box fills in `from:`
and now lists your people; you pick `@ana` and it reads `from:@ana `. You add a
word and the results appear in a panel down the right.

## Driving it with control-om-chat

The grammar drives entirely by role and name:

```bash
agent-browser open "$(control-om-chat url \
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

Open **Search in: This channel** from that result panel to inspect the
room-scope choices. The equivalent DM scope picker is available after opening
search on `?view=dm&dm=ana&alerts=quiet`; it offers **This DM**, **All DMs**,
and **Everywhere**. **More filters** includes `before:`, `after:`, and
`during:` date operators.

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

### Sort menu (added 2026-10-31)

On `shell-fixture.html?view=room&alerts=quiet&panel=search`, the results header
carries a **Sort** button. Clicking it opens a `menu` named **Sort search
results** (`SearchPanel.tsx:556`) with **Newest**, **Oldest** and, because the
seeded run has query text, **Most relevant** (`SearchPanel.tsx:520-556`, the
third option is gated on `ranked`). The scope picker (**Search in: This
channel**) listed **This channel**, **This server**, **Library** and
**Everywhere** on both hosts; **This thread** appears only inside a topic.
Driven 2026-10-31 on `/rooms/` (18135); the scope picker also on `/chat/`
(18136).

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
- **The query survives navigation, and a filled combobox shows no filter
  listbox.** After searching `primary` in a topic and going **Back to #ops**,
  the channel's **Search #ops** combobox still holds `primary`. Clicking it
  then lists no `From a specific user` option, and the filter step looks broken.
  Drive the filter grammar from a fresh load, or clear the field first.

### Verification record

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `panel=search` heading **1 results**, **Sort** → menu **Sort search results** (Newest / Oldest / Most relevant), `searchState=error` ("The search service is unavailable"), and the **Search #ops** combobox's six filter options (from:, in:, mentions:, has:, is:, More filters). `/chat/` (18138): **1 results**, **Sort**, and **Search in: This channel** → This channel / This server / Library / Everywhere. **Limitations:** the `from:` user option, the topic search box and date filters were not re-driven; backend ranking stays pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`search-01`, `search-02`, `chat-08`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): combobox **Search #ops** → **From a specific user** → **@ana** gave `from:@ana `; `panel=search` **1 results**; the scope picker; the **Sort** menu. `/chat/` (18136): `panel=search` **1 results** and the scope picker. **Limitations:** Date filters, backend ranking, the topic live-search request (2026-10-29 stands), and `/chat/` grammar. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: `panel=search` **1 results**; `searchState=error` reads "The search service is unavailable"; **Search this topic: CPI print — Aug** on `search=live`; **Search #ops** with `from:` lists @kyle, @ana, @dax, @mira. `/chat/`: `panel=search` **1 results** and the topic search box. **Limitations:** Date filters and backend ranking. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frame 22).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `?view=topic&topic=cpi-print-aug&alerts=quiet&search=live` showed the **Search this topic: CPI print — Aug** box. **Limitations:** Scoped requests, the user filter, date filters and `/chat/` were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 15, 49).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=topic&topic=cpi-print-aug&alerts=quiet&search=live` showed the **Search this topic: CPI print — Aug** box. **Limitations:** The scoped request ids, **From a specific user**, `?panel=search`, `searchState=error`, date filters, ranking and `/chat/` were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 19).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `?view=topic&topic=cpi-print-aug&search=live` showed the **Search this topic: CPI print — Aug** box. **Limitations:** The scoped request ids, the **From a specific user** filter, `?panel=search`, `searchState=error`, date filters, ranking and `/chat/` were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 23). Previous record: 2026-10-26 at `5820fbea`.
