# Cline + VS Code PowerShell — Observed Stall Patterns

> Summary of every terminal stall pattern observed running Cline (Claude Sonnet)
> in VS Code on Windows 10 with PowerShell 7. Intended for sharing with other
> Cline users running the same stack.
>
> All patterns share one root cause. Mitigations are at the bottom.

---

## Root Cause

VS Code injects invisible shell-integration escape sequences into the terminal
buffer to detect when a command finishes and to extract its exit code. Any
output that writes over or corrupts those sequences causes Cline to never
receive the "command finished" signal. The terminal appears hung even though
the underlying command completed successfully.

Three independent inputs corrupt the markers:

| Corruption source                     | Mechanism                                                                                                                                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **ANSI spinner / progress animation** | Carriage-return overwriting (`\r`) from animated progress bars rewrites the escape sequence mid-stream.                                                                                                                  |
| **Non-ASCII bytes in arguments**      | Characters outside 7-bit ASCII (em-dash, curly quotes, arrows, section sign) are re-encoded by PowerShell's argument parser before they reach git/gh, corrupting the byte sequence the marker detector expects.          |
| **PowerShell argument parser stall**  | Multi-line or binary-looking strings passed inline to a command cause PowerShell to interpret the argument as incomplete input and wait indefinitely for more -- the command never starts, so no marker is ever written. |

---

## Observed Stall Patterns

### Pattern 1 -- `npm test` / Vitest animated spinner

|                          |                                                                                                                                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Symptom**              | Command never returns; VS Code tab spins; `Ctrl+C` required to recover.                                                                                                                               |
| **Trigger**              | Running `npm test` or `npx vitest` without redirecting output.                                                                                                                                        |
| **Root cause**           | Vitest's animated progress spinner emits ANSI `\r` sequences that overwrite shell-integration markers.                                                                                                |
| **False success signal** | None -- the command genuinely hangs until killed.                                                                                                                                                     |
| **Mitigation**           | `$env:CI = '1'; npm test -- --run *> test-out.txt 2>&1; Write-Host "EXIT:$LASTEXITCODE"` then read the file. The `CI` flag switches Vitest to its non-animated reporter; `--run` prevents watch mode. |

---

### Pattern 2 -- `gh pr create` / `gh issue create` spinner + interactive prompt

|                          |                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **Symptom**              | Command stalls; if it does appear to complete, output is garbled.                                                   |
| **Trigger**              | Running `gh pr create` or `gh issue create` without `--no-browser` and without redirecting output.                  |
| **Root cause**           | `gh` shows an animated spinner and may prompt for browser confirmation; both corrupt markers.                       |
| **False success signal** | Sometimes the PR/issue IS created; only the result reporting breaks.                                                |
| **Mitigation**           | Always `--no-browser`; redirect all output: `gh pr create ... *> pr-out.txt 2>&1; Write-Host "EXIT:$LASTEXITCODE"`. |

---

### Pattern 3 -- `gh issue create` interactive mode

|                |                                                                                                                             |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Symptom**    | Terminal hangs waiting for input.                                                                                           |
| **Trigger**    | Using `gh issue create` (interactive by default on Windows).                                                                |
| **Root cause** | `gh issue create` opens an interactive editor/prompt even when all fields are supplied.                                     |
| **Mitigation** | Use `gh api repos/.../issues --method POST --field title="..." --field body=@body.md` instead. Never use `gh issue create`. |

---

### Pattern 4 -- Non-ASCII literal in `git commit -m "..."`

|                          |                                                                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Symptom**              | Command appears to stall or returns with a NativeCommandError; but git may have already committed successfully.             |
| **Trigger**              | Commit message contains an em-dash, curly quotes, arrows, or any non-ASCII glyph passed inline via `-m`.                    |
| **Root cause**           | Non-ASCII bytes corrupt VS Code shell-integration markers. The command succeeds but the result is never signalled.          |
| **False success signal** | YES -- the commit was created. `git log` will show it. Assuming failure here causes double-commits or wasted retries.       |
| **Mitigation**           | Write message to `git-msg.txt` (ASCII only), commit with `git --no-pager commit -F git-msg.txt`, then delete the temp file. |

---

### Pattern 5 -- Non-ASCII literal in any shell argument

|                |                                                                                                                                                                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Symptom**    | Command stalls silently; or completes but result is never signalled.                                                                                                                                                                              |
| **Trigger**    | Any shell command containing a non-ASCII character as a literal -- em-dash in a `gh` title, section sign in a `grep` pattern, curly quotes in a commit message, etc.                                                                              |
| **Root cause** | Same marker corruption as Pattern 4, applies to all commands not just git.                                                                                                                                                                        |
| **Mitigation** | Keep all shell arguments to plain 7-bit ASCII. Build glyphs via `[char]0x2014` (PowerShell) or `node -e "process.stdout.write('\u2014')"`. Use file-write tools for any file edits that need non-ASCII content -- never route them via the shell. |

---

### Pattern 6 -- `gh api --field body="multi-line"` PowerShell stall

|                          |                                                                                                                                   |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Symptom**              | Command never starts; terminal appears to wait for more input.                                                                    |
| **Trigger**              | Passing a multi-line string via `--field body="..."` inline in `gh api`.                                                          |
| **Root cause**           | PowerShell's argument parser sees the newline(s) as an incomplete here-string and waits for a closing delimiter that never comes. |
| **False success signal** | None -- the command never runs.                                                                                                   |
| **Mitigation**           | Write body to a file, use `--field body=@body.md`. The `@` prefix tells `gh api` to read from file.                               |

---

### Pattern 7 -- Piping streaming output through `Select-Object` / `Select-String`

|                |                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Symptom**    | Command stalls; terminal never returns control.                                                                               |
| **Trigger**    | `npm test -- --run 2>&1                                                                                                       | Select-Object -Last 30` or any pipe from a streaming/animated command. |
| **Root cause** | The pipe keeps the stream open; animated ANSI sequences pass through the filter into the terminal buffer, corrupting markers. |
| **Mitigation** | Never pipe from streaming commands. Redirect to file: `command *> out.txt 2>&1`, then read the file separately.               |

---

### Pattern 8 -- False failure assumption after a silent stall

|                |                                                                                                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Symptom**    | Cline reports a command as failed or missing; retries it; side-effects are duplicated (double commit, double issue).                                                              |
| **Trigger**    | Any of Patterns 1-7 above. The underlying command completed; only the result reporting broke.                                                                                     |
| **Root cause** | Cline infers failure from absence of a result signal. The inference is wrong when markers are corrupted.                                                                          |
| **Mitigation** | After any apparent stall: run `git log --oneline -3` / `git status` / `gh issue list` to verify true state before retrying. Treat absence of a result as "unknown", not "failed". |

---

## Mitigations Summary

| Action                    | Safe form                                                                           |
| ------------------------- | ----------------------------------------------------------------------------------- |
| `git commit`              | `git --no-pager commit -F git-msg.txt` (ASCII body); delete temp file after         |
| `git push`                | `git --no-pager push origin main 2>&1` (plain text stderr, no marker corruption)    |
| `npm test`                | `$env:CI = '1'; npm test -- --run *> out.txt 2>&1; Write-Host "EXIT:$LASTEXITCODE"` |
| `gh pr create`            | `gh pr create --no-browser --body-file body.md *> out.txt 2>&1`                     |
| `gh` issue/comment body   | `--field body=@body.md` (write to file first)                                       |
| `gh issue create`         | Do not use -- use `gh api ... --method POST` instead                                |
| Non-ASCII in args         | Use `[char]0x2014` / `node -e` with `\uXXXX` escapes; never paste glyphs            |
| File edits with non-ASCII | Use IDE/tool file-write APIs that bypass the terminal encoding layer                |
| Piped output              | Never pipe from streaming commands; redirect to file and read separately            |
| Apparent stall recovery   | `git log --oneline -3` / `git status` before assuming failure                       |

---

## What We Tried -- and What Worked

### The .clinerules problem

The natural first response to discovering these patterns is to write them down
as rules and load them into Cline's system prompt -- using a `.clinerules` file
(Cline's per-project custom instructions mechanism). We did this. It did not
reliably prevent violations.

The reason is structural. Cline reads `.clinerules` once at session start and
loads the text into its context window. By the time a commit or test command is
actually being constructed -- often after an extended implementation session --
that initial context may be many thousands of tokens deep in the past. The
model's attention weight on rules from early in the session diminishes
naturally. Rules written as passive prose ("MUST NOT use inline -m") compete
with the goal-directed momentum of the task. Under that momentum, the model
pattern-matches to the most natural-looking command form rather than recalling
a constraint read earlier.

Rephrasing, reordering, and highlighting the rules all made marginal
differences. The fundamental problem is that a static document read at session
start must remain retrievable and salient at the exact future moment a risky
command is being written -- which is exactly when the model is focused on
something else.

### What we tried next: git hooks as a re-injection mechanism

The idea was to use git hooks to get the rules back into context at the moment
of risk, rather than relying on memory. A `commit-msg` hook fires on every
`git commit`; its stdout lands in Cline's command result -- which is active
context at that exact moment. We committed a hook that printed the full
eight-point checklist on every commit, and a second hook that printed it again
on every push.

**What happened:** the commit+push chain stalled. The hooks fired correctly, but
printing a 20-line block of text on both commit and push meant two back-to-back
bursts of terminal output in a single command. That is more total output, which
is more shell-integration marker-corruption surface (same root cause as Pattern
7). The command succeeded -- `git log` confirmed it -- but result-reporting
broke anyway.

The checklist-printing was counterproductive. More hook output = more stall risk.

### What the hooks are now

After that finding we stripped the checklist from both hooks:

- **`commit-msg`** -- hard-rejects any commit whose message contains a non-ASCII
  byte. Outputs one short error line on rejection; completely silent on success.
  This is the one enforcement the hook can provide that does not add noise: it
  turns a silent stall (Pattern 4) into a loud, fixable error before the command
  even runs. **Tested:** commit with an em-dash in the message was rejected with
  exit code 1 and no stall (`COMMIT REJECTED: non-ASCII character on line 1`).
- **`pre-push`** -- silent pass-through, reserved for future rules.

The hooks are committed and wired via `git config core.hooksPath scripts/hooks`.

### What remains unsolved

The `.clinerules` approach fails on salience over a long session. The checklist-
printing hook approach failed by adding corruption surface. The hard-reject on
non-ASCII is the one demonstrably useful enforcement found so far.

Everything else in this doc is mitigation by convention -- patterns you have to
enforce through code review and prompt-engineering discipline, not through any
mechanism that fires automatically. That is the honest state of the problem.

The `.clinerules` file still has value for session orientation, but it cannot be
relied on as a sole enforcement mechanism for commands issued deep into a session.
