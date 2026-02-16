# Global UX / UI Blueprint

> Machine-managed by `tools/pc-prepare-features`. Edit PRD/context and rerun instead of hand-editing this file.

**Last Updated:** 2026-02-16

## User journeys

Primary persona: Developer/PO running local CLI workflows with explicit gates.

### Journey 01: Bootstrap + safe template reapply

- Goal: deliver `bootstrap-safe-template-reapply` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 02: Deterministic work-item execution with explicit gates

- Goal: deliver `deterministic-work-item-execution-with-explicit-gates` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 03: Output offload + structured logs + shared runner

- Goal: deliver `output-offload-structured-logs-shared-runner` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 04: Resume safety + fail-closed commit gate + scoped autofix

- Goal: deliver `resume-safety-fail-closed-commit-gate-scoped-autofix` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 05: Single-worktree orchestration + template-drift hardening

- Goal: deliver `single-worktree-orchestration-template-drift-hardening` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 06: Orchestrator roles + Plan Reviewer gate + role-specific prompts

- Goal: deliver `orchestrator-roles-plan-reviewer-gate-role-specific-prompts` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 07: Anti-hardcode test policy + synthetic end-to-end smoke feature

- Goal: deliver `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 08: Incremental PRD-to-features + post-run learning loop

- Goal: deliver `incremental-prd-to-features-post-run-learning-loop` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 09: Output offload enforcement

- Goal: deliver `output-offload-enforcement` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 10: Resume in-progress tickets

- Goal: deliver `resume-in-progress-tickets` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 11: Commit gated by completed ticket docs

- Goal: deliver `commit-gated-by-completed-ticket-docs` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 12: Shared runner library

- Goal: deliver `shared-runner-library` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 13: Structured logs for CI/tests/precommit/feature runs

- Goal: deliver `structured-logs-for-ci-tests-precommit-feature-runs` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 14: Unified autofix script

- Goal: deliver `unified-autofix-script` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 15: Precommit restage + vanilla Codex config

- Goal: deliver `precommit-restage-vanilla-codex-config` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 16: Single worktree per feature

- Goal: deliver `single-worktree-per-feature` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 17: Workflow hardening for template drift + autofix recovery

- Goal: deliver `workflow-hardening-for-template-drift-autofix-recovery` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 18: Orchestrator + sub-agent roles

- Goal: deliver `orchestrator-sub-agent-roles` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 19: Role-specific prompts + Plan Reviewer

- Goal: deliver `role-specific-prompts-plan-reviewer` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 20: Incremental prd-to-features

- Goal: deliver `incremental-prd-to-features` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 21: Learning loop proposals

- Goal: deliver `learning-loop-proposals` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 22: Worktree policy + naming convention

- Goal: deliver `worktree-policy-naming-convention` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 23: Anti-cheat testing strategy

- Goal: deliver `anti-cheat-testing-strategy` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

### Journey 24: End-to-end workflow smoke test with a synthetic feature

- Goal: deliver `end-to-end-workflow-smoke-test-with-a-synthetic-feature` with deterministic scope and traceability.
- Entry: updated PRD + approved prepare workflow artifacts.
- Steps:
  1. Human runs `make prepare-features` and verifies PM gate approval.
  2. Feature docs are generated/updated in dependency order with prerequisites: (none).
  3. Human runs `make review-features` and confirms findings are reflected in feature docs.
  4. Human executes the feature with `make feature F=<feature-id>`.
- Exit: feature docs contain requirements, fixes backlog, and execution-ready tasks.

## Workflows

| Feature                                                         | Workflow                     | Dependencies | Human validation checkpoint |
| --------------------------------------------------------------- | ---------------------------- | ------------ | --------------------------- |
| Bootstrap + safe template reapply                               | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Deterministic work-item execution with explicit gates           | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Output offload + structured logs + shared runner                | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Resume safety + fail-closed commit gate + scoped autofix        | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Single-worktree orchestration + template-drift hardening        | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Orchestrator roles + Plan Reviewer gate + role-specific prompts | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Anti-hardcode test policy + synthetic end-to-end smoke feature  | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Incremental PRD-to-features + post-run learning loop            | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Output offload enforcement                                      | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Resume in-progress tickets                                      | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Commit gated by completed ticket docs                           | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Shared runner library                                           | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Structured logs for CI/tests/precommit/feature runs             | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Unified autofix script                                          | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Precommit restage + vanilla Codex config                        | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Single worktree per feature                                     | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Workflow hardening for template drift + autofix recovery        | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Orchestrator + sub-agent roles                                  | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Role-specific prompts + Plan Reviewer                           | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Incremental prd-to-features                                     | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Learning loop proposals                                         | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Worktree policy + naming convention                             | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| Anti-cheat testing strategy                                     | Prepare -> Review -> Execute | (none)       | Before first `make feature` |
| End-to-end workflow smoke test with a synthetic feature         | Prepare -> Review -> Execute | (none)       | Before first `make feature` |

## UX constraints

- Keep command UX explicit and deterministic; avoid hidden background behavior.
- Any ambiguity must present numbered options (2-4) with explanation and risk.
- Decisions must be persisted so reruns remain deterministic.
- Manual checkpoints happen only at explicit gates; no implicit pauses.
