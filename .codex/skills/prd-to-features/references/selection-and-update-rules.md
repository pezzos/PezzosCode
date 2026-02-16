# PRD-to-Features Rules

## Naming Convention

- Prefix feature folders with an ordered index that matches the PRD prioritized feature list.
- When `docs/02-features/feature-order.json` is present, use its ordered slug list as the primary index order source.
- Use two-digit padding: `01-<feature-name>`, `02-<feature-name>`, etc.

## Update-in-Place Rules

- Do not create duplicate feature folders.
- Do not overwrite an existing feature folder unless explicitly asked.
- If a folder exists, update only missing sections or leave it unchanged and report it.
- Hydration is mandatory by default: generated/updated feature docs must be adapted
  to the specific PRD feature (skeleton-only output is invalid).

## Incremental Mode (Default for Existing Projects)

- Read `docs/03-logs/implementation-log.md` and `docs/03-logs/decision-log.md`.
- Skip features marked completed, rejected, or deferred.
- Add only missing features not already present in `docs/02-features/`.

## Output Format

- List of feature folders created or updated (with index prefix).
- List of features skipped because they already exist.
- List of features skipped because completed/rejected/deferred (with evidence).
- Sections populated for each feature.
- Missing context/questions that block safe completion.

## Definition of Done

- Feature folders created only for missing P0/P1 items in the PRD.
- Folder order matches `feature-order.json` when present, otherwise PRD list order.
- Template sections match the chosen product surfaces.
- Hydrated content is feature-specific and removes unresolved template markers.
- No TODO placeholders remain unless blocked by missing PRD context.
- Skipped items are explicitly reported with reasons.
- Existing feature folders are never deleted.
- Features with `Status: Done` in `dev-tasks.md` are skipped.
