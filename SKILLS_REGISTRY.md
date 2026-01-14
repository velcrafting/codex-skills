# Skills Registry

This repo uses skills as repeatable, verifiable work units.
Skills are grouped by responsibility boundary.

## Skill groups
- meta: planning, intake, governance, decision capture
- system: cross-cutting governance artifacts (architecture contracts, state machines, invariants)
- frontend: UI, client state, accessibility, performance
- backend: domain rules, persistence, integrations, jobs, observability
- shared: primitives and contracts only (no side effects)
- api (optional): request/response contracts and client wiring (no business rules)

## How to choose a skill
Pick the smallest skill that can produce a verifiable artifact.
If a task spans layers, invoke multiple skills and log each.

## Skill index
A quick map of what exists and what it’s for (one-line descriptions only).
For full contracts, see each skill’s `SKILL.md`.

### meta
- meta/ask-questions-if-underspecified: Ask minimal clarifying questions when requirements are ambiguous.
- meta/bootstrap-repo: Create or refresh the standard repo scaffold and runtime folders.
- meta/create-plan: Produce an executable work plan with scope, steps, validation, and risks.
- meta/decision-capture: Record non-trivial decisions and tradeoffs in a durable log.
- meta/governance-sync: Bring repo governance docs back into alignment with current reality.
- meta/intake-interview: Produce an Intake Brief capturing intent, constraints, and success criteria.
- meta/personalize-repo: Tailor governance docs and create repo-local `REPO_PROFILE.json`.
- meta/spec-sculptor: Convert loose requirements into a tighter spec artifact suitable for execution.

### system
- system/system-contract-map: Maintain system-level contract diagrams and cross-boundary invariants.
- system/state-machine-mapper: Model component/service behavior as a state machine for branching or async flows.

### frontend
- frontend/component-scaffold: Add a new component following repo conventions and exports.
- frontend/data-fetching-integration: Connect UI to data source with typed calls, UI states, and caching rules.
- frontend/state-modeling: Define client state shape and transitions for non-trivial flows.
- frontend/a11y-semantics-pass: Improve semantics and accessibility coverage for UI changes.
- frontend/performance-pass-ui: Identify and reduce avoidable UI performance regressions.
- frontend/form-validation: Add input validation rules and UX patterns for forms.
- frontend/frontend-test-additions: Add or extend UI tests to cover intended behavior.
- frontend/ui-refactor-extract: Refactor UI code without behavior change (extract/rename/reorganize).

### backend
- backend/endpoint-scaffold: Create a validated, authorized endpoint with error mapping and tests.
- backend/domain-logic-module: Add or refactor domain rules in a testable module boundary.
- backend/persistence-layer-change: Implement schema/migration changes and update access patterns safely.
- backend/integration-adapter: Build an external API adapter with retries/timeouts/error mapping.
- backend/job-worker-orchestration: Add background jobs and orchestration with idempotency and observability.
- backend/observability-audit: Ensure logging/metrics/tracing and auditability match the quality bar.
- backend/backend-test-additions: Add or extend backend tests for new behavior or regressions.
- backend/authz-policy: Define and enforce authorization rules for protected actions.

### shared
- shared/primitives: Define stable primitives (types, helpers) with no side effects.
- shared/schema-types: Define shared schemas/types used across layers.
- shared/error-taxonomy: Define and enforce error codes/shapes across boundaries.
- shared/ids-correlation: Define correlation/trace identifiers and propagation rules.
- shared/time-units: Define canonical time units/durations and conversions.

### api (optional)
- api/contract-update: Update request/response contracts and client wiring (no business rules).
- api/client-generation: Generate or update typed API clients from canonical contracts.
- api/compatibility-check: Assess whether an API change is backward-compatible or breaking.

## Decision guide

### Add a new API endpoint
- backend/endpoint-scaffold
- shared/error-taxonomy
- shared/schema-types
- api/contract-update (if used)
Checks: unit or integration tests, typecheck, lint

### Make a breaking API change
- api/compatibility-check
- api/contract-update
- api/client-generation (if clients are generated)
- meta/decision-capture (if the break is non-trivial)
Checks: contract validation, consumer typecheck, versioning or migration notes

### Add a new DB column or table
- backend/persistence-layer-change
- backend/domain-logic-module (if invariants change)
- backend/observability-audit (if audit needed)
Checks: migration up, tests, typecheck

### Add a new UI screen backed by API data
- frontend/component-scaffold
- frontend/data-fetching-integration
- frontend/state-modeling
- frontend/a11y-semantics-pass
Checks: typecheck, lint, basic UI state coverage

### Refactor existing UI without behavior change
- frontend/ui-refactor-extract
- frontend/frontend-test-additions
Checks: tests, typecheck

### External API integration
- backend/integration-adapter
- backend/observability-audit
- shared/error-taxonomy
Checks: contract tests or mocks, timeouts, retry policy

### Add a background job / scheduled worker
- backend/job-worker-orchestration
- backend/observability-audit
- backend/backend-test-additions
Checks: idempotency proven, retries bounded, logs/metrics present, tests cover retry + terminal failure

### Change authorization rules for a protected action
- backend/authz-policy
- shared/error-taxonomy (if deny shapes/codes change)
- backend/backend-test-additions
- backend/observability-audit (if action is sensitive)
Checks: fail-closed enforced, allow/deny tests, no sensitive leakage in deny responses

### Change cross-boundary architecture or core system structure
- system/system-contract-map
Checks: diagrams updated under `docs/diagrams/system`, invariants updated, sequences reflect current flow

### Change behavior of a component or service with branching or async flow
- system/state-machine-mapper *(especially for retries, polling, job orchestration, staged authz, or multi-step workflows)*
Checks: colocated `*.state-machine.md` updated, transition table covers all code paths, error and retry paths modeled

## Diagram artifacts
Some skills require durable artifacts outside `.codex/`:
- `system/system-contract-map` writes to `docs/diagrams/system/`
- `system/state-machine-mapper` writes colocated `*.state-machine.md` next to the code it describes

## Skill contract requirements
Every skill must define:
- purpose, inputs, outputs, non-goals
- checks that prove success
- failure modes and recovery steps

## Telemetry
All skill invocations must append a record to:
- repo: `.codex/telemetry/skills.telemetry.jsonl`
Optionally also append to:
- global: `~/.codex/telemetry/skills.telemetry.jsonl`
See `SKILLS_TELEMETRY.md` for schema.

Note: The canonical, publishable Codex distribution lives in `~/.codex/publish/` and is generated via `scripts/project_ops/publish_sync.sh`.
