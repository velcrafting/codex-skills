---
name: governance-sync
description: End-of-work audit that identifies which governance artifacts should be updated based on actual changes. Use when wrapping a milestone/checkpoint or after multi-file/structural work.
---
# Governance Sync

## Goal
Keep governance artifacts truthful with minimal churn.

## Non-negotiables
- Read-only. Do not edit files automatically.
- Recommend updates only when triggered by actual changes.
- Be explicit about what changed and why that forces a doc update.

## Workflow
1) Inspect what changed
- Prefer git diff/summary when available, otherwise use the user’s change summary.

2) Determine which artifacts’ truth conditions changed
Common candidates:
- Tree map (Tree.txt / tree.md)
- Roadmap (roadmap.md)
- Architecture docs (ARCHITECTURE.md)
- Agent rules (AGENTS.md)
- Decision log (DECISIONS.md)
- Review queue (REVIEW_QUEUE.md)
- Suggestions log (SUGGESTIONS.md)
- Domain docs (docs/*)

3) Output a delta checklist

## Output (follow exactly)

# Governance Sync

## Trigger summary
- Change type: <bugfix | feature | refactor | restructure | docs>
- Structural change: <yes/no>
- Decision required: <yes/no>

## Required updates
[ ] <File>: <exact update needed and why>

## Optional updates
[ ] <File>: <nice-to-have update and why>

## Risks if skipped
- <Risk 1>
- <Risk 2>
