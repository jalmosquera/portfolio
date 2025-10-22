# Personal Portfolio - Django REST API

[Spanish Version](README.md) | [Complete Documentation](docs/en/)

Professional REST API for personal portfolio built with Django and Django REST Framework. Modular system with interactive OpenAPI documentation, multilanguage support, and multi-environment configuration.

## Table of Contents

- [Key Features](#key-features)
- [Technologies](#technologies)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [API Documentation](#api-documentation)
  - [Main Endpoints](#main-endpoints)
  - [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Testing](#testing)
- [Deployment](#deployment)
- [Commit Conventions](#commit-conventions)
- [Complete Documentation](#complete-documentation)
- [License](#license)

---

## Key Features

- **Complete REST API**: Professional implementation with Django REST Framework
- **Interactive Documentation**: OpenAPI 3.0 with drf-spectacular (Swagger UI and ReDoc)
- **Modular Architecture**: Organized by apps (projects, skills, about, contact)
- **camelCase Responses**: Modern JSON convention for frontend integration
- **Multi-Environment**: Separate configurations for development and production
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment Ready**: Configured for Railway with Gunicorn and WhiteNoise
- **CORS Enabled**: Full support for frontend applications
- **Custom Admin**: Optimized Django administration interface
- **Bilingual Documentation**: Spanish and English in code and documentation

## Technologies

### Backend
- **Django 4.2+**: High-level web framework
- **Django REST Framework 3.14+**: Toolkit for building REST APIs
- **drf-spectacular 0.28.0**: OpenAPI 3.0 schema generation

### Database
- **PostgreSQL**: Production database
- **SQLite**: Development database

### Server and Deployment
- **Gunicorn 21.2+**: WSGI HTTP server for Python
- **WhiteNoise 6.6+**: Static file serving
- **Railway**: Deployment platform

### Utilities
- **python-decouple 3.8+**: Separation of configuration from code
- **Pillow 10.0+**: Image processing
- **django-cors-headers 4.3+**: CORS handling

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client / Frontend                        │
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
│                    Modular Apps                              │
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

For more architectural details, see [Project Architecture](docs/en/architecture.md).

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- PostgreSQL (production only)
- Git

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd portfolio

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your configurations

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (to access admin)
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Run development server
python manage.py runserver
```

### Configuration

The project uses `python-decouple` to handle environment variables. Create a `.env` file based on `.env.example`:

```env
# Django Configuration
DJANGO_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database Configuration (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

See complete documentation at [Environment Variables](docs/en/environment-variables.md).

## API Documentation

The project includes interactive documentation automatically generated with drf-spectacular:

- **ReDoc** (recommended): `http://localhost:8000/`
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Main Endpoints

#### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List all projects (paginated) |
| GET | `/api/projects/{id}/` | Get project detail |
| GET | `/api/projects/featured/` | List featured projects |
| POST | `/api/projects/` | Create new project (admin) |
| PUT/PATCH | `/api/projects/{id}/` | Update project (admin) |
| DELETE | `/api/projects/{id}/` | Delete project (admin) |

#### Skills
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/skills/` | List all skills |
| GET | `/api/skills/{id}/` | Get skill detail |
| GET | `/api/skills/featured/` | List featured skills |
| GET | `/api/skills/by_category/` | Skills grouped by category |
| POST | `/api/skills/` | Create new skill (admin) |
| PUT/PATCH | `/api/skills/{id}/` | Update skill (admin) |
| DELETE | `/api/skills/{id}/` | Delete skill (admin) |

#### Skill Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/skill-categories/` | List categories with their skills |
| GET | `/api/skill-categories/{id}/` | Get category detail |
| POST | `/api/skill-categories/` | Create new category (admin) |
| PUT/PATCH | `/api/skill-categories/{id}/` | Update category (admin) |
| DELETE | `/api/skill-categories/{id}/` | Delete category (admin) |

#### About
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/about/` | List all profiles |
| GET | `/api/about/{id}/` | Get profile detail |
| GET | `/api/about/active/` | Get current active profile |
| POST | `/api/about/` | Create new profile (admin) |
| PUT/PATCH | `/api/about/{id}/` | Update profile (admin) |
| DELETE | `/api/about/{id}/` | Delete profile (admin) |

#### Contact
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/contact/` | List contact messages (admin) |
| GET | `/api/contact/{id}/` | Get message detail (admin) |
| GET | `/api/contact/unread/` | List unread messages (admin) |
| POST | `/api/contact/` | Send contact message (public) |
| POST | `/api/contact/{id}/mark_read/` | Mark as read (admin) |
| POST | `/api/contact/{id}/mark_replied/` | Mark as replied (admin) |

### Usage Examples

#### List Featured Projects
```bash
curl -X GET http://localhost:8000/api/projects/featured/
```

Response:
```json
[
  {
    "id": 1,
    "title": "E-Commerce Platform",
    "description": "Complete e-commerce platform...",
    "shortDescription": "Online sales system with Django",
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

#### Get Skills by Category
```bash
curl -X GET http://localhost:8000/api/skills/by_category/
```

Response:
```json
[
  {
    "id": 1,
    "name": "Backend",
    "description": "Backend technologies and APIs",
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
        "description": "Python web framework",
        "yearsExperience": 5,
        "isFeatured": true,
        "order": 1
      }
    ]
  }
]
```

#### Send Contact Message
```bash
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Project inquiry",
    "message": "Hello, I am interested in learning more about...",
    "phone": "+1 555 1234567"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Project inquiry",
  "message": "Hello, I am interested in learning more about...",
  "phone": "+1 555 1234567",
  "isRead": false,
  "isReplied": false,
  "createdAt": "2024-01-22T09:15:00Z",
  "updatedAt": "2024-01-22T09:15:00Z"
}
```

For more examples and details, see [API Documentation](docs/en/api.md).

## Project Structure

```
portfolio/
├── apps/                           # Django applications
│   ├── projects/                   # Projects app
│   │   ├── api/
│   │   │   ├── router.py          # Route configuration
│   │   │   ├── serializers.py     # DRF serializers
│   │   │   └── views.py           # API ViewSets
│   │   ├── migrations/            # DB migrations
│   │   ├── tests/                 # Unit tests
│   │   ├── admin.py               # Admin configuration
│   │   └── models.py              # Data models
│   ├── skills/                    # Skills app
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── admin.py               # Custom admin
│   │   └── models.py              # SkillCategory and Skill
│   ├── about/                     # Personal information app
│   │   ├── api/
│   │   ├── migrations/
│   │   ├── tests/
│   │   └── models.py              # AboutMe model
│   └── contact/                   # Contact messages app
│       ├── api/
│       ├── migrations/
│       ├── tests/
│       └── models.py              # ContactMessage model
├── core/                          # Main configuration
│   ├── settings/
│   │   ├── __init__.py           # Configuration selector
│   │   ├── base.py               # Base configuration
│   │   ├── development.py        # Development configuration
│   │   └── production.py         # Production configuration
│   ├── asgi.py                   # ASGI configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── urls.py                   # Main URLs
├── docs/                          # Documentation
│   ├── es/                       # Spanish documentation
│   │   ├── arquitectura.md
│   │   ├── api.md
│   │   ├── modelos.md
│   │   ├── instalacion.md
│   │   ├── deploy.md
│   │   ├── variables-entorno.md
│   │   ├── testing.md
│   │   └── contribucion.md
│   └── en/                       # English documentation
│       ├── architecture.md
│       ├── api.md
│       ├── models.md
│       ├── installation.md
│       ├── deployment.md
│       ├── environment-variables.md
│       ├── testing.md
│       └── contributing.md
├── static/                        # Static files
├── media/                         # Uploaded files
├── tests/                         # Integration tests
│   └── fixtures/                 # Test fixtures
├── .git/                          # Git repository
│   └── hooks/
│       └── commit-msg            # Validation hook
├── manage.py                      # Django management script
├── requirements.txt               # Main dependencies
├── requirements-test.txt          # Testing dependencies
├── pytest.ini                     # Pytest configuration
├── conftest.py                    # Global test configuration
├── schema.yml                     # Generated OpenAPI schema
├── .env.example                   # Environment variables template
├── .gitignore                     # Files ignored by Git
├── .gitmessage                    # Commit template
├── COMMIT_CONVENTIONS.md          # Commit conventions
├── TESTING.md                     # Testing guide
├── README.md                      # Readme in Spanish
└── README.en.md                   # This file (English)
```

## Data Models

### Project
Represents a portfolio project.

**Fields:**
- `title`: Project title
- `description`: Detailed description
- `short_description`: Brief summary
- `image`: Project image or screenshot
- `url`: Live project URL
- `github_url`: GitHub repository URL
- `technologies`: Technologies used (comma-separated)
- `is_featured`: Display in featured section
- `order`: Display order
- `created_at`, `updated_at`: Timestamps

### SkillCategory
Groups related skills.

**Fields:**
- `name`: Category name
- `description`: Category description
- `order`: Display order
- `created_at`, `updated_at`: Timestamps

### Skill
Represents a skill or technology.

**Fields:**
- `name`: Skill name
- `category`: Category (ForeignKey to SkillCategory)
- `proficiency`: Level ('beginner', 'intermediate', 'advanced', 'expert')
- `percentage`: Proficiency percentage (0-100)
- `icon`: Icon class or URL
- `description`: Skill description
- `years_experience`: Years of experience
- `is_featured`: Display in featured skills
- `order`: Order within category
- `created_at`, `updated_at`: Timestamps

### AboutMe
Personal information for the "About me" section.

**Fields:**
- `name`: Full name
- `title`: Professional title
- `bio`: Biography
- `email`: Contact email
- `phone`: Phone number
- `location`: Location
- `profile_image`: Profile photo
- `resume_file`: CV/Resume file
- `linkedin_url`, `github_url`, `twitter_url`, `website_url`: Social URLs
- `is_active`: Active profile (only one active at a time)
- `created_at`, `updated_at`: Timestamps

### ContactMessage
Message sent through contact form.

**Fields:**
- `name`: Sender's name
- `email`: Sender's email
- `subject`: Message subject
- `message`: Message content
- `phone`: Phone number (optional)
- `is_read`: Marked as read
- `is_replied`: Marked as replied
- `created_at`, `updated_at`: Timestamps

For relationship diagrams and complete details, see [Models and Database](docs/en/models.md).

## Testing

The project includes a complete test suite with pytest and pytest-django.

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=apps --cov-report=html

# Run tests for a specific app
pytest apps/skills/tests/

# Run tests in verbose mode
pytest -v
```

Current coverage: ~96%

For more information, see [TESTING.md](TESTING.md) and [Testing Guide](docs/en/testing.md).

## Deployment

### Railway (Recommended)

1. **Prepare environment variables**:
   - `DJANGO_ENV=production`
   - `SECRET_KEY=<your-secret-key>`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=<your-domain.railway.app>`
   - `DATABASE_URL` (provided by Railway)

2. **Connect Git repository**:
   - Railway will automatically detect the Django project
   - Install dependencies from `requirements.txt`
   - Run migrations automatically

3. **Configure PostgreSQL database**:
   - Add PostgreSQL service in Railway
   - `DATABASE_URL` will be configured automatically

4. **Post-deployment commands**:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

For deployment on other platforms (Heroku, DigitalOcean, AWS), see [Deployment Guide](docs/en/deployment.md).

## Commit Conventions

The project uses a commit conventions system with automatic validation. Each commit must follow this format:

```
<type>: <emoji> <short description>
- <detailed change 1>
- <detailed change 2>
- <additional context if needed>
```

### Commit Types

| Type | Emoji | Description |
|------|-------|-------------|
| `feat` | ✨ | New feature |
| `fix` | 🐛 | Bug fix |
| `docs` | 📚 | Documentation changes |
| `style` | 💄 | Code style changes |
| `refactor` | ♻️  | Code refactoring |
| `perf` | ⚡ | Performance improvements |
| `test` | ✅ | Add or update tests |
| `build` | 🏗️  | Build system or dependencies |
| `ci` | 👷 | CI configuration |
| `chore` | 🔧 | Other changes |

### Example
```
feat: ✨ add user authentication system
- Implement JWT token-based authentication
- Create login and registration endpoints
- Add password hashing with bcrypt
- Include authentication middleware for protected routes
```

The project includes a `commit-msg` hook that automatically validates the format.

For more details, see [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md).

## Complete Documentation

For detailed documentation, consult the following resources:

### Spanish
- [Installation Guide](docs/es/instalacion.md) - Complete installation instructions
- [Project Architecture](docs/es/arquitectura.md) - Design and architectural patterns
- [API Documentation](docs/es/api.md) - Complete endpoint reference
- [Models and Database](docs/es/modelos.md) - Schemas and relationships
- [Deployment Guide](docs/es/deploy.md) - Production deployment
- [Environment Variables](docs/es/variables-entorno.md) - Complete configuration
- [Testing Guide](docs/es/testing.md) - Tests and coverage
- [Contributing Guide](docs/es/contribucion.md) - How to contribute to the project

### English
- [Installation Guide](docs/en/installation.md) - Complete installation instructions
- [Project Architecture](docs/en/architecture.md) - Design and architectural patterns
- [API Documentation](docs/en/api.md) - Complete endpoint reference
- [Models and Database](docs/en/models.md) - Schemas and relationships
- [Deployment Guide](docs/en/deployment.md) - Production deployment
- [Environment Variables](docs/en/environment-variables.md) - Complete configuration
- [Testing Guide](docs/en/testing.md) - Tests and coverage
- [Contributing Guide](docs/en/contributing.md) - How to contribute

## License

MIT License

---

**Built with Django and Django REST Framework**

For more information or support, consult the documentation or open an issue on GitHub.
