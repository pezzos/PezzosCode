[![CI](https://github.com/pezzos/PezzosCode/actions/workflows/ci.yml/badge.svg)](https://github.com/pezzos/PezzosCode/actions/workflows/ci.yml)

# PezzosCode bootstrap

> A reusable starter kit for docs-first, AI-assisted development.

## Purpose

This repo provides:
- A structured documentation system in `docs/`.
- Reusable skills for Codex in `.codex/skills/`.
- Helper scripts in `tools/`.
- Ready-to-copy AI usage rules in `AGENTS.md`.

## Quick Start

1. Clone this repo (or use it as a GitHub template).
2. For an existing project, run:
   ```bash
   ./tools/bootstrap-into /path/to/your/project
   ```
3. Fill out core context:
   - `docs/00-context/vision.md`
   - `docs/00-context/system-map.md`
   - `docs/00-context/users.md`
   - `docs/00-context/assumptions.md`
   - `docs/00-context/context-boundaries-operating-model.md`
4. Define requirements in `docs/01-product/prd.md`.
5. Start your first feature from `docs/02-features/feature-template/`.

## Structure / Map

- `docs/` - Documentation system (see `docs/README.md`).
- `.codex/skills/` - Reusable Codex skills.
- `tools/` - Helper scripts (see `tools/README.md`).
- `AGENTS.md` - Repo-specific AI rules.

## Related Docs

- `docs/README.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/01-product/prd.md`
- `docs/04-process/definition-of-done.md`
- `docs/04-process/ticket-execution-protocol.md`
