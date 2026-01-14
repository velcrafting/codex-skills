---
name: observability-audit
description: Ensure logging/metrics/tracing and auditability match the quality bar for changed behavior.
metadata:
  short-description: Observability pass
  layer: backend
  mode: write
  idempotent: true
---

# Skill: backend/observability-audit

## Purpose
Improve and standardize observability so the system is operable after changes:
- logs: structured, queryable, minimal but sufficient
- metrics: counters/timers/gauges for key outcomes
- traces: propagation and spans where available
- audit: records for sensitive actions when required

This skill is a pass over changed behavior, not feature work.

---

## Inputs
- Changed components/endpoints/jobs
- Risk posture (from repo docs/profile if present)
- Observability standards (from `REPO_PROFILE.json` if present)
- Correlation/id propagation standard (if any)

---

## Outputs
- Improved logging:
  - include correlation id
  - include primary identifiers (request id, user id where safe, entity id)
  - include outcome + error codes
- Metrics updates if repo uses them:
  - success/fail counters
  - latency timing
  - queue depth / retries (for jobs)
- Tracing spans or propagation fixes if repo uses tracing
- Audit entries for protected actions if applicable

---

## Non-goals
- Implementing business logic
- Adding heavy instrumentation everywhere
- Logging secrets or sensitive payloads

---

## Workflow
1) Identify repo observability standards (profile/docs).
2) Add structured logs at critical boundaries:
   - request start/end
   - job start/end
   - external call start/end (adapter boundary)
3) Ensure errors are observable:
   - log error codes/taxonomy, not raw stack spam only
   - include retry decisions (retrying vs terminal)
4) Add metrics if the repo uses them:
   - count outcomes
   - measure latency
5) Ensure correlation ids propagate:
   - inbound request → domain → adapter → logs
6) Add audit entries where required:
   - authz-protected actions
   - fund movement / order placement / credential updates (example categories)
7) Run validations.

---

## Checks
- Logs answer: what happened, to what, by whom (when safe), and why
- No secrets logged; sensitive values redacted
- Correlation id present on critical flows (where available)
- Metrics/tracing updated when repo supports them
- Changes are minimal and focused on the modified behavior

---

## Failure modes
- No logging standard → follow conservative structured logging and document assumptions.
- High-cardinality metrics risk → avoid unbounded labels.
- Sensitive data risk → redact or omit; prefer identifiers over payloads.

---

## Telemetry
Log:
- skill: `backend/observability-audit`
- areas: `logs | metrics | tracing | audit` (subset)
- files_touched
- outcome: `success | partial | blocked`
