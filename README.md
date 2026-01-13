# Codex Kit

This repository is a **published distribution of a local Codex runtime**.

It contains reusable skills, scripts, templates, and governance documents
used to operate Codex as a structured development system.

## What this repo is
- A **clean, shareable subset** of a local Codex installation
- Intended for:
  - reuse across machines
  - sharing with collaborators
  - publishing to GitHub
- Generated deterministically from a local runtime

## What this repo is not
- Not the runtime environment
- Not machine-specific
- Not where telemetry, logs, or auth live
- Not edited directly

## Source of truth
- Runtime lives at: `~/.codex/`
- This repo lives at: `~/.codex/publish/`
- This repo is generated via:
  ```sh
  ~/.codex/scripts/project_ops/publish_sync.sh
