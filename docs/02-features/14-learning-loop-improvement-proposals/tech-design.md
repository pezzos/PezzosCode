# Technical Design: Learning loop improvement proposals

> **Architecture & implementation approach**

---

## Overview

**Feature:** Learning loop improvement proposals

**Status:** Draft

**Last Updated:** 2026-02-08

### Summary

Implement deterministic proposal generation after failed/stalled workflow runs, writing structured entries to `docs/possible-improvements.md` without auto-applying fixes.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Consume workflow outcome + step context (`WI`, `agent`, `step`, failure summary).
- Render proposals using the existing markdown entry template in `docs/possible-improvements.md`.
- Enforce proposal deduplication by normalized failure signature.
- Keep proposal generation as a post-run side effect only when run outcome is fail/stall.

## Architecture

### System Context

```text
make feature -> tools/pc-feature -> execution outcome (pass/fail/stall)
                                 -> proposal generator (fail/stall only)
                                 -> docs/possible-improvements.md (append/update)
```

### Data Model

Proposal signature fields:

- `work_item_id`
- `agent_name`
- `step`
- `normalized_failure_summary`

Stored output is markdown entries (no new database).

## Implementation Plan

1. Define failure/stall trigger points in `tools/pc-feature` post-run flow.
2. Build proposal payload from available runtime metadata.
3. Implement markdown append/update helper for `docs/possible-improvements.md`.
4. Add signature-based dedup (skip or consolidate duplicates).
5. Add tests for generation, dedup, and no-op-on-success behavior.

## Validation Strategy

- Unit tests for signature normalization and dedup decisions.
- Integration-style tests for fail/stall run paths producing proposal entries.
- Guard test verifying successful runs do not create proposal entries.

## Documentation Needs

- [x] Process/doc updates
- [x] Implementation log entry
- [x] Validation log entry (if tests executed)
- [ ] API documentation
- [ ] User guide updates

## Related Documents

- Feature Spec: `docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md`
- Dev Tasks: `docs/02-features/14-learning-loop-improvement-proposals/dev-tasks.md`
- Test Plan: `docs/02-features/14-learning-loop-improvement-proposals/test-plan.md`
- Improvement registry: `docs/possible-improvements.md`

## Change Log

| Date       | Version | Changes                                             | Author       |
| ---------- | ------- | --------------------------------------------------- | ------------ |
| 2026-02-08 | 0.2     | Rebased design to explicit fail/stall proposal flow | Codex        |
| 2026-02-05 | 0.1     | Initial design                                      | Primary user |
