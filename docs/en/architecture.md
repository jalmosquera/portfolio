# Project Architecture

[Spanish Version](../es/arquitectura.md) | [Back to README](../../README.en.md)

This document describes the architecture and design patterns used in the Portfolio API project.

## Table of Contents

- [Overview](#overview)
- [Architectural Patterns](#architectural-patterns)
- [Application Structure](#application-structure)
- [API Layer](#api-layer)
- [Model Layer](#model-layer)
- [Multi-Environment Configuration](#multi-environment-configuration)
- [Data Flow](#data-flow)
- [Design Decisions](#design-decisions)

---

## Overview

The Portfolio API project is built following **modular architecture** and **separation of concerns** principles. It uses Django as the base framework and Django REST Framework for exposing REST services.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           Client                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │   React    │  │    Vue     │  │  Angular   │  ...           │
│  └────────────┘  └────────────┘  └────────────┘                │
└────────────┬────────────────────────────────────────────────────┘
             │ HTTP/HTTPS (JSON camelCase)
             │ CORS Headers
┌────────────▼────────────────────────────────────────────────────┐
│                      Presentation Layer                          │
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
│                      Application Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Modular Apps                             │  │
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
│                      Persistence Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Django ORM                             │  │
│  │  - Automatic migrations                                   │  │
│  │  - Model validations                                      │  │
│  │  - Relationships (ForeignKey, ManyToMany)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                         Database                                 │
│  ┌──────────────┐              ┌──────────────┐                │
│  │    SQLite    │              │  PostgreSQL  │                │
│  │ (Development)│              │ (Production) │                │
│  └──────────────┘              └──────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Architectural Patterns

### 1. Layered Architecture

The project is organized in well-defined layers:

- **Presentation Layer**: Django REST Framework ViewSets and Routers
- **Application Layer**: Business logic in models and serializers
- **Persistence Layer**: Django ORM
- **Data Layer**: PostgreSQL/SQLite

### 2. Modular Monolith

The project follows the **Modular Monolith** pattern, where each Django app represents an independent domain module:

- **projects**: Portfolio project management
- **skills**: Skills and technologies management
- **about**: Personal and biographical information
- **contact**: Contact messages

Each module is self-contained with its own models, views, serializers, tests, and admin configuration.

### 3. RESTful API Design

REST principles are followed:
- Resources identified by URLs (`/api/projects/`, `/api/skills/`)
- CRUD operations mapped to HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Consistent JSON responses
- Appropriate HTTP status codes
- Partial HATEOAS with links in documentation

### 4. API-First Approach

The API is the main contract:
- OpenAPI 3.0 documentation automatically generated
- Schema-first with drf-spectacular
- Versioning prepared for future versions
- Data validation on input and output

## Application Structure

Each Django application follows a consistent structure:

```
apps/<app_name>/
├── api/
│   ├── __init__.py
│   ├── router.py          # DRF route configuration
│   ├── serializers.py     # Serializers (validation and transformation)
│   └── views.py           # ViewSets (endpoint logic)
├── migrations/            # Database migrations
│   └── __init__.py
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_views.py
├── __init__.py
├── admin.py              # Django Admin configuration
├── apps.py               # Application configuration
├── models.py             # Data models
└── views.py              # Traditional views (if needed)
```

### Responsibilities by Component

#### Models (`models.py`)
- Data structure definition
- Business validations
- Custom model methods
- `__str__` methods for readable representation
- Meta options (ordering, verbose_name, etc.)

#### Serializers (`api/serializers.py`)
- Transformation between JSON and Python models
- Input data validation
- Calculated and read-only fields
- Conversion to camelCase for responses
- Nested serializers when necessary

#### ViewSets (`api/views.py`)
- API endpoints (CRUD)
- Custom actions (@action)
- Filtering, searching, and ordering
- Pagination
- Documentation with @extend_schema decorators

#### Admin (`admin.py`)
- Custom administration interface
- list_display, list_filter, search_fields
- Inline editing
- Fieldsets for form organization
- Custom actions

#### Tests (`tests/`)
- Model unit tests
- Serializer tests
- API endpoint tests
- Fixtures for test data
- Minimum 90% coverage

## API Layer

### Django REST Framework ViewSets

`ModelViewSet` is used to provide complete CRUD operations:

```python
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name', 'percentage']
    ordering = ['category__order', 'order', 'name']
```

### Custom Actions

Additional endpoints with the `@action` decorator:

```python
@action(detail=False, methods=['get'])
def featured(self, request):
    """Get featured skills only"""
    featured_skills = self.queryset.filter(is_featured=True)
    serializer = self.get_serializer(featured_skills, many=True)
    return Response(serializer.data)
```

### Routers

Automatic URL configuration with `DefaultRouter`:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'skill-categories', SkillCategoryViewSet, basename='skill-category')

urlpatterns = router.urls
```

Automatically generates:
- `/api/skills/` - List and creation
- `/api/skills/{id}/` - Detail, update, deletion
- `/api/skills/featured/` - Custom action

## Model Layer

### Model Design

Models follow principles of:
- **Single Responsibility**: Each model represents a business entity
- **Normalization**: Avoid data redundancy
- **Clear Relationships**: ForeignKey with descriptive related_name
- **Timestamps**: created_at and updated_at in all models
- **Verbose Names**: Fields with readable names for admin

### Example: Skill Model

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

## Multi-Environment Configuration

The project uses separate configuration by environment:

```
core/settings/
├── __init__.py       # Configuration selector based on DJANGO_ENV
├── base.py          # Common configuration for all environments
├── development.py   # Development configuration
└── production.py    # Production configuration
```

### Base Settings (`base.py`)

Shared configuration:
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

## Data Flow

### Request Flow (Read)

```
1. Client → GET /api/skills/
2. Django URL Router → core/urls.py
3. Include Router → apps/skills/api/router.py
4. ViewSet → SkillViewSet.list()
5. QuerySet → Skill.objects.all()
6. Serializer → SkillSerializer(queryset, many=True)
7. Response → JSON camelCase
8. Client ← JSON Response
```

### Request Flow (Write)

```
1. Client → POST /api/skills/
2. Django URL Router → core/urls.py
3. ViewSet → SkillViewSet.create()
4. Serializer → SkillSerializer(data=request.data)
5. Validation → serializer.is_valid(raise_exception=True)
6. Save → serializer.save()
7. Model → skill.save() [triggers signals, validators]
8. Response → JSON with created object (201 Created)
9. Client ← JSON Response
```

## Design Decisions

### 1. camelCase in JSON

**Decision**: Use camelCase in JSON responses instead of snake_case.

**Reason**:
- Standard convention in JavaScript/TypeScript
- Better integration with modern frontends
- Consistency with JS ecosystem

**Implementation**:
```python
# In serializers
class SkillSerializer(serializers.ModelSerializer):
    categoryId = serializers.PrimaryKeyRelatedField(source='category', ...)
    categoryName = serializers.CharField(source='category.name', ...)
    yearsExperience = serializers.IntegerField(source='years_experience')
```

### 2. ViewSets vs APIView

**Decision**: Use ViewSets for standard CRUD operations.

**Reason**:
- Less boilerplate code
- Automatic URL generation with routers
- Consistency between endpoints
- Better integration with drf-spectacular

### 3. Modular Monolith vs Microservices

**Decision**: Start with modular monolith.

**Reason**:
- Deployment simplicity
- Lower communication overhead
- Easy ACID transactions
- Easy migration to microservices if needed

### 4. SQLite vs PostgreSQL

**Decision**: SQLite for development, PostgreSQL for production.

**Reason**:
- SQLite: No additional installation, fast for development
- PostgreSQL: Robust, scalable, supported by cloud platforms

### 5. Test Structure

**Decision**: Tests organized by type (models, serializers, views).

**Reason**:
- Easier to locate tests
- More focused tests
- Better maintainability
- Clear coverage by component

### 6. API Documentation

**Decision**: drf-spectacular instead of drf-yasg.

**Reason**:
- OpenAPI 3.0 support (more modern)
- Better integration with DRF 3.14+
- More accurate automatic generation
- Active maintenance

---

## Next Steps

To deepen specific aspects:
- [Models and Database](models.md)
- [API Documentation](api.md)
- [Testing Guide](testing.md)
- [Environment Variables](environment-variables.md)

[Back to Main README](../../README.en.md)
