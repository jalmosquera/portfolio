# Portfolio Personal - Django REST API

Portafolio personal desarrollado con Django y Django REST Framework para mostrar proyectos, habilidades y información profesional.

## Características

- ✅ API REST completa con Django REST Framework
- ✅ Documentación interactiva con drf-spectacular (OpenAPI 3.0)
- ✅ Estructura modular por apps (projects, skills, about, contact)
- ✅ Respuestas JSON en formato camelCase
- ✅ Configuración multi-entorno (desarrollo/producción)
- ✅ SQLite para desarrollo, PostgreSQL para producción
- ✅ Preparado para deploy en Railway
- ✅ Soporte para CORS
- ✅ Documentación bilingüe (español/inglés)

## Estructura del Proyecto

```
portfolio/
├── apps/
│   ├── projects/        # Gestión de proyectos
│   │   └── api/         # API endpoints, serializers, routers
│   ├── skills/          # Gestión de habilidades
│   │   └── api/
│   ├── about/           # Información personal
│   │   └── api/
│   └── contact/         # Mensajes de contacto
│       └── api/
├── core/
│   ├── settings/        # Configuración por entorno
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/              # Archivos estáticos
├── media/               # Archivos subidos
└── manage.py
```

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd portfolio
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El proyecto estará disponible en: `http://localhost:8000`

## Documentación de la API

La API incluye documentación interactiva generada automáticamente con **drf-spectacular** siguiendo el estándar OpenAPI 3.0.

### Acceder a la Documentación

Una vez que el servidor esté corriendo, puedes acceder a:

- **ReDoc** (página principal): `http://localhost:8000/`
  - Interfaz moderna y limpia para explorar la API
  - Documentación bilingüe (español/inglés)
  - Incluye ejemplos de request/response

- **Swagger UI**: `http://localhost:8000/api/docs/`
  - Interfaz interactiva para probar los endpoints
  - Permite ejecutar requests directamente desde el navegador

- **OpenAPI Schema**: `http://localhost:8000/api/schema/`
  - Schema en formato YAML/JSON
  - Compatible con cualquier herramienta OpenAPI

### Generar Schema Estático

Para generar un archivo estático del schema:

```bash
python manage.py spectacular --color --file schema.yml
```

## Endpoints de la API

### Projects
- `GET /api/projects/` - Listar todos los proyectos
- `GET /api/projects/{id}/` - Detalle de un proyecto
- `GET /api/projects/featured/` - Proyectos destacados
- `POST /api/projects/` - Crear proyecto (admin)
- `PUT /api/projects/{id}/` - Actualizar proyecto (admin)
- `DELETE /api/projects/{id}/` - Eliminar proyecto (admin)

### Skills
- `GET /api/skills/` - Listar todas las habilidades
- `GET /api/skills/{id}/` - Detalle de una habilidad
- `GET /api/skills/featured/` - Habilidades destacadas
- `GET /api/skills/by_category/` - Habilidades agrupadas por categoría
- `GET /api/skill-categories/` - Listar categorías de habilidades

### About
- `GET /api/about/` - Listar perfiles
- `GET /api/about/active/` - Obtener perfil activo
- `GET /api/about/{id}/` - Detalle de perfil

### Contact
- `GET /api/contact/` - Listar mensajes (admin)
- `POST /api/contact/` - Enviar mensaje de contacto
- `GET /api/contact/unread/` - Mensajes no leídos (admin)
- `POST /api/contact/{id}/mark_read/` - Marcar como leído (admin)
- `POST /api/contact/{id}/mark_replied/` - Marcar como respondido (admin)

## Deploy en Railway

### 1. Instalar Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login en Railway

```bash
railway login
```

### 3. Inicializar proyecto

```bash
railway init
```

### 4. Agregar PostgreSQL

```bash
railway add
# Seleccionar PostgreSQL
```

### 5. Configurar variables de entorno en Railway

- `DJANGO_ENV=production`
- `SECRET_KEY=<tu-secret-key>`
- `DATABASE_URL=<configurado-automaticamente>`

### 6. Deploy

```bash
railway up
```

## Tecnologías Utilizadas

- Django 4.2+
- Django REST Framework 3.14+
- drf-spectacular (documentación OpenAPI 3.0)
- PostgreSQL (producción)
- SQLite (desarrollo)
- Python 3.9+
- Gunicorn (servidor WSGI)
- WhiteNoise (archivos estáticos)
- python-decouple (variables de entorno)

## Convenciones de Código

- **JSON Keys**: camelCase (no snake_case)
- **Python Code**: snake_case
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE

## Licencia

MIT License

## Autor

Tu Nombre
