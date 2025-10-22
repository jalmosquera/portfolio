# Arquitectura del Proyecto

[English Version](../en/architecture.md) | [Volver al README](../../README.md)

Este documento describe la arquitectura y patrones de diseno utilizados en el proyecto Portfolio API.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Patrones Arquitectonicos](#patrones-arquitectonicos)
- [Estructura de Aplicaciones](#estructura-de-aplicaciones)
- [Capa de API](#capa-de-api)
- [Capa de Modelos](#capa-de-modelos)
- [Configuracion Multi-Entorno](#configuracion-multi-entorno)
- [Flujo de Datos](#flujo-de-datos)
- [Decisiones de Diseno](#decisiones-de-diseno)

---

## Vision General

El proyecto Portfolio API esta construido siguiendo los principios de **arquitectura modular** y **separacion de responsabilidades**. Utiliza Django como framework base y Django REST Framework para la exposicion de servicios REST.

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         Cliente                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │   React    │  │    Vue     │  │  Angular   │  ...           │
│  └────────────┘  └────────────┘  └────────────┘                │
└────────────┬────────────────────────────────────────────────────┘
             │ HTTP/HTTPS (JSON camelCase)
             │ CORS Headers
┌────────────▼────────────────────────────────────────────────────┐
│                      Capa de Presentacion                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │             API Documentation Layer                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │   ReDoc    │  │  Swagger   │  │   Schema   │         │  │
│  │  │  (Root)    │  │  /api/docs │  │ /api/schema│         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Django REST Framework Routers                  │  │
│  │  /api/projects/    /api/skills/    /api/about/           │  │
│  │  /api/contact/     /api/skill-categories/                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                      Capa de Aplicacion                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Apps Modulares                           │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │  │
│  │  │ Projects │  │  Skills  │  │  About   │  │ Contact  │ │  │
│  │  │          │  │          │  │          │  │          │ │  │
│  │  │ ViewSets │  │ ViewSets │  │ ViewSets │  │ ViewSets │ │  │
│  │  │ Serializ.│  │ Serializ.│  │ Serializ.│  │ Serializ.│ │  │
│  │  │ Models   │  │ Models   │  │ Models   │  │ Models   │ │  │
│  │  │ Admin    │  │ Admin    │  │ Admin    │  │ Admin    │ │  │
│  │  │ Tests    │  │ Tests    │  │ Tests    │  │ Tests    │ │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                      Capa de Persistencia                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Django ORM                             │  │
│  │  - Migraciones automaticas                                │  │
│  │  - Validaciones de modelo                                 │  │
│  │  - Relaciones (ForeignKey, ManyToMany)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                      Base de Datos                               │
│  ┌──────────────┐              ┌──────────────┐                │
│  │    SQLite    │              │  PostgreSQL  │                │
│  │ (Development)│              │ (Production) │                │
│  └──────────────┘              └──────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Patrones Arquitectonicos

### 1. Arquitectura en Capas (Layered Architecture)

El proyecto esta organizado en capas bien definidas:

- **Capa de Presentacion**: Django REST Framework ViewSets y Routers
- **Capa de Aplicacion**: Logica de negocio en models y serializers
- **Capa de Persistencia**: Django ORM
- **Capa de Datos**: PostgreSQL/SQLite

### 2. Modular Monolith

El proyecto sigue el patron de **Monolito Modular**, donde cada app Django representa un modulo de dominio independiente:

- **projects**: Gestion de proyectos del portafolio
- **skills**: Gestion de habilidades y tecnologias
- **about**: Informacion personal y biografica
- **contact**: Mensajes de contacto

Cada modulo es autocontenido con sus propios modelos, vistas, serializadores, tests y configuracion de admin.

### 3. RESTful API Design

Se siguen los principios REST:
- Recursos identificados por URLs (`/api/projects/`, `/api/skills/`)
- Operaciones CRUD mapeadas a metodos HTTP (GET, POST, PUT, PATCH, DELETE)
- Respuestas consistentes en formato JSON
- Codigos de estado HTTP apropiados
- HATEOAS parcial con links en documentacion

### 4. API-First Approach

La API es el contrato principal:
- Documentacion OpenAPI 3.0 generada automaticamente
- Schema-first con drf-spectacular
- Versionamiento preparado para futuras versiones
- Validacion de datos en entrada y salida

## Estructura de Aplicaciones

Cada aplicacion Django sigue una estructura consistente:

```
apps/<app_name>/
├── api/
│   ├── __init__.py
│   ├── router.py          # Configuracion de rutas DRF
│   ├── serializers.py     # Serializadores (validacion y transformacion)
│   └── views.py           # ViewSets (logica de endpoints)
├── migrations/            # Migraciones de base de datos
│   └── __init__.py
├── tests/                 # Tests unitarios
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_views.py
├── __init__.py
├── admin.py              # Configuracion Django Admin
├── apps.py               # Configuracion de la aplicacion
├── models.py             # Modelos de datos
└── views.py              # Vistas tradicionales (si son necesarias)
```

### Responsabilidades por Componente

#### Models (`models.py`)
- Definicion de estructura de datos
- Validaciones de negocio
- Metodos de modelo personalizados
- Metodos `__str__` para representacion legible
- Meta opciones (ordering, verbose_name, etc.)

#### Serializers (`api/serializers.py`)
- Transformacion entre JSON y modelos Python
- Validacion de datos de entrada
- Campos calculados y de solo lectura
- Conversion a camelCase para respuestas
- Serializadores anidados cuando es necesario

#### ViewSets (`api/views.py`)
- Endpoints de API (CRUD)
- Acciones personalizadas (@action)
- Filtrado, busqueda y ordenamiento
- Paginacion
- Documentacion con decoradores @extend_schema

#### Admin (`admin.py`)
- Interfaz de administracion personalizada
- list_display, list_filter, search_fields
- Edicion inline
- Fieldsets para organizar formularios
- Acciones personalizadas

#### Tests (`tests/`)
- Tests unitarios de modelos
- Tests de serializadores
- Tests de endpoints API
- Fixtures para datos de prueba
- Cobertura minima del 90%

## Capa de API

### Django REST Framework ViewSets

Se utilizan `ModelViewSet` para proporcionar operaciones CRUD completas:

```python
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name', 'percentage']
    ordering = ['category__order', 'order', 'name']
```

### Acciones Personalizadas

Endpoints adicionales con el decorador `@action`:

```python
@action(detail=False, methods=['get'])
def featured(self, request):
    """Obtener solo habilidades destacadas"""
    featured_skills = self.queryset.filter(is_featured=True)
    serializer = self.get_serializer(featured_skills, many=True)
    return Response(serializer.data)
```

### Routers

Configuracion automatica de URLs con `DefaultRouter`:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'skill-categories', SkillCategoryViewSet, basename='skill-category')

urlpatterns = router.urls
```

Genera automaticamente:
- `/api/skills/` - Lista y creacion
- `/api/skills/{id}/` - Detalle, actualizacion, eliminacion
- `/api/skills/featured/` - Accion personalizada

### Documentacion OpenAPI

Uso de drf-spectacular para generar documentacion:

```python
@extend_schema_view(
    list=extend_schema(
        summary="List all skills",
        description="Retrieve a list of all skills with search and ordering support.",
        tags=["Skills"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a skill",
        description="Get details of a specific skill by ID.",
        tags=["Skills"],
    ),
)
class SkillViewSet(viewsets.ModelViewSet):
    # ...
```

## Capa de Modelos

### Diseno de Modelos

Los modelos siguen principios de:
- **Single Responsibility**: Cada modelo representa una entidad de negocio
- **Normalizacion**: Evitar redundancia de datos
- **Relaciones Claras**: ForeignKey con related_name descriptivos
- **Timestamps**: created_at y updated_at en todos los modelos
- **Verbose Names**: Campos con nombres legibles para el admin

### Ejemplo: Modelo Skill

```python
class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__order", "order", "name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.category.name})"
```

### Validaciones

- **Validadores de campo**: MinValueValidator, MaxValueValidator
- **Choices**: Para campos con valores limitados (proficiency)
- **Unique constraints**: Para evitar duplicados
- **Custom validation**: En el metodo clean() cuando es necesario

## Configuracion Multi-Entorno

El proyecto utiliza configuracion separada por entorno:

```
core/settings/
├── __init__.py       # Selector de configuracion basado en DJANGO_ENV
├── base.py          # Configuracion comun a todos los entornos
├── development.py   # Configuracion de desarrollo
└── production.py    # Configuracion de produccion
```

### Base Settings (`base.py`)

Configuracion compartida:
- INSTALLED_APPS
- MIDDLEWARE
- TEMPLATES
- REST_FRAMEWORK settings
- SPECTACULAR_SETTINGS
- PASSWORD_VALIDATORS
- Internationalization

### Development Settings (`development.py`)

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### Production Settings (`production.py`)

```python
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: v.split(","))

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Selector de Entorno

`core/settings/__init__.py`:

```python
import os
from decouple import config

env = config('DJANGO_ENV', default='development')

if env == 'production':
    from .production import *
elif env == 'development':
    from .development import *
```

## Flujo de Datos

### Request Flow (Lectura)

```
1. Cliente → GET /api/skills/
2. Django URL Router → core/urls.py
3. Include Router → apps/skills/api/router.py
4. ViewSet → SkillViewSet.list()
5. QuerySet → Skill.objects.all()
6. Serializer → SkillSerializer(queryset, many=True)
7. Response → JSON camelCase
8. Cliente ← JSON Response
```

### Request Flow (Escritura)

```
1. Cliente → POST /api/skills/
2. Django URL Router → core/urls.py
3. ViewSet → SkillViewSet.create()
4. Serializer → SkillSerializer(data=request.data)
5. Validation → serializer.is_valid(raise_exception=True)
6. Save → serializer.save()
7. Model → skill.save() [triggers signals, validators]
8. Response → JSON con objeto creado (201 Created)
9. Cliente ← JSON Response
```

### Accion Personalizada Flow

```
1. Cliente → GET /api/skills/featured/
2. Django URL Router → core/urls.py
3. ViewSet → SkillViewSet.featured()
4. QuerySet Filtrado → Skill.objects.filter(is_featured=True)
5. Serializer → SkillSerializer(featured_skills, many=True)
6. Response → JSON camelCase
7. Cliente ← JSON Response
```

## Decisiones de Diseno

### 1. camelCase en JSON

**Decision**: Usar camelCase en respuestas JSON en lugar de snake_case.

**Razon**:
- Convencion estandar en JavaScript/TypeScript
- Mejor integracion con frontends modernos
- Consistencia con el ecosistema JS

**Implementacion**:
```python
# En serializers
class SkillSerializer(serializers.ModelSerializer):
    categoryId = serializers.PrimaryKeyRelatedField(source='category', ...)
    categoryName = serializers.CharField(source='category.name', ...)
    yearsExperience = serializers.IntegerField(source='years_experience')
```

### 2. ViewSets vs APIView

**Decision**: Usar ViewSets para operaciones CRUD estandar.

**Razon**:
- Menos codigo boilerplate
- Generacion automatica de URLs con routers
- Consistencia entre endpoints
- Mejor integracion con drf-spectacular

### 3. Modular Monolith vs Microservicios

**Decision**: Comenzar con monolito modular.

**Razon**:
- Simplicidad de deployment
- Menor overhead de comunicacion
- Transacciones ACID facilmente
- Facil migracion a microservicios si es necesario

### 4. SQLite vs PostgreSQL

**Decision**: SQLite para desarrollo, PostgreSQL para produccion.

**Razon**:
- SQLite: Sin instalacion adicional, rapido para desarrollo
- PostgreSQL: Robusto, escalable, soportado por plataformas cloud

### 5. Estructura de Tests

**Decision**: Tests organizados por tipo (models, serializers, views).

**Razon**:
- Facilita ubicar tests
- Tests mas focalizados
- Mejor mantenibilidad
- Cobertura clara por componente

### 6. API Documentation

**Decision**: drf-spectacular en lugar de drf-yasg.

**Razon**:
- Soporte OpenAPI 3.0 (mas moderno)
- Mejor integracion con DRF 3.14+
- Generacion automatica mas precisa
- Mantenimiento activo

---

## Proximos Pasos

Para profundizar en aspectos especificos:
- [Modelos y Base de Datos](modelos.md)
- [Documentacion de API](api.md)
- [Guia de Testing](testing.md)
- [Variables de Entorno](variables-entorno.md)

[Volver al README Principal](../../README.md)
