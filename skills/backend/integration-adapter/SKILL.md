---
name: integration-adapter
description: Build an external API adapter with timeouts, retries, idempotency, and error mapping.
metadata:
  short-description: External adapter + reliability policy
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/integration-adapter

## Purpose
Integrate with an external service via a dedicated adapter that enforces:
- timeouts
- retry policy
- idempotency where applicable
- error mapping into shared taxonomy
- observability (logs/metrics/traces) consistent with repo standards

This skill prevents “HTTP calls sprinkled everywhere.”

---

## Inputs
- External API/service name + base URL (or SDK)
- Required operations (list)
- Auth mechanism (token, key, oauth) WITHOUT secrets
- Expected failure cases (timeouts, rate limits, invalid responses)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Adapter module with a narrow interface
- Retry/timeout configuration
- Error mapping to shared taxonomy
- Contract tests or mocks (preferred)
- Minimal observability instrumentation

---

## Non-goals
- Implementing domain rules (use `backend/domain-logic-module`)
- Building orchestration/jobs (use `backend/job-worker-orchestration`)
- Storing secrets in code

---

## Workflow
1) Create adapter boundary:
   - `ExternalServiceClient` or module functions
2) Implement calls with:
   - explicit timeouts
   - bounded retries (with backoff) where safe
   - idempotency keys when supported/needed
3) Normalize errors:
   - map external errors to internal taxonomy
4) Add contract tests/mocks:
   - validate request construction
   - validate response parsing and error handling
5) Add basic observability:
   - correlation id propagation if present
6) Run validations per profile.

---

## Checks
- Adapter is the only place external calls exist for this integration
- Timeouts are explicit
- Retry policy is bounded and safe (no infinite loops)
- If retries, backoff, rate limiting, or multi-step external workflows are introduced,
 - recommend `system/state-machine-mapper` to model external interaction states explicitly.

- Errors map to internal taxonomy
- Tests cover:
  - success
  - timeout or retry scenario
  - bad response parsing

---

## Failure modes
- Retry safety unclear → default to no retry and document why.
- Rate limits encountered → add backoff and respect headers if available.
- External contract unstable → increase mocking/contract tests and tighten parsing.
- Retry/backoff logic added without explicit state modeling →
  require `system/state-machine-mapper` before shipping.

---

## Telemetry
Log:
- skill: `backend/integration-adapter`
- service: `<name>`
- retries: `none | bounded`
- timeout
