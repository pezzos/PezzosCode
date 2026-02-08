# Test Plan: Incremental prd-to-features

> **Validation strategy**

---

## Overview

**Feature:** Incremental prd-to-features

**Status:** Draft

**Last Updated:** 2026-02-08

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Test Strategy

- Validate create-missing behavior from PRD list.
- Validate done-feature skip logic from `dev-tasks.md` status.
- Validate no-duplicate/no-delete guarantees on reruns.
- Validate summary output contains explicit action reasons.

## Planned Test Commands

- `python -m unittest discover -s tests -p "test_*.py"`
- `tools/offload-proxy/pp rg -n "prd-to-features|incremental|Status: Done|never delete|missing only" .codex/skills/prd-to-features docs/04-process/human-orchestration-workflow.md docs/02-features/12-incremental-prd-to-features`
- `tools/offload-proxy/pp rg -n "12-incremental-prd-to-features" docs/03-logs`

## Acceptance Tests

- Existing feature folders remain untouched unless explicitly updated for missing sections.
- Features marked `Status: Done` are skipped.
- Missing PRD features are created once and not duplicated on rerun.
- No feature folder deletion occurs.

## Approval

**Approved By:** TBD

**Date:** TBD

## Related Documents

- Feature Spec: `docs/02-features/12-incremental-prd-to-features/feature-spec.md`
- Tech Design: `docs/02-features/12-incremental-prd-to-features/tech-design.md`
- Dev Tasks: `docs/02-features/12-incremental-prd-to-features/dev-tasks.md`
- Bug Log: `docs/03-logs/bug-log.md`

## Change Log

| Date       | Changes                                    | Author       |
| ---------- | ------------------------------------------ | ------------ |
| 2026-02-08 | Rebased tests to current incremental rules | Codex        |
| 2026-02-05 | Initial test plan                          | Primary user |
