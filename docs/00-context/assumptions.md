# Assumptions, Risks & Unknowns

## Assumptions

<!-- Things we believe to be true but haven't validated -->

### User Assumptions

- [x] Primary user is a single developer/PO who wants to run the full workflow with Codex.
- [x] User wants to bootstrap/update projects quickly with minimal manual work beyond describing intent.
- [x] User prefers one opinionated workflow for personal tools/habits over broad customization.
- [x] User expects AI/script automation to remove most deterministic manual fixups.

### Technical Assumptions

- [x] macOS is the primary supported environment.
- [x] Git is available and integrated into the workflow.
- [x] Codex CLI is available and used as the primary AI executor.
- [x] Projects may use Python, TypeScript/Node, Rust, or Go depending on need.
- [x] Bootstrapping should work for new or existing repos in arbitrary directories.
- [x] Tooling must be idempotent and safe to re-run without corrupting state.
- [x] Scripts can write structured logs under `logs/` and offload output under `.offload/`.
- [x] Deterministic steps can be delegated to scripts with a shared runner library.
- [x] Precommit/CI runs locally and can re-stage auto-fixed files.
- [x] Post-MVP hardening should prioritize lower token usage and fewer human prompts.
- [x] Unused skills/over-complex paths can be removed without reducing core workflow reliability.

### Business Assumptions

- [x] The project is for personal use; no external market validation required.
- [x] Simplicity and robustness matter more than feature breadth.
- [x] MVP baseline is already validated by successful use in other projects.

## Risks

<!-- Potential issues that could impact success -->

### High Priority Risks

| Risk                                                                  | Impact | Probability | Mitigation Strategy                                                         |
| --------------------------------------------------------------------- | ------ | ----------- | --------------------------------------------------------------------------- |
| Tooling is not idempotent and re-runs corrupt state or duplicate work | High   | Medium      | Enforce replace-in-place updates, skip completed work, add guardrails/tests |
| Template updates are hard to propagate to existing projects           | High   | Medium      | Provide a bootstrap reapply path that is safe and skips unchanged files     |
| AI workflow burns tokens on repeatable steps                          | High   | Medium      | Auto-fix deterministic steps; compact prompts/log output; enforce offload   |
| Error handling is brittle and fails to recover                        | High   | Medium      | Fail fast with clear errors; add deterministic recovery/retry paths         |
| Over-automation applies wrong fixes silently                          | High   | Medium      | Keep fail-closed checks and explicit HIGH-risk human gate                   |

### Medium Priority Risks

| Risk                                                                    | Impact | Probability | Mitigation Strategy                                           |
| ----------------------------------------------------------------------- | ------ | ----------- | ------------------------------------------------------------- |
| Codex CLI or dependencies are missing/misconfigured on a target machine | Med    | Medium      | Check dependencies early; provide actionable error messages   |
| Workflow assumes a clean Git state and fails on unexpected changes      | Med    | Medium      | Validate allowed paths and report unexpected diffs            |
| Bootstrapping into existing repos introduces conflicts                  | Med    | Medium      | Prompt for overwrite/merge/skip and keep diffs small          |
| Useful behavior is removed while pruning complexity                     | Med    | Medium      | Prune in small steps with regression checks and rollback path |

## Unknowns

<!-- Questions we need to answer -->

### Critical Unknowns

- None currently. Assume git, codex, and make are available on the primary user's machine.

### Important Unknowns

- Practical token budget targets per work item are not yet formalized.
- Minimum useful logging detail after compaction is not yet formalized.

## Validation Log

<!-- Track how we validate/invalidate assumptions -->

| Date       | Assumption                           | Method        | Result                                 | Action Taken                               |
| ---------- | ------------------------------------ | ------------- | -------------------------------------- | ------------------------------------------ |
| 2026-02-14 | MVP reached; post-MVP hardening only | User decision | Scope confirmed for optimization phase | Update context docs and feature priorities |
| 2026-01-30 | Minimal dependency checks needed     | User decision | Assume dependencies exist locally      | Keep checks minimal                        |
| 2026-01-30 | Approval representation              | User decision | Prompt + optional frontmatter flag     | Use prompt and `approval: "granted"`       |
