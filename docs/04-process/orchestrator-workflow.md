# Orchestrator Workflow

## 0) One-shot validation

```bash
python3 scripts/orchestrator_validate.py --output-json .orchestrator/validation_summary.json
```

## 1) Initialize control plane

```bash
python3 scripts/orchestrator_guard.py init
python3 scripts/orchestrator_guard.py assert
python3 scripts/orchestrator_guard.py run-status
python3 scripts/orchestrator_guard.py policy-show
python3 scripts/runtime_profiles.py summary
```

If `assert` fails, recover ownership before delegating.

## 2) Pick the right entrypoint

- Planning, routing, or skill selection -> `orchestrator-governance`
- Approved plan execution -> `execute-approved-plan-safely`
- Low-level native-role loop -> `orchestrator-agent-loop`

## 3) Inspect native role registry

```bash
python3 scripts/runtime_profiles.py summary
python3 scripts/runtime_profiles.py role frontend-developer
python3 scripts/runtime_profiles.py role security-specialist
```

## 4) Review or delegate scoped work

- Review product docs with specialists:
  Launch one native role per `(document, role)` pair and keep same-document reviews sequential.
- Implementation work:
  Delegate to the smallest write-enabled role that matches the scope.
- Homogeneous multi-target work:
  Prefer `spawn_agents_on_csv` when each row is independently scoped.

## 5) Route common documentation follow-ups

- After `refresh-context-docs`, auto-chain `build-prd-from-context` only if `docs/00-context/*` changed materially.
- After product-doc updates, route `sync-root-files-from-docs` when root operational files may need realignment.
- Route `reconcile-readmes` only when README drift or duplication is the actual problem.
- After accepted work, update `docs/03-logs/*` through the canonical global `update-project-logs` skill.

## 6) Review and iterate autonomously

- Review native-role JSON outputs, tests, findings, and diff summaries.
- Decide `REVIEW_READY`, `REVISE`, or `DONE`.
- Use specialist findings and `questions_for_user` when the job was review/analyze/test only.
- Keep orchestrator as the final arbiter.
- No mandatory human checkpoint between iterations.
