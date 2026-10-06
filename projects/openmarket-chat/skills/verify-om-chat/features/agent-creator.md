# Agent creation, import and sharing

## Sub-features

The previous implementation covered local agent creation/import, private Try,
server catalog publication and adoption, reviewed updates/rollback, revocation,
channel use, and native coding runs. Its detailed verification receipt belongs
to GUI commit `1c11e3319a866475826f6321c945dda06fee1e68`, not the current product
HEAD. Those flows are absent from the current product tree and are not current
working behavior.

## How to get to it (user POV)

On current product HEAD `231c95f49820399fc10e40e87facee6ba606c6b0`, open **Agents**
and choose **+ Wire an agent**. The app opens Settings → Agent Settings and
offers an **install OM** link. There are no creation, import, or catalog
controls in this product revision.

## Driving it with control-om-chat

Use the run-owned source fixture to record current reachability:

```text
tools/visual/shell-fixture.html?view=agents
```

Wait for the roster, choose **+ Wire an agent**, and verify the Settings dialog
opens at **Agent Settings**. This is `verified-unreachable` for the creator,
import, and catalog behavior at product HEAD `231c95f4`. The observed result is
not a daemon prerequisite: the UI route itself is absent in this product tree.
Do not use the old two-daemon creator recipe as a current verification recipe.

## Gotchas

This is a product gap relative to the previously verified GUI implementation,
not evidence that creation is reachable behind the local source fixture. The
older full-flow receipts referenced GUI/daemon revisions outside the current
product HEAD; retain them only as historical context and do not claim their
native coding, catalog, or delivery results for this product revision.

### Verification record

**Last verified:** 2026-10-06. **Product commit:** `231c95f49820399fc10e40e87facee6ba606c6b0`. **Scope:** opened Agent Center and chose **+ Wire an agent**; it opened Settings → Agent Settings with an **install OM** link, not an agent creator/import/catalog flow. **Limitations:** Creator behavior is absent at this product HEAD; this is recorded as a product gap. Daemon-backed paths were not driven.
