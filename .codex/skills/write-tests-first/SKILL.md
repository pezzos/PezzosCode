---
name: write-tests-first
description: Write tests before implementation to lock in expected behavior and verify failures first. Use when a user asks to add tests first, practice TDD, or define test cases before coding.
---

# Write Tests First

## Overview
Define and add tests before implementation to lock in expected behavior.

## Inputs
- Feature spec or bug description.
- Target files/modules.
- Preferred test framework (if any).

## Steps
1) Read the relevant spec or bug log entry.
2) Write test cases for happy path, edge cases, and failures.
3) Run tests to confirm they fail for the right reason.
4) Implement minimal code changes to pass.
5) Re-run tests to confirm success.

## Commands
- `rg --files -g '*test*' -g '*spec*'`
- Test command (ask if not documented).

## Output
- New or updated tests that fail before code changes and pass after.

## DoD
- Tests cover acceptance criteria and key edge cases.
- Tests pass after implementation.
