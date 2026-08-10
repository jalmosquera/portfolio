# 🔌 API reference

[← Back to documentation index](../README.md)

## 🌐 Base URL

The browser uses same-origin relative URLs:

```text
/api
```

In local development, the frontend API configuration points to the local Django server. In production, Nginx proxies `/api/*` to Gunicorn.

## 🧭 Core and documentation endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/` | API root |
| `GET` | `/api/health/` | Django health check |
| `GET` | `/api/schema/` | OpenAPI schema |
| `GET` | `/api/swagger/` | Swagger UI |
| `GET` | `/api/redoc/` | ReDoc UI |
| `GET` | `/admin/` | Private Django Admin interface |

## 🧩 Portfolio endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/about/` | Visible bilingual About Me content |
| `GET` | `/api/technologies/` | Technology catalogue |
| `GET` | `/api/projects/` | Visible projects |
| `GET` | `/api/projects/?slug={slug}` | Filter the project collection for one case study |
| `GET` | `/api/projects/{id}/` | Retrieve a project by its database identifier |
| `GET` | `/api/project-images/` | Project gallery images |
| `GET` | `/api/tech-details/` | Project technical details |
| `GET` | `/api/problem-solutions/` | Project problems and solutions |
| `GET` | `/api/lessons/` | Lessons learned |

The exact filters and response schemas are discoverable through Swagger or ReDoc. Those generated documents are the authoritative field-level API reference.

## 📄 Dynamic CV

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/cv/` | Active database-driven CV content |
| `GET` | `/api/cv/download/` | Generate and download a PDF variant |

The download endpoint supports the application's compact/visual format and active language choices. The generated filename is controlled by the CV configuration in Django Admin.

## ✉️ Contact and analytics

| Method | Path | Purpose | Throttle |
| --- | --- | --- | --- |
| `POST` | `/api/contact/` | Store an inquiry and trigger email delivery | `5/hour` |
| `POST` | `/api/visits/` | Atomically record a site visit | `120/hour` |

Contact delivery failures do not discard a valid inquiry. The inquiry remains available in Django Admin with the notification timestamps or recorded email error.

## 🌍 Language negotiation

Translated endpoints use the request language, normally through the standard header:

```http
Accept-Language: es
```

or:

```http
Accept-Language: en
```

English is the backend fallback language. The frontend language selector sends the active language when requesting translated data and generating the CV.

## 🖼️ Media URLs

Uploaded project images and CV portraits are returned as media URLs. In production, Nginx serves `/media/*` from the shared read-only media volume. Frontend components should use the centralized URL helpers rather than hardcoding backend hosts.

## 🔐 Administration

Content creation and editing belong to Django Admin, not the public API. Production should protect `/admin/` with strong Django credentials and preferably Cloudflare Access.
