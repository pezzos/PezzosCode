# Expected Features

## Purpose

Capture explicit features the human expects, before PRD generation. These are
inputs to the PRD feature list and must be reflected unless explicitly rejected.

## Feature Candidates

- Feature:
  - Owner:
  - Problem:
  - Outcome:
  - Priority: P0 | P1 | P2
  - Notes:

## Current Expected Features

- Feature: Worktree policy for parallel roles
  - Owner: Developer/PO
  - Problem: Parallel roles contaminate each other's context or diffs
  - Outcome: Clean isolation for planner/plan-reviewer/patcher/tester/reporter
  - Priority: P1
  - Notes: Naming convention `../<repo_name>-<feature_name>-<agent_name>`

- Feature: Orchestrator + sub-agent roles
  - Owner: Developer/PO
  - Problem: Single agent context gets overloaded
  - Outcome: Clear role separation and predictable gates
  - Priority: P1
  - Notes: Orchestrator approves Plan/Patch/Test/Report

- Feature: Output offload enforcement
  - Owner: Developer/PO
  - Problem: Large outputs waste tokens and derail context
  - Outcome: Noisy outputs stored in `.offload/` and referenced by id
  - Priority: P0
  - Notes: Use `tools/offload-proxy/pp`

- Feature: Resume in-progress tickets
  - Owner: Developer/PO
  - Problem: Interrupted ticket runs should be resumable without restarting from scratch
  - Outcome: Automatic resume when worklog exists; completed steps are skipped; tests/CI re-run
  - Priority: P0
  - Notes: Skip commit if already recorded in the worklog

- Feature: Commit gated by completed ticket docs
  - Owner: Developer/PO
  - Problem: Commits should only happen when ticket documentation is complete and DoD is satisfied
  - Outcome: Auto-fill Tests Run/Report and check DoD before commit
  - Priority: P0
  - Notes: Commit step enforces ticket doc completion

- Feature: Anti-cheat testing strategy
  - Owner: Developer/PO
  - Problem: Hardcoded implementations pass shallow tests
  - Outcome: Tests validate behavior through fixtures/invariants/contracts
  - Priority: P1
  - Notes: Seeded randomness and multiple fixtures

- Feature: Shared runner library for tools/scripts
  - Owner: Developer/PO
  - Problem: Inconsistent command invocation and missing metadata across tools
  - Outcome: Shared runner (`lib/pc_runner.*`) standardizes Codex/Serena runs, profiles, logging, and metadata injection
  - Priority: P0
  - Notes: Inject `work_item_id`, `agent_name`, `run_id`

- Feature: Structured logs for CI/tests/precommit/feature runs
  - Owner: Developer/PO
  - Problem: Failures are hard to debug; no tail-friendly logs or timestamps
  - Outcome: Logs written to `logs/<WI>/<step>.log` with `[WI-...][agent][step]` prefix and timestamps
  - Priority: P0
  - Notes: Reduce verbosity for formatter/linter output

- Feature: Precommit autofix restaging + vanilla Codex config
  - Owner: Developer/PO
  - Problem: Autofixes don't re-stage files; precommit Codex behavior is noisy and inconsistent
  - Outcome: Precommit re-adds modified files (`git add -u`) and prints what changed; Codex runs with vanilla config for staged fixes only
  - Priority: P0
  - Notes: No log updates required for precommit fixes

- Feature: Unified autofix script for CI + precommit
  - Owner: Developer/PO
  - Problem: Duplicate logic for autofix across CI and hooks
  - Outcome: Single script (e.g., `scripts/pc-ci-check`) used by `make ci` and precommit
  - Priority: P0

- Feature: Remove feature-worktrees.json
  - Owner: Developer/PO
  - Problem: Worktree tracking file is unnecessary with one worktree per feature
  - Outcome: Orchestrator uses a single worktree per feature without extra tracking files
  - Priority: P0

- Feature: Incremental prd-to-features
  - Owner: Developer/PO
  - Problem: Regenerating features can delete or duplicate work
  - Outcome: Add missing features only; never delete existing; skip already Done features
  - Priority: P1
  - Notes: Detect `Status: Done` in `dev-tasks.md`

- Feature: Role prompts + Plan Reviewer gate
  - Owner: Developer/PO
  - Problem: Role behavior is inconsistent; plans skip structured validation
  - Outcome: Dedicated prompts per role and a Plan Reviewer who validates plans without editing code
  - Priority: P1
  - Notes: Feature generation uses five steps (data model → logic → edge cases → UI → integration)

- Feature: Post-run improvement proposals with human gate
  - Owner: Developer/PO
  - Problem: Failures repeat without systematic learning
  - Outcome: After `make feature` completes/stops, propose a patch (not auto-applied) and log in `docs/possible-improvements.md`
  - Priority: P1
  - Notes: Errors logged with work item id, agent, step

- Feature: Offload system audit + upgrade plan
  - Owner: Developer/PO
  - Problem: Offload reliability and retention are untracked
  - Outcome: Audit offload, add index (id, cmd, wi, agent, timestamp, size) and list/get/purge commands
  - Priority: P2
  - Notes: Include retention policy

- Feature: Compact log skills
  - Owner: Developer/PO
  - Problem: Decision/implementation logs become verbose over time
  - Outcome: Skills produce compact versions without losing source data
  - Priority: P2

- Feature: Feature gating in precommit
  - Owner: Developer/PO
  - Problem: Later features may advance while earlier ones are incomplete
  - Outcome: Soft warning when modifying a feature while earlier features are not Done; consider hard block later
  - Priority: P2

- Feature: Skill mining from repeated prompts
  - Owner: Developer/PO
  - Problem: Recurrent prompt patterns waste time and tokens
  - Outcome: Detect recurring prompts and propose reusable skills (e.g., `fix-issue.md`)
  - Priority: P2
  - Notes: Analyze prompts + offloaded outputs; propose DoD and steps

- Feature: Workflow hardening for template drift and autofix recovery
  - Owner: Developer/PO
  - Problem: Pre-commit or CI can fail when template files drift from living files or autofix steps do not fully resync touched files
  - Outcome: Deterministic hardening flow auto-detects drift, repairs scoped files, re-stages only allowed paths, and re-runs checks with clear fail-close remediation
  - Priority: P0
  - Notes: Prioritize pre-commit drift scenarios where templates and repo files are out of sync

- Feature: End-to-end workflow smoke test with a synthetic feature
  - Owner: Developer/PO
  - Problem: Full workflow regressions are hard to catch without a realistic Plan -> Patch -> Test -> Report run
  - Outcome: Repeatable synthetic/fake feature test validates end-to-end orchestration, gates, resume behavior, and logs before real feature work
  - Priority: P1
  - Notes: Keep fixture lightweight so teams can run collaborative workflow checks quickly
