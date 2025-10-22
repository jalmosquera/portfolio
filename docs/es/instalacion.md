# Guia de Instalacion

[English Version](../en/installation.md) | [Volver al README](../../README.md)

Guia detallada para instalar y configurar el proyecto Portfolio API en tu entorno local.

## Tabla de Contenidos

- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalacion Paso a Paso](#instalacion-paso-a-paso)
- [Configuracion de Variables de Entorno](#configuracion-de-variables-de-entorno)
- [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
- [Creacion de Superusuario](#creacion-de-superusuario)
- [Carga de Datos de Prueba](#carga-de-datos-de-prueba)
- [Verificacion de la Instalacion](#verificacion-de-la-instalacion)
- [Problemas Comunes](#problemas-comunes)

---

## Requisitos del Sistema

### Software Requerido

- **Python**: Version 3.9 o superior
  - Verificar: `python --version` o `python3 --version`
- **pip**: Gestor de paquetes de Python
  - Verificar: `pip --version` o `pip3 --version`
- **Git**: Para clonar el repositorio
  - Verificar: `git --version`

### Software Opcional (Recomendado)

- **PostgreSQL**: Para base de datos de produccion (10 o superior)
- **virtualenv** o **venv**: Para entornos virtuales aislados
- **PostgreSQL GUI**: pgAdmin, DBeaver, o TablePlus

### Sistemas Operativos Soportados

- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS (10.14 o superior)
- Windows 10/11 (con WSL recomendado)

---

## Instalacion Paso a Paso

### 1. Clonar el Repositorio

```bash
# Clonar via HTTPS
git clone https://github.com/tu-usuario/portfolio.git

# O via SSH
git clone git@github.com:tu-usuario/portfolio.git

# Navegar al directorio del proyecto
cd portfolio
```

### 2. Crear Entorno Virtual

Es **altamente recomendado** usar un entorno virtual para aislar las dependencias del proyecto.

#### En Linux/macOS:

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate

# Verificar que el entorno esta activo (deberia mostrar (.venv) en el prompt)
```

#### En Windows:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# O en PowerShell
.venv\Scripts\Activate.ps1
```

**Desactivar entorno virtual** (cuando termines):

```bash
deactivate
```

### 3. Actualizar pip

Es buena practica actualizar pip antes de instalar dependencias:

```bash
pip install --upgrade pip
```

### 4. Instalar Dependencias

#### Dependencias de Produccion

```bash
pip install -r requirements.txt
```

Esto instalara:
- Django 4.2+
- djangorestframework 3.14+
- drf-spectacular 0.28.0
- psycopg2-binary (para PostgreSQL)
- python-decouple
- django-cors-headers
- Pillow
- whitenoise
- gunicorn

#### Dependencias de Desarrollo (Opcional)

Para ejecutar tests y desarrollo:

```bash
pip install -r requirements-test.txt
```

Esto instalara adicionalmente:
- pytest
- pytest-django
- pytest-cov
- factory-boy

### 5. Verificar Instalacion de Dependencias

```bash
pip list
```

Deberia mostrar todas las dependencias instaladas.

---

## Configuracion de Variables de Entorno

### 1. Copiar Archivo de Ejemplo

```bash
cp .env.example .env
```

### 2. Editar Variables de Entorno

Abre el archivo `.env` y configura las variables:

```env
# ========================================
# Django Configuration
# ========================================
DJANGO_ENV=development
SECRET_KEY=tu-clave-secreta-unica-y-segura-aqui
DEBUG=True

# ========================================
# Database Configuration
# ========================================
# Para desarrollo (SQLite - no requiere configuracion adicional)
# Para produccion (PostgreSQL):
DATABASE_URL=postgresql://usuario:password@localhost:5432/portfolio_db

# ========================================
# Email Configuration
# ========================================
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# ========================================
# CORS Configuration
# ========================================
# Agregar origenes permitidos separados por comas
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# ========================================
# Production Settings (Optional)
# ========================================
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
```

### 3. Generar SECRET_KEY Segura

Para generar una SECRET_KEY unica:

```python
# Ejecutar en Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pega en `.env`:

```env
SECRET_KEY=django-insecure-abc123...xyz789
```

**IMPORTANTE**: Nunca compartas tu SECRET_KEY ni la subas a control de versiones.

### 4. Configuracion de Email (Opcional)

Para usar Gmail:

1. Ve a tu cuenta de Google
2. Habilita "Verificacion en 2 pasos"
3. Genera una "Contrasena de aplicacion"
4. Usa esa contrasena en `EMAIL_HOST_PASSWORD`

---

## Migraciones de Base de Datos

### 1. Crear Base de Datos (Solo PostgreSQL)

Si usas PostgreSQL en produccion:

```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE portfolio_db;

-- Crear usuario
CREATE USER portfolio_user WITH PASSWORD 'tu_password';

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;

-- Salir
\q
```

### 2. Ejecutar Migraciones

```bash
# Aplicar migraciones
python manage.py migrate
```

Esto creara todas las tablas necesarias:
- `projects_project`
- `skills_skillcategory`
- `skills_skill`
- `about_aboutme`
- `contact_contactmessage`
- Tablas de Django (auth, sessions, admin, etc.)

Deberia ver una salida similar a:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, projects, skills, about, contact
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying skills.0001_initial... OK
  Applying contact.0001_initial... OK
```

### 3. Verificar Migraciones

```bash
# Ver el estado de las migraciones
python manage.py showmigrations

# Deberia mostrar [X] en todas las migraciones
```

---

## Creacion de Superusuario

Para acceder al panel de administracion Django:

```bash
python manage.py createsuperuser
```

Completa los datos solicitados:

```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

**Recomendaciones**:
- Usa un nombre de usuario diferente a "admin" por seguridad
- Usa una contrasena fuerte (minimo 8 caracteres, letras, numeros, simbolos)
- Guarda las credenciales en un lugar seguro

---

## Carga de Datos de Prueba

### Opcion 1: Manualmente via Admin

1. Iniciar el servidor: `python manage.py runserver`
2. Ir a: `http://localhost:8000/admin/`
3. Iniciar sesion con el superusuario creado
4. Agregar datos manualmente

### Opcion 2: Via Shell de Django

```bash
python manage.py shell
```

```python
from apps.skills.models import SkillCategory, Skill
from apps.projects.models import Project

# Crear categoria de habilidades
backend = SkillCategory.objects.create(
    name="Backend",
    description="Backend technologies",
    order=1
)

# Crear habilidades
django_skill = Skill.objects.create(
    name="Django",
    category=backend,
    proficiency="expert",
    percentage=95,
    years_experience=5,
    description="Python web framework",
    is_featured=True,
    order=1
)

# Crear proyecto
project = Project.objects.create(
    title="Portfolio API",
    description="Professional REST API for personal portfolio",
    short_description="Django REST API",
    technologies="Django,DRF,PostgreSQL",
    is_featured=True,
    order=1
)

print("Datos de prueba creados!")
```

### Opcion 3: Fixtures (Si estan disponibles)

```bash
python manage.py loaddata fixtures/initial_data.json
```

---

## Verificacion de la Instalacion

### 1. Recolectar Archivos Estaticos

```bash
python manage.py collectstatic --noinput
```

### 2. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Deberia ver:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 22, 2024 - 10:30:45
Django version 4.2.x, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 3. Verificar Endpoints

Abre tu navegador y visita:

- **API Documentation (ReDoc)**: http://localhost:8000/
- **Swagger UI**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/
- **API Endpoints**:
  - http://localhost:8000/api/projects/
  - http://localhost:8000/api/skills/
  - http://localhost:8000/api/about/
  - http://localhost:8000/api/contact/

### 4. Ejecutar Tests (Opcional)

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=apps

# Si todo esta bien, deberia mostrar:
# ===== X passed in Y.XXs =====
```

---

## Problemas Comunes

### Problema: "Command not found: python"

**Solucion**:

```bash
# En Linux/macOS, intenta:
python3 manage.py runserver

# O crea un alias:
alias python=python3
```

### Problema: "No module named 'django'"

**Solucion**:

Asegurate de que el entorno virtual esta activado:

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

Reinstala las dependencias:

```bash
pip install -r requirements.txt
```

### Problema: "ModuleNotFoundError: No module named 'decouple'"

**Solucion**:

```bash
pip install python-decouple
```

### Problema: "SECRET_KEY not set"

**Solucion**:

Verifica que el archivo `.env` existe y contiene `SECRET_KEY`:

```bash
cat .env | grep SECRET_KEY
```

### Problema: "FATAL: password authentication failed for user"

**Solucion PostgreSQL**:

1. Verifica que PostgreSQL esta corriendo:

```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list
```

2. Verifica las credenciales en `.env`
3. Prueba la conexion:

```bash
psql -U portfolio_user -d portfolio_db -h localhost
```

### Problema: "Port 8000 is already in use"

**Solucion**:

Usa un puerto diferente:

```bash
python manage.py runserver 8080
```

O encuentra y detiene el proceso:

```bash
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: "Migrations are not applied"

**Solucion**:

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar todas las migraciones
python manage.py migrate

# Si hay problemas, intenta:
python manage.py migrate --run-syncdb
```

### Problema: Error con Pillow (imagenes)

**Solucion**:

Instala dependencias del sistema:

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libjpeg-dev zlib1g-dev

# macOS
brew install jpeg

# Luego reinstala Pillow
pip install --upgrade Pillow
```

---

## Proximos Pasos

Una vez instalado correctamente:

1. **Explora el Admin**: http://localhost:8000/admin/
2. **Lee la documentacion de API**: http://localhost:8000/
3. **Configura tu entorno de desarrollo**: Editor, linters, etc.
4. **Revisa la arquitectura**: [arquitectura.md](arquitectura.md)
5. **Ejecuta los tests**: [testing.md](testing.md)

---

## Recursos Adicionales

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [python-decouple](https://github.com/henriquebastos/python-decouple)

---

[Volver al README Principal](../../README.md) | [Variables de Entorno](variables-entorno.md) | [Deployment](deploy.md)
