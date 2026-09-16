---
name: git-subrepo-operations
description: Procedural guidance and constraints for managing canonical context using git-subrepo
globs: ["**/.gitrepo", "context/**"]
---

# Git Subrepo Operations Skill

**Applies to**: Any modification, synchronisation, or operation involving `.gitrepo` tracked folders (e.g., `context/`).

---

## 1. Core Constraints

When operating on `.gitrepo` tracked directories, you **MUST NOT**:
- Use native Git submodule commands (e.g., `git submodule update`).
- Manually edit the `.gitrepo` state file (it tracks upstream URL, branch, and commit deterministically).

Instead, you **MUST** use the 3rd-party tool `git-subrepo`. Escalate to the user if it is missing (`brew install git-subrepo`).

---

## 2. macOS PATH Prepending Requirement

Non-login agent subshells default to `/bin/bash` (macOS v3.2), which triggers a bash version error because `git-subrepo` requires Bash 5+. Homebrew Bash 5+ is already installed.
- DO NOT probe for bash or run `brew install bash`.
- ALWAYS prepend the Homebrew binary path to `PATH` on every `git subrepo` command.

**Correct**:
`PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo <subcommand>`

**Incorrect**:
`git subrepo <subcommand>`

---

## 3. Push and Pull Workflow

**`git status` MUST be completely clean before any pull/push.**

If there are unstaged or uncommitted changes:
1. `git stash`
2. `PATH="..." git subrepo pull <dir>`
3. `git stash pop`

---

## 4. Banned Operations

| Action | Required | Forbidden |
|--------|----------|-----------|
| Pull updates | `PATH="..." git subrepo pull <dir>` | `git pull`, native `git submodule update` |
| Push updates | `PATH="..." git subrepo push <dir>` | `git push` directly in the subfolder |
| Troubleshoot bash error | Prepend `PATH="..."` | `brew install bash` (already installed) |
| Fix unstaged changes | Stash, pull, pop | Hand-editing `.gitrepo` or ignoring |
