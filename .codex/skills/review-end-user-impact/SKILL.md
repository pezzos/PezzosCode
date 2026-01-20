---
name: review-end-user-impact
description: Review staged git changes from the end-user point of view, focusing on impact, expectations, and usability rather than technical details. Use when a user asks questions like "Is the change ok for users?" or "Review the change as an end-user" and the review should be based on the staged diff and user definitions in docs/00-context/users.md.
---

# Review End User Impact

## Overview
Review the staged diff from the perspective of the defined end users, describing how the change affects their experience, outcomes, and expectations.

## Workflow

### 1) Load user context
- Read `docs/00-context/users.md` to understand who the end users are.
- If the file is missing, empty, or clearly a placeholder, ask the user for the real end-user definition before proceeding.

### 2) Inspect the staged diff only
- Use `git diff --cached` as the sole source of code changes.
- Do not use unstaged or untracked changes.
- If there are no staged changes, state that and ask the user to stage changes.

### 3) Review from the end-user POV
- Describe changes in terms of user goals, outcomes, and workflows.
- Avoid implementation details, internal architecture, and technical jargon.
- Focus on what users will notice: behavior, UI/UX, performance, errors, wording, or data effects.
- Identify potential confusion, broken expectations, or new friction.
- Call out changes that require user education, migration, or updated documentation.

### 4) Output format
Provide a concise, user-facing review in this structure:
- Summary (1-3 sentences)
- User impact (who is affected and how)
- Potential pain points or confusion
- Risk to user trust or expectations
- Suggested improvements (non-technical, user-facing)
- Questions/assumptions (if anything blocks a clear user review)

### 5) Process compliance
- List commands executed and summarize their results as part of the response.

## Notes
- Prefer clarity over completeness; if the diff is large, ask for a narrower scope.
- If the change is entirely internal and non-user-facing, say so explicitly.
