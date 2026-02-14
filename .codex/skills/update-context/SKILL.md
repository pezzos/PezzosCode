---
name: update-context
description: Update `docs/00-context/*` from a large project-description input plus an iterative Q&A loop. Use when the user runs `/update-context` with a very large project description (or asks to refresh context docs) and wants complete context files, either by filling template files or enriching already-populated files.
---

# Update Context

## Overview

Use this skill to transform a detailed project description into complete and consistent context docs under `docs/00-context/`.
Run a gap-driven question loop until required fields are complete, then update files with either template-fill or enrich-existing behavior.

## Inputs

1. Primary input:
   - `/update-context <very large project description>`
2. Follow-up input:
   - User answers to clarification questions.

## Files in Scope

Update only:

- `docs/00-context/vision.md`
- `docs/00-context/system-map.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/00-context/users.md`
- `docs/00-context/assumptions.md`
- `docs/00-context/expected-features.md`

Do not edit `docs/00-context/AGENTS.md` unless explicitly asked.

## Mode Detection (Template vs Enrich)

Detect mode before drafting content.

Run:

```bash
python3 .codex/skills/update-context/scripts/detect_context_mode.py --json
```

Interpretation:

- `template-fill`: file content matches its paired template in `tools/templates/docs/00-context/`.
- `enrich-existing`: file content differs from template and contains project-specific context.
- `mixed`: some files are template-fill and some are enrich-existing; apply mode per file.
- `unknown`: a required file pair is missing; ask the user before writing.

## Workflow

1. Read required context structure:
   - `docs/README.md`
   - `docs/00-context/AGENTS.md`
   - `docs/00-context/*.md` in scope
   - `tools/templates/docs/00-context/*.md` in scope

2. Parse the input description into normalized facts:
   - product purpose and problem
   - users/personas/journeys
   - scope boundaries and non-goals
   - architecture/components/deployment/ops
   - assumptions/risks/unknowns
   - expected features with owner/problem/outcome/priority

3. Run a completeness gap analysis using:
   - `references/context-file-checklist.md`

4. Ask targeted clarification questions in batches:
   - Ask only unresolved fields.
   - Group related fields to minimize back-and-forth.
   - Resolve contradictions explicitly (quote conflicting facts, then ask which is correct).
   - Continue asking until required checklist items are complete or explicitly marked "unknown by decision".

5. Draft updates with mode-specific behavior:
   - Template-fill mode:
     - keep template headings/order/structure.
     - replace placeholders with concrete project facts.
     - remove unresolved placeholders; never leave template TODO text.
   - Enrich-existing mode:
     - preserve valid existing project context.
     - merge new facts without rewriting sections unnecessarily.
     - update outdated statements only when user-provided input confirms the change.
     - keep historical notes only when still true; otherwise replace with current truth.

6. Run cross-file consistency checks:
   - personas in `users.md` align with `vision.md`.
   - boundaries/non-goals in `context-boundaries-operating-model.md` align with `vision.md` and `system-map.md`.
   - assumptions/risks/unknowns in `assumptions.md` align with architecture and workflow statements.
   - expected features map to the same product boundaries and user outcomes.

7. Apply the patch to the six in-scope files.

8. Report:
   - mode detection summary per file
   - questions asked and resolved
   - files updated
   - unresolved items (if any) explicitly flagged

## Questioning Rules

- Prefer specific, answerable questions over broad prompts.
- Use one canonical term for each concept (for example: "primary user", "non-goals", "deployment environment").
- If the user provides a partial answer, keep unresolved subfields in the next question batch.
- Stop asking only when all required fields are complete enough to write each file without invented details.
- If a detail remains unknown, write it explicitly as an open unknown/risk in `assumptions.md` instead of guessing.

## Quality Bar

- No leftover template placeholders.
- No contradictions across the six files.
- Content reflects user input and clarifications, not guessed facts.
- Diffs are focused and preserve existing valid context in enrich-existing mode.

## Commands

- Mode detection:

```bash
python3 .codex/skills/update-context/scripts/detect_context_mode.py --json
```

- Optional mode review with diff snippet:

```bash
python3 .codex/skills/update-context/scripts/detect_context_mode.py --show-diff --max-diff-lines 60
```

- Validate skill:

```bash
python3 /Users/alexandrepezzotta/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/update-context
```
