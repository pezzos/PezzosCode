# Technical Design: Simplify worktree tracking

> **Architecture & implementation approach**

---

## Overview

**Feature:** Simplify worktree tracking

**Status:** Draft

**Last Updated:** 2026-02-05

### Summary

Remove the tracking file requirement and simplify orchestrator behavior to a single worktree per feature.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Doc/template updates
- Tooling cleanup

## Architecture

### System Context

```
User/PO → CLI tools/scripts → Repo docs/logs
```

### Data Model

None beyond local repo files unless otherwise specified.

## Documentation Needs

- [x] Process/doc updates
- [ ] API documentation
- [ ] User guide updates
- [ ] Runbook for operations

## Related Documents

- Feature Spec: [link to feature-spec.md]
- Dev Tasks: [link to dev-tasks.md]
- Test Plan: [link to test-plan.md]
- System Map: [link to docs/00-context/system-map.md]

## Change Log

| Date       | Version | Changes        | Author       |
| ---------- | ------- | -------------- | ------------ |
| 2026-02-05 | 0.1     | Initial design | Primary user |
