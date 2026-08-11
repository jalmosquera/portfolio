# 📁 Project structure

[← Back to documentation index](../README.md)

## 🗺️ Repository map

```text
portfolio/
├── .github/workflows/       # CI and homelab deployment automation
├── backend/                 # Django, DRF, admin, PDF generation and email delivery
│   ├── apps/                # Domain-oriented Django applications
│   ├── core/                # Global settings, URLs, health checks, WSGI and ASGI
│   ├── tests/               # Backend integration and domain tests
│   ├── Dockerfile           # Gunicorn production image
│   └── manage.py            # Django command entry point
├── frontend/                # React and Vite application
│   ├── emails/              # React Email source templates
│   ├── public/svg/          # Technology and interface SVG assets
│   ├── src/                 # Pages, components, API layer and translations
│   └── Dockerfile           # Build stage and Nginx runtime image
├── docs/                    # Focused technical documentation
├── scripts/                 # Production deployment and rollback scripts
├── docker-compose.yml       # Complete homelab production topology
├── .env.example             # Safe environment-variable contract
├── README.md                # English documentation hub
└── README.es.md             # Spanish project introduction
```

## 🐍 Backend domains

Each Django application owns one business capability:

| App | Responsibility |
| --- | --- |
| `about` | Bilingual About Me singleton |
| `analytics` | Anonymous first-party sessions/events, aggregated reporting and superuser dashboard API |
| `contact` | Public inquiries and email delivery status |
| `projects` | Project identity, visibility, featured state and technologies |
| `project_images` | Ordered project galleries |
| `problem_solution` | Case-study problem and solution |
| `tech_details` | Technical implementation details |
| `lessons` | Lessons learned per project |
| `technology` | Reusable technology catalogue and icons |
| `resume` | Dynamic CV content and PDF generation |

A typical app can contain:

```text
apps/domain/
├── api/
│   ├── routes.py
│   ├── serializers.py
│   └── views.py
├── migrations/
├── admin.py
├── models.py
└── services/                # Domain orchestration when needed
```

## ⚛️ Frontend structure

```text
frontend/src/
├── assets/                  # Imported images and branding
├── components/
│   ├── home/                # Home-page sections
│   ├── layout/              # Navbar and footer
│   ├── project-detail/      # Project case-study UI
│   ├── projects/            # Project lists and cards
│   ├── resume/              # CV selector and download UI
│   └── ui/                  # Shared interface primitives
├── context/                 # Application-wide React context
├── i18n/                    # English and Spanish UI messages
├── lib/
│   ├── api/                 # Axios clients and domain requests
│   └── config/              # Centralized route and asset URL builders
├── pages/                   # Route-level screens
├── App.jsx                  # Application routing/composition
└── main.jsx                 # React entry point
```

## ✉️ Email templates

React Email sources live in `frontend/emails/`. They are exported as HTML into:

```text
backend/apps/contact/templates/contact/
```

Django fills those templates with inquiry data and sends them through the configured email backend. See [💻 Local development](development.md#-transactional-email-templates).

## 🐳 Infrastructure files

- `docker-compose.yml` is the production source of truth.
- `backend/Dockerfile` creates the Python/Gunicorn image.
- `frontend/Dockerfile` builds React and serves it with Nginx.
- `scripts/deploy.sh` performs selective builds and automatic failure recovery.
- `scripts/rollback.sh` restores the previously tagged application images.
- `.github/workflows/deploy-production.yml` connects merges to `main` with the homelab runner.
