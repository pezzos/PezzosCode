---
name: prd-to-features
description: Convert docs/01-product/prd.md prioritized features into numbered folders under docs/02-features using template and selection rules, with incremental skip logic for completed or existing work. Use when the user asks to generate feature docs from the PRD or backfill missing feature folders.
---

# PRD to Features

## Overview

Generate feature folders from the PRD and fill template files while preserving
incremental safety (no duplicate creation or destructive overwrite).

## Inputs

- `docs/01-product/prd.md`
- `docs/02-features/AGENTS.md`
- `docs/02-features/feature-template/`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`

## Detailed Rules

Read `references/selection-and-update-rules.md` for naming, incremental mode,
skip logic, output contract, and full DoD requirements.

## Steps

1. Read `docs/02-features/AGENTS.md` and follow the selection rule for product surfaces.
2. Read `docs/01-product/prd.md` and extract the prioritized feature list and scope boundaries.
3. Run the planning helper to preview folder mapping before writes.
4. Execute creation/update with `tools/prd-to-features`.
5. Verify that output respects incremental rules from `references/selection-and-update-rules.md`.
6. If a feature cannot be specified safely, stop and request missing context.

## Deterministic Helpers

- Preview (read-only):
  - `python3 .codex/skills/prd-to-features/scripts/plan_feature_folders.py --json`
- Execute:
  - `tools/prd-to-features`

## Commands

- `python3 .codex/skills/prd-to-features/scripts/plan_feature_folders.py --json`
- `tools/prd-to-features`

## DoD

See `references/selection-and-update-rules.md#definition-of-done`.
