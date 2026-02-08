# Test Plan: Feature gating + skill mining

> **Validation strategy**

---

## Overview

**Feature:** Feature gating + skill mining

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

- Validate feature status parsing and sequencing-warning logic in precommit.
- Validate warning remains advisory (non-blocking).
- Validate skill-mining thresholds and candidate output quality.

## Planned Test Commands

- `python -m unittest discover -s tests -p "test_*.py"`
- `tools/offload-proxy/pp rg -n "Status:|feature|warning|precommit" tools/pc-precommit tests docs/02-features`
- `tools/offload-proxy/pp rg -n "skill|pattern|proposal" tools tests docs/possible-improvements.md`

## Acceptance Tests

- Editing a later feature with earlier unfinished features emits a warning and still exits successfully.
- Warning message lists blocking earlier features and guidance.
- Repeated pattern fixtures generate candidate skill proposals; low-frequency noise does not.
- Proposals are written for human review and are not auto-installed.

## Approval

**Approved By:** TBD

**Date:** TBD

## Related Documents

- Feature Spec: `docs/02-features/16-feature-gating-and-skill-mining/feature-spec.md`
- Tech Design: `docs/02-features/16-feature-gating-and-skill-mining/tech-design.md`
- Dev Tasks: `docs/02-features/16-feature-gating-and-skill-mining/dev-tasks.md`
- Bug Log: `docs/03-logs/bug-log.md`

## Change Log

| Date       | Changes                                                  | Author       |
| ---------- | -------------------------------------------------------- | ------------ |
| 2026-02-08 | Rebased tests for soft gating and skill-mining proposals | Codex        |
| 2026-02-05 | Initial test plan                                        | Primary user |
