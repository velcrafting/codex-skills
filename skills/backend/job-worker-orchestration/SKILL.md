---
name: job-worker-orchestration
description: Add background jobs and orchestration with idempotency, retries, and observability aligned to repo conventions.
metadata:
  short-description: Jobs + orchestration
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/job-worker-orchestration

## Purpose
Implement background work safely using the repo’s job system (queue/cron/worker) with:
- explicit idempotency guarantees
- bounded retries and backoff
- durable state and re-entrancy safety
- observability (logs/metrics/traces) sufficient to operate it

Use when work is async, scheduled, long-running, or must survive restarts.

---

## Inputs
- Job intent (what it does, why it’s async)
- Trigger type:
  - event-driven (enqueue)
  - scheduled (cron)
  - periodic poller
- Payload shape (fields + types)
- Idempotency key strategy (preferred) or invariants that ensure idempotency
- Failure expectations:
  - transient vs permanent errors
  - acceptable delay
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Job definition/handler
- Enqueue/schedule wiring
- Idempotency mechanism:
  - idempotency key + dedupe storage OR
  - safe “exactly-once-ish” strategy documented
- Retry/backoff policy (bounded)
- Dead-letter or quarantine path if repo supports it
- Tests:
  - unit tests for handler logic
  - integration tests for enqueue/execute when infrastructure exists
- Minimal operational notes (inline comments or docs per repo norms)

---

## Non-goals
- Implementing domain rules inside the job handler (use `backend/domain-logic-module`)
- External API integration details (use `backend/integration-adapter` for the adapter)
- Schema changes beyond what is needed for idempotency tracking (use `backend/persistence-layer-change` if substantial)

---

## Workflow
1) Identify job framework and conventions (prefer `REPO_PROFILE.json`).
2) Define the job contract:
   - payload schema
   - execution guarantees
   - expected side effects
3) Establish idempotency:
   - choose key, define dedupe boundary
   - ensure retries do not duplicate side effects
4) Implement handler as orchestrator:
   - call domain modules and adapters
   - keep handler thin
5) Define retry policy:
   - bounded attempts
   - backoff strategy
   - classify errors (retryable vs not)
6) Add dead-letter/quarantine behavior if supported:
   - after max retries, record failure and stop looping
7) Add observability:
   - log start/end + key fields
   - emit metrics counters/timers if repo uses them
   - propagate correlation ids if present
8) Add tests.
9) Run repo validations.

If this job introduces multi-step branching, retries, polling states, or backoff logic,
recommend `system/state-machine-mapper` unless explicitly waived.

---

## Checks
- Idempotency is explicit and correct for all side effects
- Retry/backoff is bounded and safe
- Permanent failures do not loop forever
- Observability exists to answer:
  - did it run?
  - did it succeed?
  - why did it fail?
  - will it retry?
- Tests cover:
  - happy path
  - one retryable failure path
  - one non-retryable failure path (or max-retry behavior)
- Typecheck/lint/tests pass if configured

---

## Failure modes
- Idempotency unclear → block until defined (do not ship “best effort”).
- Job framework unknown → consult repo docs/profile or recommend `personalize-repo`.
- Retry policy unsafe → default to no retry and document why.
- Side effects scattered → extract to domain modules/adapters.

---

## Telemetry
Log:
- skill: `backend/job-worker-orchestration`
- trigger: `event | cron | poller`
- idempotency: `keyed | invariant | unknown`
- retries: `none | bounded`
- tests_added: `unit | integration | none`
- files_touched
- outcome: `success | partial | blocked`
