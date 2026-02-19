# PezzosCode Security Baseline

> Machine-managed by `tools/pc-prepare-features`. Update context/PRD/process docs and rerun `make prepare-features` instead of hand-editing.

## Security scope boundaries

- Local-first, macOS CLI only, single Developer/PO user; no cloud services, daemons, or multi-user trust model.
- In-scope assets: repository files, templates, workflow docs, `.offload/` payloads, `logs/<WI>/<step>.log`, work-item evidence under `docs/02-features/*`, durable logs in `docs/03-logs/*`, and commit gate metadata.
- In-scope trust boundaries: human PO command authority, role-owned file boundaries, feature worktree boundary, and script execution through shared runner metadata (`work_item_id`, `agent_name`, `run_id`).
- Out of scope: remote IAM, network perimeter controls, SaaS tenancy, and Windows-specific hardening.
- Non-negotiable boundary controls: no remote data transfer (NFR-101), idempotent/recoverable reruns (NFR-301), deterministic stage order (NFR-401), and token-safe offload behavior (NFR-501).

## Threat model and attack surface

| Attack surface                                                  | Project-specific threat                                                     | Impact                                                                            | Required mitigation                                                                                                                                                 |
| --------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Protected orchestration commands (`make feature`, `pc-feature`) | AI/role executes protected commands without explicit PO approval            | Unauthorized high-impact changes                                                  | Enforce FR-015 command authority and explicit HIGH-risk approval gate with `Awaiting PO Approval` stop state                                                        |
| Stage transition logic                                          | Bypass of Plan Reviewer, tester, or reporter gates                          | Unreviewed code and missing evidence reaches commit                               | State machine enforces Plan -> Patch -> Test -> Report and loops failures back to Planner                                                                           |
| Template reapply and drift repair                               | Overbroad writes, path misuse, or destructive overwrite of non-scoped files | Repo corruption and loss of audit trail                                           | Scoped overwrite/merge/skip policies, deterministic drift repair, fail-closed unresolved drift remediation (FR-014)                                                 |
| Resume logic                                                    | Tampered/incomplete state causes unsafe stage skipping                      | False success and broken idempotency                                              | Resume only from valid evidence, always re-run tests/CI, preserve active WIP by default (FR-012)                                                                    |
| Offload/log surfaces (`.offload`, `logs`)                       | Secrets/noisy output leaked into prompts or missing traceability            | Data exposure and poor forensics                                                  | Mandatory `tools/offload-proxy/pp`, pointer IDs instead of inline dumps, timestamped structured logs (FR-004, FR-006)                                               |
| Role-scoped artifacts                                           | Cross-role writes to planner/tester/reporter owned files                    | Gate evidence spoofing                                                            | Role ownership boundaries and protected log/write rules from ticket-execution protocol                                                                              |
| Commit gate                                                     | Commit occurs with missing DoD/test/report evidence                         | Non-auditable insecure merge                                                      | Fail-closed commit gate requires complete planner/tester/reporter artifacts (FR-013)                                                                                |
| Prepare-features retry governance                               | Security artifact remains unchanged while open PM/security TODO items exist | Known blockers persist across loops and security acceptance becomes non-auditable | On retry iterations, require targeted section deltas linked to PM issue ids and security TODO ids; unchanged output is allowed only when actionable lists are empty |
| Toolchain/runtime dependencies                                  | Local dependency drift breaks deterministic controls                        | Silent control regression                                                         | Preflight dependency checks plus shared runner/script-first deterministic execution                                                                                 |

## Feature security focus map

| Feature slug                                                   | Security objective                             | Primary threats addressed                                           | Required security evidence                                                                   |
| -------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `bootstrap-safe-template-reapply`                              | Safe, idempotent bootstrap/update              | Destructive overwrite, path misuse                                  | Conflict decisions recorded; rerun does not duplicate or delete completed artifacts          |
| `output-offload-structured-logs-shared-runner`                 | Confidentiality + traceability for noisy steps | Prompt leakage, missing audit chain                                 | `.offload` pointer IDs, metadata index, and `logs/<WI>/<step>.log` prefixes/timestamps       |
| `deterministic-work-item-execution-with-explicit-gates`        | Enforce authority + risk gates                 | Unauthorized execution, gate bypass                                 | Preflight report, HIGH-risk approval artifact, blocked status when approval absent           |
| `single-worktree-orchestration-template-drift-hardening`       | Constrain write scope and drift recovery       | Cross-worktree drift, overbroad repair                              | One feature worktree policy and scoped repair logs with explicit unresolved remediation      |
| `resume-safety-fail-closed-commit-gate-scoped-autofix`         | Safe recovery and evidence-complete commits    | Unsafe resume, premature commit, autofix overreach                  | Resume markers, re-run test/CI evidence, blocked commit when required fields missing         |
| `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`  | Preserve role integrity                        | Role confusion, reviewer bypass                                     | Role-scoped outputs and Plan Reviewer approval before patching                               |
| `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature` | Detect workflow/security regressions early     | Weak tests hide gate regressions                                    | Fixture/seed/invariant/boundary test evidence and synthetic smoke pass/fail logs             |
| `incremental-prd-to-features-post-run-learning-loop`           | Prevent doc integrity regressions              | Rewriting/deleting completed features, unsafe auto-process mutation | Add-missing-only diffs, skip `Status: Done`, human approval record for improvement proposals |

## Security controls for this project

- Authority and risk controls: only human PO/user may run `make feature` and `pc-feature` unless explicit in-run approval is granted; HIGH-risk work must stop at preflight with status `Awaiting PO Approval` until explicit approval is recorded.
- Workflow integrity controls: mandatory Plan -> Patch -> Test -> Report sequence with Plan Reviewer gate before patching; Tester is restricted to Planner Allowed Tests and forbidden orchestration commands.
- Data handling controls: no remote/cloud transfer (NFR-101); noisy output must be offloaded via `tools/offload-proxy/pp`; prompts carry pointer IDs rather than raw command dumps.
- Observability controls: structured logs remain in predictable `logs/<WI>/<step>.log` paths with timestamped `[WI-...][agent][step]` prefixes.
- Write-scope and recovery controls: single feature worktree default, role-owned file boundaries, scoped deterministic drift repair/autofix, and fail-closed behavior on unresolved drift.
- Protected-log control: precommit autofix cannot mutate `docs/03-logs/*` or feature execution logs.
- Commit integrity controls: commit gate blocks when planner/tester/reporter artifacts or ticket DoD evidence are incomplete; final `make ci` gate runs after role-loop success with at most one autofix rerun.
- Retry-loop accountability control: when `pm_feedback_json` or `security_open_todos_json` contains open security-assigned action items, the next security iteration must include targeted section updates plus explicit issue/TODO id mapping in rationale.

## Verification and evidence

- Required per work item: preflight report (scope, risk, files-to-change, TDD, DoD), Plan Reviewer/tester/reporter outcomes, offload pointer IDs, structured step logs, resume markers, and commit-gate decision records.
- Durable traceability: update `docs/03-logs/*` with decisions, implementation notes, bug records, and validation outcomes after execution.
- Security regression checks for prepare-features outputs:
  - Command authority wording remains explicit for protected commands.
  - HIGH-risk path demonstrates block-without-approval behavior.
  - Offload/log requirements stay present in PRD, design, and UX artifacts.
  - Dependency ordering does not bypass gate-establishing features.
  - Resume and commit controls remain fail-closed.
- Retry-loop evidence rule: when PM feedback/TODO items target security, `changed_sections` must be non-empty and `change_rationale` must map updates to PM issue and TODO ids.
- Loop-4 closure evidence: PM-001 and PM-TODO-065 are resolved by targeted updates in threat, control, verification, and alignment sections while preserving prior valid controls.

## Alignment anchors

- Context boundary anchor: `docs/00-context/context-boundaries-operating-model.md`.
- PRD anchors: FR-004, FR-006, FR-012, FR-013, FR-014, FR-015; NFR-101, NFR-301, NFR-401, NFR-501, NFR-601.
- Process anchors: `docs/04-process/ticket-execution-protocol.md`, `docs/04-process/output-offload.md`, `docs/04-process/definition-of-done.md`, `docs/04-process/human-orchestration-workflow.md`.
- Ordering anchor: `docs/01-product/feature-order.json` dependency arrays and PM-TODO-059 dependency-contract consistency.
- UX/design anchors: deterministic gate wording in `ux-ui.md` and gated state-machine ownership in `design.md`.
- PM issue anchor: PM-001 and PM-TODO-065 (security owner) are addressed in prepare iteration 4 by required section-level security updates, without reverting previously resolved baseline controls.
