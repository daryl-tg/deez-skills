## The Rule

Comment the *why*, never the *what*. If a comment restates the
code, delete it. If the code needs a comment to explain what it
does, fix the code.

---

## Comments to Kill on Sight

### Narrating the Obvious

Line-by-line play-by-play of code that already reads fine. LLMs
do this compulsively. Every assignment gets a comment. Every
function call gets a label. The result is twice the lines with
zero additional information.

**Delete comments like:**
```c
// Create a new server
server = server_new();

// Set the port to 8080
server_set_port(server, 8080);

// Start the server
server_start(server);
```

The test: delete the comment. Can a competent developer still
understand the code? If yes, the comment was waste.

### The Name Tag

Commenting a variable or function to explain what the name
already says. Means the name is either good (comment is
redundant) or bad (fix the name).

**Delete comments like:**
```c
int count; // the count
char *name; // stores the user's name
void init_logger(void); // initializes the logger
```

### The Synonym Comment

Restating the function signature in prose. LLMs treat this as
mandatory doc-comment etiquette. A doc comment that adds nothing
beyond what the name and types already convey is pure noise.

**Delete comments like:**
```c
// Sets the port to the given value.
void server_set_port(server_t *s, int port);

// Returns the current buffer size.
size_t buffer_get_size(buffer_t *buf);
```

A useful doc comment tells you something the signature doesn't —
preconditions, error behavior, thread safety, lifetime.

### Changelog Journals

Tracking who changed what and when inside the file. That's what
`git log` does, and it never lies.

**Delete comments like:**
```c
// 2024-01-15: Fixed off-by-one (JD)
// 2023-11-02: Added retry logic (AK)
// 2023-08-30: Initial implementation (MR)
```

### Commented-Out Code

Dead code disguised as a comment. Version control remembers
everything. If you might need it later, that's what `git log`
and `git stash` are for.

**Delete on sight:**
```c
// do_old_thing(ctx);
// if (legacy_mode) {
//     handle_legacy();
// }
```

### Section Banners

ASCII art dividers, box-drawing headers, long separator lines.
If you need visual landmarks to navigate a file, the file is
too long or lacks structure. Extract functions. Split files.

**Delete comments like:**
```c
/************************************/
/*          INITIALIZATION          */
/************************************/

// ========== HELPERS ==========

////////////////////////////////////////////////////////////////////////////////
// Scope Model Instantiation
////////////////////////////////////////////////////////////////////////////////
```

### Closing Brace Labels

If the brace is so far from its opening that you can't tell
what it closes, the block is too long. Refactor instead.

**Delete comments like:**
```c
    }  // end if
  }  // end for
}  // end process_request
```

### Apologetic Comments

Comments that explain why the code is bad instead of making it
better. If you know it's wrong, fix it now or file a ticket.

**Delete comments like:**
```c
// This is a hack, but it works
// I know this is ugly but we're in a hurry
// FIXME: this whole function needs a rewrite
```

The FIXME without a ticket number is a prayer, not a plan.

---

## Comments Worth Writing

### The Why Comment

Explains a decision that isn't obvious from the code. Without
it, someone will "fix" correct code or repeat a mistake.

**Good:**
```c
// Sync twice: the third-party API sometimes drops the first
// ack. See #42.
sync(handle);
sync(handle);
```

```c
// Set property to nil before calling the handler to prevent
// reentrancy from triggering the callback again.
handler = self.completion_handler;
self.completion_handler = NULL;
handler();
```

### The Warning Comment

Prevents future breakage. Points out non-obvious coupling,
ordering constraints, or consequences.

**Good:**
```c
// Do not reorder: the database driver deadlocks if
// disconnect() runs before flush().
flush(conn);
disconnect(conn);
```

```c
// Intentional truncation to 32-bit for hash distribution.
// Do not "fix" to 64-bit.
hash &= hash;
```

### The Workaround Comment

Documents why code deviates from the obvious approach. Links
to the external cause so the workaround can be removed later.

**Good:**
```c
// Work around glibc bug #98765: sendmmsg returns EINVAL on
// msg_controllen > 4096 with kernel < 6.2.
if (controllen > 4096) {
    controllen = 4096;
}
```

### The Public API Doc Comment

Every exported function, type, and constant gets a doc comment.
Non-negotiable. The comment describes:

- What it does (one sentence).
- Parameters that aren't obvious from name + type.
- Return values, especially error conditions.
- Thread safety, if not obvious from context.
- Ownership or lifetime, where applicable.

**Good:**
```c
// Read up to `len` bytes from the file into `buf`. Returns
// the number of bytes read, or -1 on error with errno set.
// Returns 0 at end of file.
ssize_t file_read(file_t *f, void *buf, size_t len);
```

```go
// Lookup returns the data associated with key.
//
// This operation is not safe for concurrent use.
func (*Cache) Lookup(key string) (data []byte, ok bool)
```

A doc comment that merely restates the signature in English
fails this test. It must add something the signature alone
doesn't carry.

### Struct and Config Field Comments

Fields whose meaning or valid range isn't obvious from name +
type. Optional fields should state the default.

**Good:**
```go
type Options struct {
    // Points to the directory containing the manifest and
    // per-chapter text files.
    //   {BaseDir}/manifest.json
    //   {BaseDir}/{name}/{name}-part{number}.txt
    BaseDir string

    WelcomeMessage  string // shown at login
    ProtocolVersion string // checked against incoming requests
    PageLength      int    // lines per page; default: 20
}
```

### TODOs with a Trail

A TODO without a ticket reference is a wish. Attach a bug
number so it can be tracked, prioritized, and eventually
closed.

**Good:**
```c
// TODO: github.com/org/repo/issues/42 - Remove after the
// v3 migration window closes.
```

**Bad:**
```c
// TODO: clean this up later
// TODO(john): refactor
```

---

## Making Comments Unnecessary

These practices eliminate the need for most comments. Prefer
them over commenting.

### Intent-Revealing Names

```c
// Bad:
int d; // elapsed time in days

// Good:
int elapsed_days;
```

```c
// Bad:
setTimeout(blastOff, 86400000); // ms in a day

// Good:
const int MS_PER_DAY = 60 * 60 * 24 * 1000;
setTimeout(blastOff, MS_PER_DAY);
```

### Encapsulated Conditionals

Extract complex booleans into a named variable or function.
The name becomes the comment.

```c
// Bad:
if (u->age >= 18 && u->has_sub && !u->banned) { ... }

// Good:
bool eligible = is_adult(u) && has_active_plan(u)
                && !is_flagged(u);
if (eligible) { ... }
```

### Small Functions

If a function needs a paragraph of comments to walk through
its steps, it has too many steps. Split it into smaller
functions whose names are the explanation.

### Types Over Comments

An enum is better than a magic string with a comment. A
`struct meters` is better than `/* meters */ double`.

### Tests as Documentation

A well-named test case explains expected behavior more
reliably than any comment, and it breaks when the behavior
changes:

```c
void test_cell_select_wraps_column_major(void);
void test_config_rejects_unknown_modifier(void);
```

---

## LLM-Specific Habits

LLMs have distinctive commenting tics beyond the general
anti-patterns above. Watch for these when reviewing or
prompting.

### Echoing Every Block

After an if/else, loop, or function boundary, the LLM drops
a comment summarizing what the next block does — even when
the code is three lines long and self-evident. This doubles
the vertical footprint of simple code for no gain.

### Ceremonial Doc Comments

Generating a doc comment for every function regardless of
visibility or complexity. Internal helpers that are two lines
long don't need a `/** ... */` block restating their name.
Reserve doc comments for public APIs and non-trivial
internals.

### The Reassurance Comment

Comments that exist to make the code feel explained rather
than to convey information. They read like the LLM is
narrating its thought process.

**Delete comments like:**
```c
// Now we can safely proceed
// At this point, the connection is established
// Handle the result accordingly
```

### Counting Comments

Numbering the steps in a function: "Step 1: ...", "Step 2:
...", "Step 3: ...". If the function has enough steps to need
numbering, it has too many steps.

---

Remember: the goal isn't zero comments. It's zero *useless*
comments. Every comment in the codebase should tell you
something the code cannot.
