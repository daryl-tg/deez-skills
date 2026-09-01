## The Rule

State the principle, not its instances. If the reader
can derive the examples from the rule, the examples are
clutter.

---

## Patterns to Avoid

### Enumerating the Obvious

Listing specific cases that any competent reader would
recognize from the general directive alone. The list
adds length without adding judgment.

**Bad:**
```
Scan staged files for secrets: `.env`, `*.pem`,
`*.key`, `*.p12`, `*.pfx`, `*credentials*`,
`*secret*`, `*token*`, `id_rsa`, `id_ed25519`,
`*.keystore`, `*.jks`.
```

**Good:**
```
Scan staged files for secrets before committing.
```

The reader knows what a secret looks like. The glob
list doesn't make them better at spotting one — it
just makes them think the list is exhaustive and
anything not on it is fine.

### Showing Bad Examples

Demonstrating what not to do when the rule already
makes it clear. If "use imperative mood, under 72
characters" is the instruction, the reader does not
need to see `fixed stuff` and `WIP` labeled as bad.

**Bad:**
```
Good:
    parser: reject unterminated string literals

Bad:
    fixed stuff
    Update parser.go
    Various improvements and cleanups
    WIP
```

**Good:**
```
    parser: reject unterminated string literals
    tls: add client certificate support
    cmd/serve: fix crash on empty config file
```

Good examples establish the convention. Bad examples
state what the rule already forbids.

### Restating the Tool

Explaining what a well-known tool or flag does when
the instruction is just to use it.

**Bad:**
```
Use `git add -p` to stage hunks selectively when a
file contains changes for more than one logical
commit.
```

**Good:**
```
Use `git add -p` when a file spans multiple commits.
```

The reader knows what `git add -p` does. Say when to
use it, not what it does.

### Spelling Out Consequences

Appending "this makes X harder and Y harder" when the
reader already understands why a rule exists. Trust
that a competent reader sees the reasoning.

**Bad:**
```
Mixing a bugfix with a cosmetic rename makes both
harder to review and harder to revert.
```

**Good:**
```
Do not mix unrelated changes in one commit.
```

The reader knows why.

---

## When Specifics Help

Not all enumeration is bad. Specifics earn their place
when they establish a convention the reader would not
guess, or when they draw a boundary that requires
judgment.

A commit message format like `<area>: <what changed>`
is a convention. Without the examples, the reader
might use a different style. The examples define the
standard, not illustrate the obvious.

The test: remove the example. Would a competent reader
following the rule produce the same result? If yes,
the example is noise. If they might reasonably diverge,
keep it.
