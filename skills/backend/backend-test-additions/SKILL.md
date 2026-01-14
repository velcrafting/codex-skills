---
name: backend-test-additions
description: Add or extend backend tests to prove behavior, invariants, and regressions for services/endpoints/jobs.
metadata:
  short-description: Backend tests
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/backend-test-additions

## Purpose
Add backend tests that prove:
- domain invariants
- endpoint behavior and error mapping
- job behavior (idempotency/retries) where applicable
- integration adapter parsing and failure handling

Prefer deterministic, high-signal tests.

---

## Inputs
- Target module/endpoint/job
- Behavior to validate (acceptance criteria)
- Existing test stack and conventions (from repo/profile)
- Mocking strategy (fixtures, fakes, contract tests) if present

---

## Outputs
- New or updated test files
- Supporting fixtures/mocks
- Optional helper utilities if consistent with repo norms

---

## Non-goals
- Adding a new test framework
- Snapshot-only testing unless repo standard
- Broad refactors just to “make it testable” (prefer small extraction)

---

## Workflow
1) Identify test layers available:
   - unit tests (domain)
   - integration tests (endpoint boundary)
   - contract tests (external adapters)
2) Choose the highest-value layer with lowest flake risk.
3) Define minimum test set (default):
   - happy path
   - at least two failure paths:
     - validation/auth/error mapping OR invariant violation OR external failure
4) Mock at boundaries:
   - external APIs mocked at adapter boundary
   - persistence mocked only if repo standard; otherwise use test DB
5) Keep tests deterministic:
   - avoid time-based waits when possible
   - control randomness, time, and ids
6) Run tests using repo commands.

---

## Checks
- Tests pass locally (or a deterministic alternative is documented)
- Coverage includes:
  - happy path
  - at least 2 failure paths
- Tests assert outcomes users/operators care about:
  - status codes, error codes, invariants, retry decisions
- Minimal flakiness risk

---

## Failure modes
- Test commands unknown → consult `REPO_PROFILE.json` or recommend `personalize-repo`.
- Flaky tests → stabilize by removing timing dependence and controlling mocks.
- Hard-to-test coupling → extract minimal module boundary and test there.

---

## Telemetry
Log:
- skill: `backend/backend-test-additions`
- test_type: `unit | integration | contract`
- failure_paths_covered: count
- files_touched
- outcome: `success | partial | blocked`
