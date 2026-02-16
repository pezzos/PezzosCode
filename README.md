[![CI](https://github.com/pezzos/PezzosCode/actions/workflows/ci.yml/badge.svg)](https://github.com/pezzos/PezzosCode/actions/workflows/ci.yml)

# PezzosCode bootstrap

> Docs-first, AI-first starter kit for a single developer/PO workflow.

## Purpose

- Bootstrap a repo with the PezzosCode docs, tools, and skills.
- Keep execution predictable with a CLI-only operating model.
- Preserve traceability through context docs and chronological logs.

## Quick Start

1. Bootstrap into a target repo:
   ```bash
   ./tools/bootstrap-into /path/to/your/project
   ```
2. Fill core context in `docs/00-context/`.
3. Refresh global blueprints + feature generation with `make prepare-features`.
4. Run pre-execution findings pass with `make review-features`.
5. Execute work using the ticket protocol in `docs/04-process/ticket-execution-protocol.md`.

## Structure / Map

- `docs/` - Context, product, features, logs, and process docs.
- `tools/` - Workflow scripts (`bootstrap-into`, `pc-prepare-features`, `pc-review-features`, `pc-feature`, `pc-commit`, offload proxy).
- `.codex/skills/` - Reusable Codex skills.
- `AGENTS.md` - Repo execution rules for AI agents.

## Related Docs

- `docs/README.md`
- `docs/00-context/vision.md`
- `docs/00-context/system-map.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/04-process/ticket-execution-protocol.md`
