---
name: prd-to-features
description: Convert docs/01-product/prd.md into feature folders under docs/02-features using the template in docs/02-features/feature-template and the selection rules in docs/02-features/AGENTS.md. Use when a user wants to turn the PRD prioritized feature list into fully populated feature docs.
---

# PRD to Features

## Overview
Generate feature folders from the PRD and fill the feature template files, respecting product surface selection rules.

## Inputs
- `docs/01-product/prd.md`
- `docs/02-features/AGENTS.md`
- `docs/02-features/feature-template/`
- `docs/00-context/*.md` (optional, for additional context)

## Steps
1) Read `docs/02-features/AGENTS.md` and follow the selection rule for product surfaces.
2) Read `docs/01-product/prd.md` and extract the prioritized feature list and scope boundaries.
3) For each P0/P1 feature, create `docs/02-features/<feature-name>/` using the template files.
4) Fill `feature-spec.md`, `tech-design.md`, `dev-tasks.md`, and `test-plan.md` using PRD context.
5) Uncomment only the template sections that match the product surfaces; keep the rest commented.
6) If a feature cannot be fully specified from the PRD, list missing inputs and request clarification.

## Output Format
- List of feature folders created or updated.
- Sections populated for each feature.
- Missing context/questions.

## Commands
- `rg -n "Prioritized Feature List" docs/01-product/prd.md`
- `cat docs/01-product/prd.md`
- `cat docs/02-features/AGENTS.md`
- `cp -R docs/02-features/feature-template/* docs/02-features/<feature-name>/`

## DoD
- Feature folders created for each P0/P1 item in the PRD.
- Template sections match the chosen product surfaces.
- No TODO placeholders remain unless blocked by missing PRD context (must be called out).
