from html import escape

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.lessons.models import Lesson
from apps.problem_solution.models import ProblemSolution
from apps.project_images.models import ProjectImage
from apps.projects.models import Project
from apps.tech_details.models import TechDetail
from apps.technology.models import Technologies


TECHNOLOGIES = {
    "Python": {"icon": "🐍", "color": "#f2c94c"},
    "Django": {"icon": "◩", "color": "#69b88d"},
    "Docker": {"icon": "🐳", "color": "#68a9e8"},
    "Linux": {"icon": "♟", "color": "#f1f1f1"},
    "Nginx": {"icon": "⬡", "color": "#68bd82"},
    "PostgreSQL": {"icon": "🐘", "color": "#7ba5d6"},
    "Raspberry Pi": {"icon": "◉", "color": "#d2768c"},
}

PROJECTS = (
    {
        "title": "Alternativa 2.0",
        "slug": "alternativa-2-0",
        "short_description": "Restaurant SaaS platform for digital menus and online ordering.",
        "description": "A self-hosted platform that helps restaurants manage menus, QR access, orders and daily operations from one dashboard.",
        "github": "https://github.com/jalmosquera",
        "live_url": "",
        "technologies": ("Python", "Django", "Docker", "Nginx", "PostgreSQL"),
        "accent": "#d7794f",
        "problem": "Restaurants needed an affordable way to digitize menus and centralize orders without depending on multiple services.",
        "solution": "A modular Django platform with QR menus, role-based management and a Dockerized self-hosted deployment.",
        "details": {
            "Backend": ("Django REST Framework", "PostgreSQL"),
            "Infrastructure": ("Docker Compose", "Nginx"),
        },
        "lessons": (
            "Design domain boundaries before adding restaurant-specific features.",
            "Keep deployment reproducible from the first production iteration.",
        ),
    },
    {
        "title": "Alternativa Kiosk",
        "slug": "alternativa-kiosk",
        "short_description": "Tablet kiosk application designed for restaurant self-service.",
        "description": "A focused kiosk interface connected to the restaurant platform, optimized for touch devices and constrained hardware.",
        "github": "https://github.com/jalmosquera",
        "live_url": "",
        "technologies": ("Python", "Django", "Nginx", "Raspberry Pi"),
        "accent": "#b86447",
        "problem": "Small restaurants needed self-service ordering without purchasing expensive proprietary kiosk hardware.",
        "solution": "A lightweight web kiosk deployed on Raspberry Pi devices and synchronized with the main restaurant backend.",
        "details": {
            "Device": ("Raspberry Pi", "Touch display"),
            "Delivery": ("Nginx", "Local network mode"),
        },
        "lessons": (
            "Touch interfaces require different spacing and feedback than desktop dashboards.",
            "Offline-friendly behavior matters on unreliable restaurant networks.",
        ),
    },
    {
        "title": "Abogado CRM",
        "slug": "abogado-crm",
        "short_description": "Client and case management platform for independent law firms.",
        "description": "A secure CRM for organizing clients, matters, deadlines and documents with a deployment model suitable for small firms.",
        "github": "https://github.com/jalmosquera",
        "live_url": "",
        "technologies": ("Python", "Django", "Docker", "Linux", "PostgreSQL"),
        "accent": "#8f513e",
        "problem": "Independent lawyers were tracking clients, cases and deadlines across spreadsheets and disconnected tools.",
        "solution": "A centralized Django CRM with structured case records, deadline tracking and controlled access to sensitive information.",
        "details": {
            "Backend": ("Django", "PostgreSQL"),
            "Operations": ("Docker", "Linux"),
        },
        "lessons": (
            "Sensitive domains need explicit access rules instead of UI-only restrictions.",
            "Auditability should be considered alongside the initial data model.",
        ),
    },
)


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
        technologies = {}
        for name, defaults in TECHNOLOGIES.items():
            technology, _ = Technologies.objects.update_or_create(name=name, defaults=defaults)
            technologies[name] = technology

        for order, data in enumerate(PROJECTS):
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

            if not project.image:
                thumbnail = build_thumbnail(project.title, project.short_description, data["accent"])
                project.image.save(f"seed/{project.slug}.svg", ContentFile(thumbnail.encode()), save=True)

            ProblemSolution.objects.update_or_create(
                project=project,
                defaults={"problem": data["problem"], "solution": data["solution"]},
            )

            TechDetail.objects.filter(project=project).delete()
            TechDetail.objects.bulk_create(
                TechDetail(project=project, category=category, text=text)
                for category, items in data["details"].items()
                for text in items
            )

            Lesson.objects.filter(project=project).delete()
            Lesson.objects.bulk_create(Lesson(project=project, text=text) for text in data["lessons"])

            ProjectImage.objects.update_or_create(
                project=project,
                title="Dashboard overview",
                defaults={"image": project.image.name, "order": order},
            )

        self.stdout.write(self.style.SUCCESS("Portfolio demo data is ready."))
