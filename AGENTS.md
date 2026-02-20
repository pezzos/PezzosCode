# AGENTS.md

This repository uses the documentation system in `docs/` as the primary source
of context for AI-assisted work. The source of truth is:

- `docs/README.md` for structure and usage
- `docs/00-context/` for product context and system map
- `docs/00-context/context-boundaries-operating-model.md` for scope boundaries, operating model, and MVP stop conditions
- `docs/01-product/` for requirements and success criteria
- `docs/02-features/` for feature-level specs, designs, tasks, and tests
- `docs/03-logs/` for decisions, implementation notes, bugs, and validation
- `docs/04-process/` for workflow and quality standards (work item execution must follow `docs/04-process/ticket-execution-protocol.md` and PO loop uses `docs/04-process/human-orchestration-workflow.md`)

Rules:

- Keep diffs small and focused.
- Perform a systematic review: list executed commands and summarize results.
- If context is missing or unclear, ask for the relevant document rather than
  guessing.
- For any work item implementation, run `make feature F=<feature-id>` and follow `docs/04-process/ticket-execution-protocol.md`.
- Run `make prepare-features` before generating/updating feature folders from the PRD.
- Run `make review-features` after generation and before first `make feature` for affected features.
- **Execution authority:** Only the human PO/user may run `make feature` or `pc-feature`. Codex is forbidden from invoking either command unless the user gives explicit approval in the current turn.
- Treat `make feature` as an orchestrator/bootstrap command, not a Planner plan step or test command.
- Enforce **Plan → Patch → Test → Report** for every work item.
- If HIGH RISK and approval is not granted, stop after Preflight and set status to "Awaiting PO Approval". If approval is granted, continue execution.
- Codex MUST use Serena for symbol-aware navigation and edits when available.
- Codex MUST use `tools/offload-proxy/pp` for commands that can produce large output (e.g., `rg`, `sed` on large ranges, tests, or logs).
- Do not paste large command outputs into prompts; use `pp` and share the pointer id.
- Do not use `tools/offload-proxy/pp` for filesystem write commands (e.g., `mkdir`, `cp`, `mv`, `rm`) to avoid unnecessary escalation.
- Codex MUST update `docs/03-logs/*.md` to record decisions, implementation changes, bugs, validations, and insights. If no log entry is needed, explicitly state why in the response.
- Orchestrator pattern: use separate sessions for roles when parallelizing; use a single feature worktree by default.
- Worktree naming: `../<repo_name>-<feature_name>-<agent_name>` (e.g., `../PezzosCode-auth-impl`).
- Role scope (single feature worktree):
- Planner writes only `docs/02-features/<feature>/planner-log.md`.
- Tester writes only `docs/02-features/<feature>/validation-log.md`.
- Reporter writes only `docs/02-features/<feature>/reporter-log.md`.
- Patcher edits implementation scope only and must not edit planner-owned `dev-tasks.md` or role-scoped logs (`planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`).
- Orchestrator uses a single worktree per feature and squashes role outputs into `main` (no `feature-worktrees.json`).

## Setup commands

- None defined. Ask if project-specific setup is required.

## Tests/Lint

- `make lint` to run pre-commit checks for tracked files.
- `make test` to run docs/skills checks and run Python unittest discovery only when a local `tests/` directory exists.
- `make ci` to run the full local CI gate (`lint` + `test`).

## DoD

- Follow `docs/04-process/definition-of-done.md`.

## Git conventions

- Use clear, scoped commit messages.
- Do not amend commits unless explicitly requested.
