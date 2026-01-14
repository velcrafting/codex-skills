---
name: frontend-test-additions
description: Add or extend frontend tests to cover intended behavior and critical UI states.
metadata:
  short-description: Frontend tests
  layer: frontend
  mode: write
  idempotent: false
---

# Skill: frontend/frontend-test-additions

## Purpose
Add frontend tests that prove behavior, prevent regressions, and validate UI states.
Prefer tests that are stable and aligned with repo testing conventions.

---

## Inputs
- Target component/route/flow
- Behavior to prove (acceptance criteria)
- Existing test framework and patterns (from repo or `REPO_PROFILE.json`)
- Mocking strategy (MSW, fetch mocks, fixtures) if present

---

## Outputs
- New or updated tests
- Supporting fixtures/mocks if needed
- Optional: test helper utilities if consistent with repo patterns

---

## Non-goals
- Refactoring unrelated UI code
- Adding a new test framework
- Snapshot-only testing unless repo standard and justified

---

## Workflow
1) Identify test stack:
   - unit/component tests (testing-library)
   - e2e tests (playwright/cypress)
   - choose the highest-value lowest-flake layer available
2) Define minimum test set (default):
   - happy path render
   - at least one error or empty state
   - at least one interaction (if interactive)
3) Prefer role/name queries over brittle selectors.
4) Mock data at the boundary:
   - API layer via MSW/mocks
   - avoid mocking internal implementation details
5) Add tests incrementally and keep them deterministic.
6) Run tests using repo commands.

---

## Checks
- Tests pass locally (or explain deterministic alternative if tests cannot run)
- Tests validate intended user-observable behavior
- Tests cover at least two states when data-driven:
  - success + (error or empty)
- Minimal flakiness risk:
  - avoid time-based waits without reason
  - prefer explicit awaits on UI changes

---

## Failure modes
- Test commands unknown → consult `REPO_PROFILE.json` or recommend `personalize-repo`.
- Flaky tests appear → stabilize by removing timing dependence and improving mocks.
- Difficult to test due to tight coupling → recommend extraction or boundary mocking.

---

## Telemetry
Log:
- skill: `frontend/frontend-test-additions`
- test_type: `unit | component | e2e`
- states_covered: `success | loading | error | empty` (subset)
- files_touched
- outcome: `success | partial | blocked`
