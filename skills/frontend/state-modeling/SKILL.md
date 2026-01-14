---
name: state-modeling
description: Define client state shape and transitions for non-trivial UI flows (multi-step, branching, async, derived state).
metadata:
  short-description: Explicit UI state + transitions
  layer: frontend
  mode: write
  idempotent: false
---

# Skill: frontend/state-modeling

## Purpose
Make non-trivial UI state explicit and testable by defining:
- state shape
- transitions
- derived selectors
- async and error pathways

Use when UI behavior is more than “render props and call an API”.

---

## Inputs
- Target UI flow (screen/component) and its states
- Events/actions that cause transitions
- Any async edges (fetch, debounce, retry, polling)
- Existing state system:
  - local state / reducer
  - context
  - Zustand/Redux/XState/etc (prefer repo profile)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- State model implementation aligned with repo patterns:
  - reducer/state machine/store module as appropriate
- Transition definitions (explicit mapping from event → next state)
- Derived selectors/utilities where needed
- Minimal tests if repo uses state unit tests (recommended when non-trivial)

---

## Non-goals
- Changing backend logic or API contracts
- Introducing new state libraries without explicit request
- Large refactors unrelated to the target flow

---

## Workflow
1) Identify the smallest state model that makes behavior explicit.
2) Enumerate states and events:
   - idle, loading, success, error, empty (if data-driven)
   - plus domain-specific UI states (editing, confirming, submitting, etc.)
3) Implement transitions:
   - event-driven (actions)
   - include error and retry transitions
   - include cancellation/reset paths if applicable
4) Keep rendering components dumb:
   - state model owns transitions
   - UI consumes state + dispatches events
5) Validate with repo commands and minimal tests where appropriate.

---

## Checks
- State transitions cover all expected UI paths
- Async flows have deterministic handling (retry/cancel/timeout if relevant)
- No unreachable or dead-end states introduced
- Typecheck passes (if configured)

---

## Failure modes
- Flow is ambiguous → invoke `$ask-questions-if-underspecified` or `meta/intake-interview`.
- State complexity growing uncontrolled → recommend splitting into sub-flow modules.
- Async edge cases missed → recommend `system/state-machine-mapper` for very complex flows.

---

## Telemetry
Log:
- skill: `frontend/state-modeling`
- state_system_used: `useReducer | zustand | redux | xstate | context | other`
- files_touched
- outcome: `success | partial | blocked`
