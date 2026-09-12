---
name: git-subrepo
description: Procedural instructions and operational guidance for managing canonical context and upstream/downstream synchronisation using git-subrepo.
globs: ["**/.gitrepo", "context/**"]
---

# Git Subrepo Skill

Manage external repositories nested within the codebase as standard files. Bypass native Git submodules complexity.

**Architecture**: Framework maintains canonical context in `agents-framework` (`main` branch). Downstream projects consume as subrepo under `context/`.

**Execution Environment (macOS Bash 4+)**:
Homebrew Bash 5+ is already installed at `/opt/homebrew/bin/bash` (Apple Silicon) or `/usr/local/bin/bash` (Intel). However, non-login agent subshells default to `/bin/bash` (macOS v3.2), which triggers `bashplus: The 'bashplus' library requires that 'Bash 4.0+' is installed... Try: 'brew install bash'`.
**DO NOT waste tokens probing for bash or running `brew install bash`.**
Always prepend Homebrew to `PATH` on every `git subrepo` command:
`PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo <subcommand>`

**Core Commands**:

- Clone: `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo clone <repository-url> <subdirectory> -b <branch>`
- Init (existing folder): `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo init <subdirectory> -r <repository-url> -b <branch>`
- Pull: `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo pull <subdirectory>` (requires clean working tree)
- Push: `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo push <subdirectory>` (requires clean working tree)
- Status: `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo status <subdirectory>`

**Invariants & Rules**:

1. **Tool Dependency**: `git-subrepo` is 3rd-party (`brew install git-subrepo`). Escalate if missing. Don't use native Git submodule commands.
2. **State Tracking**: NEVER hand-edit `.gitrepo`. It tracks URL, branch, last synced commit.
3. **Clean Working Tree Required**: `git status` must be clean before pull/push. (Use `git stash` if needed).
4. **History Handling**: Assume upstream commits are squashed.
5. **Prerequisites & PATH**: git 2.30+, bash 4.0+. Never attempt to reinstall bash if `bashplus` fails; always pass `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"`.

**Downstream Workflows**:

- Initial Adoption: `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo clone https://github.com/Schmoiger/agents-framework.git context -b main` -> `uv run python context/scripts/generators/generate_adapters.py` -> `uv run python context/scripts/validators/adapter_drift.py` -> commit.
- Pull Updates: Ensure clean -> `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo pull context` -> generate adapters -> validate drift -> commit.
- Push Improvements: Validate drift & tests -> `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo push context` -> Create PR in upstream.

**Upstream Workflows (`agents-framework`)**:

- Development: Work directly on `main` (or PRs) in `agents-framework`.
- Releases/Downstream: Changes are pulled by downstream projects via `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo pull context`.

**Troubleshooting**:

- *bashplus / Bash 4.0+ error*: Homebrew Bash is already installed. Do NOT run `brew install bash` or inspect paths. Prepend `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"` to the command.
- *Unstaged changes*: Stash, pull, pop.
- *Merge Conflict*: Resolve in editor, `git add`, `git commit -m "merge..."`, `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo clean context`.
- *Out-of-Sync/Corrupted*: `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo status context`, `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo pull context --force`.

