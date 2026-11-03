# Reproduce a defect a listed sender reports without asking
mode: observe

When a listed sender reports a defect in a room the Router listens to, and
does not address the agent, the Router may dispatch `bug-fix` with
`--rule silent-repro`.

The Worker reproduces the defect and stops at a verified local candidate. It
reports `ready`. Nothing is delivered without the operator's word.

The rule stays in `observe` until the operator has reviewed the recorded
`would accept` decisions and runs
`deez super-clanker policy set silent-repro --mode auto`.
