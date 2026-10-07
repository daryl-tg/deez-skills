# Agent creation, import and sharing

## Sub-features

The current product tree includes local agent creation and import, a catalog,
private Try, server publication and adoption, reviewed updates and rollback,
revocation, channel use, and native coding runs. The creator and catalog UI are
gated by daemon roster capabilities and explicit owner identity.

## How to get to it (user POV)

Open **Agents** and go to the roster's **Your agents** section for creation,
import, and catalog actions when the daemon advertises roster support. The
separate **+ Wire an agent** button remains an Agent Settings shortcut; it is
not the creator entry point.

## Driving it with control-om-chat

Open the source fixture route:

```text
tools/visual/shell-fixture.html?view=agents
```

This pass confirmed the Agent Center roster and **+ Wire an agent**. That
button opens Settings → Agent Settings with an **install OM** link. The roster
creator/import form was absent because this fixture did not provide supported
roster operations and explicit owner identity (`RosterCreateForm.tsx:226-231`).
The local parity services on ports 4001 and 3002 were not running, so the
source fixture could not satisfy those prerequisites. Record creator, import,
catalog, adoption, and update journeys as verified-unreachable on this lane;
use the documented isolated daemon lane to prove them end to end.

## Gotchas

The UI is present in the current product tree, but this source fixture cannot
provide its daemon capability and owner prerequisites. Do not describe this as a
product gap or claim that the gated flows were live-verified. The older full-flow
receipts remain historical context until the current daemon lane is exercised.

### Verification record

**Last verified:** 2026-10-07. **Product commit:** `a0916a25d19bdd5d8890669b89617c2e253679a2`. **Scope:** opened this feature’s documented source-fixture entry route on the current product revision and checked its initial rendered state. **Limitations:** this pass rechecked route reachability only; detailed interactions remain as recorded above and daemon-backed behavior was not re-exercised.
