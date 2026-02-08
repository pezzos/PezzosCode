# Technical Design: Feature gating + skill mining

> **Architecture & implementation approach**

---

## Overview

**Feature:** Feature gating + skill mining

**Status:** Draft

**Last Updated:** 2026-02-08

### Summary

Implement a soft precommit sequencing warning and a bounded skill-mining pipeline that proposes reusable skills from repeated workflow patterns.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Parse feature completion status from `docs/02-features/*/dev-tasks.md`.
- Emit non-blocking warnings in `tools/pc-precommit` when sequencing policy is violated.
- Mine repeated prompt/workflow patterns with threshold-based heuristics.
- Output proposals as human-reviewed artifacts (no auto-install).

## Architecture

### System Context

```text
git commit -> tools/pc-precommit
              |-> parse feature statuses -> soft warning
              |-> continue commit flow

periodic/manual miner -> prompts + logs + .offload
                       -> repeated pattern detector
                       -> skill proposal entries
```

### Data Model

Gating input:

- feature id (folder prefix)
- `Status:` line from each feature `dev-tasks.md`

Skill-mining candidate fields:

- pattern signature
- frequency/count
- evidence locations
- proposed skill name/description

## Implementation Plan

1. Add status parser helper for feature `dev-tasks.md` files.
2. Add non-blocking sequencing warning to precommit path.
3. Implement pattern-mining heuristics with minimum-frequency threshold.
4. Render candidate skill proposals in markdown format for PO review.
5. Add tests for parser correctness, warning behavior, and mining thresholds.

## Validation Strategy

- Parser tests for valid/malformed status lines.
- Precommit tests asserting warning text and non-blocking exit behavior.
- Mining tests confirming repeated patterns produce proposals while one-offs do not.

## Documentation Needs

- [x] Process/doc updates
- [x] Implementation log entry
- [x] Validation log entry (if tests executed)
- [ ] API documentation
- [ ] User guide updates

## Related Documents

- Feature Spec: `docs/02-features/16-feature-gating-and-skill-mining/feature-spec.md`
- Dev Tasks: `docs/02-features/16-feature-gating-and-skill-mining/dev-tasks.md`
- Test Plan: `docs/02-features/16-feature-gating-and-skill-mining/test-plan.md`
- Precommit Tooling: `tools/pc-precommit`

## Change Log

| Date       | Version | Changes                                        | Author       |
| ---------- | ------- | ---------------------------------------------- | ------------ |
| 2026-02-08 | 0.2     | Rebased design to explicit warning/mining flow | Codex        |
| 2026-02-05 | 0.1     | Initial design                                 | Primary user |
