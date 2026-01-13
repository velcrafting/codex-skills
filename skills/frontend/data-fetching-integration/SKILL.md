# Skill: frontend/data-fetching-integration

## Purpose
Wire UI to an API/data source with typed inputs/outputs, loading/error states, and caching rules.

## Inputs
- Endpoint contract (method/path/req/res) or data source description
- UI entry point(s) needing data
- Repo profile (REPO_PROFILE.json) if present

## Outputs
- Client call or API wrapper usage
- Query/mutation hook (or equivalent abstraction used by the repo)
- UI states: loading, error, empty, success
- Cache key + invalidation/refetch rules documented in code comments

## Config
- Follow repo data tooling (React Query/SWR/custom) as defined in REPO_PROFILE.json.
- If missing, ask which data layer is used and whether optimistic updates are allowed.

## Non-goals
- Do not change backend contracts.
- Do not implement business rules client-side beyond display and basic validation.

## Checks
- Run required checks from REPO_PROFILE.json.
- Confirm UI handles the four states (loading/error/empty/success).

## Failure modes
- Stale cache: fix keys/invalidation.
- Race conditions: cancellation/latest-only guards.
