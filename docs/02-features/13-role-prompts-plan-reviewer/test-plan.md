# Test Plan: Role prompts + Plan Reviewer

> **Validation strategy**

---

## Overview

**Feature:** Role prompts + Plan Reviewer

**Status:** Completed

**Last Updated:** 2026-02-09

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Test Strategy

- Validate prompt-loading behavior in `tools/pc-feature` (base + task variants).
- Validate plan-reviewer gate outcomes (APPROVE/BLOCK/CONFLICT) through `tests/test_pc_feature.py`.
- Validate process-doc references to role prompts and Plan Reviewer constraints.

## Planned Test Commands

- `python -m unittest discover -s tests -p "test_*.py"`
- `tools/offload-proxy/pp rg -n "load_prompt_template|plan-reviewer" tools/pc-feature tests/test_pc_feature.py`
- `tools/offload-proxy/pp rg -n "prompts/<role>|Plan Reviewer|Allowed Tests" docs/04-process`

## Acceptance Tests

- Prompt loading is file-based and covered by tests.
- Missing prompt files fail with clear errors.
- Plan Reviewer gate behavior is enforced before patching.
- Process docs and prompt files describe the same gate semantics.

## Approval

**Approved By:** TBD

**Date:** TBD

## Related Documents

- Feature Spec: `docs/02-features/13-role-prompts-plan-reviewer/feature-spec.md`
- Tech Design: `docs/02-features/13-role-prompts-plan-reviewer/tech-design.md`
- Dev Tasks: `docs/02-features/13-role-prompts-plan-reviewer/dev-tasks.md`
- Bug Log: `docs/03-logs/bug-log.md`

## Change Log

| Date       | Changes                                    | Author       |
| ---------- | ------------------------------------------ | ------------ |
| 2026-02-08 | Rebased tests for current prompt/gate flow | Codex        |
| 2026-02-05 | Initial test plan                          | Primary user |
