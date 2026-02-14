---
name: sync-root-from-context
description: Synchronize live root project files (AGENTS, Makefile, hooks, config) from docs/00-context and docs/01-product/prd.md while preserving repo-specific safety constraints. Use when context or PRD changes and root-level operational files need to be realigned.
---

# Sync Root Files From Context

Use this skill when the project context or PRD changes and the live root files
need to reflect the real project (not the generic templates).

## Inputs to read

1. `docs/00-context/` (vision, system map, users, assumptions, context boundaries)
2. `docs/01-product/prd.md`

## Detailed Checklist

Use `references/root-file-checklist.md` for the full per-file update and
validation checklist.

## Workflow

1. Read the context and PRD. Summarize the project purpose, scope, platforms,
   and key workflows in 5-10 bullets.
2. Update only the files listed in `references/root-file-checklist.md`.
3. If any file can’t be safely inferred from docs, ask a targeted question
   before editing.
4. Run the validation checks defined in `references/root-file-checklist.md`.
5. Keep diffs small and focused; do not change `tools/templates/root/*` here.

## Output checklist

See `references/root-file-checklist.md#output-checklist`.
