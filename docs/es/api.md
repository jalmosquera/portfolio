# Documentacion de API

[English Version](../en/api.md) | [Volver al README](../../README.md)

Referencia completa de la API REST del Portfolio. Todos los endpoints devuelven JSON en formato camelCase.

## Tabla de Contenidos

- [Base URL](#base-url)
- [Autenticacion](#autenticacion)
- [Formato de Respuestas](#formato-de-respuestas)
- [Paginacion](#paginacion)
- [Filtrado y Busqueda](#filtrado-y-busqueda)
- [Codigos de Estado HTTP](#codigos-de-estado-http)
- [Endpoints por Recurso](#endpoints-por-recurso)
  - [Projects](#projects)
  - [Skills](#skills)
  - [Skill Categories](#skill-categories)
  - [About](#about)
  - [Contact](#contact)
- [Ejemplos de Integracion](#ejemplos-de-integracion)

---

## Base URL

**Desarrollo**: `http://localhost:8000`
**Produccion**: `https://tu-dominio.com`

Todos los endpoints de la API estan bajo el prefijo `/api/`:
- `http://localhost:8000/api/projects/`
- `http://localhost:8000/api/skills/`

## Autenticacion

Actualmente la API es **publica** para operaciones de lectura (GET).

Las operaciones de escritura (POST, PUT, PATCH, DELETE) requieren:
- **Django Admin Authentication**: Para uso interno
- **Session Authentication**: Para acceso administrativo

### Futuro: JWT Authentication

Se planea implementar autenticacion JWT para endpoints administrativos.

## Formato de Respuestas

Todas las respuestas son JSON con nomenclatura **camelCase**:

```json
{
  "id": 1,
  "name": "Django",
  "categoryId": 1,
  "categoryName": "Backend",
  "yearsExperience": 5,
  "isFeatured": true,
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-20T14:45:00Z"
}
```

### Respuesta de Error

```json
{
  "detail": "Not found."
}
```

O con validacion:

```json
{
  "name": ["This field is required."],
  "email": ["Enter a valid email address."]
}
```

## Paginacion

Los endpoints de lista utilizan paginacion automatica.

**Parametros**:
- `page`: Numero de pagina (por defecto: 1)
- `page_size`: Tamano de pagina (por defecto: 10, max: 100)

**Respuesta paginada**:

```json
{
  "count": 42,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Proyecto 1",
      // ...
    }
  ]
}
```

## Filtrado y Busqueda

### Busqueda (`?search=`)

Busqueda de texto en campos especificos:

```bash
GET /api/skills/?search=python
GET /api/projects/?search=django
```

### Ordenamiento (`?ordering=`)

Ordenar resultados:

```bash
GET /api/skills/?ordering=name          # Ascendente
GET /api/skills/?ordering=-percentage   # Descendente
GET /api/projects/?ordering=order,-created_at  # Multiple
```

## Codigos de Estado HTTP

| Codigo | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | GET, PUT, PATCH exitosos |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Datos invalidos |
| 401 | Unauthorized | Autenticacion requerida |
| 403 | Forbidden | Sin permisos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Server Error | Error del servidor |

---

## Endpoints por Recurso

## Projects

Gestion de proyectos del portafolio.

### Listar Proyectos

```http
GET /api/projects/
```

**Parametros de Query**:
- `search`: Buscar en titulo, descripcion, tecnologias
- `ordering`: Ordenar por `order`, `created_at`, `title`
- `page`: Numero de pagina

**Respuesta** (200 OK):

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "E-Commerce Platform",
      "description": "Plataforma completa de comercio electronico...",
      "shortDescription": "Sistema de ventas online",
      "imageUrl": "/media/projects/ecommerce.png",
      "url": "https://demo.example.com",
      "githubUrl": "https://github.com/user/ecommerce",
      "technologies": ["Django", "React", "PostgreSQL", "Redis"],
      "isFeatured": true,
      "order": 1,
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-20T14:45:00Z"
    }
  ]
}
```

### Obtener Proyecto

```http
GET /api/projects/{id}/
```

**Respuesta** (200 OK):

```json
{
  "id": 1,
  "title": "E-Commerce Platform",
  "description": "Plataforma completa de comercio electronico con carrito de compras, pasarela de pagos, gestion de inventario...",
  "shortDescription": "Sistema de ventas online",
  "imageUrl": "/media/projects/ecommerce.png",
  "url": "https://demo.example.com",
  "githubUrl": "https://github.com/user/ecommerce",
  "technologies": ["Django", "React", "PostgreSQL", "Redis"],
  "isFeatured": true,
  "order": 1,
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-20T14:45:00Z"
}
```

### Proyectos Destacados

```http
GET /api/projects/featured/
```

Devuelve solo proyectos con `isFeatured: true`.

**Respuesta** (200 OK):

```json
[
  {
    "id": 1,
    "title": "E-Commerce Platform",
    // ...campos del proyecto
  }
]
```

### Crear Proyecto (Admin)

```http
POST /api/projects/
Content-Type: application/json
```

**Body**:

```json
{
  "title": "Nuevo Proyecto",
  "description": "Descripcion detallada del proyecto",
  "shortDescription": "Resumen breve",
  "url": "https://proyecto.com",
  "githubUrl": "https://github.com/user/proyecto",
  "technologies": "Django,React,PostgreSQL",
  "isFeatured": true,
  "order": 5
}
```

**Respuesta** (201 Created):

```json
{
  "id": 6,
  "title": "Nuevo Proyecto",
  // ...campos completos
  "createdAt": "2024-01-22T15:30:00Z",
  "updatedAt": "2024-01-22T15:30:00Z"
}
```

### Actualizar Proyecto (Admin)

```http
PUT /api/projects/{id}/
PATCH /api/projects/{id}/
Content-Type: application/json
```

**Body** (PUT - todos los campos):

```json
{
  "title": "Proyecto Actualizado",
  "description": "Nueva descripcion",
  // ...todos los campos
}
```

**Body** (PATCH - campos parciales):

```json
{
  "isFeatured": false,
  "order": 10
}
```

**Respuesta** (200 OK):

```json
{
  "id": 1,
  // ...campos actualizados
  "updatedAt": "2024-01-22T16:00:00Z"
}
```

### Eliminar Proyecto (Admin)

```http
DELETE /api/projects/{id}/
```

**Respuesta** (204 No Content)

---

## Skills

Gestion de habilidades y tecnologias.

### Listar Habilidades

```http
GET /api/skills/
```

**Parametros de Query**:
- `search`: Buscar en name, description
- `ordering`: Ordenar por `order`, `name`, `percentage`

**Respuesta** (200 OK):

```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Django",
      "categoryId": 1,
      "categoryName": "Backend",
      "proficiency": "expert",
      "percentage": 95,
      "icon": "devicon-django-plain",
      "description": "Framework web de Python para desarrollo rapido",
      "yearsExperience": 5,
      "isFeatured": true,
      "order": 1,
      "createdAt": "2024-01-10T08:00:00Z",
      "updatedAt": "2024-01-10T08:00:00Z"
    }
  ]
}
```

### Obtener Habilidad

```http
GET /api/skills/{id}/
```

**Respuesta** (200 OK):

```json
{
  "id": 1,
  "name": "Django",
  "categoryId": 1,
  "categoryName": "Backend",
  "proficiency": "expert",
  "percentage": 95,
  "icon": "devicon-django-plain",
  "description": "Framework web de Python para desarrollo rapido y seguro",
  "yearsExperience": 5,
  "isFeatured": true,
  "order": 1,
  "createdAt": "2024-01-10T08:00:00Z",
  "updatedAt": "2024-01-10T08:00:00Z"
}
```

### Habilidades Destacadas

```http
GET /api/skills/featured/
```

**Respuesta** (200 OK):

```json
[
  {
    "id": 1,
    "name": "Django",
    "categoryId": 1,
    "categoryName": "Backend",
    // ...campos completos
  }
]
```

### Habilidades por Categoria

```http
GET /api/skills/by_category/
```

Devuelve habilidades agrupadas por categoria.

**Respuesta** (200 OK):

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
        // ...campos completos
      },
      {
        "id": 2,
        "name": "Django REST Framework",
        // ...
      }
    ],
    "createdAt": "2024-01-10T08:00:00Z",
    "updatedAt": "2024-01-10T08:00:00Z"
  },
  {
    "id": 2,
    "name": "Frontend",
    "description": "Tecnologias de frontend y UI",
    "order": 2,
    "skills": [
      // ...habilidades de frontend
    ]
  }
]
```

### Crear Habilidad (Admin)

```http
POST /api/skills/
Content-Type: application/json
```

**Body**:

```json
{
  "name": "FastAPI",
  "categoryId": 1,
  "proficiency": "intermediate",
  "percentage": 70,
  "icon": "fastapi-icon",
  "description": "Framework moderno para APIs con Python",
  "yearsExperience": 2,
  "isFeatured": false,
  "order": 5
}
```

**Respuesta** (201 Created):

```json
{
  "id": 16,
  "name": "FastAPI",
  "categoryId": 1,
  "categoryName": "Backend",
  // ...campos completos
  "createdAt": "2024-01-22T15:45:00Z",
  "updatedAt": "2024-01-22T15:45:00Z"
}
```

### Actualizar Habilidad (Admin)

```http
PATCH /api/skills/{id}/
Content-Type: application/json
```

**Body**:

```json
{
  "percentage": 95,
  "proficiency": "expert",
  "yearsExperience": 6
}
```

### Eliminar Habilidad (Admin)

```http
DELETE /api/skills/{id}/
```

**Respuesta** (204 No Content)

---

## Skill Categories

Categorias de habilidades.

### Listar Categorias

```http
GET /api/skill-categories/
```

**Respuesta** (200 OK):

```json
{
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Backend",
      "description": "Tecnologias de backend y APIs",
      "order": 1,
      "skills": [
        {
          "id": 1,
          "name": "Django",
          // ...campos completos
        }
      ],
      "createdAt": "2024-01-10T08:00:00Z",
      "updatedAt": "2024-01-10T08:00:00Z"
    }
  ]
}
```

### Obtener Categoria

```http
GET /api/skill-categories/{id}/
```

### Crear Categoria (Admin)

```http
POST /api/skill-categories/
Content-Type: application/json
```

**Body**:

```json
{
  "name": "DevOps",
  "description": "Herramientas de DevOps y CI/CD",
  "order": 5
}
```

### Actualizar Categoria (Admin)

```http
PATCH /api/skill-categories/{id}/
```

### Eliminar Categoria (Admin)

```http
DELETE /api/skill-categories/{id}/
```

---

## About

Informacion personal del portafolio.

### Listar Perfiles

```http
GET /api/about/
```

**Respuesta** (200 OK):

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Juan Alberto Perez",
      "title": "Full Stack Developer",
      "bio": "Desarrollador con 5+ anos de experiencia...",
      "email": "juan@example.com",
      "phone": "+52 555 1234567",
      "location": "Ciudad de Mexico, Mexico",
      "profileImageUrl": "/media/about/profile.jpg",
      "resumeFileUrl": "/media/about/resumes/cv.pdf",
      "linkedinUrl": "https://linkedin.com/in/juanperez",
      "githubUrl": "https://github.com/juanperez",
      "twitterUrl": "https://twitter.com/juanperez",
      "websiteUrl": "https://juanperez.dev",
      "isActive": true,
      "createdAt": "2024-01-05T10:00:00Z",
      "updatedAt": "2024-01-20T12:00:00Z"
    }
  ]
}
```

### Obtener Perfil

```http
GET /api/about/{id}/
```

### Perfil Activo

```http
GET /api/about/active/
```

Devuelve el perfil marcado como activo (solo debe haber uno).

**Respuesta** (200 OK):

```json
{
  "id": 1,
  "name": "Juan Alberto Perez",
  "title": "Full Stack Developer",
  // ...campos completos
}
```

Si no hay perfil activo:

```json
{}
```

### Crear Perfil (Admin)

```http
POST /api/about/
Content-Type: application/json
```

**Body**:

```json
{
  "name": "Juan Alberto Perez",
  "title": "Full Stack Developer",
  "bio": "Desarrollador con experiencia...",
  "email": "juan@example.com",
  "phone": "+52 555 1234567",
  "location": "Ciudad de Mexico, Mexico",
  "linkedinUrl": "https://linkedin.com/in/juanperez",
  "githubUrl": "https://github.com/juanperez",
  "isActive": true
}
```

**Nota**: Si `isActive: true`, automaticamente desactivara otros perfiles.

### Actualizar Perfil (Admin)

```http
PATCH /api/about/{id}/
```

### Eliminar Perfil (Admin)

```http
DELETE /api/about/{id}/
```

---

## Contact

Mensajes de contacto.

### Listar Mensajes (Admin)

```http
GET /api/contact/
```

**Respuesta** (200 OK):

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Maria Lopez",
      "email": "maria@example.com",
      "subject": "Consulta sobre proyecto",
      "message": "Hola, me interesa colaborar en...",
      "phone": "+52 555 9876543",
      "isRead": false,
      "isReplied": false,
      "createdAt": "2024-01-22T09:15:00Z",
      "updatedAt": "2024-01-22T09:15:00Z"
    }
  ]
}
```

### Obtener Mensaje (Admin)

```http
GET /api/contact/{id}/
```

### Mensajes No Leidos (Admin)

```http
GET /api/contact/unread/
```

Devuelve solo mensajes con `isRead: false`.

**Respuesta** (200 OK):

```json
[
  {
    "id": 1,
    "name": "Maria Lopez",
    // ...campos completos
    "isRead": false
  }
]
```

### Enviar Mensaje (Publico)

```http
POST /api/contact/
Content-Type: application/json
```

**Body**:

```json
{
  "name": "Carlos Ramirez",
  "email": "carlos@example.com",
  "subject": "Pregunta sobre servicios",
  "message": "Hola, quisiera saber mas sobre tus servicios de desarrollo...",
  "phone": "+52 555 1112233"
}
```

**Validaciones**:
- `name`: Requerido, max 200 caracteres
- `email`: Requerido, email valido
- `subject`: Requerido, max 300 caracteres
- `message`: Requerido
- `phone`: Opcional, max 20 caracteres

**Respuesta** (201 Created):

```json
{
  "id": 11,
  "name": "Carlos Ramirez",
  "email": "carlos@example.com",
  "subject": "Pregunta sobre servicios",
  "message": "Hola, quisiera saber mas sobre tus servicios...",
  "phone": "+52 555 1112233",
  "isRead": false,
  "isReplied": false,
  "createdAt": "2024-01-22T14:30:00Z",
  "updatedAt": "2024-01-22T14:30:00Z"
}
```

### Marcar Como Leido (Admin)

```http
POST /api/contact/{id}/mark_read/
```

**Respuesta** (200 OK):

```json
{
  "id": 1,
  "name": "Maria Lopez",
  // ...campos completos
  "isRead": true,
  "updatedAt": "2024-01-22T15:00:00Z"
}
```

### Marcar Como Respondido (Admin)

```http
POST /api/contact/{id}/mark_replied/
```

**Respuesta** (200 OK):

```json
{
  "id": 1,
  "name": "Maria Lopez",
  // ...campos completos
  "isReplied": true,
  "updatedAt": "2024-01-22T15:30:00Z"
}
```

---

## Ejemplos de Integracion

### JavaScript (Fetch API)

```javascript
// Obtener habilidades por categoria
async function getSkillsByCategory() {
  const response = await fetch('http://localhost:8000/api/skills/by_category/');
  const data = await response.json();
  return data;
}

// Enviar mensaje de contacto
async function sendContactMessage(formData) {
  const response = await fetch('http://localhost:8000/api/contact/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(JSON.stringify(error));
  }

  return await response.json();
}

// Uso
sendContactMessage({
  name: 'Juan Perez',
  email: 'juan@example.com',
  subject: 'Consulta',
  message: 'Hola, tengo una pregunta...'
})
  .then(data => console.log('Mensaje enviado:', data))
  .catch(error => console.error('Error:', error));
```

### React (Axios)

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Cliente axios configurado
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Obtener proyectos destacados
export const getFeaturedProjects = async () => {
  const response = await apiClient.get('/projects/featured/');
  return response.data;
};

// Obtener perfil activo
export const getActiveProfile = async () => {
  const response = await apiClient.get('/about/active/');
  return response.data;
};

// Hook de React
import { useState, useEffect } from 'react';

function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getFeaturedProjects()
      .then(data => {
        setProjects(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { projects, loading, error };
}
```

### Python (requests)

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Obtener habilidades
def get_skills():
    response = requests.get(f'{BASE_URL}/skills/')
    response.raise_for_status()
    return response.json()

# Crear proyecto (requiere autenticacion)
def create_project(data, session):
    response = session.post(
        f'{BASE_URL}/projects/',
        json=data
    )
    response.raise_for_status()
    return response.json()

# Uso
skills_data = get_skills()
print(f"Total skills: {skills_data['count']}")

for skill in skills_data['results']:
    print(f"- {skill['name']}: {skill['percentage']}%")
```

### curl

```bash
# GET proyectos destacados
curl -X GET http://localhost:8000/api/projects/featured/ \
  -H "Accept: application/json"

# POST mensaje de contacto
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Subject",
    "message": "Test message content"
  }'

# GET con busqueda y ordenamiento
curl -X GET "http://localhost:8000/api/skills/?search=python&ordering=-percentage" \
  -H "Accept: application/json"
```

---

## Documentacion Interactiva

Para explorar la API de manera interactiva, visita:

- **ReDoc**: `http://localhost:8000/`
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

---

[Volver al README Principal](../../README.md) | [Arquitectura](arquitectura.md) | [Modelos](modelos.md)
