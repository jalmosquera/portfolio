# 📋 Portfolio — Pending Tasks / Tareas Pendientes

> 🕒 Last updated / Última actualización: April 2026 · Active branch / Rama activa: `feat/frontend-portfolio`

---

## 📖 Table of Contents

- [📘 Documentation (English)](#-documentation-english)
- [📗 Documentación (Español)](#-documentación-español)
- [🔐 Security & Configuration](#-security--configuration)
- [🧱 Backend (Django + DRF)](#-backend-django--drf)
- [🎨 Frontend (React + Vite + Tailwind)](#-frontend-react--vite--tailwind)
- [🔄 CI/CD & DevOps](#-cicd--devops)
- [🧪 Testing](#-testing)
- [📦 Infrastructure & Database](#-infrastructure--database)
- [📝 Documentation Tasks](#-documentation-tasks)
- [✅ Recently Completed](#-recently-completed)

---

## 📘 Documentation (English)

This is a **fullstack portfolio project** built as a monorepo with a Django REST API backend and a React + Vite frontend.

### 🏗️ Project Structure

```
portfolio/
├── backend/        # Django 5.2 + DRF + PostgreSQL
│   ├── core/       # Main settings, URLs, WSGI/ASGI
│   └── apps/       # projects, technology, tech_details,
│                   # project_images, lessons, problem_solution
├── frontend/       # React 19 + Vite + Tailwind CSS 4
│   └── src/
│       ├── pages/       # HomePage, ProjectsPage, ProjectDetailPage
│       ├── components/  # layout, home, projects, ui
│       └── lib/api/     # API clients per entity
└── .venv/          # Python virtual environment (git-ignored)
```

### 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/jalmosquera/portfolio.git
cd portfolio

# 2. Backend setup
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp .env.example .env             # fill in your variables
cd backend && python manage.py migrate
python manage.py runserver

# 3. Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### 🔑 Required Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for prod |
| `DATABASE_URL` | PostgreSQL connection string |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins |

### 🧪 Running Tests

```bash
cd backend
pytest                        # run all tests
pytest --cov=apps             # with coverage report
```

---

## 📗 Documentación (Español)

Este es un **proyecto de portafolio fullstack** organizado como monorepo, con un backend en Django REST Framework y un frontend en React + Vite.

### 🏗️ Estructura del Proyecto

```
portfolio/
├── backend/        # Django 5.2 + DRF + PostgreSQL
│   ├── core/       # Settings principal, URLs, WSGI/ASGI
│   └── apps/       # projects, technology, tech_details,
│                   # project_images, lessons, problem_solution
├── frontend/       # React 19 + Vite + Tailwind CSS 4
│   └── src/
│       ├── pages/       # HomePage, ProjectsPage, ProjectDetailPage
│       ├── components/  # layout, home, projects, ui
│       └── lib/api/     # Clientes API por entidad
└── .venv/          # Entorno virtual Python (ignorado por git)
```

### 🚀 Cómo Empezar

```bash
# 1. Clonar el repositorio
git clone https://github.com/jalmosquera/portfolio.git
cd portfolio

# 2. Configurar el backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp .env.example .env             # completar las variables
cd backend && python manage.py migrate
python manage.py runserver

# 3. Configurar el frontend (nueva terminal)
cd frontend
npm install
npm run dev
```

### 🔑 Variables de Entorno Requeridas

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en desarrollo, `False` en producción |
| `DATABASE_URL` | Cadena de conexión PostgreSQL |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma |
| `CORS_ALLOWED_ORIGINS` | Orígenes del frontend permitidos |

### 🧪 Correr los Tests

```bash
cd backend
pytest                        # correr todos los tests
pytest --cov=apps             # con reporte de cobertura
```

---

## 🔐 Security & Configuration

- [ ] Move `SECRET_KEY` to environment variables (`.env`)
- [ ] Set `DEBUG=False` in production and configure `ALLOWED_HOSTS`
- [ ] Create `.env.example` with all required variables documented
- [ ] Add `python-decouple` or `django-environ` for env var management
- [ ] Restrict `CORS_ALLOWED_ORIGINS` to real production domains

---

## 🧱 Backend (Django + DRF)

- [ ] Add pagination to `projects` and `technology` endpoints
- [ ] Implement advanced filters in `ProjectsViewSet` (by tech, featured, slug)
- [ ] Add serializer validations (required fields, max lengths)
- [ ] Complete `lessons` and `problem_solution` serializers with nested fields
- [ ] Add global search endpoint (`/api/search/`)
- [ ] Configure `drf-spectacular` with project metadata (title, version, contact)
- [ ] Document all endpoints with docstrings for OpenAPI
- [ ] Review and complete test suite (cover 400/404 error cases)
- [ ] Add `django-storages` + S3/Cloudinary for production image storage
- [ ] Configure migrations for CI environment

---

## 🎨 Frontend (React + Vite + Tailwind)

- [ ] Complete `ProjectDetailPage` with lessons and problem/solution sections
- [ ] Implement skeleton loaders while API data is loading
- [ ] Add error handling and empty state in `ProjectsPage`
- [ ] Improve mobile responsiveness of the `Hero` component
- [ ] Implement lazy loading for images in `ProjectCard`
- [ ] Add entrance animations with Framer Motion or CSS transitions
- [ ] Connect `Contact` section with a functional form (EmailJS or similar)
- [ ] Implement dark / light mode toggle
- [ ] Optimize images (WebP format, compression, proper dimensions)
- [ ] Add SEO metadata (Open Graph, meta description, favicon)

---

## 🔄 CI/CD & DevOps

- [ ] **Create GitHub Actions CI workflow:**
  - Run `pytest` on every PR to backend
  - Run `eslint` on the frontend
  - Build the frontend to verify it compiles
- [ ] **Create GitHub Actions CD workflow (auto deploy):**
  - Deploy backend to Railway / Render / Fly.io on merge to `main`
  - Deploy frontend to Vercel / Netlify on merge to `main`
- [ ] Add CI status badge to `README.md`
- [ ] Configure secrets in GitHub Actions (`Settings > Secrets and variables`)
- [ ] Create `Dockerfile` for the backend
- [ ] Create `docker-compose.yml` for local development (backend + postgres)
- [ ] Add health check endpoint (`/api/health/`) for monitoring

---

## 🧪 Testing

- [ ] Increase backend test coverage to ≥ 80%
- [ ] Add integration tests for main endpoints
- [ ] Configure `pytest-cov` and coverage reports in CI
- [ ] Add frontend unit tests with Vitest
- [ ] Add E2E tests with Playwright or Cypress for critical flows

---

## 📦 Infrastructure & Database

- [ ] Set up production database (Supabase / Railway Postgres)
- [ ] Add seed script with example data
- [ ] Configure automatic database backups
- [ ] Review indexes on models with frequent queries

---

## 📝 Documentation Tasks

- [ ] Write complete `README.md` with:
  - Project description
  - Installation instructions (backend + frontend)
  - Required environment variables
  - How to run tests
  - Link to production deploy
- [ ] Document monorepo architecture
- [ ] Add contribution guide (`CONTRIBUTING.md`)

---

## ✅ Recently Completed

- [x] Frontend bootstrap with React + Vite + Tailwind 4
- [x] Django REST Framework + drf-spectacular setup
- [x] Test suite with pytest-django
- [x] Fix all backend serializers and views
- [x] UI redesign to match mockup
- [x] Add `.gitignore` (excludes `.venv`, `__pycache__`, `node_modules`, etc.)
- [x] Frontend ↔ backend integration with per-entity API clients

---

> 💡 **Quick start / Inicio rápido:**
> ```bash
> # Backend
> cd backend && source ../.venv/bin/activate && python manage.py runserver
>
> # Frontend
> cd frontend && npm run dev
> ```
