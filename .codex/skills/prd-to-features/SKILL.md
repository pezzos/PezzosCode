---
name: prd-to-features
description: Convert docs/01-product/prd.md into feature folders under docs/02-features using the template in docs/02-features/feature-template and the selection rules in docs/02-features/AGENTS.md. Use when a user wants to turn the PRD prioritized feature list into fully populated feature docs.
---

# PRD to Features

## Overview
Generate feature folders from the PRD and fill the feature template files, respecting product surface selection rules. Supports incremental mode to avoid duplicate features on existing projects.

## Inputs
- `docs/01-product/prd.md`
- `docs/02-features/AGENTS.md`
- `docs/02-features/feature-template/`
- `docs/00-context/*.md` (optional, for additional context)
- `docs/03-logs/implementation-log.md` (for completed items)
- `docs/03-logs/decision-log.md` (for rejected/deferred items)

## Naming Convention
- Prefix feature folders with an ordered index that matches the PRD prioritized feature list.
- Use two-digit padding: `01-<feature-name>`, `02-<feature-name>`, etc.

## Update-in-Place Rules
- Do not create duplicate feature folders.
- Do not overwrite an existing feature folder unless explicitly asked.
- If a folder exists, update only missing sections or leave it unchanged and report it.

## Incremental Mode (Default for Existing Projects)
- Read `docs/03-logs/implementation-log.md` and `docs/03-logs/decision-log.md`.
- Skip features that are marked completed, rejected, or deferred in logs.
- Add only missing features not already present in `docs/02-features/`.

## Steps
1) Read `docs/02-features/AGENTS.md` and follow the selection rule for product surfaces.
2) Read `docs/01-product/prd.md` and extract the prioritized feature list and scope boundaries.
3) In incremental mode, skip any feature already present in `docs/02-features/` or noted as completed/rejected/deferred in logs.
4) For each remaining P0/P1 feature, create `docs/02-features/<index>-<feature-name>/` using the template files.
5) Fill `feature-spec.md`, `tech-design.md`, `dev-tasks.md`, and `test-plan.md` using PRD context.
6) Uncomment only the template sections that match the product surfaces; keep the rest commented.
7) If a feature cannot be fully specified from the PRD, list missing inputs and request clarification.

## Output Format
- List of feature folders created or updated (with index prefix).
- List of features skipped because they already exist.
- List of features skipped because they are completed/rejected/deferred (with log reference).
- Sections populated for each feature.
- Missing context/questions.

## Commands
- `rg -n "Prioritized Feature List" docs/01-product/prd.md`
- `cat docs/01-product/prd.md`
- `cat docs/02-features/AGENTS.md`
- `cat docs/03-logs/implementation-log.md`
- `cat docs/03-logs/decision-log.md`
- `cp -R docs/02-features/feature-template/* docs/02-features/<index>-<feature-name>/`

## DoD
- Feature folders created only for missing P0/P1 items in the PRD.
- Folder order matches PRD list via numeric prefixes.
- Template sections match the chosen product surfaces.
- No TODO placeholders remain unless blocked by missing PRD context (must be called out).
- Skipped items are explicitly reported with reasons.
