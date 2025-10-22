# Variables de Entorno

[English Version](../en/environment-variables.md) | [Volver al README](../../README.md)

Documentacion completa de todas las variables de entorno utilizadas en el proyecto Portfolio API.

## Tabla de Contenidos

- [Introduccion](#introduccion)
- [Variables Requeridas](#variables-requeridas)
- [Variables Opcionales](#variables-opcionales)
- [Configuracion por Entorno](#configuracion-por-entorno)
- [Ejemplos de Configuracion](#ejemplos-de-configuracion)
- [Seguridad](#seguridad)

---

## Introduccion

El proyecto utiliza [python-decouple](https://github.com/henriquebastos/python-decouple) para gestionar variables de entorno. Esto permite:

- **Separacion de configuracion del codigo**
- **Seguridad**: Credenciales fuera del repositorio
- **Flexibilidad**: Diferentes configs por entorno
- **Facilidad**: Un solo archivo `.env`

### Archivo .env

Crea un archivo `.env` en la raiz del proyecto basado en `.env.example`:

```bash
cp .env.example .env
```

**IMPORTANTE**: El archivo `.env` **NO** debe subirse a Git. Ya esta incluido en `.gitignore`.

---

## Variables Requeridas

### DJANGO_ENV

**Tipo**: String
**Valores**: `development`, `production`
**Por defecto**: `development`
**Descripcion**: Determina que configuracion de Django usar.

```env
DJANGO_ENV=development  # Para desarrollo local
DJANGO_ENV=production   # Para produccion
```

**Impacto**:
- `development`: Usa `core.settings.development` (SQLite, DEBUG=True)
- `production`: Usa `core.settings.production` (PostgreSQL, DEBUG=False)

### SECRET_KEY

**Tipo**: String
**Por defecto**: Valor inseguro (solo para desarrollo)
**Descripcion**: Clave secreta de Django para firmas criptograficas.

```env
SECRET_KEY=tu-clave-secreta-unica-y-muy-larga-aqui
```

**Generar una SECRET_KEY**:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**IMPORTANTE**:
- En produccion, **DEBE** ser una clave unica y segura
- **NUNCA** compartas esta clave
- **NUNCA** la subas a Git
- Cambiala si se compromete

---

## Variables Opcionales

### DEBUG

**Tipo**: Boolean
**Por defecto**: `False` (produccion), `True` (desarrollo)
**Descripcion**: Habilita/deshabilita modo debug de Django.

```env
DEBUG=True   # Desarrollo
DEBUG=False  # Produccion
```

**ADVERTENCIA**: **NUNCA** uses `DEBUG=True` en produccion.

**Cuando DEBUG=True**:
- Muestra paginas de error detalladas
- Expone informacion sensible
- Desactiva caching
- Sirve archivos estaticos automaticamente

### DATABASE_URL

**Tipo**: String (URL de conexion)
**Requerido en**: Produccion
**Descripcion**: URL de conexion a PostgreSQL.

```env
# Formato: postgresql://usuario:password@host:puerto/nombre_bd
DATABASE_URL=postgresql://portfolio_user:mi_password@localhost:5432/portfolio_db
```

**Componentes**:
- `usuario`: Usuario de PostgreSQL
- `password`: Contrasena del usuario
- `host`: Servidor (localhost, IP, o dominio)
- `puerto`: Puerto (por defecto 5432)
- `nombre_bd`: Nombre de la base de datos

**Nota**: En desarrollo no es necesario (usa SQLite por defecto).

### ALLOWED_HOSTS

**Tipo**: String (separado por comas)
**Por defecto**: `*` (en produccion)
**Descripcion**: Dominios/IPs permitidos para servir la aplicacion.

```env
# Desarrollo
ALLOWED_HOSTS=localhost,127.0.0.1

# Produccion
ALLOWED_HOSTS=tudominio.com,www.tudominio.com,api.tudominio.com

# Railway
ALLOWED_HOSTS=tu-app.up.railway.app
```

**IMPORTANTE**: En produccion, especifica solo los dominios reales (no uses `*`).

---

## Email Configuration

### EMAIL_HOST

**Tipo**: String
**Por defecto**: `smtp.gmail.com`
**Descripcion**: Servidor SMTP para envio de correos.

```env
EMAIL_HOST=smtp.gmail.com          # Gmail
EMAIL_HOST=smtp.sendgrid.net       # SendGrid
EMAIL_HOST=smtp.mailgun.org        # Mailgun
```

### EMAIL_PORT

**Tipo**: Integer
**Por defecto**: `587`
**Descripcion**: Puerto del servidor SMTP.

```env
EMAIL_PORT=587    # TLS
EMAIL_PORT=465    # SSL
EMAIL_PORT=25     # Sin encriptacion (no recomendado)
```

### EMAIL_USE_TLS

**Tipo**: Boolean
**Por defecto**: `True`
**Descripcion**: Usar TLS para conexion segura.

```env
EMAIL_USE_TLS=True
```

### EMAIL_HOST_USER

**Tipo**: String
**Descripcion**: Usuario/email para autenticacion SMTP.

```env
EMAIL_HOST_USER=tu-email@gmail.com
```

### EMAIL_HOST_PASSWORD

**Tipo**: String
**Descripcion**: Contrasena del email.

```env
EMAIL_HOST_PASSWORD=tu-app-password
```

**Para Gmail**:
1. Habilita verificacion en 2 pasos
2. Genera una "Contrasena de aplicacion"
3. Usa esa contrasena aqui (no tu contrasena normal)

### DEFAULT_FROM_EMAIL

**Tipo**: String
**Por defecto**: Valor de `EMAIL_HOST_USER`
**Descripcion**: Email "From" por defecto para correos salientes.

```env
DEFAULT_FROM_EMAIL=noreply@tudominio.com
```

---

## CORS Configuration

### CORS_ALLOWED_ORIGINS

**Tipo**: String (separado por comas)
**Por defecto**: `http://localhost:3000,http://localhost:5173`
**Descripcion**: Origenes permitidos para peticiones CORS.

```env
# Desarrollo
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000

# Produccion
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com,https://app.tudominio.com
```

**Nota**: En produccion, especifica solo tus dominios frontend reales.

---

## Configuracion por Entorno

### Desarrollo (.env.development)

```env
# Django
DJANGO_ENV=development
SECRET_KEY=django-insecure-for-development-only
DEBUG=True

# Database (SQLite por defecto, no requiere DATABASE_URL)

# Email (console backend, no requiere configuracion SMTP)

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Produccion (.env.production)

```env
# Django
DJANGO_ENV=production
SECRET_KEY=tu-clave-super-secreta-y-larga-aqui-generada-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Database
DATABASE_URL=postgresql://usuario:password@db-host:5432/portfolio_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@tudominio.com
EMAIL_HOST_PASSWORD=tu-app-password-aqui
DEFAULT_FROM_EMAIL=Portfolio <noreply@tudominio.com>

# CORS
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Security (opcional, configurados en settings)
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
DATABASE_URL=${{DATABASE_URL}}  # Proporcionado por Railway automaticamente

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

## Ejemplos de Configuracion

### Configuracion Minima (Desarrollo)

```env
DJANGO_ENV=development
SECRET_KEY=any-random-string-for-development
DEBUG=True
```

Esto es suficiente para comenzar en desarrollo. El proyecto usara SQLite, email de consola, y CORS por defecto.

### Configuracion Completa (Produccion)

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

## Seguridad

### Mejores Practicas

1. **Nunca subas `.env` a Git**
   ```bash
   # Verifica que esta en .gitignore
   cat .gitignore | grep .env
   ```

2. **Usa claves fuertes**
   - SECRET_KEY: Al menos 50 caracteres aleatorios
   - Contrasenas de BD: Combinacion de letras, numeros, simbolos

3. **Rota credenciales comprometidas**
   - Genera nueva SECRET_KEY
   - Cambia contrasenas de BD y email
   - Actualiza en todos los entornos

4. **Limita acceso**
   - `.env` debe tener permisos restrictivos:
     ```bash
     chmod 600 .env
     ```

5. **Usa servicios de gestion de secretos** (produccion)
   - AWS Secrets Manager
   - Google Cloud Secret Manager
   - HashiCorp Vault
   - Railway Variables (si usas Railway)

### Variables Sensibles

Estas variables **NUNCA** deben exponerse:
- `SECRET_KEY`
- `DATABASE_URL` (contiene contrasenas)
- `EMAIL_HOST_PASSWORD`
- Cualquier API key o token

### Verificar Seguridad

```bash
# Asegurarse que .env no esta trackeado
git status --ignored

# Verificar que no hay secretos en el historial
git log --all --full-history --source -- .env

# Si .env esta en Git (ERROR), removerlo:
git rm --cached .env
git commit -m "Remove .env from repository"
```

---

## Troubleshooting

### Error: "SECRET_KEY not set"

**Solucion**: Verifica que existe `.env` con `SECRET_KEY`:

```bash
cat .env | grep SECRET_KEY
```

### Error: "CORS origin not allowed"

**Solucion**: Agrega tu frontend URL a `CORS_ALLOWED_ORIGINS`:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,tu-nuevo-origen
```

### Error: "Database connection failed"

**Solucion**: Verifica `DATABASE_URL`:

1. Formato correcto
2. Credenciales validas
3. Base de datos existe
4. Servidor accesible

```bash
# Probar conexion
psql $DATABASE_URL
```

### Valores no se actualizan

**Solucion**: Reinicia el servidor Django:

```bash
# Ctrl+C para detener
python manage.py runserver
```

---

## Referencias

- [python-decouple documentation](https://github.com/henriquebastos/python-decouple)
- [Django Settings Best Practices](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [12 Factor App](https://12factor.net/config)

---

[Volver al README Principal](../../README.md) | [Instalacion](instalacion.md) | [Deployment](deploy.md)
