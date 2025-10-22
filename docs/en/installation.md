# Installation Guide

[Spanish Version](../es/instalacion.md) | [Back to README](../../README.en.md)

Detailed guide to install and configure the Portfolio API project in your local environment.

## Table of Contents

- [System Requirements](#system-requirements)
- [Step-by-Step Installation](#step-by-step-installation)
- [Environment Variables Configuration](#environment-variables-configuration)
- [Database Migrations](#database-migrations)
- [Superuser Creation](#superuser-creation)
- [Loading Test Data](#loading-test-data)
- [Installation Verification](#installation-verification)
- [Common Issues](#common-issues)

---

## System Requirements

### Required Software

- **Python**: Version 3.9 or higher
  - Check: `python --version` or `python3 --version`
- **pip**: Python package manager
  - Check: `pip --version` or `pip3 --version`
- **Git**: To clone the repository
  - Check: `git --version`

### Optional Software (Recommended)

- **PostgreSQL**: For production database (version 10 or higher)
- **virtualenv** or **venv**: For isolated virtual environments
- **PostgreSQL GUI**: pgAdmin, DBeaver, or TablePlus

### Supported Operating Systems

- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS (10.14 or higher)
- Windows 10/11 (WSL recommended)

---

## Step-by-Step Installation

### 1. Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/your-username/portfolio.git

# Or via SSH
git clone git@github.com:your-username/portfolio.git

# Navigate to project directory
cd portfolio
```

### 2. Create Virtual Environment

It's **highly recommended** to use a virtual environment to isolate project dependencies.

#### On Linux/macOS:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Verify environment is active (should show (.venv) in prompt)
```

#### On Windows:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Or in PowerShell
.venv\Scripts\Activate.ps1
```

**Deactivate virtual environment** (when finished):

```bash
deactivate
```

### 3. Update pip

It's good practice to update pip before installing dependencies:

```bash
pip install --upgrade pip
```

### 4. Install Dependencies

#### Production Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2+
- djangorestframework 3.14+
- drf-spectacular 0.28.0
- psycopg2-binary (for PostgreSQL)
- python-decouple
- django-cors-headers
- Pillow
- whitenoise
- gunicorn

#### Development Dependencies (Optional)

To run tests and development:

```bash
pip install -r requirements-test.txt
```

This will additionally install:
- pytest
- pytest-django
- pytest-cov
- factory-boy

### 5. Verify Dependencies Installation

```bash
pip list
```

Should show all installed dependencies.

---

## Environment Variables Configuration

### 1. Copy Example File

```bash
cp .env.example .env
```

### 2. Edit Environment Variables

Open the `.env` file and configure the variables:

```env
# ========================================
# Django Configuration
# ========================================
DJANGO_ENV=development
SECRET_KEY=your-unique-and-secure-secret-key-here
DEBUG=True

# ========================================
# Database Configuration
# ========================================
# For development (SQLite - no additional configuration required)
# For production (PostgreSQL):
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# ========================================
# Email Configuration
# ========================================
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# ========================================
# CORS Configuration
# ========================================
# Add allowed origins separated by commas
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# ========================================
# Production Settings (Optional)
# ========================================
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### 3. Generate Secure SECRET_KEY

To generate a unique SECRET_KEY:

```python
# Run in Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the result and paste in `.env`:

```env
SECRET_KEY=django-insecure-abc123...xyz789
```

**IMPORTANT**: Never share your SECRET_KEY or upload it to version control.

### 4. Email Configuration (Optional)

To use Gmail:

1. Go to your Google account
2. Enable "2-Step Verification"
3. Generate an "App password"
4. Use that password in `EMAIL_HOST_PASSWORD`

---

## Database Migrations

### 1. Create Database (PostgreSQL Only)

If using PostgreSQL in production:

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE portfolio_db;

-- Create user
CREATE USER portfolio_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;

-- Exit
\q
```

### 2. Run Migrations

```bash
# Apply migrations
python manage.py migrate
```

This will create all necessary tables:
- `projects_project`
- `skills_skillcategory`
- `skills_skill`
- `about_aboutme`
- `contact_contactmessage`
- Django tables (auth, sessions, admin, etc.)

You should see output similar to:

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

### 3. Verify Migrations

```bash
# Check migration status
python manage.py showmigrations

# Should show [X] on all migrations
```

---

## Superuser Creation

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Complete the requested information:

```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

**Recommendations**:
- Use a different username than "admin" for security
- Use a strong password (minimum 8 characters, letters, numbers, symbols)
- Save credentials in a secure location

---

## Loading Test Data

### Option 1: Manually via Admin

1. Start the server: `python manage.py runserver`
2. Go to: `http://localhost:8000/admin/`
3. Login with the created superuser
4. Add data manually

### Option 2: Via Django Shell

```bash
python manage.py shell
```

```python
from apps.skills.models import SkillCategory, Skill
from apps.projects.models import Project

# Create skill category
backend = SkillCategory.objects.create(
    name="Backend",
    description="Backend technologies",
    order=1
)

# Create skills
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

# Create project
project = Project.objects.create(
    title="Portfolio API",
    description="Professional REST API for personal portfolio",
    short_description="Django REST API",
    technologies="Django,DRF,PostgreSQL",
    is_featured=True,
    order=1
)

print("Test data created!")
```

### Option 3: Fixtures (If Available)

```bash
python manage.py loaddata fixtures/initial_data.json
```

---

## Installation Verification

### 1. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 2. Run Development Server

```bash
python manage.py runserver
```

You should see:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 22, 2024 - 10:30:45
Django version 4.2.x, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 3. Verify Endpoints

Open your browser and visit:

- **API Documentation (ReDoc)**: http://localhost:8000/
- **Swagger UI**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/
- **API Endpoints**:
  - http://localhost:8000/api/projects/
  - http://localhost:8000/api/skills/
  - http://localhost:8000/api/about/
  - http://localhost:8000/api/contact/

### 4. Run Tests (Optional)

```bash
# Run all tests
pytest

# With coverage
pytest --cov=apps

# If everything is fine, should show:
# ===== X passed in Y.XXs =====
```

---

## Common Issues

### Issue: "Command not found: python"

**Solution**:

```bash
# On Linux/macOS, try:
python3 manage.py runserver

# Or create an alias:
alias python=python3
```

### Issue: "No module named 'django'"

**Solution**:

Ensure virtual environment is activated:

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'decouple'"

**Solution**:

```bash
pip install python-decouple
```

### Issue: "SECRET_KEY not set"

**Solution**:

Verify that `.env` file exists and contains `SECRET_KEY`:

```bash
cat .env | grep SECRET_KEY
```

### Issue: "FATAL: password authentication failed for user"

**PostgreSQL Solution**:

1. Verify PostgreSQL is running:

```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list
```

2. Verify credentials in `.env`
3. Test connection:

```bash
psql -U portfolio_user -d portfolio_db -h localhost
```

### Issue: "Port 8000 is already in use"

**Solution**:

Use a different port:

```bash
python manage.py runserver 8080
```

Or find and stop the process:

```bash
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: "Migrations are not applied"

**Solution**:

```bash
# Check pending migrations
python manage.py showmigrations

# Apply all migrations
python manage.py migrate

# If there are problems, try:
python manage.py migrate --run-syncdb
```

### Issue: Error with Pillow (images)

**Solution**:

Install system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libjpeg-dev zlib1g-dev

# macOS
brew install jpeg

# Then reinstall Pillow
pip install --upgrade Pillow
```

---

## Next Steps

Once correctly installed:

1. **Explore the Admin**: http://localhost:8000/admin/
2. **Read the API documentation**: http://localhost:8000/
3. **Configure your development environment**: Editor, linters, etc.
4. **Review the architecture**: [architecture.md](architecture.md)
5. **Run the tests**: [testing.md](testing.md)

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [python-decouple](https://github.com/henriquebastos/python-decouple)

---

[Back to Main README](../../README.en.md) | [Environment Variables](environment-variables.md) | [Deployment](deployment.md)
