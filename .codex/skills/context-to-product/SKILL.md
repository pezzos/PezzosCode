---
name: context-to-product
description: Reflect docs/00-context into docs/01-product/prd.md by extracting user, vision, system, and assumptions context and ensuring the PRD template is filled consistently. Use when a user wants to turn context docs into a complete PRD or validate that PRD mirrors the context.
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

## Steps
1) Read all `docs/00-context/*.md` files and summarize the product intent, users, constraints, and risks.
2) Open `docs/01-product/prd.md` and map context to each PRD section (problem statement, users, scope, success metrics, non-goals, prioritized feature list).
3) Fill or update the PRD template with concrete statements derived from context.
4) If any required PRD section cannot be filled from context, list the gaps and ask for missing details.
5) Keep PRD content aligned with the terminology used in the context docs.

## Output Format
- Brief summary of how context mapped into the PRD.
- List of sections updated.
- Open questions or missing context.

## Commands
- `rg --files docs/00-context`
- `cat docs/00-context/*.md`
- `cat docs/01-product/prd.md`

## DoD
- PRD reflects all relevant context (users, problem, scope, constraints).
- Success metrics, non-goals, scope boundaries, and prioritized feature list are present and consistent.
- Gaps are called out explicitly.
