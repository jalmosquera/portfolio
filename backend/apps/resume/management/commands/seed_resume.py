from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.resume.models import (
    Resume,
    ResumeContent,
    ResumeEducation,
    ResumeExperience,
    ResumeExperienceBullet,
    ResumeHighlight,
    ResumeSkill,
)


PROFILE = {
    "en": {
        "headline": "Backend Developer specialized in Python and Django",
        "location": "Málaga, Spain · Remote",
        "profile": "Backend developer specialized in Python and Django, experienced in building production APIs and SaaS systems. I develop reliable backends with Django REST Framework, PostgreSQL and real deployments, focused on software that solves business problems.",
        "highlights": ["Real client projects delivered to production", "Production SaaS systems", "Experience building software for real businesses"],
        "role": "Freelance Backend Developer",
        "experience_location": "From Spain · Present · Remote",
        "experience_summary": "Design, delivery and operation of backend systems used by real clients.",
        "bullets": [
            "Production REST APIs used by real clients with Django REST Framework",
            "Design and implementation of multi-tenant SaaS systems",
            "Authentication, permissions and user role management",
            "PostgreSQL integration and query optimization",
            "Production deployments and maintenance with Railway and Vercel",
            "Solutions for restaurants, CRM systems and administration panels",
        ],
        "institution": "Unidad Educativa Liceo Alcázar",
        "qualification": "High School Diploma in Science",
        "education_location": "Caracas, Venezuela",
    },
    "es": {
        "headline": "Desarrollador backend especializado en Python y Django",
        "location": "Málaga, España · Remoto",
        "profile": "Desarrollador backend especializado en Python y Django, con experiencia construyendo APIs y sistemas SaaS en producción. Desarrollo backends sólidos con Django REST Framework, PostgreSQL y despliegues reales, enfocado en crear software funcional que resuelve problemas de negocio.",
        "highlights": ["Proyectos reales entregados a clientes en producción", "Sistemas SaaS en producción", "Experiencia construyendo software para negocio real"],
        "role": "Desarrollador backend freelance",
        "experience_location": "Desde España · Actualidad · Remoto",
        "experience_summary": "Diseño, entrega y operación de sistemas backend utilizados por clientes reales.",
        "bullets": [
            "Desarrollo de APIs REST en producción con Django REST Framework",
            "Diseño e implementación de sistemas SaaS multi-tenant",
            "Gestión de autenticación, permisos y roles de usuario",
            "Integración con PostgreSQL y optimización de consultas",
            "Despliegue y mantenimiento en producción con Railway y Vercel",
            "Soluciones para restaurantes, CRM y paneles administrativos",
        ],
        "institution": "Unidad Educativa Liceo Alcázar",
        "qualification": "Bachiller en Ciencias",
        "education_location": "Caracas, Venezuela",
    },
}

SKILLS = [
    ("Python", "py.svg"),
    ("Django", "dj.svg"),
    ("Django REST Framework", "dj.svg"),
    ("FastAPI", "fastapi.svg"),
    ("PostgreSQL", "postgresql.svg"),
    ("Docker", "docker.svg"),
    ("Git", "git.svg"),
    ("Linux", "linux.svg"),
    ("JWT authentication", "jwt.svg"),
    ("REST APIs", "swagger.svg"),
    ("SaaS architecture", ""),
    ("CI/CD", "gitlab.svg"),
]


def translate(instance, language, **fields):
    instance.set_current_language(language)
    for field, value in fields.items():
        setattr(instance, field, value)
    instance.save()


class Command(BaseCommand):
    help = "Create or refresh the editable bilingual CV data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--if-empty",
            action="store_true",
            help="Seed only when the CV has not been configured yet.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["if_empty"] and Resume.objects.filter(content__isnull=False).exists():
            self.stdout.write("Dynamic CV already configured; keeping database content.")
            return
        resume, _ = Resume.objects.update_or_create(
            singleton=True,
            defaults={
                "name": "Jalberth Mosquera",
                "email": "Jmosquera2305@gmail.com",
                "phone": "+34 623 73 65 66",
                "linkedin_url": "https://www.linkedin.com/in/jalberth-mosquera-077975387/",
                "github_url": "https://github.com/jalmosquera",
                "public_filename": "Jalberth_Mosquera_CV.pdf",
                "is_active": True,
            },
        )
        content, _ = ResumeContent.objects.get_or_create(resume=resume)
        for language, data in PROFILE.items():
            translate(content, language, headline=data["headline"], location=data["location"], profile=data["profile"])

        if not resume.portrait:
            portrait_path = Path(__file__).resolve().parents[2] / "assets" / "portrait.jpg"
            with portrait_path.open("rb") as portrait:
                resume.portrait.save("jalberth-mosquera.jpg", File(portrait), save=True)

        resume.highlights.all().delete()
        for order, texts in enumerate(zip(PROFILE["en"]["highlights"], PROFILE["es"]["highlights"])):
            item = ResumeHighlight.objects.create(resume=resume, order=order)
            translate(item, "en", text=texts[0])
            translate(item, "es", text=texts[1])

        resume.skills.all().delete()
        for order, (name, icon_name) in enumerate(SKILLS):
            ResumeSkill.objects.create(resume=resume, name=name, icon_name=icon_name, order=order)

        resume.experiences.all().delete()
        experience = ResumeExperience.objects.create(resume=resume, company="Mosquera Soft", period="2024 - Present", order=0)
        for language, data in PROFILE.items():
            translate(experience, language, role=data["role"], location=data["experience_location"], summary=data["experience_summary"])
        for order, (english, spanish) in enumerate(zip(PROFILE["en"]["bullets"], PROFILE["es"]["bullets"])):
            bullet = ResumeExperienceBullet.objects.create(resume=resume, experience=experience, order=order)
            translate(bullet, "en", text=english)
            translate(bullet, "es", text=spanish)

        resume.education.all().delete()
        education = ResumeEducation.objects.create(resume=resume, period="2006", order=0)
        for language, data in PROFILE.items():
            translate(education, language, institution=data["institution"], qualification=data["qualification"], location=data["education_location"])

        self.stdout.write(self.style.SUCCESS("Dynamic CV data is ready."))
