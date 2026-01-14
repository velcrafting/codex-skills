---
name: data-fetching-integration
description: Wire UI to a data source with typed inputs/outputs, loading/error/empty states, and caching rules.
metadata:
  short-description: Data hookup + UI states
  layer: frontend
  mode: write
  idempotent: false
---

# Skill: frontend/data-fetching-integration

## Purpose
Connect UI to an API/data source using the repo’s data tooling, ensuring:
- typed inputs/outputs
- correct UI state handling
- explicit caching and invalidation behavior

---

## Inputs
- Data source definition:
  - endpoint contract (method/path/request/response) OR
  - client function signature OR
  - data description (if contract not formalized yet)
- UI entry point(s) that need the data
- Expected behavior:
  - read vs write
  - polling or realtime needs
  - optimistic updates allowed (yes/no)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Data call wired via repo tooling (React Query/SWR/custom)
- A hook / loader / data module consistent with repo patterns
- UI state coverage:
  - loading
  - error
  - empty
  - success
- Explicit cache key strategy and invalidation/refetch rules (code comments or helper constants)

---

## Non-goals
- Changing backend behavior or contracts
- Adding business rules client-side beyond presentation and basic form validation
- Building a new data layer abstraction unless explicitly requested

---

## Workflow
1) Identify the repo’s data fetching pattern (prefer `REPO_PROFILE.json`).
2) Implement the data call using existing client conventions.
3) Define a stable cache key derived from request inputs.
4) Add invalidation rules:
   - mutations invalidate queries that depend on changed data
   - avoid global invalidation unless required
5) Implement UI states:
   - loading: skeleton/spinner (repo standard)
   - error: recoverable messaging + retry path if appropriate
   - empty: explicit “no data” state
   - success: render
6) Run required validations (typecheck/lint/tests per profile).

---

## Checks
- Typecheck passes (if configured)
- UI handles loading/error/empty/success states deterministically
- Cache key is stable and unique
- Invalidation/refetch behavior is explicit
- No silent swallowing of errors

---

## Failure modes
- Data tooling unclear → ask which is used (React Query/SWR/custom) and default caching expectations.
- Stale cache → fix keys and invalidation rules; avoid ad-hoc refetch loops.
- Race conditions → add latest-only guards, cancellation, or stable request identity.
- Contract ambiguity → recommend `api/contract-update` or `shared/schema-types` before hard wiring.

---

## Telemetry
Log:
- skill: `frontend/data-fetching-integration`
- data_tooling: `react-query | swr | custom | unknown`
- cache_keys_added_or_changed
- files_touched
- outcome: `success | partial | blocked`
