# Jalberth Mosquera Portfolio

Production is intentionally a one-command Docker Compose stack.

```bash
git clone https://github.com/jalmosquera/portfolio.git
cd portfolio
docker compose up -d
```

Every startup uses Docker's build cache to ensure the containers match the checked-out code. The first startup automatically:

- generates persistent Django and PostgreSQL secrets;
- creates the PostgreSQL, media and static volumes;
- applies Django migrations and runs `collectstatic`;
- starts Django with Gunicorn;
- serves React, `/api`, `/admin`, `/static` and `/media` through Nginx;
- exposes only `127.0.0.1:2323` for Cloudflare Tunnel.

Check the stack:

```bash
docker compose ps
curl --fail http://127.0.0.1:2323/healthz
```

See [`docs/production-deployment.md`](docs/production-deployment.md) for Cloudflare, updates, backups and optional overrides.
