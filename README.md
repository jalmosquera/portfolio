# Portfolio Personal - API REST con Django

[English Version](README.en.md) | [Documentacion Completa](docs/es/)

API REST profesional para portafolio personal desarrollada con Django y Django REST Framework. Sistema modular con documentacion interactiva OpenAPI, soporte multilenguaje y configuracion multi-entorno.

## Indice de Contenidos

- [Caracteristicas Principales](#caracteristicas-principales)
- [Tecnologias](#tecnologias)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Inicio Rapido](#inicio-rapido)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalacion](#instalacion)
  - [Configuracion](#configuracion)
- [Documentacion API](#documentacion-api)
  - [Endpoints Principales](#endpoints-principales)
  - [Ejemplos de Uso](#ejemplos-de-uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos de Datos](#modelos-de-datos)
- [Testing](#testing)
- [Deployment](#deployment)
- [Convenciones de Commits](#convenciones-de-commits)
- [Documentacion Completa](#documentacion-completa)
- [Licencia](#licencia)

---

## Caracteristicas Principales

- **API REST Completa**: Implementacion profesional con Django REST Framework
- **Documentacion Interactiva**: OpenAPI 3.0 con drf-spectacular (Swagger UI y ReDoc)
- **Arquitectura Modular**: Organizacion por apps (projects, skills, about, contact)
- **Respuestas camelCase**: Convencion JSON moderna para integracion frontend
- **Multi-Entorno**: Configuraciones separadas para desarrollo y produccion
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (produccion)
- **Deployment Ready**: Configurado para Railway con Gunicorn y WhiteNoise
- **CORS Habilitado**: Soporte completo para aplicaciones frontend
- **Admin Personalizado**: Interfaz de administracion Django optimizada
- **Documentacion Bilingue**: Espanol e Ingles en codigo y documentacion

## Tecnologias

### Backend
- **Django 4.2+**: Framework web de alto nivel
- **Django REST Framework 3.14+**: Toolkit para crear APIs REST
- **drf-spectacular 0.28.0**: Generacion de esquemas OpenAPI 3.0

### Base de Datos
- **PostgreSQL**: Base de datos de produccion
- **SQLite**: Base de datos de desarrollo

### Servidor y Deployment
- **Gunicorn 21.2+**: Servidor WSGI HTTP para Python
- **WhiteNoise 6.6+**: Servicio de archivos estaticos
- **Railway**: Plataforma de deployment

### Utilidades
- **python-decouple 3.8+**: Separacion de configuracion del codigo
- **Pillow 10.0+**: Procesamiento de imagenes
- **django-cors-headers 4.3+**: Manejo de CORS

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     Cliente / Frontend                       │
│           (React, Vue, Angular, Mobile App, etc.)           │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS (JSON)
                     │ CORS Enabled
┌────────────────────▼────────────────────────────────────────┐
│                   Django REST Framework                      │
│                   ┌─────────────────────┐                    │
│                   │   API Documentation │                    │
│                   │  Swagger + ReDoc    │                    │
│                   └─────────────────────┘                    │
├──────────────────────────────────────────────────────────────┤
│                    Apps Modulares                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Projects │ │  Skills  │ │  About   │ │ Contact  │       │
│  │          │ │          │ │          │ │          │       │
│  │ Models   │ │ Models   │ │ Models   │ │ Models   │       │
│  │ Views    │ │ Views    │ │ Views    │ │ Views    │       │
│  │ Serializ.│ │ Serializ.│ │ Serializ.│ │ Serializ.│       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├──────────────────────────────────────────────────────────────┤
│                       Django ORM                             │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│          PostgreSQL (Prod) / SQLite (Dev)                   │
└─────────────────────────────────────────────────────────────┘
```

Para mas detalles sobre la arquitectura, consulta [Arquitectura del Proyecto](docs/es/arquitectura.md).

## Inicio Rapido

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- PostgreSQL (solo para produccion)
- Git

### Instalacion

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd portfolio

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario (para acceder al admin)
python manage.py createsuperuser

# 7. Recolectar archivos estaticos
python manage.py collectstatic --noinput

# 8. Ejecutar servidor de desarrollo
python manage.py runserver
```

### Configuracion

El proyecto utiliza `python-decouple` para manejar variables de entorno. Crea un archivo `.env` basado en `.env.example`:

```env
# Django Configuration
DJANGO_ENV=development
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
DEBUG=True

# Database Configuration (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-email

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

Ver documentacion completa en [Variables de Entorno](docs/es/variables-entorno.md).

## Documentacion API

El proyecto incluye documentacion interactiva generada automaticamente con drf-spectacular:

- **ReDoc** (recomendado): `http://localhost:8000/`
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Esquema OpenAPI**: `http://localhost:8000/api/schema/`

### Endpoints Principales

#### Projects (Proyectos)
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/projects/` | Listar todos los proyectos (paginado) |
| GET | `/api/projects/{id}/` | Obtener detalle de un proyecto |
| GET | `/api/projects/featured/` | Listar proyectos destacados |
| POST | `/api/projects/` | Crear nuevo proyecto (admin) |
| PUT/PATCH | `/api/projects/{id}/` | Actualizar proyecto (admin) |
| DELETE | `/api/projects/{id}/` | Eliminar proyecto (admin) |

#### Skills (Habilidades)
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/skills/` | Listar todas las habilidades |
| GET | `/api/skills/{id}/` | Obtener detalle de una habilidad |
| GET | `/api/skills/featured/` | Listar habilidades destacadas |
| GET | `/api/skills/by_category/` | Habilidades agrupadas por categoria |
| POST | `/api/skills/` | Crear nueva habilidad (admin) |
| PUT/PATCH | `/api/skills/{id}/` | Actualizar habilidad (admin) |
| DELETE | `/api/skills/{id}/` | Eliminar habilidad (admin) |

#### Skill Categories (Categorias de Habilidades)
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/skill-categories/` | Listar categorias con sus habilidades |
| GET | `/api/skill-categories/{id}/` | Obtener detalle de una categoria |
| POST | `/api/skill-categories/` | Crear nueva categoria (admin) |
| PUT/PATCH | `/api/skill-categories/{id}/` | Actualizar categoria (admin) |
| DELETE | `/api/skill-categories/{id}/` | Eliminar categoria (admin) |

#### About (Informacion Personal)
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/about/` | Listar todos los perfiles |
| GET | `/api/about/{id}/` | Obtener detalle de un perfil |
| GET | `/api/about/active/` | Obtener perfil activo actual |
| POST | `/api/about/` | Crear nuevo perfil (admin) |
| PUT/PATCH | `/api/about/{id}/` | Actualizar perfil (admin) |
| DELETE | `/api/about/{id}/` | Eliminar perfil (admin) |

#### Contact (Mensajes de Contacto)
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/contact/` | Listar mensajes de contacto (admin) |
| GET | `/api/contact/{id}/` | Obtener detalle de un mensaje (admin) |
| GET | `/api/contact/unread/` | Listar mensajes no leidos (admin) |
| POST | `/api/contact/` | Enviar mensaje de contacto (publico) |
| POST | `/api/contact/{id}/mark_read/` | Marcar como leido (admin) |
| POST | `/api/contact/{id}/mark_replied/` | Marcar como respondido (admin) |

### Ejemplos de Uso

#### Listar Proyectos Destacados
```bash
curl -X GET http://localhost:8000/api/projects/featured/
```

Respuesta:
```json
[
  {
    "id": 1,
    "title": "E-Commerce Platform",
    "description": "Plataforma de comercio electronico completa...",
    "shortDescription": "Sistema de ventas online con Django",
    "imageUrl": "/media/projects/ecommerce.png",
    "url": "https://demo.example.com",
    "githubUrl": "https://github.com/user/ecommerce",
    "technologies": ["Django", "React", "PostgreSQL"],
    "isFeatured": true,
    "order": 1,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-20T14:45:00Z"
  }
]
```

#### Obtener Habilidades por Categoria
```bash
curl -X GET http://localhost:8000/api/skills/by_category/
```

Respuesta:
```json
[
  {
    "id": 1,
    "name": "Backend",
    "description": "Tecnologias de backend y APIs",
    "order": 1,
    "skills": [
      {
        "id": 1,
        "name": "Django",
        "categoryId": 1,
        "categoryName": "Backend",
        "proficiency": "expert",
        "percentage": 95,
        "icon": "django-icon",
        "description": "Framework web de Python",
        "yearsExperience": 5,
        "isFeatured": true,
        "order": 1
      }
    ]
  }
]
```

#### Enviar Mensaje de Contacto
```bash
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Perez",
    "email": "juan@example.com",
    "subject": "Consulta sobre proyecto",
    "message": "Hola, me interesa saber mas sobre...",
    "phone": "+52 555 1234567"
  }'
```

Respuesta:
```json
{
  "id": 1,
  "name": "Juan Perez",
  "email": "juan@example.com",
  "subject": "Consulta sobre proyecto",
  "message": "Hola, me interesa saber mas sobre...",
  "phone": "+52 555 1234567",
  "isRead": false,
  "isReplied": false,
  "createdAt": "2024-01-22T09:15:00Z",
  "updatedAt": "2024-01-22T09:15:00Z"
}
```

Para mas ejemplos y detalles, consulta [Documentacion de API](docs/es/api.md).

## Estructura del Proyecto

```
portfolio/
├── apps/                           # Aplicaciones Django
│   ├── projects/                   # App de proyectos
│   │   ├── api/
│   │   │   ├── router.py          # Configuracion de rutas
│   │   │   ├── serializers.py     # Serializadores DRF
│   │   │   └── views.py           # ViewSets de la API
│   │   ├── migrations/            # Migraciones de BD
│   │   ├── tests/                 # Tests unitarios
│   │   ├── admin.py               # Configuracion admin
│   │   └── models.py              # Modelos de datos
│   ├── skills/                    # App de habilidades
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── admin.py               # Admin personalizado
│   │   └── models.py              # SkillCategory y Skill
│   ├── about/                     # App de informacion personal
│   │   ├── api/
│   │   ├── migrations/
│   │   ├── tests/
│   │   └── models.py              # AboutMe model
│   └── contact/                   # App de mensajes de contacto
│       ├── api/
│       ├── migrations/
│       ├── tests/
│       └── models.py              # ContactMessage model
├── core/                          # Configuracion principal
│   ├── settings/
│   │   ├── __init__.py           # Selector de configuracion
│   │   ├── base.py               # Configuracion base
│   │   ├── development.py        # Configuracion desarrollo
│   │   └── production.py         # Configuracion produccion
│   ├── asgi.py                   # Configuracion ASGI
│   ├── wsgi.py                   # Configuracion WSGI
│   └── urls.py                   # URLs principales
├── docs/                          # Documentacion
│   ├── es/                       # Documentacion en espanol
│   │   ├── arquitectura.md
│   │   ├── api.md
│   │   ├── modelos.md
│   │   ├── instalacion.md
│   │   ├── deploy.md
│   │   ├── variables-entorno.md
│   │   ├── testing.md
│   │   └── contribucion.md
│   └── en/                       # Documentacion en ingles
│       ├── architecture.md
│       ├── api.md
│       ├── models.md
│       ├── installation.md
│       ├── deployment.md
│       ├── environment-variables.md
│       ├── testing.md
│       └── contributing.md
├── static/                        # Archivos estaticos
├── media/                         # Archivos subidos
├── tests/                         # Tests de integracion
│   └── fixtures/                 # Fixtures para tests
├── .git/                          # Repositorio Git
│   └── hooks/
│       └── commit-msg            # Hook de validacion
├── manage.py                      # Script de gestion Django
├── requirements.txt               # Dependencias principales
├── requirements-test.txt          # Dependencias de testing
├── pytest.ini                     # Configuracion pytest
├── conftest.py                    # Configuracion global tests
├── schema.yml                     # Esquema OpenAPI generado
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore                     # Archivos ignorados por Git
├── .gitmessage                    # Template para commits
├── COMMIT_CONVENTIONS.md          # Convenciones de commits
├── TESTING.md                     # Guia de testing
├── README.md                      # Este archivo (Espanol)
└── README.en.md                   # Readme en Ingles
```

## Modelos de Datos

### Project (Proyecto)
Representa un proyecto del portafolio.

**Campos:**
- `title`: Titulo del proyecto
- `description`: Descripcion detallada
- `short_description`: Resumen breve
- `image`: Imagen o screenshot del proyecto
- `url`: URL del proyecto en vivo
- `github_url`: URL del repositorio GitHub
- `technologies`: Tecnologias utilizadas (separadas por comas)
- `is_featured`: Mostrar en seccion destacados
- `order`: Orden de visualizacion
- `created_at`, `updated_at`: Timestamps

### SkillCategory (Categoria de Habilidad)
Agrupa habilidades relacionadas.

**Campos:**
- `name`: Nombre de la categoria
- `description`: Descripcion de la categoria
- `order`: Orden de visualizacion
- `created_at`, `updated_at`: Timestamps

### Skill (Habilidad)
Representa una habilidad o tecnologia.

**Campos:**
- `name`: Nombre de la habilidad
- `category`: Categoria (ForeignKey a SkillCategory)
- `proficiency`: Nivel ('beginner', 'intermediate', 'advanced', 'expert')
- `percentage`: Porcentaje de dominio (0-100)
- `icon`: Clase de icono o URL
- `description`: Descripcion de la habilidad
- `years_experience`: Anos de experiencia
- `is_featured`: Mostrar en habilidades destacadas
- `order`: Orden dentro de la categoria
- `created_at`, `updated_at`: Timestamps

### AboutMe (Informacion Personal)
Informacion personal para la seccion "Sobre mi".

**Campos:**
- `name`: Nombre completo
- `title`: Titulo profesional
- `bio`: Biografia
- `email`: Email de contacto
- `phone`: Telefono
- `location`: Ubicacion
- `profile_image`: Foto de perfil
- `resume_file`: Archivo CV/Resume
- `linkedin_url`, `github_url`, `twitter_url`, `website_url`: URLs sociales
- `is_active`: Perfil activo (solo uno activo a la vez)
- `created_at`, `updated_at`: Timestamps

### ContactMessage (Mensaje de Contacto)
Mensaje enviado a traves del formulario de contacto.

**Campos:**
- `name`: Nombre del remitente
- `email`: Email del remitente
- `subject`: Asunto del mensaje
- `message`: Contenido del mensaje
- `phone`: Telefono (opcional)
- `is_read`: Marcado como leido
- `is_replied`: Marcado como respondido
- `created_at`, `updated_at`: Timestamps

Para diagramas de relaciones y detalles completos, consulta [Modelos y Base de Datos](docs/es/modelos.md).

## Testing

El proyecto incluye una suite completa de tests con pytest y pytest-django.

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con coverage
pytest --cov=apps --cov-report=html

# Ejecutar tests de una app especifica
pytest apps/skills/tests/

# Ejecutar tests en modo verbose
pytest -v
```

Cobertura actual: ~96%

Para mas informacion, consulta [TESTING.md](TESTING.md) y [Guia de Testing](docs/es/testing.md).

## Deployment

### Railway (Recomendado)

1. **Preparar variables de entorno**:
   - `DJANGO_ENV=production`
   - `SECRET_KEY=<tu-clave-secreta>`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=<tu-dominio.railway.app>`
   - `DATABASE_URL` (proporcionado por Railway)

2. **Conectar repositorio Git**:
   - Railway detectara automaticamente el proyecto Django
   - Instalara dependencias de `requirements.txt`
   - Ejecutara migraciones automaticamente

3. **Configurar base de datos PostgreSQL**:
   - Agregar servicio PostgreSQL en Railway
   - `DATABASE_URL` se configurara automaticamente

4. **Comandos post-deployment**:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Para deployment en otras plataformas (Heroku, DigitalOcean, AWS), consulta [Guia de Deployment](docs/es/deploy.md).

## Convenciones de Commits

El proyecto utiliza un sistema de convenciones de commits con validacion automatica. Cada commit debe seguir este formato:

```
<tipo>: <emoji> <descripcion corta>
- <cambio detallado 1>
- <cambio detallado 2>
- <contexto adicional si es necesario>
```

### Tipos de Commit

| Tipo | Emoji | Descripcion |
|------|-------|-------------|
| `feat` | ✨ | Nueva funcionalidad |
| `fix` | 🐛 | Correccion de bug |
| `docs` | 📚 | Cambios en documentacion |
| `style` | 💄 | Cambios de estilo de codigo |
| `refactor` | ♻️  | Refactorizacion de codigo |
| `perf` | ⚡ | Mejoras de rendimiento |
| `test` | ✅ | Agregar o actualizar tests |
| `build` | 🏗️  | Sistema de build o dependencias |
| `ci` | 👷 | Configuracion de CI |
| `chore` | 🔧 | Otros cambios |

### Ejemplo
```
feat: ✨ add user authentication system
- Implement JWT token-based authentication
- Create login and registration endpoints
- Add password hashing with bcrypt
- Include authentication middleware for protected routes
```

El proyecto incluye un hook `commit-msg` que valida automaticamente el formato.

Para mas detalles, consulta [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md).

## Documentacion Completa

Para documentacion detallada, consulta los siguientes recursos:

### Espanol
- [Guia de Instalacion](docs/es/instalacion.md) - Instrucciones completas de instalacion
- [Arquitectura del Proyecto](docs/es/arquitectura.md) - Diseno y patrones arquitectonicos
- [Documentacion de API](docs/es/api.md) - Referencia completa de endpoints
- [Modelos y Base de Datos](docs/es/modelos.md) - Esquemas y relaciones
- [Guia de Deploy](docs/es/deploy.md) - Deployment en produccion
- [Variables de Entorno](docs/es/variables-entorno.md) - Configuracion completa
- [Guia de Testing](docs/es/testing.md) - Tests y cobertura
- [Guia de Contribucion](docs/es/contribucion.md) - Como contribuir al proyecto

### English
- [Installation Guide](docs/en/installation.md) - Complete installation instructions
- [Project Architecture](docs/en/architecture.md) - Design and architectural patterns
- [API Documentation](docs/en/api.md) - Complete endpoint reference
- [Models and Database](docs/en/models.md) - Schemas and relationships
- [Deployment Guide](docs/en/deployment.md) - Production deployment
- [Environment Variables](docs/en/environment-variables.md) - Complete configuration
- [Testing Guide](docs/en/testing.md) - Tests and coverage
- [Contributing Guide](docs/en/contributing.md) - How to contribute

## Licencia

MIT License

---

**Desarrollado con Django y Django REST Framework**

Para mas informacion o soporte, consulta la documentacion o abre un issue en GitHub.
