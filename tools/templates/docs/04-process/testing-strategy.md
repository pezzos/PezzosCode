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

Anti-hardcode rules
- Controlled randomization: seed randomness so tests are repeatable.
- Multiple fixtures: cover diverse inputs so fixed outputs fail.
- Invariants: assert general properties, not only exact values.
