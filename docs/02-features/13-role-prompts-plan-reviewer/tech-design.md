# Technical Design: Role prompts + Plan Reviewer

> **Architecture & implementation approach**

---

## Overview

**Feature:** Role prompts + Plan Reviewer

**Status:** Completed

**Last Updated:** 2026-02-09

### Summary

This design updates F-13 from “create prompts” to “stabilize prompt contracts.” The implementation aligns role prompts, task-specific prompt variants, and Plan Reviewer gate behavior with the live `pc-feature` workflow.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Prompt loading remains file-based (`prompts/*.md`) with task fallback.
- Prompt/template parity between root and `tools/templates/prompts/`.
- Plan Reviewer gate uses explicit context (preflight, allowed tests, policy basis).
- Tests cover prompt loading paths and plan-reviewer gate transitions.

## Architecture

### System Context

```text
Developer/PO -> make feature -> tools/pc-feature
                    |            |
                    |            +-> prompts/*.md
                    |            +-> tests/test_pc_feature.py
                    |
                    +-> docs/04-process/*.md
```

### Artifact Map

- Runtime prompts: `prompts/*.md`
- Template prompts: `tools/templates/prompts/*.md`
- Workflow engine: `tools/pc-feature`
- Gate tests: `tests/test_pc_feature.py`
- Process references: `docs/04-process/*.md`

### Data Model

No persistent datastore changes. Artifacts are markdown prompt files and workflow code/tests.

## Implementation Plan

1. Audit prompt files used by `tools/pc-feature` (role + task variants).
2. Reconcile root prompt files and template prompt files to the same contract.
3. Tighten Plan Reviewer gate wording where it conflicts with current risk-policy behavior.
4. Add/refresh workflow tests for prompt loading and reviewer gate outcomes.
5. Sync process docs if gate wording changed.

## Validation Strategy

- Unit/integration tests in `tests/test_pc_feature.py` must cover:
  - prompt lookup success/failure paths
  - plan-reviewer approve path
  - plan-reviewer block retry path
  - plan-reviewer policy conflict path
- Doc checks ensure process docs reference canonical prompt paths and role behavior.

## Documentation Needs

- [x] Process/doc updates
- [x] Implementation log entry
- [x] Validation log entry (if tests executed)
- [ ] API documentation
- [ ] User guide updates

## Related Documents

- Feature Spec: `docs/02-features/13-role-prompts-plan-reviewer/feature-spec.md`
- Dev Tasks: `docs/02-features/13-role-prompts-plan-reviewer/dev-tasks.md`
- Test Plan: `docs/02-features/13-role-prompts-plan-reviewer/test-plan.md`
- Ticket Protocol: `docs/04-process/ticket-execution-protocol.md`

## Change Log

| Date       | Version | Changes                              | Author       |
| ---------- | ------- | ------------------------------------ | ------------ |
| 2026-02-08 | 0.2     | Rebased design to current prompt set | Codex        |
| 2026-02-05 | 0.1     | Initial design                       | Primary user |
