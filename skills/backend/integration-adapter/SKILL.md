# Skill: backend/integration-adapter

## Purpose
Create an external API adapter with timeouts, retries, error mapping, and idempotency where needed.

## Inputs
- External API base URL + auth method (high-level, no secrets)
- Required operations (list)
- Expected failure modes (rate limit, 5xx, timeouts)
- Repo profile (REPO_PROFILE.json) if present

## Outputs
- Adapter module exposing a small, typed interface
- Error mapping to shared/error-taxonomy
- Retry/timeout policy documented
- Tests using mocks or contract harness

## Config
- Use repo’s HTTP client conventions and observability hooks from REPO_PROFILE.json if present.

## Non-goals
- Do not leak external API shapes directly into domain code.
- Do not log secrets or full payloads.

## Checks
- Tests pass (mocked or contract).
- Observability fields include correlation IDs when available.

## Failure modes
- Flaky retries: tighten policy and add jitter/backoff.
- Leaky abstractions: wrap and normalize responses.
