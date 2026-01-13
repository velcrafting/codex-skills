#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/.codex"
PUB="${ROOT}/publish"

# Start clean (but keep git metadata if you init a repo in publish/)
mkdir -p "${PUB}"
rm -rf "${PUB}/skills" "${PUB}/scripts" "${PUB}/templates"
mkdir -p "${PUB}/skills" "${PUB}/scripts" "${PUB}/templates"

# Copy only selected skill groups (edit this list)
for grp in meta system frontend backend shared api project-ops; do
  if [ -d "${ROOT}/skills/${grp}" ]; then
    mkdir -p "${PUB}/skills/${grp}"
    rsync -a --delete \
      --exclude "examples/**" \
      --exclude "templates/**" \
      "${ROOT}/skills/${grp}/" "${PUB}/skills/${grp}/"
  fi
done

# Copy selected scripts (edit this list)
if [ -d "${ROOT}/scripts" ]; then
  rsync -a --delete \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    "${ROOT}/scripts/" "${PUB}/scripts/"
fi

# Copy templates (optional)
if [ -d "${ROOT}/templates" ]; then
  rsync -a --delete \
    "${ROOT}/templates/" "${PUB}/templates/"
fi

# Copy top-level docs you want published (edit this list)
for f in SKILLS_REGISTRY.md SKILLS_TELEMETRY.md DOCS_MAP.md; do
  if [ -f "${ROOT}/${f}" ]; then
    rsync -a "${ROOT}/${f}" "${PUB}/${f}"
  fi
done

echo "Publish sync complete → ${PUB}"
