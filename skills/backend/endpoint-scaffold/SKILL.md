---
name: endpoint-scaffold
description: Create a validated, authorized backend endpoint with error mapping and tests.
metadata:
  short-description: Endpoint + validation + auth + tests
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/endpoint-scaffold

## Purpose
Add or extend an API endpoint in a way that is:
- validated (request + response shape)
- authorized (authn/authz hooks enforced)
- mapped to a stable error taxonomy
- covered by tests

This skill is the default entry point for backend feature exposure.

---

## Inputs
- Endpoint intent (what it does, who calls it)
- Contract surface (preferred):
  - method + path
  - request fields + types
  - response shape + types
- Authorization expectation:
  - public / authenticated / role-based / resource-based
- Error expectations:
  - list of expected failure cases
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- New or updated endpoint handler/controller/router entry
- Input validation (schema/types) consistent with repo patterns
- Authorization enforcement consistent with repo patterns
- Error mapping consistent with shared error taxonomy
- Tests:
  - unit tests for handler logic and validation OR
  - integration tests at route boundary (preferred when available)

---

## Non-goals
- Implementing complex domain rules inside the handler (use `backend/domain-logic-module`)
- Changing persistence schema (use `backend/persistence-layer-change`)
- Changing API contracts across consumers (use `api/contract-update` if needed)
- Cross-cutting architecture rewrites

---

## Workflow
1) Discover repo endpoint conventions:
   - routing system, validation library, error shape, auth middleware
   - prefer `REPO_PROFILE.json` if present
2) Define contract explicitly:
   - request parsing + validation
   - response shape
3) Enforce authorization:
   - fail closed by default
   - ensure resource checks exist if needed
4) Call domain logic via a module boundary:
   - handler orchestrates, domain module decides
5) Map errors to a stable taxonomy:
   - user errors vs system errors vs auth errors
6) Add tests at the highest stable layer available:
   - route integration tests if infra exists
   - otherwise unit tests of handler + domain module
7) If this endpoint introduces branching, retries, async coordination, or multi-step behavior,
   recommend `system/state-machine-mapper` and pause until the behavior is modeled or explicitly waived.

---

## Checks
- Endpoint returns correct status/shape for success
- Validation rejects malformed inputs deterministically
- Authorization cannot be bypassed (fail closed)
- Error responses conform to shared error taxonomy
- Tests cover:
  - happy path
  - at least 2 failure cases (validation + auth or domain)
- Typecheck/lint pass if configured

---

## Failure modes
- No error taxonomy exists → recommend `shared/error-taxonomy` before shipping.
- Authz rules unclear → recommend `backend/authz-policy` or `$decision-capture`.
- Contract unclear → recommend `meta/ask-questions-if-underspecified` or `api/contract-update`.
- Handler becomes “god function” → extract domain logic into `backend/domain-logic-module`.
- Non-trivial branching or async flow added without a state model →
  block completion and recommend `system/state-machine-mapper`.

---

## Telemetry
Log:
- skill: `backend/endpoint-scaffold`
- endpoint: `<method> <path>` (if known)
- authz: `public | authenticated | role | resource`
- tests_added: `unit | integration | none`
- files_touched
- outcome: `success | partial | blocked`
