# Skills Guide

This repository uses a small set of bootstrap-local skills plus a larger catalog of global recommended skills.
Use `.orchestrator/profile-catalog.json`, `.orchestrator/native-role-manifest.json`, and `.codex/config.toml` for specialist routing.

## Shared rules

- Orchestrator owns decomposition, native-role routing, arbitration, and completion.
- Delegated roles return structured `coder_output_v1` JSON.
- Human approval is not required between routine orchestration steps.
- Human approval is required only for destructive/high-risk operations.
- Global logs (`docs/03-logs/*`) are orchestrator-owned after acceptance.
- Specialist routing is driven by `.orchestrator/profile-catalog.json`, `.orchestrator/native-role-manifest.json`, `.orchestrator/skills-catalog.json`, and `prompts/specialists/`.

## Bootstrap-local skills

- `orchestrator-governance`: local routing, ownership, and native-role selection.
- `orchestrator-agent-loop`: low-level native-role execution conventions.
- `review-product-docs-with-specialists`: local multi-specialist review panels for `docs/01-product`.
- `autofix-coder`: pre-commit fallback quality-fix role.
- `update-docs-lite`: bootstrap-local legacy shortcut for concise traceability updates.

## Global recommended skills

These are not duplicated as local wrappers; the orchestrator should call the canonical global skill when needed.

- `refresh-context-docs`: refresh `docs/00-context` with minimal diffs.
- `build-prd-from-context`: formalize or refresh `docs/01-product/*` from context/process docs.
- `execute-approved-plan-safely`: user-facing entrypoint once a plan is approved.
- `sync-root-files-from-docs`: realign root operational files after context/product changes.
- `reconcile-readmes`: deduplicate and normalize README files.
- `update-project-logs`: canonical project-memory and logs update skill.

See each skill folder `SKILL.md` for the exact workflow and constraints.
