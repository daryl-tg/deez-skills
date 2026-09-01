# chart-schema → @orangecharts/chart-schema: audited migration map

Reference for the first application of `migrating-types-to-orange-shared`. Verified against kiyotaka-frontend @ July 2026 (branch `production`, `src/shared/chart-schema/` at 11 files + README). Re-verify counts before executing — this map is the audit's starting point, not a substitute for running Step 0.

## Package shape

- Name: `@orangecharts/chart-schema`, first release `0.1.0` via `./release.sh chart-schema minor` from a committed `0.0.0`.
- Subpath exports required by real consumers: `.` (barrel), `./tools`, `./cursor-modes`, `./technical-scripts`, `./tool-field-specs`. Keep `./tool-level-defaults` **unexported** (internal to `tools.ts` only). Add `./types`, `./id`, `./indicator-types`, `./native-aliases`, `./multichart` for the later collab-service/openmarket adoptions.
- 7 files need `.js` added to relative specifiers when moved (index.ts ×8, id.ts, indicator-types.ts, cursor-modes.ts, tool-field-specs.ts, technical-scripts.ts, tools.ts ×2).
- Self-consistency test to port into the package: drift-guard check #5 (alias/display-name targets resolve to real `INDICATOR_TYPES` keys; technical-script alias targets resolve to real subtype keys).

## Category A — folder is the live source (move + rewrite specifiers)

20 files import `@/shared/chart-schema[...]` (16 `src/` + 4 `tests/` as of 2026-07-24 on `daryl/ui-kscript-publish-dialog` — counts drift by branch, re-run the grep first). Notable non-obvious sites:

- `tests/composables/toolsSidebar/useToolSelection.spec.ts` — `vi.mock('@/shared/chart-schema/tools', …)`: the **mock specifier string** must change too.
- `tests/browser/chart/tool-style-undo.browser.ts` — dynamic `await import(...)` of `/tools` and `/tool-field-specs`.
- `tests/shared/chart-schema/tools-layout.spec.ts` — relocate (its mirrored `src/` path dies); repoint import to the package.
- Comment-only references (no import): `src/agent-bridge/decomposer/drawing/tool-identity.ts` (×2), `src/components/objects/tool-prop-sections.ts`, `src/components/objects/ToolPropertiesEditor.vue`.
- Barrel consumers pull `SYNC_KEYS`, `SYMBOL_SYNC_FIELDS`, `LAYOUT_CHART_COUNT`/`LayoutMode`, `FIB_DEFAULT_LEVELS`, `TOOLS`.

After cutover: delete `src/shared/chart-schema/`; `src/shared/` is then empty — delete it too.

## Category B — FE source is the truth today (INVERT)

| Mirrored constant | FE definition site | Inversion |
|---|---|---|
| `INDICATOR_TYPES` keys + `overlayType`/`dataType` | ~100 control classes `src/indicators/controls/*/index.ts` (literal class fields; registry key in `indicatorRegistry.set('<KEY>', …)`) | Class fields read `INDICATOR_TYPES.<KEY>.overlayType` / `.dataType` from the package. **Worker controls too**: 98 of 110 files under `src/workers/indicators/controls/` carry the same `dataType` literals (confirmed 2026-07-24) and the old guard never checked them — an unguarded second copy; invert them the same way. |
| `TECHNICAL_SCRIPT_SUBTYPES` keys | `src/constants/scriptEditor/technicalIndicatorScripts.constants.ts` (`TECHNICAL_INDICATOR_SCRIPTS`) | Script **bodies** stay FE-side (deliberately not in the schema). Type the map `satisfies Record<TechnicalScriptSubtype, …>` against the package so key drift is a compile error. |
| `DEFAULT_TOOL_COLOR` | `src/constants/chartColors.constants.ts` | Re-export from the package; delete the local literal. |
| `FIB_DEFAULT_LEVELS` | `src/constants/fibonacci.constants.ts` (`DefaultFibonacciLevelsConfig`) | Derive from the package value. Note `register-tools.ts` already imports the schema's copy — dual truth today; inversion collapses it. |

## Drift guard disposition (`scripts/check-chart-schema.mjs`, npm script `check:chart-schema`)

The script text-reads `src/shared/chart-schema/*.ts` from disk — left untouched it breaks the moment the folder is deleted, and a `src/`-scoped grep never notices. Keep the npm-script name; rewrite the body:

| Check | Disposition |
|---|---|
| 1. `INDICATOR_TYPES` ↔ `indicatorRegistry.set` keys + overlayType/dataType values | **Dies** — inversion makes controls consume the package; nothing left to compare |
| 2. `TECHNICAL_SCRIPT_SUBTYPES` ↔ `TECHNICAL_INDICATOR_SCRIPTS` keys | **Dies** — replaced by the `satisfies` typing |
| 3. `TOOLS` ⊆ `TOOL_ICONS` | **Keep, retarget** — icons are FE assets; read `TOOLS` keys from the installed package |
| 4. `DEFAULT_TOOL_COLOR` + `FIB_DEFAULT_LEVELS` values | **Dies** — inversion removes the local literals |
| 5. Alias targets resolve to real keys | **Moves into the package** as its self-consistency test |
| 6. Gate-vocabulary sweep (`.startsWith`/`.includes` UPPER_SNAKE tokens over `src/`) | **Keep, retarget** — sweeps FE source; vocab (`INDICATOR_TYPES` keys + dataTypes) now read from the installed package; `GATE_NON_OVERLAY_ALLOWLIST` stays FE-side |

Also rewrite the script's header comment and failure message ("re-copy to collab-service + openmarket" is dead — external consumers adopt the npm package instead).

## Verification caveat

The repo-root grep for the old path also hits frozen QA snapshots (`qa/orderflow/proof-u*/summary.json` — point-in-time artifacts, not live code). Confirm such hits are inert instead of chasing them; everything under `src/`, `tests/`, `scripts/`, and configs must be zero.

## FE dev loop

Add the dev-serve-only sibling-source alias for `@orangecharts/chart-schema` in `vite.config.ts` next to the `titan-dev`/kscript blocks (see `authoring-orange-shared-packages` → Local dev loop).

## Out of scope

collab-service and openmarket cutovers happen in their own cycles — they stop hand-copying and adopt the npm package. No other repo under `/Users/dboon/Gitlab` carries a copy (verified by content search, July 2026).
