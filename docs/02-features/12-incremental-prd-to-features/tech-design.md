# Technical Design: Incremental prd-to-features

> **Architecture & implementation approach**

---

## Overview

**Feature:** Incremental prd-to-features

**Status:** Draft

**Last Updated:** 2026-02-05

### Summary

Update feature generation to be additive-only and skip Done features based on dev-tasks status.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Status detection
- Additive update

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
