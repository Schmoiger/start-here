[ ] Check standards are DRY, do not include code samples, even no installation notes (tech-standards needs work)
[ ] Investigate Comprehensive Pre-Commit Validators: Upgrade british_english.py beyond a hardcoded list to comprehensive dictionary-based checks (e.g. pyspelling/Hunspell) and add pre-commit enforcement against forbidden toolchains.
[ ] Replace per-repo context in existing repositories (e.g. bollinger) with the canonical standards subrepo (`git subrepo clone git@github.com:Schmoiger/start-here.git context -b standards`).
[ ] Configure GitHub Actions secrets and variables in repository settings (`ANTHROPIC_API_KEY` in Secrets, `RUN_LLM_TESTS` in Variables) to support CI LLM consistency testing.
[ ] Framework has token bloat for simple tasks. Implement system 1 thinking (Jev) to pre-classify the work: use Jev to pick which workflow to follow. Add system one models to model LUT.
[ ] Add new workflow for trivial work, uses a general purpose agent. 
[ ] revise Persona to be formatted the same (as author.md)
[ ] Fully revise AGENTS.md (its generator) as it is currently a repeat of inventory of agents so not DRY. Instead it should list the base workflow e.g. system one, system two; workflow selection, if multi-agent.
[ ] Improve use of HANDOFF.md: orchestrator only maintains build/HANDOFF.md but agents maintain service-scoped HANDOFF.md. Should be described in multi-agent skill. How is HANDOFF.md different to the status payload the sub-agent returns to the orchestrator.
[ ] Analyise low level logs (see Openrouter or Langfuse) to optimise the context delivery (there's a lot going on, not all relevant).
[ ] TDD skill should enforce commit after each phase (not assuming this will be by the orchestrator)
[ ] Committing is token-intesive. Investigate and rationalise.
[ ] Do we need context/agents/cursor-workflow-helper.mdc? Is it created by the Cursor runtime projection? Check.

## Done

[x] Review folder structure in bollinger project and figure out which best practice to standardise in start-here project. For example: whether to use /build folder or /handoff.
[x] Review agents for DRY compliance. For example: @python-coder has assumptions on tech (Pytest) embedded whereas it should look at tech-standards.md
[x] Create agent that specifically looks at the effectiveness of other agents, i.e. efficient tokenomics.
[x] Update all start-here /context from bollinger /context
[x] When agents commit they should push as well (to protect from accidental deletion) - update agent-standards
[x] When an orchestrator spawns a sub-agent does it give the right context files (rules, standards)? They always seem to forget.
[WON'TDO] Keep both context and context-compressed folders - don't know which is more effective yet.
[x] Update the readme
[x] Adopt British English 'artefact' convention
[x] Workflow should have tasks.md for tracking
[x] Add persona (e.g. Dr. Sarah Chen from new-dev)
[x] Formalise the parallel workflow. Solution architect identifies 1) context domains and 2) dependencies between context domains (blocking points). Tasks are written as phases = work between blocking points. Each domain works in parallel up to those blocking points. Within each domain there might be further opportunities for parallel working. At blocking points tech-lead then solution-architect does quality verification. A diagram will help.
[x] We have security agent at the end. Better is to have LESS agents by-design = at QA points: architecture, tasks, blocking points. Bugs are added and fixed before proceeding.
[x] For full YOLO mode how can we have some bash commands authorised and not others? Need a risk rating surfaced with all human intervention requests.
[x] Add section in agent-standards on agent invocation because it's not in the expected .claude/agents way
[x] Merge ui-designer and visual-designer agents
[x] Add template for settings.local.json
[x] Investigate Option 2 (Failure-Mode Transparency / Fail-Fast Rule): Update agent-standards with an explicit invariant forbidding silent tool substitution when standard-mandated tools (e.g. uv, yarn dlx) fail.
[x] Remove `context/scripts/coordinate.sh` — superseded by YAML workflow definitions (`context/workflows/*.yaml`) and agent runtime orchestration.
[x] Fix `prepare-commit-msg` git hook and telemetry extraction via the runtime adapter layer (install hook symlink, support Claude Code, Antigravity, and Codex session telemetry per `context/models.yaml`).
[x] Make `Agent-Session` `model=` verifiable instead of agent-typed — commit a6d1f40 records `model=claude-sonnet-4.5` although that session ran on DeepSeek: the authoring agent substituted a default from repo precedent (`git log --all` shows 87 `Co-Authored-By: Claude Sonnet 4.5` trailers) because no runtime signal existed (`env` exposes only `CLINE_BUILD_ENV`/`CLINE_CONNECTOR_CLI_LAUNCH`/`CLINE_DESKTOP_CLI_PATH` etc., no model variable; `git config` has none). This violates `context/templates/commit-message-template.md:71` ("Do not substitute a default; use what was actually used") and line 83 ("Do not use a fixed co-author"), yet nothing catches it: `context/scripts/prepare-commit-msg.py:562-641` only injects/replaces `tokens=`, and `context/scripts/validators/workspace_conventions.py:87-95` accepts any `model=[a-z0-9.-]+` regardless of truth. Fix: populate `model=` and `tool=` in the hook from the same runtime extraction it already runs for tokens (Claude Code / Antigravity / Copilot / Codex / Cline), have the `commit-msg` validator reject a hand-written `model=` that runtime telemetry does not corroborate or cannot confirm, and state in `context/rules/workspace-conventions.md:43`, `context/skills/agent-workflows.md:24`, and `context/templates/commit-message-template.md:59-60` that both fields are hook-owned. Acceptance: a commit whose `model=` contradicts the runtime session fails `commit-msg`; hook-written `tool=`/`model=` match the runtime for at least Cline and Claude Code; `uv run pytest context/scripts/tests/` green.
[x] Extend harness to the Cline runtime (including adding generated files to gitignore, working out how to extract telemetry information)
[x] Rationalise the frontmatter context in the agents - not all are required.
[x] Fix the hard-coded `Co-Authored-By: Claude <noreply@anthropic.com>` trailer — agents write it literally (the one in 160f756 was chosen by hand) while `context/scripts/validators/workspace_conventions.py:77` only validates the shape `^Co-Authored-By: .+ <.+@.+\..+>$`. Derive it from git config or runtime identity instead of hardcoding it.