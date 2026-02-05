# Technical Design: Unified autofix for CI + precommit

> **Architecture & implementation approach**

---

## Overview

**Feature:** Unified autofix for CI + precommit

**Status:** Draft

**Last Updated:** 2026-02-05

### Summary

Refactor autofix steps into a single script and enforce precommit restaging with vanilla Codex config.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

- Script invoked by make and hooks
- Clear stdout messaging

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
