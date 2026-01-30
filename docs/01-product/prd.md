# Product Requirements Document (PRD)

> **Single source of truth for WHAT the product must do**

---

## Overview

**Product Name:** PezzosCode

**Version:** 0.1

**Last Updated:** 2026-01-30

**Status:** Draft

### Executive Summary
<!-- 2-3 sentences describing what this product/feature does and why it matters -->

PezzosCode bootstraps a new project with a standardized, AI-first workflow and tooling.
It enables a single developer/PO to describe features and let AI execute tickets with minimal manual setup.
The focus is simplicity, robustness, and idempotent re-runs.

## Problem Statement

### User Pain Points
1. **Bootstrapping AI-first projects is manual and inconsistent**
   - Who experiences it: single developer/PO.
   - Current workaround: manual setup and ad-hoc templates.
   - Impact: wasted time, inconsistent process, broken AI workflows.

2. **AI workflows break on small issues**
   - Who experiences it: single developer/PO.
   - Current workaround: manual fixes and repeated setup.
   - Impact: token waste, loss of momentum, unreliable execution.

### Success Criteria
<!-- How we'll know if we've solved the problem -->

| Metric | Current | Target | Measure |
|--------|---------|--------|---------|
| Bootstrap in one command | Manual setup | One command | Manual verification |
| Ticket execution reliability | Inconsistent | Minimal failures | Worklog + user confirmation |

### Success Metrics (Template)
<!-- List the specific, trackable outcomes that define success -->
- **Bootstrap time:** baseline manual, target one command, timeframe immediate, data source user confirmation.
- **Ticket execution success rate:** baseline inconsistent, target reliable for approved tickets, data source worklogs.
- **Idempotent reruns:** baseline manual recovery, target safe rerun without duplication, data source worklogs.

## Users & Use Cases

### Target Users

**Primary Persona: Developer/PO (single user)**
- **Who they are:** Entrepreneur building multiple projects with Codex as the executor.
- **Goals:** Bootstrap projects fast; describe features and let AI implement.
- **Frustrations:** Manual setup, workflow breaks, inconsistent process adherence.
- **Technical level:** Intermediate to advanced (workflow should still be simple).

**Secondary Persona:** None (single-user focus).

### Core Use Cases

#### Use Case 1: Bootstrap a project
**Actor:** Developer/PO

**Preconditions:** Target repo exists (new or existing).

**Main Flow:**
1. User runs bootstrap command.
2. System copies templates/tools into target repo.
3. User begins filling context docs.

**Postconditions:** Repo is ready for PezzosCode workflow.

**Alternative Flows:**
- **Alt 1:** Existing files conflict; user chooses overwrite/merge/skip.

#### Use Case 2: Execute approved tickets
**Actor:** Developer/PO

**Preconditions:** Context, PRD, features, and tickets are defined.

**Main Flow:**
1. User runs ticket execution command.
2. System generates preflight, runs TDD, implements, and logs results.
3. User approves gates when required.

**Postconditions:** Ticket is implemented and documented.

## Prioritized Feature List (Template)
<!-- Ordered list of features tied to the PRD scope -->
| Priority | Feature | Outcome | Notes |
|----------|---------|---------|-------|
| P0 | Bootstrap templates into a repo | Project is ready for AI workflow | Idempotency required |
| P0 | Execute ticket workflow | AI can implement approved tasks reliably | Requires Codex CLI |
| P1 | Update/reapply templates | Existing repos stay in sync | Avoid conflicts |
| P2 | Optional CLI/TUI wrapper | Faster iteration for user | Separate project if UI |

## Requirements

### Functional Requirements

#### Must Have (P0)
- [ ] **FR-001:** Bootstrap a project with PezzosCode templates in one command.
  - **Rationale:** Eliminates manual setup and inconsistency.
  - **Acceptance Criteria:** Templates, tools, and docs are copied into a target repo.

- [ ] **FR-002:** Execute a ticket end-to-end with AI and minimal manual work.
  - **Rationale:** Primary user goal is AI execution with minimal intervention.
  - **Acceptance Criteria:** Preflight → tests → implementation → logs → gates.

#### Should Have (P1)
- [ ] **FR-101:** Reapply templates to existing repos safely.
  - **Rationale:** Enables template evolution without losing local edits.
  - **Acceptance Criteria:** Conflicts handled by overwrite/merge/skip; idempotent reruns.

#### Nice to Have (P2)
- [ ] **FR-201:** Single command to loop over approved features/tickets.
  - **Rationale:** Reduce manual step orchestration.
  - **Acceptance Criteria:** CLI can run the standard loop with user approvals.

### Non-Functional Requirements

#### Performance
- [ ] **NFR-001:** Commands should complete promptly for small/medium repos.
  - **Metric:** Runtime of bootstrap/ticket workflows.
  - **Target:** Reasonable for local developer workflow.

#### Security
- [ ] **NFR-101:** No remote/cloud data transfer.
  - **Rationale:** Keep workflow local and predictable.
  - **Compliance:** None.

#### Usability
- [ ] **NFR-201:** CLI-only with minimal prompts.
  - **Metric:** Number of required prompts per workflow.
  - **Target:** Only necessary gates (e.g., HIGH-risk approvals).

#### Reliability
- [ ] **NFR-301:** Idempotent reruns and recoverable failures.
  - **Metric:** Ability to rerun after error without corruption.
  - **Target:** No duplicate worklog sections or inconsistent status.

### Constraints

**Technical Constraints:**
- macOS-first support; no Windows support.
- CLI-only; no UI in this project.
- Requires git, codex, make, and language runtimes as needed.

**Business Constraints:**
- Personal use; optimize for simplicity and robustness.

**Regulatory/Compliance:**
- None.

## User Experience

### User Journey
```
Bootstrap → Context/PRD → Features → Tickets → Execute → Repeat
```

### Key Screens/Interactions
1. **CLI: Bootstrap**
   - Purpose: Seed a repo with templates/tools.
   - Key elements: Command output and optional overwrite/merge/skip prompts.
   - Actions: Run bootstrap/update.

2. **CLI: Execute Ticket**
   - Purpose: Run the ticket workflow with AI.
   - Key elements: Preflight, gates, test results, commit suggestion.
   - Actions: Approve gates when required.

### Error States
| Scenario | User Experience | System Behavior |
|----------|----------------|-----------------|
| Missing dependencies | Clear error | Fail fast with instructions |
| HIGH-risk ticket without approval | Blocked | Stop after preflight |
| Rerun after partial failure | Resume safely | Replace-in-place updates |

## Scope

### Scope Boundaries (Template)
<!-- Define what this PRD covers and what it explicitly avoids -->
- **System boundaries:** local CLI tools, templates, and docs.
- **User boundaries:** single developer/PO; no secondary users.
- **Data boundaries:** local repos and docs only; no remote storage.
- **Platform boundaries:** macOS CLI.

### Non-Goals (Template)
<!-- Explicitly state what this PRD is not trying to achieve -->
- Cloud services or remote state.
- UI or multi-user collaboration.
- Windows support.
- Extra complexity or configuration beyond essentials.

### In Scope
- Bootstrap templates into repos.
- Update/reapply templates safely.
- Execute ticket workflow with AI.

### Out of Scope
- UI/desktop/web interfaces.
- Cloud sync or remote storage.
- Windows support.

### Future Considerations
- Optional CLI/TUI wrapper for looping approved tickets.

## Dependencies

### Internal Dependencies
- **Docs/templates:** in `tools/templates/docs`.
- **Tools:** CLI scripts in `tools/`.

### External Dependencies
- **Codex CLI:** required for AI execution.
- **Git/Make:** required for workflow and tests.
- **Language runtimes:** Python/Node/Rust/Go as needed.

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Tooling is not idempotent and re-runs corrupt state | High | Medium | Replace-in-place updates; tests for idempotency |
| Template updates are hard to propagate | High | Medium | Safe reapply with skip/merge |
| AI workflow burns tokens on repeatable steps | High | Medium | Keep prompts minimal; skip completed work |
| Missing dependencies cause failures | Med | Medium | Preflight checks and clear errors |

## Open Questions

- None currently. Dependencies are assumed to exist locally (git, codex, make), and HIGH-risk approvals are handled via a prompt with optional `approval: "granted"` in ticket frontmatter.

## Appendix

### Related Documents
- docs/00-context/vision.md
- docs/00-context/users.md
- docs/00-context/system-map.md
- docs/00-context/assumptions.md
- docs/00-context/context-boundaries-operating-model.md

### Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-30 | 0.1 | Draft PRD from context docs | Primary user |
