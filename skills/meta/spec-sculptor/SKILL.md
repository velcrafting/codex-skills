name: spec-sculptor
description: Convert a storm of thoughts into a concise feature spec suitable for planning and implementation.
metadata:
  short-description: Ideas → spec
  mode: spec
  read-only: true

# Spec Sculptor

## Goal
Produce a concise spec that prevents implementation-by-guessing.

## Non-negotiables
- Read-only mode.
- No code, no file edits, no implementation steps.
- Capture edge cases and risks explicitly.

## Workflow
1) Summarize the user’s intent in 2–3 sentences.
2) Extract requirements and group them.
3) Identify conflicts and ask at most 3 follow-ups if truly necessary.
4) Output spec using template.

## Output template (follow exactly)

# Feature Spec

## Problem
<What problem are we solving and why now?>

## Users and scenarios
- <User type>: <scenario>
- <User type>: <scenario>

## Goals
- G1:
- G2:

## Non-goals
- NG1:
- NG2:

## Requirements
### Functional
- FR1:
- FR2:
- FR3:

### Data model (conceptual)
- Entities:
- Key fields:
- State machine:

### UX / Ops (if applicable)
- Surfaces:
- Operator actions:

## Edge cases
- E1:
- E2:
- E3:

## Risks and mitigations
- R1: <risk> → <mitigation>
- R2: <risk> → <mitigation>

## Open questions
- Q1:
- Q2:
- Q3:
