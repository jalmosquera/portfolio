# Environment Variables

[Spanish Version](../es/variables-entorno.md) | [Back to README](../../README.en.md)

Complete documentation of all environment variables used in the Portfolio API project.

## Table of Contents

- [Introduction](#introduction)
- [Required Variables](#required-variables)
- [Optional Variables](#optional-variables)
- [Environment-Specific Configuration](#environment-specific-configuration)
- [Configuration Examples](#configuration-examples)
- [Security](#security)

---

## Introduction

The project uses [python-decouple](https://github.com/henriquebastos/python-decouple) to manage environment variables. This allows:

- **Separation of configuration from code**
- **Security**: Credentials outside the repository
- **Flexibility**: Different configs per environment
- **Ease**: Single `.env` file

### .env File

Create a `.env` file in the project root based on `.env.example`:

```bash
cp .env.example .env
```

**IMPORTANT**: The `.env` file should **NOT** be uploaded to Git. It's already included in `.gitignore`.

---

## Required Variables

### DJANGO_ENV

**Type**: String
**Values**: `development`, `production`
**Default**: `development`
**Description**: Determines which Django configuration to use.

```env
DJANGO_ENV=development  # For local development
DJANGO_ENV=production   # For production
```

**Impact**:
- `development`: Uses `core.settings.development` (SQLite, DEBUG=True)
- `production`: Uses `core.settings.production` (PostgreSQL, DEBUG=False)

### SECRET_KEY

**Type**: String
**Default**: Insecure value (development only)
**Description**: Django secret key for cryptographic signing.

```env
SECRET_KEY=your-unique-and-very-long-secret-key-here
```

**Generate a SECRET_KEY**:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**IMPORTANT**:
- In production, **MUST** be a unique and secure key
- **NEVER** share this key
- **NEVER** upload to Git
- Change it if compromised

---

## Optional Variables

### DEBUG

**Type**: Boolean
**Default**: `False` (production), `True` (development)
**Description**: Enables/disables Django debug mode.

```env
DEBUG=True   # Development
DEBUG=False  # Production
```

**WARNING**: **NEVER** use `DEBUG=True` in production.

**When DEBUG=True**:
- Shows detailed error pages
- Exposes sensitive information
- Disables caching
- Serves static files automatically

### DATABASE_URL

**Type**: String (connection URL)
**Required in**: Production
**Description**: PostgreSQL connection URL.

```env
# Format: postgresql://user:password@host:port/database_name
DATABASE_URL=postgresql://portfolio_user:my_password@localhost:5432/portfolio_db
```

**Components**:
- `user`: PostgreSQL user
- `password`: User password
- `host`: Server (localhost, IP, or domain)
- `port`: Port (default 5432)
- `database_name`: Database name

**Note**: Not necessary in development (uses SQLite by default).

### ALLOWED_HOSTS

**Type**: String (comma-separated)
**Default**: `*` (in production)
**Description**: Allowed domains/IPs to serve the application.

```env
# Development
ALLOWED_HOSTS=localhost,127.0.0.1

# Production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Railway
ALLOWED_HOSTS=your-app.up.railway.app
```

**IMPORTANT**: In production, specify only real domains (don't use `*`).

---

## Email Configuration

### EMAIL_HOST

**Type**: String
**Default**: `smtp.gmail.com`
**Description**: SMTP server for sending emails.

```env
EMAIL_HOST=smtp.gmail.com          # Gmail
EMAIL_HOST=smtp.sendgrid.net       # SendGrid
EMAIL_HOST=smtp.mailgun.org        # Mailgun
```

### EMAIL_PORT

**Type**: Integer
**Default**: `587`
**Description**: SMTP server port.

```env
EMAIL_PORT=587    # TLS
EMAIL_PORT=465    # SSL
EMAIL_PORT=25     # No encryption (not recommended)
```

### EMAIL_USE_TLS

**Type**: Boolean
**Default**: `True`
**Description**: Use TLS for secure connection.

```env
EMAIL_USE_TLS=True
```

### EMAIL_HOST_USER

**Type**: String
**Description**: User/email for SMTP authentication.

```env
EMAIL_HOST_USER=your-email@gmail.com
```

### EMAIL_HOST_PASSWORD

**Type**: String
**Description**: Email password.

```env
EMAIL_HOST_PASSWORD=your-app-password
```

**For Gmail**:
1. Enable 2-step verification
2. Generate an "App password"
3. Use that password here (not your regular password)

### DEFAULT_FROM_EMAIL

**Type**: String
**Default**: Value of `EMAIL_HOST_USER`
**Description**: Default "From" email for outgoing emails.

```env
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

---

## CORS Configuration

### CORS_ALLOWED_ORIGINS

**Type**: String (comma-separated)
**Default**: `http://localhost:3000,http://localhost:5173`
**Description**: Allowed origins for CORS requests.

```env
# Development
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000

# Production
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://app.yourdomain.com
```

**Note**: In production, specify only your real frontend domains.

---

## Environment-Specific Configuration

### Development (.env.development)

```env
# Django
DJANGO_ENV=development
SECRET_KEY=django-insecure-for-development-only
DEBUG=True

# Database (SQLite by default, doesn't require DATABASE_URL)

# Email (console backend, doesn't require SMTP configuration)

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Production (.env.production)

```env
# Django
DJANGO_ENV=production
SECRET_KEY=your-super-secret-and-long-key-here-generated-randomly
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@db-host:5432/portfolio_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-app-password-here
DEFAULT_FROM_EMAIL=Portfolio <noreply@yourdomain.com>

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security (optional, configured in settings)
SECURE_SSL_REDIRECT=True
```

### Railway (.env.railway)

```env
# Django
DJANGO_ENV=production
SECRET_KEY=${{SECRET_KEY}}  # Railway variable
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_STATIC_URL}}

# Database
DATABASE_URL=${{DATABASE_URL}}  # Provided by Railway automatically

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=${{EMAIL_USER}}
EMAIL_HOST_PASSWORD=${{EMAIL_PASSWORD}}

# CORS
CORS_ALLOWED_ORIGINS=${{FRONTEND_URL}}
```

---

## Configuration Examples

### Minimal Configuration (Development)

```env
DJANGO_ENV=development
SECRET_KEY=any-random-string-for-development
DEBUG=True
```

This is sufficient to start in development. The project will use SQLite, console email, and default CORS.

### Complete Configuration (Production)

```env
# ========================================
# Django Core
# ========================================
DJANGO_ENV=production
SECRET_KEY=bq4j&9s@k!l2m#n5p$r6t%u8v*w0x^y1z@a-b_c+d=e~f
DEBUG=False
ALLOWED_HOSTS=api.portfolio.com,portfolio.com

# ========================================
# Database
# ========================================
DATABASE_URL=postgresql://portfolio_user:secure_pass_123@db.example.com:5432/portfolio_prod

# ========================================
# Email
# ========================================
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.your_sendgrid_api_key_here
DEFAULT_FROM_EMAIL=Portfolio <noreply@portfolio.com>

# ========================================
# CORS
# ========================================
CORS_ALLOWED_ORIGINS=https://portfolio.com,https://www.portfolio.com,https://app.portfolio.com

# ========================================
# Security
# ========================================
SECURE_SSL_REDIRECT=True
```

---

## Security

### Best Practices

1. **Never upload `.env` to Git**
   ```bash
   # Check it's in .gitignore
   cat .gitignore | grep .env
   ```

2. **Use strong keys**
   - SECRET_KEY: At least 50 random characters
   - DB passwords: Combination of letters, numbers, symbols

3. **Rotate compromised credentials**
   - Generate new SECRET_KEY
   - Change DB and email passwords
   - Update in all environments

4. **Limit access**
   - `.env` should have restrictive permissions:
     ```bash
     chmod 600 .env
     ```

5. **Use secret management services** (production)
   - AWS Secrets Manager
   - Google Cloud Secret Manager
   - HashiCorp Vault
   - Railway Variables (if using Railway)

### Sensitive Variables

These variables should **NEVER** be exposed:
- `SECRET_KEY`
- `DATABASE_URL` (contains passwords)
- `EMAIL_HOST_PASSWORD`
- Any API key or token

### Verify Security

```bash
# Ensure .env is not tracked
git status --ignored

# Check no secrets in history
git log --all --full-history --source -- .env

# If .env is in Git (ERROR), remove it:
git rm --cached .env
git commit -m "Remove .env from repository"
```

---

## Troubleshooting

### Error: "SECRET_KEY not set"

**Solution**: Verify `.env` exists with `SECRET_KEY`:

```bash
cat .env | grep SECRET_KEY
```

### Error: "CORS origin not allowed"

**Solution**: Add your frontend URL to `CORS_ALLOWED_ORIGINS`:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,your-new-origin
```

### Error: "Database connection failed"

**Solution**: Verify `DATABASE_URL`:

1. Correct format
2. Valid credentials
3. Database exists
4. Server accessible

```bash
# Test connection
psql $DATABASE_URL
```

### Values don't update

**Solution**: Restart Django server:

```bash
# Ctrl+C to stop
python manage.py runserver
```

---

## References

- [python-decouple documentation](https://github.com/henriquebastos/python-decouple)
- [Django Settings Best Practices](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [12 Factor App](https://12factor.net/config)

---

[Back to Main README](../../README.en.md) | [Installation](installation.md) | [Deployment](deployment.md)
