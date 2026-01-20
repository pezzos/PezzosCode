# AGENTS.md

Purpose of this folder:
- Organize feature-specific documentation.

Structure:
- Each feature should have its own folder under `docs/02-features/`.
- Use the templates in `docs/02-features/feature-template/` to create:
  - `feature-spec.md`
  - `tech-design.md`
  - `dev-tasks.md`
  - `test-plan.md`
- Feature tickets live at `docs/02-features/<feature>/ticket-TASK-XXX.md` and follow `docs/04-process/ticket-template.md`.

Selection rule for skills:
- Read `docs/01-product/prd.md` and relevant context to determine product surfaces (CLI/TUI/API/UI).
- Only uncomment and fill template sections that match those surfaces; keep others commented out.
- If a new surface is introduced later, uncomment and complete only the newly relevant blocks.
