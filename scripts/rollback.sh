#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

: "${PRODUCTION_ENV_FILE:?Set PRODUCTION_ENV_FILE to the server-only environment file path}"
COMPOSE=(docker compose --project-name portfolio --env-file "$PRODUCTION_ENV_FILE" -f docker-compose.prod.yml)

for image in portfolio-backend:rollback portfolio-frontend:rollback; do
  if ! docker image inspect "$image" >/dev/null 2>&1; then
    echo "Rollback image is missing: $image" >&2
    exit 1
  fi
done

docker tag portfolio-backend:rollback portfolio-backend:current
docker tag portfolio-frontend:rollback portfolio-frontend:current

"${COMPOSE[@]}" run --rm backend python manage.py collectstatic --noinput
"${COMPOSE[@]}" up -d --remove-orphans --wait
"${COMPOSE[@]}" ps

echo "Application images were rolled back. Database migrations were not reversed."
