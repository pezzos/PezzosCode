---
name: review-product-docs-with-specialists
description: Review one or more docs/01-product documents with specialist logical profiles, aggregate findings, ask only the blocking questions, then auto-chain into build-prd-from-context for minimal-diff updates. Use when the user asks for expert review, completeness checks, or specialist feedback on PRD, UX/UI, design, security, or visual-guidelines docs.
---

# Review Product Docs With Specialists

Operate as orchestrator only.
Do not let specialist sessions edit `docs/01-product/*` directly in this workflow.

## Overview

Use this local skill to run a structured multi-specialist review over one or more documents in `docs/01-product/`, deduplicate findings, identify blocking questions, and prepare a bounded `specialist_review_bundle` for the local `build-prd-from-context` workflow.

Default outcome:
1. review docs,
2. summarize findings,
3. ask targeted questions,
4. after answers, auto-chain into `$build-prd-from-context` for minimal-diff updates.

## Input Contract

Required:
- Repository path (default current working directory).
- Target document (`prd.md`, `design.md`, `ux-ui.md`, `security.md`, `visual-guidelines.md`) or the full managed bundle.

Optional:
- Explicit specialist profiles requested by the user.
- Review depth: `standard` or `extended`.
- Intent keywords such as SEO, compliance, analytics, performance, content, or growth.

## Preflight

1. Run `python3 ../build-prd-from-context/scripts/discover_inputs.py --repo-root . --json` from the repository root, or the equivalent local path.
2. Stop with explicit failure if `docs/00-context` or `docs/04-process` is missing or empty.
3. Run `python3 scripts/resolve_review_panel.py --repo-root . --target <doc> --json` for the selected targets.
4. Use repo-local prompts from `prompts/specialists/` when present; otherwise fall back to bundled prompts in `assets/prompts/specialists/`.

## Standard Panels

- `prd.md` → `product-manager`, `dependency-planner`, `end-user-critic`
- `design.md` → `backend-architect`, `devops-automator`, `security-specialist`
- `ux-ui.md` → `ux-researcher`, `ui-designer`, `end-user-critic`, `accessibility-tester`
- `visual-guidelines.md` → `brand-guardian`, `ui-designer`, `visual-storyteller`, `accessibility-tester`
- `security.md` → `security-specialist`, `compliance-legal`, `backend-architect`

Automatic panel extensions:
- mention `SEO` → add `seo-specialist`
- mention `content`, `marketing`, or `growth` → add `content-strategist` or `growth-marketer`
- mention `analytics` or `metrics` → add `product-analyst`
- mention `performance` → add `performance-tester`
- mention `legal` or `compliance` → add `compliance-legal`

## Workflow

1. Discover managed docs and prerequisite inputs through `$build-prd-from-context` helpers.
2. Resolve the minimal or extended specialist panel for each target.
3. Launch one review job per `(document, profile)` pair.
4. Keep same-document multi-profile jobs sequential.
5. Ask specialists for findings, blind spots, completeness gaps, and bounded questions only.
6. Aggregate and deduplicate findings into one `specialist_review_bundle`.
7. Produce an orchestrator summary with severity, affected sections, and recommended next steps.
8. Ask only the blocking or high-impact questions.
9. Once the user answers, auto-chain into `$build-prd-from-context` with:
   - repository context,
   - process docs,
   - `specialist_review_bundle`,
   - `user_answer_bundle`.
10. In the update pass, require minimal diffs for existing files and template-fill only for missing files.

## Output Contract

Return, in order:
1. Review scope and panel used per document.
2. Aggregated findings grouped by document and severity.
3. Blind spots or missing evidence.
4. Questions for the user (blocking/high-impact only).
5. Auto-chain decision and expected `build-prd-from-context` inputs.

The intermediate bundle should follow the contract in `references/specialist-review-bundle.md`.

## Hard Rules

- Specialists do not edit `docs/01-product/*` directly in this skill.
- Do not rewrite documents inside the review phase.
- Preserve explicit user-requested profiles even if the minimal panel would otherwise be smaller.
- `compliance-legal` is advisory-only; always say it does not replace human legal validation.
- If no material gaps are found, report `NO_BLOCKING_FINDINGS` and skip the auto-update pass unless the user still wants one.

## Deterministic Helpers

- `python3 scripts/resolve_review_panel.py --repo-root . --target prd.md --json`
- `python3 scripts/resolve_review_panel.py --repo-root . --target ux-ui.md --intent "SEO and growth" --depth extended --json`
- Bundled fallback prompts live under `assets/prompts/specialists/`.
- See `references/panel-routing.md` and `references/specialist-review-bundle.md`.

## Validation

- `python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "$HOME/.codex/skills/review-product-docs-with-specialists"`
- `python3 scripts/resolve_review_panel.py --repo-root . --target prd.md --json`
