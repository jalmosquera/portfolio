# 🏠 Portfolio production deployment

[← Back to documentation index](../README.md)

> [!IMPORTANT]
> This is a **homelab deployment**. Cloudflare Tunnel is the public edge; the application itself only listens on the server's loopback interface.

## 🏗️ Architecture

```text
Internet -> Cloudflare Tunnel -> 127.0.0.1:2323 -> Nginx
                                                         |-> React /
                                                         |-> Django /api and /admin
                                                         |-> /static and /media volumes
                                                              |
                                                              v
                                                         PostgreSQL
```

Only Nginx publishes a host port, bound to loopback. PostgreSQL and Gunicorn stay inside the Docker network.

## 🚀 First installation

Requirements: Git, Docker Engine and Docker Compose v2.

```bash
cd ~/projects
gh repo clone jalmosquera/portfolio
cd portfolio
docker compose up -d
docker compose ps
```

No `.env` file is required. A short-lived `secrets-init` container generates a persistent Django secret key and PostgreSQL password on first startup. They live in the named volume `portfolio_secrets_data` and are reused on every restart.

The backend entrypoint waits for PostgreSQL through Compose dependencies, applies migrations, collects static files and then starts Gunicorn.

## ❤️ Verification

```bash
curl --fail http://127.0.0.1:2323/healthz
curl --fail \
  -H 'Host: portfolio.mosquerasoft.com' \
  -H 'X-Forwarded-Proto: https' \
  http://127.0.0.1:2323/api/health/

docker compose ps
docker compose logs --tail=200 frontend backend db
```

Backend, frontend and db must report `healthy`. `secrets-init` must report `Exited (0)`.

## ☁️ Cloudflare Tunnel

Create the published hostname:

```text
Public hostname: portfolio.mosquerasoft.com
Service type:    HTTP
Service URL:     http://127.0.0.1:2323
```

No router ports need to be opened. Protecting `/admin/` with Cloudflare Access remains recommended.

## 🔄 Updates

### Automated delivery

Every push to `main` starts `.github/workflows/deploy-production.yml`. After validation succeeds, the self-hosted homelab runner executes `scripts/deploy.sh` with the exact previous and current Git revisions.

The script:

- validates the Compose configuration;
- tags the current application images for rollback;
- rebuilds only the backend and/or frontend affected by the revision;
- waits for healthy containers;
- restores the previous images automatically if deployment fails.

When the GitHub Actions run is green, no manual server update is required.

### Manual recovery/update

If the runner is unavailable and a manual update is intentionally required:

```bash
cd ~/projects/portfolio
git pull --ff-only origin main
docker compose up -d --build --remove-orphans --wait
```

## ⚙️ Optional overrides

The defaults already target `portfolio.mosquerasoft.com` and port `2323`. To customize them:

```bash
cp .env.example .env
nano .env
docker compose up -d
```

`.env` is ignored by Git. Application secrets are still generated inside the persistent secrets volume.

## 💾 Persistent data

Named volumes:

- `portfolio_postgres_data`: PostgreSQL database.
- `portfolio_media_data`: uploaded project images and CV.
- `portfolio_static_data`: generated Django static files.
- `portfolio_secrets_data`: generated Django and database secrets.

Normal stops and rebuilds preserve them:

```bash
docker compose down
docker compose up -d
```

Never use `docker compose down -v` in production unless you intentionally want to delete all portfolio data and generated secrets.

The PostgreSQL and secrets volumes form one recovery set. Never delete only `portfolio_secrets_data` while preserving `portfolio_postgres_data`, because the regenerated database password would no longer match the existing database.

## 🪵 Logs

```bash
docker compose ps
docker compose logs --tail=200 frontend backend db
docker compose logs --follow backend frontend
```

## ↩️ Rollback

GitHub Actions tags the prior backend/frontend images as `rollback`. Restore them with:

```bash
./scripts/rollback.sh
```

Rollback restores application images but does not reverse database migrations.

## 🛟 Backups

Back up:

- PostgreSQL using `pg_dump`;
- `portfolio_media_data`;
- `portfolio_secrets_data`.

Static files and application images are reproducible and do not require backup.

## 💻 Local development without Docker

Docker Compose now represents production. For local development, run Django and Vite directly in their respective directories using their development commands; when `DB_NAME` is absent Django continues using SQLite.

See [💻 Local development](development.md) for the complete setup.
