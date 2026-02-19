# Feature Specification: Worktree policy + naming convention

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-06`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-02

### Summary

Use worktrees for parallel roles with a consistent naming convention.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Clean isolation for parallel roles
- **Current pain:** use worktrees for parallel roles is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** use worktrees for parallel roles

**So that** changes stay isolated

### User Value

- **Value proposition:** Clean isolation for parallel roles
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P1 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Define default worktree count (impl + review)
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Clean isolation for parallel roles

- [ ] **Requirement 2:** Standardize naming convention
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** Worktree already exists
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Branch name conflicts
  - **Expected behavior:** Fail safely and allow a clean retry

### User Experience Requirements

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

#### User Flow

```
CLI → Run command → Review output → Confirm next step
```

**Detailed Steps:**

1. User runs the relevant CLI command.
2. System executes the workflow step and logs output.
3. User reviews results and proceeds to the next gate.

#### Error Handling

| Scenario        | User Sees         | System Does    | Recovery Path        |
| --------------- | ----------------- | -------------- | -------------------- |
| Worktree exists | Use existing path | Skip creation  | Choose new name      |
| Branch conflict | Error message     | Abort creation | Create unique branch |

### Non-Functional Requirements

- **Performance:** CLI commands complete within reasonable local dev time
- **Scalability:** Single-user workflow; no multi-user scaling needed
- **Security:** Local-only operations, no remote data transfer
- **Compatibility:** macOS-first, CLI-only

## Acceptance Criteria

### Definition of Done

- [ ] All core functionality works as specified
- [ ] Edge cases are handled appropriately
- [ ] Error states are user-friendly
- [ ] Documentation is complete
- [ ] Tests are passing
- [ ] Code is reviewed and merged

### Test Scenarios

#### Happy Path

1. **Scenario:** Execute the primary CLI flow
   - **Given:** Repo and dependencies are present
   - **When:** The command is executed
   - **Then:** Output is correct and logs are updated

#### Unhappy Path

1. **Scenario:** Required precondition is missing
   - **Given:** A dependency or approval is missing
   - **When:** The command runs
   - **Then:** Execution stops with a clear error

### Success Metrics

| Metric                | Target   | How Measured                  |
| --------------------- | -------- | ----------------------------- |
| {feature['outcome']}  | Achieved | Logs and user confirmation    |
| Fewer workflow errors | Reduced  | Error summaries               |
| Token waste           | Lower    | Offload ids and prompt review |

## Scope

### In Scope

- Implement the feature as described in the PRD
- Update process docs and templates as needed

### Out of Scope

- UI/TUI interfaces
- Cloud services

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Risk of inconsistent adoption without clear documentation
- Risk of skipping gates under time pressure

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                      | Risk                                                                                                                                                                                                                            | Action                                                                                                                                                                                                                     |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-06-001 | High     | patcher | patch          | Yes      | Unsanitized worktree/branch input can enable command or ref-name injection | The spec requires a naming convention but does not define an allowed-character policy for feature/agent inputs used by CLI scripts. Without strict validation, crafted values can break shell safety or create unsafe git refs. | Enforce a strict allowlist (for example `^[a-z0-9-]+$`) for feature/agent tokens, reject anything else, and execute git commands with fully quoted arguments and `--` separators (no eval/string-built command execution). |
| SEC-06-002 | High     | patcher | patch          | Yes      | Worktree path traversal/symlink escape not fail-closed                     | The documented naming pattern `../<repo>-<feature>-<agent>` and cleanup behavior create a boundary risk if paths are reused or symlinked. Current docs only mention "worktree exists" handling, not canonical path enforcement. | Before create/reuse/remove, canonicalize paths, require they stay under the approved parent directory, reject symlinks, and verify target is a valid git worktree owned by this repo.                                      |
| SEC-06-003 | High     | patcher | patch          | Yes      | Manifest-driven auto-collection/cleanup lacks integrity validation         | Execution logs mention manifest tracking plus auto-collection/cleanup, but no control is specified to treat manifest content as untrusted. A tampered manifest could redirect cleanup/collection to unintended paths or refs.   | Parse manifest with strict schema, verify each entry against `git worktree list --porcelain`, ignore/reject out-of-policy entries, and store manifest with restrictive permissions.                                        |
| SEC-06-004 | Medium   | patcher | automated-test | Yes      | Security gate can fail open when CI/pre-commit errors occur                | WI-20260204-02 records `make ci` failure (PermissionError) during execution, showing a path where required validation can be incomplete. This weakens guardrails that should prevent unsafe completion.                         | Enforce fail-closed completion: block feature completion on any non-zero `make ci`/pre-commit result and require a clean rerun before completion status can advance.                                                       |
| SEC-06-005 | Medium   | patcher | automated-test | Yes      | Missing abuse-case tests for naming/conflict/symlink scenarios             | Current test scenarios cover happy path and a generic missing-precondition case, but do not validate malicious names, branch conflict abuse, symlinked existing worktrees, or manifest tampering.                               | Add negative tests that assert hard failure for invalid names, path escapes, symlink reuse, and manifest mismatch; make these tests mandatory in `make test`/`make ci`.                                                    |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                 | Risk                                                                                                                                                                                               | Action                                                                                                                                                                                   |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-06-001 | High     | patcher | patch            | Yes      | Acceptance criteria are not verifiable for end-user outcomes          | The spec still uses generic success language and a placeholder metric (`{feature['outcome']}`), so completion can be claimed without proving the user gets consistent worktree isolation behavior. | Define measurable acceptance checks for default worktree count, naming convention, branch names, and required CLI success/summary output so users can verify outcomes deterministically. |
| PROD-06-002 | High     | patcher | patch            | Yes      | Failure recovery UX is underspecified for real user retries           | Edge-case handling says 'Choose new name' but does not provide deterministic remediation steps or rerun guidance, which can leave users stuck or retrying unsafely.                                | Specify exact error text and immediate recovery actions for existing worktree, branch conflict, and missing preconditions, including explicit rerun-safety messaging.                    |
| PROD-06-003 | High     | patcher | automated-test   | Yes      | Validation gate behavior is ambiguous from a user perspective         | Execution logs show both passing and failing gate histories; without explicit fail-closed user-facing behavior, users may believe completion is allowed after failed checks.                       | Enforce and test fail-closed workflow status/output on any non-zero `make ci` or pre-commit result, aligned with SEC-06-004 and SEC-06-005.                                              |
| PROD-06-004 | Medium   | patcher | patch            | Yes      | Readiness signals are inconsistent across feature artifacts           | `dev-tasks.md` shows core tasks as Not Started while execution logs show implemented attempts and a placeholder WI entry, reducing PO confidence in workflow state.                                | Reconcile task status, remove unresolved placeholder WI entries from active tracking, and provide one authoritative readiness summary for feature review.                                |
| PROD-06-005 | Medium   | human   | human-validation | Yes      | Human usability sign-off is missing for CLI prompts and stage clarity | Automated tests alone cannot confirm that gate prompts, stage labels, and next-step instructions are clear for the Developer/PO user flow.                                                         | Require explicit human validation sign-off for prompt clarity, handoff/stage wording, and recovery instructions before feature completion.                                               |

<!-- review-findings:end -->
