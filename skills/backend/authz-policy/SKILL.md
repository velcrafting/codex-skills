---
name: authz-policy
description: Define and enforce authorization rules for protected actions, with tests and audit considerations.
metadata:
  short-description: Authz policy + enforcement
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/authz-policy

## Purpose
Define and enforce authorization policy so protected actions are:
- explicitly allowed/denied by rule
- consistently enforced at boundaries
- tested (cannot regress silently)
- auditable when required

This skill is about authorization (authz), not authentication (authn).

---

## Inputs
- Protected action(s) (what is being guarded)
- Actors/roles (who is allowed)
- Resources (what is being accessed or modified)
- Constraints:
  - tenant boundaries
  - ownership rules
  - admin overrides
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Policy definition:
  - rule function(s) or policy module (repo convention)
- Enforcement:
  - middleware/guard checks applied at the correct boundary
- Error behavior:
  - consistent deny response and error mapping
- Tests:
  - allow path
  - deny path
  - at least one edge case (missing role, wrong tenant, etc.)
- Optional: audit hook notes if action is sensitive

---

## Non-goals
- Authentication mechanism changes (login/session/token)
- Business logic changes unrelated to authz
- UI permission gating as the primary enforcement (UI may mirror but is not security)

---

## Workflow
1) Identify existing authz pattern:
   - middleware, decorators, policy objects, ability system
   - prefer `REPO_PROFILE.json`
2) Express the rule explicitly:
   - `can(actor, action, resource) -> bool` style or repo standard
3) Enforce at boundary:
   - endpoint handlers, job entry points, command handlers
   - fail closed by default
4) Ensure error shape is consistent:
   - map to shared taxonomy if present (`shared/error-taxonomy`)
5) Add tests:
   - allow/deny/edge
6) Consider auditability:
   - if action is sensitive, ensure `backend/observability-audit` is run or recommended
7) Run validations.

If authz introduces multi-step conditional flows (escalation, approvals, staged unlocks),
recommend `system/state-machine-mapper`.

---

## Checks
- Protected actions fail closed (no implicit allow)
- Policy rules are centralized (not duplicated across handlers)
- Tests prove deny cannot be bypassed
- Error response matches repo taxonomy
- No sensitive data leaked in deny responses

---

## Failure modes
- Roles/ownership unclear → block and recommend `$decision-capture`.
- Multiple inconsistent checks exist → consolidate into a single policy module.
- Edge cases discovered (tenant leakage) → treat as high severity and stop.

---

## Telemetry
Log:
- skill: `backend/authz-policy`
- actions: count
- enforcement_points: count
- tests_added: `yes | no`
- files_touched
- outcome: `success | partial | blocked`
