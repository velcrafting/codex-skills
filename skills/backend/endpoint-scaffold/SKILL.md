# Skill: backend/endpoint-scaffold

## Purpose
Create a production-grade API endpoint with validation, auth, error mapping, and tests.

## Inputs
- Method + path
- Request/response schema (or described fields)
- Auth/authz requirement
- Expected error cases
- Repo profile (REPO_PROFILE.json) if present

## Outputs
- Route/handler wired into the app
- Validation (schema + coercion rules)
- Auth/authz enforcement
- Error taxonomy mapping (consistent codes/messages)
- Tests: at least one success + one failure

## Config
- Follow backend framework + command set from REPO_PROFILE.json.
- If missing, ask which framework and how routes/tests are structured.

## Non-goals
- Do not add persistence changes unless explicitly required.
- Do not embed domain logic in the transport layer.

## Checks
- Run required checks from REPO_PROFILE.json.
- Ensure endpoint returns correct status codes and error shapes.

## Failure modes
- Missing auth guard: add enforcement at entry point.
- Unstable schema: extract to shared schema-types.
