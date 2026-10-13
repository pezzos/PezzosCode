# Docs

## Purpose

- Capture project context and execution memory for human + AI collaboration.
- Provide a simple, complete documentation system for autonomous orchestration.

## Structure

- `docs/AGENTS.md`: global documentation rules.
- `docs/00-context/`: product framing before implementation.
- `docs/01-product/`: formalized product bundle (`prd.md`, `design.md`, `ux-ui.md`,
  `security.md`, `visual-guidelines.md`, `brand-content.md`, `journey-messaging.md`,
  `infra-delivery.md`).
- `docs/02-work-items/`: orchestrator working memory.
- `docs/03-logs/`: accepted decisions and validation traces.
- `docs/04-process/`: orchestration rules and role playbooks. Includes
  `codex-runtime-maintenance.md` for global `~/.codex` runtime cleanup.

## Recommended flow

1. Start from `orchestrator-governance`.
1. Let the orchestrator run a quick context/product-doc drift pass and propose
   maintenance when needed.
1. Keep one canonical delivery phase (`POC`, `MVP`, or `custom`) documented in
   `docs/00-context/*`, `docs/01-product/prd.md`, and
   `.orchestrator/project-profile.json`.
1. Use `orchestrator-proposal-mode` for idea refinement, `orchestrator-investigate-mode`
   for diagnosis, or `orchestrator-plan-mode` for decision-complete planning.
1. Refresh context/product/root docs only when the orchestrator or maintainer has a
   concrete reason to do so.
1. Execute the approved plan through orchestrated delegation.
1. Update logs after acceptance (`docs/03-logs/*`).
1. Let the orchestrator append notable retrospective feedback into
   `.orchestrator/feedback/pending.json`; maintainers harvest that queue later from the
   skills repo rather than reopening old sessions.
1. Use `maintainer-feedback-to-backlog` when a maintainer should convert harvested
   feedback into prepared backlog tasks and acknowledge the converted digests in source
   repos.
1. Treat the richer `docs/01-product` bundle as a phased workflow:
   - deploy the managed bundle shape,
   - enrich the docs per repo with the right domain experts,
   - then run `docs-converge-implementation`, which applies the shared convergence
     contract so implementation gaps become backlog tasks instead of silent drift.

## Skills to know

Shared skills are provided globally from `~/.codex/skills`; this repository does not
need local copies of them.

- `orchestrator-governance`: default orchestration gateway, routing, guardrails, and
  lightweight doc-drift check.
- `orchestrator-proposal-mode`: idea refinement, specialist challenge, and
  recommendation before planning.
- `orchestrator-investigate-mode`: delegation-first diagnosis for long investigations.
- `orchestrator-plan-mode`: delegation-first planning entrypoint for orchestrator
  sessions.
- `orchestrator-execute-approved-plan`: approved-plan execution entrypoint.
- `maintainer-feedback-to-backlog`: maintainer sweep that harvests orchestrator
  feedback, creates prepared backlog tasks in `Skills-Lab`, and acknowledges the
  converted queue entries in source repos.
- `docs-refresh-context`: context refresh when explicitly requested or proposed by the
  orchestrator.
- `docs-build-definition`: product formalization when explicitly requested or proposed
  by the orchestrator and the source of the managed 8-file product bundle.
- `docs-review-product`: specialist review of product docs.
- `docs-converge-implementation`: read-only convergence pass that compares the enriched
  product bundle against implementation and emits prepared backlog work only when the
  shared convergence contract justifies it.
- `docs-sync-root-files`: root operational file realignment as targeted maintenance.
- `docs-reconcile-readmes`: README deduplication and cleanup as targeted maintenance.
- `docs-update-project-logs`: canonical project-memory update.
- `audit-suite`: generic audit entrypoint.
- `audit-ui`: UI and simplicity audit for a page, site, or element.
- `audit-user-flow`: targeted audit for login/signup/onboarding and similar flows.
- `audit-brand-coherence`: branding, wording, and tone coherence audit.
- `audit-user-journey`: global UX/content/tone/navigation journey audit.
- `audit-security`: security implementation audit.
- `audit-performance`: performance audit.
- `audit-seo`: SEO and content audit.

## Manual maintenance order

For a repo that was already bootstrapped and needs a clean refresh:

1. Re-seed with `repo-init-orchestrated`.
1. Refresh `docs/00-context` with `docs-refresh-context`.
1. Rebuild `docs/01-product` with `docs-build-definition`.
1. If the richer bundle is active for the repo, run the expert enrichment pass before
   treating the product docs as implementation-ready source of truth.
1. Run `docs-converge-implementation` when enriched product docs should now be checked
   against implementation and converted into bounded backlog work.
1. Realign root operational files with `docs-sync-root-files` if docs changed
   materially.
1. Optionally run `docs-review-product` when you want specialist challenge before
   planning.
1. Start orchestration from `orchestrator-governance`.

## Ownership model

- Context/product/work-items: human + orchestrator.
- Logs: orchestrator-owned after acceptance.
- Specialist profiles: invocable everywhere, but mapped by orchestrator to native Codex
  roles.
- Native roles: repo-local implementation/review outputs, not global log writing.
