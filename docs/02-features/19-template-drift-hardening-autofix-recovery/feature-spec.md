# Feature Specification: Template drift hardening + autofix recovery

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-19`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-11

### Summary

Harden the workflow when template files and living files diverge.
Precommit/CI autofix should detect drift, repair only scoped paths, restage allowed files, and fail closed when deterministic repair cannot be trusted.

## User Intent

### Who is this for?

- Primary: Developer/PO maintaining repos bootstrapped from templates.

### Why do they need it?

- Drift between template sources and living project files can repeatedly break precommit/CI and consume manual time.

### User Value

- Faster recovery from drift failures.
- Predictable, scoped autofix behavior.
- Reduced accidental modifications outside intended files.

## Feature Requirements

### Functional Requirements

- [ ] Detect template/living-file drift during precommit and CI autofix stages.
- [ ] Classify drift as safe-auto-fix vs manual-review-required.
- [ ] Apply deterministic scoped repairs for safe cases only.
- [ ] Re-stage only approved/scoped files after autofix.
- [ ] Fail closed with explicit remediation for unresolved or ambiguous drift.

### User Experience Requirements

#### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Non-Functional Requirements

- Drift checks must be deterministic and idempotent.
- Autofix must never silently modify out-of-scope files.
- Drift diagnostics must reference exact files and required actions.

## Acceptance Criteria

### Definition of Done

- Drift is detected before merge/commit gates.
- Safe one-sided drift repairs complete automatically with scoped restaging.
- Ambiguous/multi-sided drift fails with clear remediation steps.
- Behavior is validated in both precommit and CI paths.

### Test Scenarios

- One-sided drift auto-fixed and re-staged successfully.
- Bi-directional conflicting drift blocks with explicit diagnostics.
- Out-of-scope file modification attempt is detected and blocked.

### Success Metrics

- Reduced recurring precommit failures from template drift.
- Reduced manual intervention during drift-related CI failures.

## Scope

### In Scope

- Drift detection and classification.
- Scoped autofix + restage behavior.
- Failure diagnostics and guardrails.

### Out of Scope

- Automatic conflict resolution for semantic multi-file merge conflicts.
- Non-template content synchronization policies.

## Dependencies

### Requires

- `tools/pc-precommit`
- Unified autofix flow used by `make ci`
- Template sources under `tools/templates/`

### Blocks

- Reliable synthetic workflow smoke tests and predictable daily developer flow.

## Risks & Considerations

- Over-aggressive autofix can hide underlying design drift.
- Under-aggressive autofix can keep manual burden high.

## Open Questions

- Which drift categories should remain strictly manual even if a heuristic fix is possible?

## Related Documents

- PRD: `docs/01-product/prd.md`
- Output Offload: `docs/04-process/output-offload.md`
- Protocol: `docs/04-process/ticket-execution-protocol.md`

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
