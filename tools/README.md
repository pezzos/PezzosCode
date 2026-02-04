# Tools

## Purpose

Small helper scripts for bootstrapping or operating this repo.

## Structure / Map

- `tools/bootstrap-into` - Copy docs, skills, tools, and rules into another repo.
- `tools/pc-feature` - Orchestrate the work item execution protocol with Codex.
- `tools/pc-commit` - Enforce allowed paths and standardized commit messages.

## Workflow

- Use `tools/bootstrap-into` when adopting the system into an existing project.
- Use `tools/pc-feature` when executing a work item end-to-end.
- Use `tools/pc-commit` before committing in this repo.

## AI Notes

- Treat this directory as the canonical place for repo automation.
- When updating a tool, verify any template counterparts in `tools/templates/` stay aligned.
- Scripted Codex runs should respect project profiles and repo-local `CODEX_HOME`.

## Related Docs

- `docs/04-process/ticket-execution-protocol.md`
- `AGENTS.md`
