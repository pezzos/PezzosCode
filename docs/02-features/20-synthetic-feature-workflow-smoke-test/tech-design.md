# Technical Design: Synthetic feature workflow smoke test

> **Architecture & implementation approach**

---

## Overview

**Feature:** Synthetic feature workflow smoke test

**Status:** Draft

**Last Updated:** 2026-02-11

### Summary

Design a deterministic synthetic workflow fixture and runner assertions to validate orchestration behavior end-to-end.
The smoke test targets workflow mechanics (routing, gates, logging, resume), not product-specific feature logic.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

## Technical Requirements

### From Feature Spec

- Provide synthetic fixture + invocation path.
- Assert core workflow invariants across role loop and final gates.
- Emit concise stage-level diagnostics.

### Technical Constraints

- Keep test runtime bounded and deterministic.
- Avoid dependence on external services.
- Prevent synthetic artifacts from polluting real feature state.

## Architecture

### System Context

- Entry trigger: explicit smoke-test command/path.
- Fixture: minimal synthetic feature docs/tasks with known expected outcomes.
- Validator: inspects logs/artifacts and evaluates invariant checklist.

### Component Design

- Synthetic Fixture Builder
  - Creates or references a stable fake feature input set.
- Workflow Runner Adapter
  - Invokes standard execution path on synthetic fixture.
- Invariant Evaluator
  - Checks role routing, Allowed Tests policy, resume behavior, and log presence.
- Result Reporter
  - Produces concise pass/fail summary with offload/log pointers.

### Data Model

- `smoke_case`: scenario id, setup, expected stage outcomes
- `smoke_result`: pass/fail, failed stage, evidence references
- `invariant_report`: checklist by gate and role step

## Integration Points

- `tools/pc-feature` runtime path
- `tests/` for automated smoke assertions
- `logs/<WI>/...` artifacts for evidence

## Implementation Approach

### Phase 1: Fixture definition and baseline scenario

- Create minimal synthetic feature with deterministic expected path.
- Add baseline success scenario.

### Phase 2: Invariant evaluation and failure scenarios

- Add stage-level assertions and targeted failure injections.
- Validate diagnostics quality.

### Phase 3: Runner/documentation integration

- Wire smoke test invocation into developer workflow.
- Document when/how to run and interpret failures.

## Technical Decisions

### Decision 1: Reuse real workflow engine with synthetic inputs

- Reason: validates true orchestration path instead of a mocked approximation.
- Outcome: stronger signal for workflow regressions.

### Decision 2: Keep smoke assertions invariant-focused

- Reason: avoid brittleness from unrelated implementation details.
- Outcome: stable, high-value early warning test.

## Error Handling

- Fixture setup failure: fail fast with fixture remediation details.
- Missing expected logs: fail with missing-path diagnostics.
- Unexpected stage routing: fail and provide observed vs expected route.

## Testing Strategy

### Unit Tests

- Invariant evaluator behavior for pass/fail permutations.

### Integration Tests

- Synthetic run baseline pass.
- Synthetic run with injected gate violation.

### E2E Tests

- Full synthetic workflow run from initialization through final gate.

## Documentation Needs

- Add smoke-test run instructions to process docs.
- Record implementation + validation outcomes in `docs/03-logs/*`.

## Related Documents

- Feature Spec: `docs/02-features/20-synthetic-feature-workflow-smoke-test/feature-spec.md`
- Dev Tasks: `docs/02-features/20-synthetic-feature-workflow-smoke-test/dev-tasks.md`
- Test Plan: `docs/02-features/20-synthetic-feature-workflow-smoke-test/test-plan.md`

## Change Log

| Date       | Version | Changes        | Author |
| ---------- | ------- | -------------- | ------ |
| 2026-02-11 | 0.1     | Initial design | Codex  |
