#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COMPOSE=(docker compose --project-name portfolio)
STATE_DIR="$ROOT_DIR/.deploy"
BEFORE_SHA="${1:-}"
CURRENT_SHA="${2:-$(git rev-parse HEAD)}"
mkdir -p "$STATE_DIR"

has_image() {
  docker image inspect "$1" >/dev/null 2>&1
}

snapshot_images() {
  if has_image portfolio-backend:current; then
    docker tag portfolio-backend:current portfolio-backend:rollback
  fi
  if has_image portfolio-frontend:current; then
    docker tag portfolio-frontend:current portfolio-frontend:rollback
  fi
}

restore_images() {
  local restored=false
  if has_image portfolio-backend:rollback; then
    docker tag portfolio-backend:rollback portfolio-backend:current
    restored=true
  fi
  if has_image portfolio-frontend:rollback; then
    docker tag portfolio-frontend:rollback portfolio-frontend:current
    restored=true
  fi

  if [[ "$restored" == true ]]; then
    echo "Restoring the previously tagged application images..."
    "${COMPOSE[@]}" up -d --no-build --remove-orphans --wait
  else
    echo "No previous application images exist; automatic rollback is unavailable on the first deploy." >&2
  fi
}

on_error() {
  local exit_code=$?
  trap - ERR
  echo "Deployment failed. Recent container logs:" >&2
  "${COMPOSE[@]}" logs --tail=150 --no-color >&2 || true
  restore_images || true
  exit "$exit_code"
}
trap on_error ERR

BUILD_BACKEND=false
BUILD_FRONTEND=false

if ! has_image portfolio-backend:current; then
  BUILD_BACKEND=true
fi
if ! has_image portfolio-frontend:current; then
  BUILD_FRONTEND=true
fi

if [[ -z "$BEFORE_SHA" || "$BEFORE_SHA" =~ ^0+$ ]] || ! git cat-file -e "${BEFORE_SHA}^{commit}" 2>/dev/null; then
  BUILD_BACKEND=true
  BUILD_FRONTEND=true
else
  CHANGED_FILES="$(git diff --name-only "$BEFORE_SHA" "$CURRENT_SHA")"
  if grep -Eq '^(backend/|docker-compose\.yml$)' <<<"$CHANGED_FILES"; then
    BUILD_BACKEND=true
  fi
  if grep -Eq '^(frontend/|docker-compose\.yml$)' <<<"$CHANGED_FILES"; then
    BUILD_FRONTEND=true
  fi
fi

"${COMPOSE[@]}" config --quiet
snapshot_images

SERVICES=()
[[ "$BUILD_BACKEND" == true ]] && SERVICES+=(backend)
[[ "$BUILD_FRONTEND" == true ]] && SERVICES+=(frontend)
if ((${#SERVICES[@]})); then
  echo "Building: ${SERVICES[*]}"
  "${COMPOSE[@]}" build --pull "${SERVICES[@]}"
else
  echo "No application image rebuild is required for this revision."
fi

"${COMPOSE[@]}" up -d --no-build --remove-orphans --wait
"${COMPOSE[@]}" ps

if [[ -f "$STATE_DIR/current-sha" ]]; then
  cp "$STATE_DIR/current-sha" "$STATE_DIR/previous-sha"
fi
printf '%s\n' "$CURRENT_SHA" > "$STATE_DIR/current-sha"

# Remove only dangling images older than seven days. Volumes are never pruned.
docker image prune --force --filter "until=168h"

trap - ERR
echo "Deployment completed at revision $CURRENT_SHA"
