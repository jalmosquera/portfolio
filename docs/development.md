# 💻 Local development

[← Back to documentation index](../README.md)

## ✅ Requirements

- Python 3.11
- Node.js 22
- npm
- Git

Docker is required for production-like execution but not for the normal local workflow.

## 🐍 Backend setup

From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver
```

When `DB_NAME` is absent, Django uses `backend/db.sqlite3`. This keeps local onboarding independent from PostgreSQL.

> [!WARNING]
> Always run Django with the project virtual environment. A global `python` or custom shell alias can select the wrong interpreter and report false missing dependencies.

## ⚛️ Frontend setup

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite serves the development application, while Axios communicates with the local Django API through the centralized frontend configuration.

## 🔐 Environment configuration

`.env.example` documents supported variables. Real credentials belong in the ignored root `.env` file.

For local SMTP testing:

```env
EMAIL_NOTIFICATIONS_ENABLED=true
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-address@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password
CONTACT_NOTIFICATION_EMAIL=your-address@gmail.com
```

Never use the normal Gmail account password and never commit the App Password.

## 🧪 Quality checks

Backend:

```bash
source .venv/bin/activate
pytest backend/tests -q
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
```

Frontend linting:

```bash
cd frontend
npm run lint
```

Deployment scripts:

```bash
shellcheck scripts/deploy.sh scripts/rollback.sh
```

## ✉️ Transactional email templates

React Email source components:

```text
frontend/emails/
```

After intentionally modifying them, export the HTML consumed by Django:

```bash
cd frontend
npm run email:export
```

Generated templates are written to:

```text
backend/apps/contact/templates/contact/
```

Commit both the React Email source and generated Django templates so production does not need Node to render transactional emails at runtime.

## 🗄️ Migrations

Create migrations only after deliberate model changes:

```bash
python backend/manage.py makemigrations
python backend/manage.py migrate
```

Review generated migration files before committing them. Production applies committed migrations automatically when the backend container starts.

## 🌱 Git workflow

```text
main
└── dev
    └── feat/*, fix/*, docs/*, refactor/* ...
```

1. Create a focused branch from `dev`.
2. Implement and validate the change.
3. Merge the focused branch into `dev`.
4. Open a pull request from `dev` to `main`.
5. Let GitHub Actions validate and deploy the merged revision.

Use conventional commits and never add AI or co-author attribution.
