# AGENTS.md

This repository uses the documentation system in `docs/` as the primary source
of context for AI-assisted work. The source of truth is:

- `docs/README.md` for structure and usage
- `docs/00-context/` for product context and system map
- `docs/00-context/context-boundaries-operating-model.md` for scope boundaries, operating model, and MVP stop conditions
- `docs/01-product/` for requirements and success criteria
- `docs/02-features/` for feature-level specs, designs, tasks, and tests
- `docs/03-logs/` for decisions, implementation notes, bugs, and validation
- `docs/04-process/` for workflow and quality standards (ticket implementation must follow `docs/04-process/ticket-execution-protocol.md` and PO loop uses `docs/04-process/human-orchestration-workflow.md`)

Rules:

- Keep diffs small and focused.
- Perform a systematic review: list executed commands and summarize results.
- If context is missing or unclear, ask for the relevant document rather than
  guessing.
- For any ticket implementation, run `make ticket T=<id> [F=<feature-id>]` to bootstrap and execute autonomously by default, and follow `docs/04-process/ticket-execution-protocol.md`.
- Manual mode: `make ticket MANUAL=1 T=<id> [F=<feature-id>]`.
- If HIGH RISK, stop after Preflight and set status to "Awaiting PO Approval".
- Codex MUST use Serena for symbol-aware navigation and edits when available.
- Codex MUST use `tools/offload-proxy/pp` for commands that can produce large output (e.g., `rg`, `sed` on large ranges, tests, or logs).
- Codex MUST update `docs/03-logs/*.md` to record decisions, implementation changes, bugs, validations, and insights. If no log entry is needed, explicitly state why in the response.

## Setup commands

- None defined. Ask if project-specific setup is required.

## Tests/Lint

- None defined. Ask which commands to run.

## DoD

- Follow `docs/04-process/definition-of-done.md`.

## Git conventions

- Use clear, scoped commit messages.
- Do not amend commits unless explicitly requested.
