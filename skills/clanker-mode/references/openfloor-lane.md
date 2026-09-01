# The OpenFloor verification lane

Concurrent features must **never** share a device session or a Metro instance.
This is **principle-separate-before-serializing-shared-state** applied to a
physical resource.

The queue owns one permanent simulator per lane slot, named
`OpenFloor verification-lane-<slot>`. Feature runs reuse it sequentially and
**never create per-feature devices**. The main-worktree device sits outside this
pool and must never be targeted.

Take an exclusive lane. `openfloor-lane` queues when one is busy:

```bash
eval "$(openfloor-lane acquire <branch-slug> --worktree <this worktree>)"
# exports OPENFLOOR_UDID, OPENFLOOR_METRO_PORT, OPENFLOOR_LANE

openfloor-lane device <branch-slug> open OpenFloor \
  "openfloor://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A$OPENFLOOR_METRO_PORT"
```

Release the lane when the run's last drive is done, including any re-proof after
a fix. Evidence survives the release.

**One shot, at the end.** The lane is acquired once the static gates pass and
the candidate is complete, not to watch progress. Every extra session is queue
time taken from another feature.
