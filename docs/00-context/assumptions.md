# Assumptions, Risks & Unknowns

## Assumptions

<!-- Things we believe to be true but haven't validated -->

### User Assumptions
- [x] Primary user is a single developer/PO who wants to run the full workflow with Codex.
- [x] User wants to bootstrap projects quickly with minimal manual work beyond describing problems/features.
- [x] User will accept a simple, robust workflow over advanced customization.

### Technical Assumptions
- [x] macOS is the primary supported environment.
- [x] Git is available and integrated into the workflow.
- [x] Codex CLI is available and used as the primary AI executor.
- [x] Projects may use Python, TypeScript/Node, Rust, or Go depending on need.
- [x] Bootstrapping should work for new or existing repos in arbitrary directories.
- [x] Tooling must be idempotent and safe to re-run without corrupting state.

### Business Assumptions
- [x] The project is for personal use; no external market validation required.
- [x] Simplicity and robustness matter more than feature breadth.

## Risks

<!-- Potential issues that could impact success -->

### High Priority Risks
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Tooling is not idempotent and re-runs corrupt state or duplicate work | High | Medium | Enforce replace-in-place updates, skip completed work, add guardrails/tests |
| Template updates are hard to propagate to existing projects | High | Medium | Provide a bootstrap reapply path that is safe and skips unchanged files |
| AI workflow burns tokens on repeatable steps | High | Medium | Cache/skip steps where possible; keep prompts minimal and deterministic |
| Error handling is brittle and fails to recover | High | Medium | Fail fast with clear errors; allow reruns after fixes |

### Medium Priority Risks
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Codex CLI or dependencies are missing/misconfigured on a target machine | Med | Medium | Check dependencies early; provide actionable error messages |
| Workflow assumes a clean Git state and fails on unexpected changes | Med | Medium | Validate allowed paths and report unexpected diffs |
| Bootstrapping into existing repos introduces conflicts | Med | Medium | Prompt for overwrite/merge/skip and keep diffs small |

## Unknowns

<!-- Questions we need to answer -->

### Critical Unknowns
- None currently. Assume git, codex, and make are available on the primary user's machine.

### Important Unknowns
- None currently. HIGH-risk approvals are handled via a human prompt and can be recorded as `approval: "granted"` in ticket frontmatter.

## Validation Log

<!-- Track how we validate/invalidate assumptions -->

| Date | Assumption | Method | Result | Action Taken |
|------|------------|--------|--------|--------------|
| 2026-01-30 | Minimal dependency checks needed | User decision | Assume dependencies exist locally | Keep checks minimal |
| 2026-01-30 | Approval representation | User decision | Prompt + optional frontmatter flag | Use prompt and `approval: "granted"` |
