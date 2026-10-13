---
name: update-docs-lite
description: Bootstrap-local legacy shortcut for concise docs/03-logs traceability updates after orchestrator acceptance. Prefer the canonical global skill update-project-logs when it is available.
---

# Update Docs Lite

Use this only as a lightweight bootstrap-local fallback.
It is not the canonical log-update workflow.

## Trigger Phrases

- "mets juste les logs bootstrap à jour"
- "ajoute une trace concise dans docs/03-logs"
- "quick local log update"

## Do Not Use When

- The canonical global skill `update-project-logs` is available and can be used instead.
- Work is still being implemented and no accepted outcome exists yet.
- The request needs richer source evidence such as run JSON, review bundles, or validation summaries.

## Required updates

- `docs/03-logs/decision-log.md` for material decisions.
- `docs/03-logs/implementation-log.md` for meaningful code/tooling changes.
- `docs/03-logs/validation-log.md` for executed checks and outcomes.

## Constraints

- This skill is orchestrator-facing.
- Coder sessions should not call this skill during implementation.
- Keep entries concise, factual, and bounded.
- Prefer minimal diffs on existing logs.

## Style

- concise, factual, dated entries.
- include commands and high-signal results.
- avoid duplicating unchanged context.
- when the global skill is available, use it instead for canonical project memory.
