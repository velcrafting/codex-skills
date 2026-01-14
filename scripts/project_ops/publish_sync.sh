#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOME}/.codex"
PUB="${ROOT}/publish"

mkdir -p "${PUB}"
rm -rf "${PUB}/skills" "${PUB}/scripts" "${PUB}/templates"
mkdir -p "${PUB}/skills" "${PUB}/scripts" "${PUB}/templates"

# Copy all skill groups automatically
if [ -d "${ROOT}/skills" ]; then
  for grp_path in "${ROOT}/skills"/*; do
    [ -d "${grp_path}" ] || continue
    grp="$(basename "${grp_path}")"

    mkdir -p "${PUB}/skills/${grp}"
    rsync -a --delete \
      --exclude "examples/**" \
      --exclude "templates/**" \
      "${grp_path}/" "${PUB}/skills/${grp}/"

  done
fi

if [ -d "${ROOT}/scripts" ]; then
  rsync -a --delete \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    "${ROOT}/scripts/" "${PUB}/scripts/"
fi

if [ -d "${ROOT}/templates" ]; then
  rsync -a --delete \
    "${ROOT}/templates/" "${PUB}/templates/"
fi

for f in SKILLS_REGISTRY.md SKILLS_TELEMETRY.md DOCS_MAP.md; do
  if [ -f "${ROOT}/${f}" ]; then
    rsync -a "${ROOT}/${f}" "${PUB}/${f}"
  fi
done

echo "Publish sync complete → ${PUB}"
cd "${PUB}"
git status
