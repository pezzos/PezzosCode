# Implementation Log

> **What changed in code & why**
>
> A chronological record of all code changes, technical decisions made during implementation, and the reasoning behind them. This is the MEMORY that most teams miss.

---

## Purpose

This log captures:
- **What** code was changed
- **Why** the change was made
- **How** it was implemented
- **Trade-offs** considered
- **Lessons learned**

This helps with:
- Understanding the evolution of the codebase
- Debugging when things break
- Onboarding new team members
- Avoiding repeating mistakes

---

## Log Entries

### 2026-02-01 - Align README sync with context/log sources

**Feature/Bug:** Documentation maintenance

**Changed Files:**
- `.codex/skills/readme-sync/SKILL.md` - Require context/log reconciliation and exclude PRD as a source
- `README.md` - Update core context list and keep PRD as a separate step
- `docs/README.md` - Soften source-of-truth phrasing to avoid unsupported claims
- `tools/README.md` - Align tool list with context/system map
- `tools/serena/solidlsp_override/README.md` - Remove unsupported snapshot/patch details
- `tools/serena/solidlsp_override/solidlsp/language_servers/elixir_tools/README.md` - Reduce to minimal pointer

**What Changed:**
Updated the README sync rules to reconcile statements against `docs/00-context/*`
and `docs/03-logs/*`, then tightened README content to match those sources.

**Why:**
README content should reflect current, authoritative context and logs rather
than inferred or PRD-only details.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync README files

**Feature/Bug:** Documentation maintenance

**Changed Files:**
- `README.md` - Shorten root readme and point to canonical docs
- `docs/README.md` - Condense to AI-focused structure and remove duplication
- `tools/README.md` - Standardize structure and reduce repetition
- `tools/serena/solidlsp_override/README.md` - Clarify override purpose and refresh steps
- `tools/serena/solidlsp_override/solidlsp/language_servers/elixir_tools/README.md` - Compress integration notes

**What Changed:**
Rewrote README files to follow a consistent structure, reduce overlap, and keep
the root README human-focused while keeping the rest AI-friendly.

**Why:**
The README sync workflow requires concise, non-duplicative docs that point to
canonical sources.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Fix readme-sync skill frontmatter

**Feature/Bug:** Skill validation

**Changed Files:**
- `.codex/skills/readme-sync/SKILL.md` - Remove extra frontmatter lines to match skills-check expectations

**What Changed:**
Adjusted the skill header to the required 4-line frontmatter format so `make test` passes.

**Why:**
The skills check enforces a strict frontmatter layout for SKILL.md files.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Add pp write avoidance note

**Feature/Bug:** Process guardrail

**Changed Files:**
- `AGENTS.md` - Clarify pp is for large-output reads, not filesystem writes
- `.codex/skills/readme-sync/SKILL.md` - Add pp usage note for write operations

**What Changed:**
Added a brief note to avoid using `tools/offload-proxy/pp` for write commands to reduce unnecessary escalation prompts.

**Why:**
`pp` is intended for large output reads; using it for write commands can trigger avoidable permissions flow.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Add README sync skill

**Feature/Bug:** Skill addition

**Changed Files:**
- `.codex/skills/readme-sync/SKILL.md` - New skill to update README files with minimal duplication

**What Changed:**
Added a skill that scans non-template README files, applies a standardized structure, and reduces duplication with concise summaries.

**Why:**
Keep README content current and minimal for both humans (root) and AI (all others).

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync root template guardrails to live config

**Feature/Bug:** Template parity

**Changed Files:**
- `tools/templates/root/Makefile` - Add Python unit tests to `make test`, make `check` a real gate
- `tools/templates/root/.githooks/pre-commit` - Run `make test` directly
- `tools/templates/root/.codex.toml` - Add approval policy guardrail note
- `tools/templates/root/.serena/project.yml` - Add unique-list note and include Python

**What Changed:**
Aligned root templates with the current live root files and guardrail comments to keep future bootstraps consistent.

**Why:**
Templates should mirror the working repo so new projects inherit the correct checks and safety notes.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync skill guardrails for approval policy and language list

**Feature/Bug:** Skill behavior guardrails

**Changed Files:**
- `.codex/skills/sync-root-from-context/SKILL.md` - Preserve approval policy unless explicitly requested; enforce unique language list.
- `.codex.toml` - Add note to keep approval policy unchanged unless requested.
- `.serena/project.yml` - Add note to keep language list unique.

**What Changed:**
Updated the sync skill and root-file comments to prevent unintended approval policy changes and duplicate language entries on future runs.

**Why:**
The sync behavior should preserve AI-first defaults and avoid accidental config drift.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync live root tooling with current project context

**Feature/Bug:** Internal tooling sync

**Changed Files:**
- `Makefile` - Run Python unit tests as part of `make test`, make `check` a real gate
- `.githooks/pre-commit` - Use `make test` for a single source of truth
- `.serena/project.yml` - Include TOML and bash in language servers (no duplicates)
- `tools/bootstrap-into` - Add preflight command checks and `--dry-run`
- `tools/ticket-bootstrap` - Add preflight command checks and `--dry-run`

**What Changed:**
Aligned the live root files with the current repo context by ensuring tests run consistently and Serena indexes the repo’s actual file types. Added preflight validations to bootstrap scripts and a `--dry-run` mode to show planned actions without writing. Kept Codex approval policy at "never" after feedback and removed duplicate language entries.

**Why:**
The repo is a tooling/template bootstrap. Root files should reflect the actual workflows and file types used here, and safety defaults should be aligned with the documented process.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Serena LSP workspace/configuration diagnostics and early-load guard

**Feature/Bug:** LSP stability (Taplo/YAML startup errors)

**Changed Files:**
- `tools/serena/solidlsp_override/solidlsp/ls_handler.py` - Added ping watcher, import banner, and richer workspace/configuration logging
- `.codex.toml` - Added `SERENA_LSP_CONFIG_PING_DIR=/tmp` for manual pings

**What Changed:**
Added an opt-in, file-triggered ping mechanism to exercise the `workspace/configuration` handler and send `workspace/didChangeConfiguration`. Added an early import banner (guarded by `SERENA_LSP_IMPORT_BANNER=1`) to prove the override is loaded before any LSP errors print, and included request_id/item count in the request log for correlation.

**Why:**
Taplo intermittently logs `method 'workspace/configuration' not handled on client` before the Serena log file exists. This indicates the error is emitted before `.codex.toml` env overrides are applied, so we needed a way to validate early-load behavior and manually trigger config handling in-session.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same (ping watcher is opt-in, dormant unless env set)
- **Dependencies:** None

**Testing:**
- Manual: `touch /tmp/ping_workspace_configuration.toml` and verified log lines for ping/handler

**Notes:**
- If the same issue occurs for another language, set override env in the shell (e.g., `.zshrc`) so it applies before Codex starts, then use `touch /tmp/ping_workspace_configuration.<language>` to trigger a ping and confirm handler behavior in logs.
- If the error still appears before logs, enable `SERENA_LSP_IMPORT_BANNER=1` to verify whether the override is imported early enough.

**Author:** Alexandre Pezzotta

### 2026-01-31 - Root templates and bootstrap sync updates

**Feature/Bug:** Internal tooling update

**Changed Files:**
- `tools/templates/root/*` - Added top-level templates (root files, .serena, .githooks)
- `tools/bootstrap-into` - Copy root templates and treat them as conditional updates
- `.codex/skills/sync-root-from-context/SKILL.md` - New skill to sync live root files from docs context
- `docs/00-context/system-map.md` - System map updated

**What Changed:**
Created a dedicated root template directory and updated bootstrap logic to copy those templates into target repos with safe, conditional updates. Added a new skill to keep live root files in sync with project context and PRD.

**Why:**
We needed a clean separation between generic bootstrapped root files and this repo’s project-specific root files.

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
- Manual: ran `tools/bootstrap-into --self --verbose`

**Notes:**
- Root templates now live in `tools/templates/root/`.
- Live root files are project-specific and updated via the new skill.

**Author:** Alexandre Pezzotta

### [YYYY-MM-DD] - [Brief Description of Change]

**Feature/Bug:** [Link to feature or bug ticket]

**Changed Files:**
- `path/to/file1.ts`
- `path/to/file2.ts`

**What Changed:**
[Describe the code changes in technical detail]

**Why:**
[Explain the reasoning behind the change]
- Problem we were solving: [description]
- Alternative approaches considered: [list]
- Why this approach: [rationale]

**Impact:**
- **Breaking changes:** [Yes/No - describe if yes]
- **Performance:** [Better/Worse/Same - explain]
- **Dependencies:** [New dependencies added/removed]

**Testing:**
- Tests added: [describe]
- Manual testing done: [describe]

**Notes:**
- [Any gotchas, warnings, or things to watch out for]
- [Technical debt introduced or paid down]
- [Things we'd do differently next time]

**Author:** [Name]

---

### [YYYY-MM-DD] - [Another Change]

**Feature/Bug:** [Link to feature or bug ticket]

**Changed Files:**
- `path/to/file.ts`

**What Changed:**
[Description]

**Why:**
[Reasoning]

**Impact:**
- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
[Testing done]

**Notes:**
[Additional context]

**Author:** [Name]

---

## Example Entry

### 2025-01-15 - Implemented caching layer for API responses

**Feature:** [Link to feature-spec.md for performance optimization]

**Changed Files:**
- `src/api/client.ts` - Added caching middleware
- `src/cache/redis-cache.ts` - New Redis cache implementation
- `src/config/cache-config.ts` - Cache configuration
- `package.json` - Added redis dependency

**What Changed:**
Added a caching layer using Redis to cache API responses for GET requests. Implemented:
- Cache middleware that intercepts API calls
- TTL-based cache invalidation (5 minutes default)
- Cache key generation based on endpoint + query params
- Cache bypass option for authenticated requests

**Why:**
- **Problem:** API response times were averaging 800ms, causing poor UX
- **Goal:** Reduce response times to < 200ms for repeated requests
- **Alternatives considered:**
  1. In-memory caching: Rejected because we have multiple server instances
  2. CDN caching: Rejected because data is user-specific
  3. Redis caching: Chosen because it's fast, shared across instances, and we already use Redis for sessions

**Impact:**
- **Breaking changes:** No - caching is transparent to existing code
- **Performance:** Average response time reduced from 800ms to 150ms (81% improvement)
- **Dependencies:** Added `ioredis@5.3.0`
- **Infrastructure:** Requires Redis instance (already available in staging/prod)

**Testing:**
- Added unit tests for cache middleware (test/api/cache-middleware.test.ts)
- Added integration tests for cache invalidation
- Manual testing: verified cache hits/misses in Redis CLI
- Load tested with 100 concurrent users: no issues

**Notes:**
- **Watch out:** Cache invalidation strategy is simple (TTL-based). May need more sophisticated invalidation for real-time data
- **Technical debt:** Currently only caches GET requests. Should extend to POST responses where appropriate
- **Monitoring:** Added cache hit/miss metrics to dashboard
- **Next time:** Consider implementing cache warming on deployment

**Author:** Jane Doe

---

## Implementation Patterns

### Common Patterns Used
Document recurring patterns in your codebase:

#### Pattern: [Pattern Name]
**When to use:** [scenarios]

**Example:**
```typescript
// Code example
```

**Reasoning:** [why we use this pattern]

---

## Technical Debt Log

### Current Tech Debt
Track technical debt as it's introduced:

| Date Added | Location | Description | Impact | Plan to Address |
|------------|----------|-------------|--------|-----------------|
| YYYY-MM-DD | `path/to/file` | [what's wrong] | High/Med/Low | [when/how we'll fix] |

### Resolved Tech Debt
Track when debt is paid down:

| Date Resolved | Original Date | Description | How Resolved |
|---------------|---------------|-------------|--------------|
| YYYY-MM-DD | YYYY-MM-DD | [what was wrong] | [how we fixed it] |

---

## Change Statistics

### By Month
| Month | Changes | Files Modified | Authors |
|-------|---------|----------------|---------|
| 2025-01 | [count] | [count] | [count] |

### By Category
| Category | Count | % of Total |
|----------|-------|------------|
| Features | [#] | [%] |
| Bug Fixes | [#] | [%] |
| Refactoring | [#] | [%] |
| Performance | [#] | [%] |
| Security | [#] | [%] |

---

## Related Documents

- [Decision Log](decision-log.md) - Product and architectural decisions
- [Bug Log](bug-log.md) - Bug tracking and fixes
- [Validation Log](validation-log.md) - Post-deployment learnings
- [Insights](insights.md) - Patterns and improvements
