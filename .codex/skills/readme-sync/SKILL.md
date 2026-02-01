---
name: readme-sync
description: Read all non-template README.md files, reduce duplication, and update them to be concise and current.
---

# README Sync

Use this skill when README files drift out of date or repeat each other. The goal
is to keep information accurate and concise with minimal duplication.

## Scope (what to read)

1. All `README.md` files in the repo **except**:
   - Anything under `tools/templates/`
   - Anything under `examples/`

## Authoritative sources (for correctness)

- `docs/00-context/*` and `docs/03-logs/*` are the only sources of truth for
  README statements.
- Do **not** treat `docs/01-product/prd.md` as a source of truth. If a statement
  only appears in the PRD, replace it with a pointer to the relevant context or
  log instead.

## Audience rules

- Root `README.md` is for humans: keep it brief and friendly.
- All other `README.md` files are for AI: keep them compact and structured.

## Standard structure (with flexibility)

Use this order, but keep only sections that are relevant:

1. **Purpose**
2. **Quick Start** (root only; otherwise skip unless essential)
3. **Structure / Map** (AI: short list of pointers)
4. **Workflow** (only if there is a specific process to follow)
5. **Related Docs**

## Deduplication policy

- Prefer **summarizing overlapping sections** into a single concise statement.
- If multiple files repeat the same info, keep the most specific version and
  replace the others with a short pointer (1–2 lines).
- Keep a small “AI quick map” block when it materially helps navigation, even
  if that information appears elsewhere.

## Workflow

1. Enumerate README files in scope.
2. Read relevant context sources first:
   - `docs/00-context/` (vision, users, assumptions, system map, boundaries)
   - `docs/03-logs/` (implementation, decisions, bugs, validation, insights)
3. Read each README and note overlaps.
4. Decide a canonical location for repeated info.
5. Reconcile every factual statement against context/logs:
   - If supported, keep it concise.
   - If unsupported or only in PRD, replace with a short pointer.
6. Update each README to:
   - Match the standard structure
   - Remove duplication by summarizing or linking
   - Preserve essential info and any project-specific instructions
7. Keep edits concise; do not expand content beside explaining the params of a command or a script.
8. Use `tools/offload-proxy/pp` only for large-output reads (e.g., `rg`, `cat`);
   avoid it for filesystem writes like `mkdir`, `cp`, or `mv`.

## Output checklist

- All in-scope README files updated and concise.
- Overlaps reduced; canonical sources identified via short pointers.
- Root README remains human-friendly; others are AI-friendly.
