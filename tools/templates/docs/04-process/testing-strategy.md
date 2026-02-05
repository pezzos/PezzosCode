# Testing Strategy

This document defines preferred test types and anti-hardcode rules.

Contract tests

- Assert request/response shapes, status codes, and error formats at boundaries.
- Pin behavior at integration points (APIs, services, adapters).

Fuzz/property tests

- Use controlled randomization (seeded) to explore edge cases.
- Encode invariants that must always hold, not just specific examples.

Golden tests

- Snapshot known-good outputs for stable formats (serializers, renderers).
- Update intentionally, with review, when outputs change.

Anti-hardcode requirements

- Multiple fixtures per key path (at least 2 distinct inputs for each critical endpoint/behavior).
- Deterministic randomness: seed randomization so tests are repeatable.
- Invariants over outputs: assert properties that must always hold, not only exact values.
- Contract tests at boundaries (requests/responses, status codes, error shapes).
- Avoid “golden-only” tests for behaviors that should generalize.

Enforcement in workflow

- The Preflight Report or TDD Plan must state fixture coverage (>=2 fixtures per critical path), seed strategy, and invariant checks.
- Work items are blocked until the Plan/TDD Plan includes those details and contract coverage at boundaries.
- Tests must include at least two fixtures per critical path and at least one invariant-based assertion.

Deterministic randomness

- Use a fixed seed in tests that use randomization.
- Log the seed when failures occur to allow replay.
