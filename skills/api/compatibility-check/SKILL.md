---
name: compatibility-check
description: Validate API compatibility across versions or consumers.
metadata:
  short-description: API compatibility gate
  layer: api
  mode: read-only
  idempotent: true
---

# Skill: api/compatibility-check

## Purpose
Determine whether an API change is:
- backward-compatible
- conditionally compatible
- breaking

And make that status explicit before shipping.

---

## Inputs
- Old contract
- New contract
- Known consumers (if available)

---

## Outputs
- Compatibility assessment:
  - compatible / breaking / unsafe
- Explicit list of breaking changes (if any)
- Recommendation:
  - proceed
  - version
  - block

---

## Non-goals
- Modifying contracts
- Updating clients
- Implementing migrations

---

## Workflow
1) Compare old vs new contract shapes.
2) Identify removed or behaviorally changed fields.
3) Assess consumer impact.
4) Emit a clear compatibility verdict.

---

## Checks
- All removals and type changes enumerated
- Verdict is explicit and justified

---

## Failure modes
- Missing baseline contract → block and request one.
- Ambiguous change → recommend `meta/spec-sculptor`.

---

## Telemetry
Log:
- skill: `api/compatibility-check`
- verdict
- affected_consumers
- outcome
