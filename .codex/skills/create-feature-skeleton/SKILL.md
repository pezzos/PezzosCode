---
name: create-feature-skeleton
description: Create a new feature folder in docs/02-features from the feature template and populate it with a provided summary. Use when a user asks to start a new feature's docs or wants the feature template cloned and filled.
---

# Create Feature Skeleton

## Overview
Create a new feature folder from the template and fill in placeholders with the provided summary.

## Inputs
- Feature name (kebab-case).
- Short feature summary.

## Steps
1) Read `docs/README.md` to confirm the feature template location.
2) Copy `docs/02-features/feature-template/` to `docs/02-features/<feature-name>/`.
3) Replace TODO placeholders in `feature-spec.md`, `tech-design.md`, `dev-tasks.md`, and `test-plan.md` with the summary.
4) Ask for missing context when placeholders cannot be filled.

## Commands
- `mkdir -p docs/02-features/<feature-name>`
- `cp -R docs/02-features/feature-template/* docs/02-features/<feature-name>/`

## Output
- A new feature folder with populated template docs.

## DoD
- All four feature docs exist and contain no TODO placeholders.
- Feature is discoverable under `docs/02-features/`.
