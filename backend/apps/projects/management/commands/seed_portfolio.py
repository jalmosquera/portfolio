from html import escape

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.lessons.models import Lesson, LessonContent
from apps.problem_solution.models import ProblemSolution, ProblemSolutionContent
from apps.project_images.models import ProjectImage, ProjectImageContent
from apps.projects.models import Project, ProjectContent
from apps.tech_details.models import TechDetail, TechDetailContent
from apps.technology.models import Technologies


TECHNOLOGIES = {
    "Python": {"icon": "🐍", "color": "#f2c94c"},
    "Django": {"icon": "◩", "color": "#69b88d"},
    "Django REST Framework": {"icon": "◆", "color": "#d06b6b"},
    "React": {"icon": "⚛", "color": "#61dafb"},
    "Vite": {"icon": "ϟ", "color": "#a78bfa"},
    "Tailwind CSS": {"icon": "≈", "color": "#38bdf8"},
    "Zustand": {"icon": "◫", "color": "#d6a56f"},
    "JWT": {"icon": "🔐", "color": "#d8d8d8"},
    "Docker": {"icon": "🐳", "color": "#68a9e8"},
    "PostgreSQL": {"icon": "🐘", "color": "#7ba5d6"},
    "Redis": {"icon": "◇", "color": "#dc5b54"},
    "WebSockets": {"icon": "↯", "color": "#d7b56d"},
    "Cloudinary": {"icon": "☁", "color": "#5f8ff7"},
    "AWS S3": {"icon": "▰", "color": "#f39b3d"},
    "Google Calendar": {"icon": "▣", "color": "#74a1f7"},
    "Railway": {"icon": "◒", "color": "#c8b8ff"},
    "Vercel": {"icon": "▲", "color": "#f1f1f1"},
}

LEGACY_PROJECT_SLUGS = ("alternativa-kiosk", "abogado-crm")
LEGACY_TECHNOLOGIES = ("Linux", "Nginx", "Raspberry Pi")

PROJECTS = (
    {
        "title": "Alternativa 2.0",
        "slug": "alternativa-2-0",
        "short_description": "Restaurant SaaS for multilingual menus, ordering and real-time operations.",
        "description": "A full-stack restaurant platform covering multilingual catalogs, guest checkout, ingredient customization, role-based administration, promotions and real-time order notifications.",
        "github": "https://github.com/jalmosquera/saasAlternativa2.0",
        "live_url": "",
        "technologies": (
            "Python", "Django", "Django REST Framework", "React", "Vite",
            "Tailwind CSS", "JWT", "PostgreSQL", "Redis", "WebSockets", "Cloudinary",
        ),
        "accent": "#d7794f",
        "problem": "Restaurants need more than a static QR menu: products, ingredients, availability, permissions and orders must stay synchronized across customers and staff.",
        "solution": "A modular Django and React SaaS with guest checkout, granular roles, atomic order operations, WebSocket notifications and cloud media storage.",
        "details": {
            "Domain": ("Products, options and ingredients", "Orders, promotions and company settings"),
            "Realtime": ("Django Channels", "Redis-backed WebSockets"),
            "Delivery": ("PostgreSQL", "Cloudinary media storage"),
        },
        "lessons": (
            "Model product customization explicitly so pricing and stock remain consistent.",
            "Treat guest checkout and authenticated ordering as one domain with different permissions.",
        ),
    },
    {
        "title": "Eduardo Bernal Abogado",
        "slug": "eduardo-bernal-abogado",
        "short_description": "Production legal platform for appointments, clients and secure documents.",
        "description": "A client-facing legal website backed by private staff workflows, appointment availability, a protected client portal and auditable delivery of sensitive documents.",
        "github": "https://github.com/jalmosquera/landingLawyer",
        "live_url": "https://www.eduardobernalabogado.es/",
        "technologies": (
            "Python", "Django", "Django REST Framework", "React", "Vite",
            "Tailwind CSS", "Zustand", "JWT", "PostgreSQL", "AWS S3",
            "Google Calendar", "Railway", "Vercel",
        ),
        "accent": "#c8a860",
        "problem": "The law firm needed to attract clients, coordinate appointments and exchange sensitive case documents without scattering operations across informal channels.",
        "solution": "A production full-stack platform with public lead capture, staff and client roles, calendar synchronization, expiring download tokens and an access audit trail.",
        "details": {
            "Legal operations": ("Clients and case records", "Appointments and availability"),
            "Security": ("Expiring one-time download tokens", "Document access audit logs"),
            "Integrations": ("Google Calendar and Meet", "S3-ready document storage"),
        },
        "lessons": (
            "Sensitive documents require server-enforced ownership, expiry and traceability.",
            "Public scheduling must respect private availability without exposing internal calendars.",
        ),
    },
    {
        "title": "Equus Pub Digital Menu",
        "slug": "equus-pub-digital-menu",
        "short_description": "Live bilingual digital menu and ordering experience for Equus Pub.",
        "description": "A production system for a hospitality client with a multilingual catalog, ingredient customization, persistent cart, WhatsApp ordering and protected content management.",
        "github": "https://github.com/jalmosquera/digitalLetterFront",
        "live_url": "https://equuspub.vercel.app/",
        "technologies": (
            "Python", "Django", "Django REST Framework", "React", "Vite",
            "Tailwind CSS", "JWT", "PostgreSQL", "Railway", "Vercel",
        ),
        "accent": "#d38a4c",
        "problem": "A working restaurant needed a menu it could maintain without reprinting, while customers needed a fast bilingual flow for browsing and placing customized orders.",
        "solution": "A deployed Django REST and React application with translated content, role-based administration, ingredient-level customization and direct WhatsApp checkout.",
        "details": {
            "Customer experience": ("Spanish and English catalog", "Persistent customizable cart"),
            "Administration": ("JWT role-based access", "Product, category and ingredient CRUD"),
            "Production": ("Django API on Railway", "React frontend on Vercel"),
        },
        "lessons": (
            "A restaurant menu needs operational editing workflows, not only a polished public catalog.",
            "Translation and ingredient customization belong in the data model from the beginning.",
        ),
    },
)

SPANISH = {
    "alternativa-2-0": {
        "short_description": "SaaS para restaurantes con menús multilingües, pedidos y operaciones en tiempo real.",
        "description": "Una plataforma integral para restaurantes con catálogos multilingües, pedidos como invitado, personalización de ingredientes, administración por roles, promociones y notificaciones de pedidos en tiempo real.",
        "problem": "Los restaurantes necesitan más que un menú QR estático: productos, ingredientes, disponibilidad, permisos y pedidos deben mantenerse sincronizados entre clientes y personal.",
        "solution": "Un SaaS modular con Django y React, pedidos como invitado, roles granulares, operaciones atómicas, notificaciones WebSocket y almacenamiento multimedia en la nube.",
        "details": (("Dominio", "Productos, opciones e ingredientes"), ("Dominio", "Pedidos, promociones y configuración de empresa"), ("Tiempo real", "Django Channels"), ("Tiempo real", "WebSockets respaldados por Redis"), ("Infraestructura", "PostgreSQL"), ("Infraestructura", "Almacenamiento multimedia en Cloudinary")),
        "lessons": ("Modelar explícitamente la personalización mantiene consistentes los precios y el stock.", "Los pedidos como invitado y autenticados deben compartir dominio y diferenciarse mediante permisos."),
    },
    "eduardo-bernal-abogado": {
        "short_description": "Plataforma legal en producción para citas, clientes y documentos seguros.",
        "description": "Sitio legal para clientes respaldado por flujos privados para el personal, disponibilidad de citas, portal protegido y entrega auditable de documentos sensibles.",
        "problem": "El despacho necesitaba captar clientes, coordinar citas e intercambiar documentos sensibles sin dispersar la operación entre canales informales.",
        "solution": "Una plataforma full-stack en producción con captación pública, roles de personal y clientes, sincronización de calendario, descargas con caducidad y trazabilidad de acceso.",
        "details": (("Operaciones legales", "Clientes y expedientes"), ("Operaciones legales", "Citas y disponibilidad"), ("Seguridad", "Tokens de descarga únicos con caducidad"), ("Seguridad", "Registro de acceso a documentos"), ("Integraciones", "Google Calendar y Meet"), ("Integraciones", "Almacenamiento de documentos compatible con S3")),
        "lessons": ("Los documentos sensibles requieren propiedad, caducidad y trazabilidad impuestas por el servidor.", "La agenda pública debe respetar la disponibilidad privada sin exponer calendarios internos."),
    },
    "equus-pub-digital-menu": {
        "title": "Menú digital de Equus Pub",
        "short_description": "Menú digital bilingüe y experiencia de pedidos en producción para Equus Pub.",
        "description": "Sistema en producción para hostelería con catálogo multilingüe, personalización de ingredientes, carrito persistente, pedidos por WhatsApp y gestión de contenido protegida.",
        "problem": "Un restaurante en funcionamiento necesitaba actualizar el menú sin reimprimirlo y ofrecer a sus clientes una experiencia bilingüe rápida para explorar y personalizar pedidos.",
        "solution": "Aplicación desplegada con Django REST y React, contenido traducido, administración por roles, personalización por ingrediente y pedidos directos por WhatsApp.",
        "details": (("Experiencia del cliente", "Catálogo en español e inglés"), ("Experiencia del cliente", "Carrito persistente y personalizable"), ("Administración", "Acceso por roles con JWT"), ("Administración", "CRUD de productos, categorías e ingredientes"), ("Producción", "API Django en Railway"), ("Producción", "Frontend React en Vercel")),
        "lessons": ("Un menú de restaurante necesita flujos operativos de edición, no solo un catálogo público atractivo.", "La traducción y la personalización de ingredientes deben formar parte del modelo de datos desde el inicio."),
    },
}


def translate(content, language, **fields):
    content.set_current_language(language)
    for field, value in fields.items():
        setattr(content, field, value)
    content.save()


def build_thumbnail(title, subtitle, accent):
    safe_title = escape(title)
    safe_subtitle = escape(subtitle)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#171717"/>
      <stop offset="1" stop-color="#090909"/>
    </linearGradient>
    <radialGradient id="glow" cx="75%" cy="20%" r="65%">
      <stop stop-color="{accent}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#background)"/>
  <rect width="1200" height="675" fill="url(#glow)"/>
  <rect x="72" y="74" width="1056" height="527" rx="28" fill="#111" stroke="#39312d" stroke-width="2"/>
  <rect x="104" y="112" width="992" height="54" rx="12" fill="#1c1a19"/>
  <circle cx="140" cy="139" r="8" fill="{accent}"/>
  <circle cx="168" cy="139" r="8" fill="#5d5753"/>
  <circle cx="196" cy="139" r="8" fill="#5d5753"/>
  <rect x="104" y="198" width="310" height="363" rx="16" fill="#181716" stroke="#302d2b"/>
  <rect x="446" y="198" width="650" height="170" rx="16" fill="#181716" stroke="#302d2b"/>
  <rect x="446" y="394" width="309" height="167" rx="16" fill="#181716" stroke="#302d2b"/>
  <rect x="787" y="394" width="309" height="167" rx="16" fill="#181716" stroke="#302d2b"/>
  <rect x="480" y="238" width="360" height="16" rx="8" fill="{accent}" opacity=".85"/>
  <rect x="480" y="280" width="520" height="11" rx="5" fill="#514b47"/>
  <rect x="480" y="311" width="430" height="11" rx="5" fill="#383431"/>
  <text x="138" y="282" fill="#f1eeeb" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="700">{safe_title}</text>
  <text x="138" y="332" fill="#a49b95" font-family="Inter,Arial,sans-serif" font-size="21">{safe_subtitle}</text>
  <rect x="138" y="386" width="190" height="48" rx="9" fill="{accent}" opacity=".22" stroke="{accent}"/>
  <text x="174" y="417" fill="{accent}" font-family="Inter,Arial,sans-serif" font-size="18">Case Study</text>
</svg>"""


class Command(BaseCommand):
    help = "Create idempotent demonstration data for the portfolio frontend."

    @transaction.atomic
    def handle(self, *args, **options):
        Project.objects.filter(slug__in=LEGACY_PROJECT_SLUGS).delete()

        technologies = {}
        for name, defaults in TECHNOLOGIES.items():
            technology, _ = Technologies.objects.update_or_create(name=name, defaults=defaults)
            technologies[name] = technology

        for order, data in enumerate(PROJECTS):
            spanish = SPANISH[data["slug"]]
            project, _ = Project.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "short_description": data["short_description"],
                    "description": data["description"],
                    "github": data["github"],
                    "live_url": data["live_url"],
                    "is_featured": True,
                },
            )
            project.technologies.set(technologies[name] for name in data["technologies"])
            project_content, _ = ProjectContent.objects.get_or_create(project=project)
            translate(project_content, "en", title=data["title"], short_description=data["short_description"], description=data["description"])
            translate(project_content, "es", title=spanish.get("title", data["title"]), short_description=spanish["short_description"], description=spanish["description"])

            if not project.image or project.image.name.startswith("projects/seed/"):
                if project.image:
                    project.image.storage.delete(project.image.name)
                thumbnail = build_thumbnail(project.title, project.short_description, data["accent"])
                project.image.save(f"seed/{project.slug}.svg", ContentFile(thumbnail.encode()), save=True)

            problem_solution, _ = ProblemSolution.objects.update_or_create(
                project=project,
                defaults={"problem": data["problem"], "solution": data["solution"]},
            )
            problem_content, _ = ProblemSolutionContent.objects.get_or_create(problem_solution=problem_solution)
            translate(problem_content, "en", problem=data["problem"], solution=data["solution"])
            translate(problem_content, "es", problem=spanish["problem"], solution=spanish["solution"])

            TechDetail.objects.filter(project=project).delete()
            english_details = [(category, text) for category, items in data["details"].items() for text in items]
            for (category, text), (es_category, es_text) in zip(english_details, spanish["details"]):
                detail = TechDetail.objects.create(project=project, category=category, text=text)
                detail_content = TechDetailContent.objects.create(tech_detail=detail)
                translate(detail_content, "en", category=category, text=text)
                translate(detail_content, "es", category=es_category, text=es_text)

            Lesson.objects.filter(project=project).delete()
            for text, es_text in zip(data["lessons"], spanish["lessons"]):
                lesson = Lesson.objects.create(project=project, text=text)
                lesson_content = LessonContent.objects.create(lesson=lesson)
                translate(lesson_content, "en", text=text)
                translate(lesson_content, "es", text=es_text)

            project_image, _ = ProjectImage.objects.update_or_create(
                project=project,
                title="Dashboard overview",
                defaults={"image": project.image.name, "order": order},
            )
            image_content, _ = ProjectImageContent.objects.get_or_create(project_image=project_image)
            translate(image_content, "en", title="Dashboard overview")
            translate(image_content, "es", title="Vista general")

        Technologies.objects.filter(
            name__in=LEGACY_TECHNOLOGIES,
            projects__isnull=True,
        ).delete()

        self.stdout.write(self.style.SUCCESS("Portfolio demo data is ready."))
