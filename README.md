# 🚀 Jalberth Mosquera — Self-Hosted Portfolio

[![Spanish documentation](https://img.shields.io/badge/README-Español-F17D34?style=for-the-badge)](README.es.md)

> [!IMPORTANT]
> **This portfolio is deployed in a private homelab.** Production traffic reaches the application through a Cloudflare Tunnel connected to an Nginx container bound exclusively to `127.0.0.1:2323`. PostgreSQL and Django are never exposed directly to the Internet.

A bilingual, database-driven portfolio for showcasing real client projects, generating dynamic CVs and receiving contact inquiries. It combines a React frontend with a Django REST API and a production-ready Docker Compose stack designed for self-hosting.

## 📚 Documentation index

Use this README as the starting point. Each topic links to a focused document with the implementation details.

| Topic | What you will find |
| --- | --- |
| [🏗️ Architecture](docs/architecture.md) | Request flow, containers, security boundaries and major design decisions |
| [🗄️ Database](docs/database.md) | PostgreSQL/SQLite strategy, domain models, relationships, persistence and backups |
| [📁 Project structure](docs/project-structure.md) | Repository map and responsibilities of the main folders |
| [🔌 API](docs/api.md) | Public endpoints, language negotiation, admin and API documentation |
| [💻 Local development](docs/development.md) | Python and Node setup, migrations, tests, linting and email templates |
| [🏠 Homelab deployment](docs/production-deployment.md) | Cloudflare Tunnel, Docker Compose, health checks, updates, rollback and backups |

## ✨ Highlights

- 🌍 Complete English and Spanish experience with Django Parler and frontend translations.
- 🧩 Portfolio content managed from Django Admin instead of hardcoded pages.
- 🖼️ Featured projects, galleries, technology details, lessons learned and case studies.
- 📄 Dynamic compact and visual CV generation from database content.
- ✉️ Gmail SMTP notifications and bilingual contact confirmations styled with React Email.
- 📊 Private visit counter visible from Django Admin.
- 🐳 One-command production startup with Docker Compose.
- 🏠 Automated deployment to a self-hosted homelab through a GitHub Actions runner.
- ↩️ Application-image rollback without exposing the database or Gunicorn publicly.

## 🧰 Technology stack

| Layer | Technologies |
| --- | --- |
| Frontend | React 19, Vite 8, Tailwind CSS 4, Axios, React Router, Sileo |
| Backend | Python 3.11, Django 5.2, Django REST Framework, Django Parler |
| Data | PostgreSQL 17 in production, SQLite fallback for local development |
| Documents & email | ReportLab, React Email, Gmail SMTP |
| Edge & runtime | Nginx, Gunicorn, Docker Compose, Cloudflare Tunnel |
| Quality & delivery | Pytest, ESLint, GitHub Actions, self-hosted runner |

## 🧭 Production request flow

```text
Internet
   │
   ▼
Cloudflare Tunnel
   │
   ▼
127.0.0.1:2323 ──► Nginx
                      ├── /              React SPA
                      ├── /api/*         Django + Gunicorn
                      ├── /admin/*       Django Admin
                      ├── /media/*       Persistent uploads
                      └── /static/*      Collected Django assets
                                            │
                                            ▼
                                      PostgreSQL 17
```

Only Nginx publishes a host port, and that port listens on loopback. See [🏗️ Architecture](docs/architecture.md) for the complete container and trust-boundary explanation.

## ⚡ Run the production stack

Requirements: Git, Docker Engine and Docker Compose v2.

```bash
git clone https://github.com/jalmosquera/portfolio.git
cd portfolio
docker compose up -d
```

The first startup automatically:

1. 🔐 Generates persistent Django and PostgreSQL secrets.
2. 🗄️ Creates the PostgreSQL, media, static and secrets volumes.
3. 🔄 Applies Django migrations and collects static files.
4. 🦄 Starts Django through Gunicorn.
5. 🌐 Starts Nginx with the compiled React application.
6. ❤️ Waits for PostgreSQL, backend and frontend health checks.

Verify it:

```bash
docker compose ps
curl --fail http://127.0.0.1:2323/healthz
```

> [!NOTE]
> Gmail delivery requires an App Password in the server's ignored `.env` file. The application and database secrets are generated automatically inside a persistent Docker volume.

For the complete installation and Cloudflare configuration, continue with [🏠 Homelab deployment](docs/production-deployment.md).

## 🧑‍💻 Local development

The development workflow runs Django and Vite directly. Docker Compose represents the production topology.

```bash
# Terminal 1 — backend
source .venv/bin/activate
python backend/manage.py migrate
python backend/manage.py runserver

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Read [💻 Local development](docs/development.md) before configuring SMTP, regenerating email templates or running the test suite.

## 🚢 Delivery workflow

```text
feature branch → dev → pull request → main → GitHub Actions → homelab
```

Every push to `main` validates the backend, frontend and deployment scripts before the self-hosted runner invokes `scripts/deploy.sh`. The deploy script rebuilds only affected application images, waits for healthy containers and restores the previous images if deployment fails.

Manual rollback is available through GitHub Actions and `scripts/rollback.sh`. Database migrations are deliberately **not** reversed automatically.

## 🔐 Security notes

- Never commit `.env`, Gmail App Passwords or generated secrets.
- The public container binds to `127.0.0.1`, not `0.0.0.0`.
- PostgreSQL and Gunicorn live only on the internal Docker network.
- Protecting `/admin/` with Cloudflare Access is strongly recommended.
- Never run `docker compose down -v` unless permanent data deletion is intentional.

## 📄 License and ownership

This repository contains Jalberth Mosquera's personal portfolio and project presentation material. Review the repository's licensing status before reusing its branding, content, photographs or client-related assets.
