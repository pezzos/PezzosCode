---
name: context-to-product
description: Reflect docs/00-context and docs/04-process into docs/01-product/prd.md by extracting user, vision, system, and assumptions context and ensuring the PRD template is filled consistently. Use when a user wants to turn context docs into a complete PRD or validate that PRD mirrors the context.
---

# Context to Product

## Overview

Turn the context docs into a complete and consistent PRD by extracting key inputs and filling the PRD template.

## Inputs

- `docs/00-context/vision.md`
- `docs/00-context/users.md`
- `docs/00-context/system-map.md`
- `docs/00-context/assumptions.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/definition-of-done.md`
- `docs/04-process/testing-strategy.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/output-offload.md`
- `docs/04-process/git-workflow.md`

## Steps

1. Read all `docs/00-context/*.md` files and summarize the product intent, users, constraints, and risks.
2. Read `docs/04-process/*.md` and extract workflow requirements (gates, DoD, testing strategy, output offload, git workflow, orchestration).
3. Open `docs/01-product/prd.md` and map context + process requirements to each PRD section (problem statement, users, scope, success metrics, non-goals, prioritized feature list, operational requirements).
4. Fill or update the PRD template with concrete statements derived from context and process docs.
5. If the PRD lacks a section for workflow/process requirements, add one and tie it to success criteria.
6. If any required PRD section cannot be filled, list the gaps and ask for missing details.
7. Keep PRD content aligned with the terminology used in the context and process docs.

## Output Format

- Brief summary of how context mapped into the PRD.
- List of sections updated.
- Open questions or missing context.

## Commands

- `tools/offload-proxy/pp rg --files docs/00-context docs/04-process`
- `tools/offload-proxy/pp sed -n '1,200p' docs/00-context/*.md`
- `tools/offload-proxy/pp sed -n '1,200p' docs/04-process/*.md`
- `tools/offload-proxy/pp sed -n '1,200p' docs/01-product/prd.md`

## DoD

- PRD reflects all relevant context (users, problem, scope, constraints).
- PRD includes workflow/process requirements derived from `docs/04-process/`.
- Success metrics, non-goals, scope boundaries, and prioritized feature list are present and consistent.
- Gaps are called out explicitly.
