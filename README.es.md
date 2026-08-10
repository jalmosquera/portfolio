# 🚀 Jalberth Mosquera — Portfolio autoalojado

[![English documentation](https://img.shields.io/badge/README-English-F17D34?style=for-the-badge)](README.md)

> [!IMPORTANT]
> **Este portfolio está desplegado en un homelab privado.** El tráfico de producción llega mediante Cloudflare Tunnel a un contenedor de Nginx enlazado a un ip especifica. PostgreSQL y Django nunca se exponen directamente a Internet.

Portfolio bilingüe y administrado desde base de datos para presentar proyectos reales, generar CV dinámicos y recibir consultas de contacto. Combina un frontend React, una API Django REST y una infraestructura Docker Compose preparada para autoalojamiento.

## 📚 Índice de documentación

| Tema | Contenido |
| --- | --- |
| [🏗️ Arquitectura](docs/architecture.md) | Flujo de peticiones, contenedores, límites de seguridad y decisiones principales |
| [🗄️ Base de datos](docs/database.md) | PostgreSQL/SQLite, modelos, relaciones, persistencia y copias de seguridad |
| [📁 Estructura del proyecto](docs/project-structure.md) | Mapa del repositorio y responsabilidad de cada carpeta |
| [🔌 API](docs/api.md) | Endpoints públicos, idiomas, administración y documentación OpenAPI |
| [💻 Desarrollo local](docs/development.md) | Python, Node, migraciones, pruebas, lint y plantillas de correo |
| [🏠 Despliegue en homelab](docs/production-deployment.md) | Cloudflare Tunnel, Docker Compose, healthchecks, actualizaciones y rollback |

> [!NOTE]
> Los documentos especializados se mantienen en inglés para conservar una única fuente técnica de verdad. Este README ofrece la entrada completa en español y enlaces directos a cada área.

## ✨ Características principales

- 🌍 Experiencia completa en español e inglés.
- 🧩 Contenido administrable desde Django Admin.
- 🖼️ Proyectos destacados, galerías, tecnologías y casos de estudio.
- 📄 CV dinámico en formato compacto o visual generado desde la base de datos.
- ✉️ Notificaciones SMTP y confirmaciones bilingües diseñadas con React Email.
- 📊 Contador privado de visitas visible desde Django Admin.
- 🐳 Inicio de producción con un único comando Docker Compose.
- 🏠 Despliegue automatizado hacia el homelab mediante GitHub Actions.
- ↩️ Recuperación de imágenes Docker anteriores cuando un despliegue falla.

## 🧰 Stack tecnológico

| Capa | Tecnologías |
| --- | --- |
| Frontend | React 19, Vite 8, Tailwind CSS 4, Axios, React Router, Sileo |
| Backend | Python 3.11, Django 5.2, Django REST Framework, Django Parler |
| Datos | PostgreSQL 17 en producción y SQLite para desarrollo local |
| Documentos y correo | ReportLab, React Email, Gmail SMTP |
| Ejecución | Nginx, Gunicorn, Docker Compose, Cloudflare Tunnel |
| Calidad y entrega | Pytest, ESLint, GitHub Actions, runner autoalojado |

## 🧭 Flujo de producción

```text
Internet
   │
   ▼
Cloudflare Tunnel
   │
   ▼
127.0.0.1:2323 ──► Nginx
                      ├── /              Aplicación React
                      ├── /api/*         Django + Gunicorn
                      ├── /admin/*       Django Admin
                      ├── /media/*       Archivos persistentes
                      └── /static/*      Estáticos de Django
                                            │
                                            ▼
                                      PostgreSQL 17
```

## ⚡ Iniciar producción

```bash
git clone https://github.com/jalmosquera/portfolio.git
cd portfolio
docker compose up -d
```

En el primer inicio se generan los secretos, se crean los volúmenes, se aplican las migraciones, se recopilan los estáticos y se levantan los servicios con sus healthchecks.

```bash
docker compose ps
curl --fail http://127.0.0.1:2323/healthz
```

La configuración completa se encuentra en [🏠 Homelab deployment](docs/production-deployment.md).

## 🧑‍💻 Desarrollo local

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

Consultá [💻 Local development](docs/development.md) para configurar el correo, ejecutar las pruebas y regenerar las plantillas.

## 🚢 Flujo de entrega

```text
rama de feature → dev → pull request → main → GitHub Actions → homelab
```

Cuando `main` recibe cambios, GitHub Actions valida el proyecto y el runner del homelab ejecuta `scripts/deploy.sh`. Si el despliegue falla, el script intenta restaurar las imágenes anteriores. `scripts/rollback.sh` permite iniciar manualmente esa recuperación.

Las migraciones de base de datos **no se revierten automáticamente**, porque hacerlo podría destruir información.

## 🔐 Seguridad

- Nunca subas `.env`, contraseñas de aplicación ni secretos generados.
- Nginx publica únicamente `127.0.0.1:2323`.
- PostgreSQL y Gunicorn permanecen dentro de la red Docker.
- Se recomienda proteger `/admin/` mediante Cloudflare Access.
- No ejecutes `docker compose down -v` salvo que quieras eliminar permanentemente los datos.

## 📄 Licencia y propiedad

Este repositorio contiene el portfolio personal y material de presentación de proyectos de Jalberth Mosquera. Revisá el estado de la licencia antes de reutilizar su identidad visual, contenido, fotografías o recursos relacionados con clientes.
