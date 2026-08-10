#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COMPOSE=(docker compose --project-name portfolio)

for image in portfolio-backend:rollback portfolio-frontend:rollback; do
  if ! docker image inspect "$image" >/dev/null 2>&1; then
    echo "Rollback image is missing: $image" >&2
    exit 1
  fi
done

docker tag portfolio-backend:rollback portfolio-backend:current
docker tag portfolio-frontend:rollback portfolio-frontend:current

"${COMPOSE[@]}" up -d --no-build --remove-orphans --wait
"${COMPOSE[@]}" ps

echo "Application images were rolled back. Database migrations were not reversed."
