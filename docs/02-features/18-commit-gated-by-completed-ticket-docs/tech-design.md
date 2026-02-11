# Technical Design: Commit gated by completed ticket docs

> **Architecture & implementation approach**

---

## Overview

**Feature:** Commit gated by completed ticket docs

**Status:** Draft

**Last Updated:** 2026-02-11

### Summary

Add a deterministic commit precheck to `tools/pc-feature` and/or `tools/pc-commit` that validates required ticket documentation before commit generation.
The design blocks incomplete work-item commits and emits actionable remediation details.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

## Technical Requirements

### From Feature Spec

- Enforce required execution-log sections before commit.
- Keep role-scope and ownership rules unchanged.
- Emit explicit fail reasons for missing evidence.

### Technical Constraints

- No interactive git console flows.
- Do not auto-fabricate tester/reporter evidence.
- Keep commit-step behavior deterministic across reruns.

## Architecture

### System Context

- Validation occurs at final commit gate.
- Inputs: `dev-tasks.md`, role logs, final report fields.
- Output: commit allowed/blocked decision with diagnostics.

### Component Design

- Required Section Extractor
  - Parses required markers from `dev-tasks.md` and role logs.
- Completeness Evaluator
  - Compares parsed state against required checklist.
- Gate Decision Emitter
  - Returns pass/fail and remediation guidance.

### Data Model

- `required_sections`: configured list of mandatory doc fields.
- `present_sections`: parsed map from runtime artifacts.
- `gate_result`: pass/fail + missing sections list.

## Integration Points

- `tools/pc-feature` final-gate flow
- `tools/pc-commit` validation entry point
- `docs/02-features/<feature>/dev-tasks.md`
- role logs and `logs/<WI>/...`

## Implementation Approach

### Phase 1: Parser and checklist model

- Define mandatory field list and parsing strategy.
- Add robust parser for current markdown layout.

### Phase 2: Gate enforcement

- Evaluate completeness at commit stage.
- Block commit on missing required sections.

### Phase 3: Diagnostics and regression coverage

- Emit deterministic remediation output.
- Add tests for complete/incomplete edge cases.

## Technical Decisions

### Decision 1: Hard block for missing required evidence

- Reason: partial commit records undermine trust.
- Outcome: commit denied until required sections are present.

### Decision 2: Keep schema markdown-based, no extra state store

- Reason: current workflow already treats docs as source of truth.
- Outcome: no new persistence dependency.

## Error Handling

- Parser cannot locate required sections: fail with path + section guidance.
- Conflicting status across files: fail closed, require human reconciliation.

## Testing Strategy

### Unit Tests

- Parser for required section extraction.
- Completeness evaluator with mixed states.

### Integration Tests

- Final gate blocks commits when sections are missing.
- Final gate passes with complete docs.

### E2E Tests

- Simulated full run from plan to commit with both fail/pass documentation states.

## Documentation Needs

- Update protocol wording for commit-gating checks if behavior changes.
- Record decision/implementation/validation entries in `docs/03-logs/*`.

## Related Documents

- Feature Spec: `docs/02-features/18-commit-gated-by-completed-ticket-docs/feature-spec.md`
- Dev Tasks: `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`
- Test Plan: `docs/02-features/18-commit-gated-by-completed-ticket-docs/test-plan.md`

## Change Log

| Date       | Version | Changes        | Author |
| ---------- | ------- | -------------- | ------ |
| 2026-02-11 | 0.1     | Initial design | Codex  |
