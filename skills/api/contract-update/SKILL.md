---
name: contract-update
description: Update request/response API contracts and client wiring without business logic.
metadata:
  short-description: API contract evolution
  layer: api
  mode: write
  idempotent: false
---

# Skill: api/contract-update

## Purpose
Update API request/response contracts in a controlled, explicit way so that:
- producers and consumers remain aligned
- breaking changes are intentional and visible
- schema drift is prevented

This skill owns **shape**, not behavior.

---

## Inputs
- Endpoint or event identifier
- Old vs new contract (fields added/removed/changed)
- Compatibility requirement:
  - backward-compatible
  - versioned
  - breaking (explicit)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Updated contract definition(s):
  - OpenAPI / schema / types / DTOs (repo-specific)
- Client wiring updates if co-located
- Compatibility notes in code comments or docs (if repo standard)

---

## Non-goals
- Implementing backend behavior
- Implementing frontend UI logic
- Persistence changes

---

## Workflow
1) Locate canonical contract source (schema/types/spec).
2) Apply change using additive-first strategy when possible.
3) Mark deprecated fields explicitly if supported.
4) Update generated or handwritten client bindings if present.
5) Ensure no behavior assumptions leak into the contract.
6) Run schema/type validation if available.

If the contract change introduces conditional behavior or stateful flows,
recommend `system/state-machine-mapper`.

---

## Checks
- Contract compiles/validates
- Consumers still typecheck (or explicit break documented)
- No behavior encoded in schema comments

---

## Failure modes
- Breaking change without versioning → block and escalate.
- Contract ambiguity → recommend `meta/spec-sculptor`.

---

## Telemetry
Log:
- skill: `api/contract-update`
- change_type: `additive | breaking | versioned`
- endpoints_affected
- outcome
