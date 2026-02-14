# README Sync Rules

## Scope

Read all `README.md` files in the repo except:

- `tools/templates/**`
- `examples/**`

## Sources of Truth

- Treat `docs/00-context/*` and `docs/03-logs/*` as authoritative.
- Do not treat `docs/01-product/prd.md` as a source of truth for README facts.
- If a statement exists only in PRD, replace it with a pointer to context/log docs.

## Audience Rules

- Root `README.md` is for humans: brief and friendly.
- Other README files are for AI: compact and structured.

## Preferred Section Order

Keep only relevant sections in this order:

1. Purpose
2. Quick Start (root only unless essential elsewhere)
3. Structure / Map
4. Workflow
5. Related Docs

## Deduplication Policy

- Summarize overlap instead of copying large repeated sections.
- Keep the most specific canonical version and replace duplicates with short pointers.
- Keep a small AI quick-map block only when it materially improves navigation.

## Output Checklist

- In-scope READMEs are concise and current.
- Overlap is reduced with explicit canonical pointers.
- Root README remains human-friendly; other READMEs remain AI-friendly.
