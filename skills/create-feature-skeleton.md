Goal
Create a new feature folder with the standard docs template so implementation can start with clear context.

Inputs
- Feature name (kebab-case).
- Short feature summary.

Steps
1) Read `docs/README.md` and the feature template path.
2) Create `docs/02-features/<feature-name>/` from the template.
3) Fill in placeholders in `feature-spec.md`, `tech-design.md`, `dev-tasks.md`, and `test-plan.md` with the provided summary.
4) Note any missing context and ask for it.

Commands
- `mkdir -p docs/02-features/<feature-name>`
- `cp -R docs/02-features/feature-template/* docs/02-features/<feature-name>/`

Output
- A new feature folder with populated template docs.

DoD
- All four feature docs exist and have no TODO placeholders.
- Feature is discoverable from the docs structure.
