from django.db import migrations


TRANSLATIONS = {
    "en": {
        "title": "About me",
        "body": (
            "I'm a backend developer specialized in **Python**, focused on building web applications "
            "and APIs with a clear, maintainable and well-structured architecture.\n\n"
            "I work mainly with **Python, Django, FastAPI, PostgreSQL, SQLModel, Docker and Pytest**, "
            "covering everything from business logic and API design to data persistence, authentication, "
            "testing and deployment.\n\n"
            "I have developed real projects for clients, including web platforms and administration "
            "systems, taking responsibility for both the backend and production deployment. I also "
            "maintain my own **homelab**, where I deploy and manage containerized applications, databases, "
            "monitoring and infrastructure services.\n\n"
            "I'm especially interested in understanding what happens behind each tool: database design, "
            "architecture, concurrency, performance, testing and infrastructure. AI is part of my workflow "
            "as a tool to accelerate development, research and problem-solving, while I remain focused on "
            "understanding and controlling the code I build.\n\n"
            "I'm currently continuing to deepen my knowledge of **Python and backend development**, while "
            "expanding my skills in **Docker, PostgreSQL, CI/CD, Linux and software architecture**.\n\n"
            "**Main stack**\n\n"
            "**Backend:** Python · Django · Django REST Framework · FastAPI · SQLModel\n"
            "**Databases:** PostgreSQL · MySQL · SQLite · Redis\n"
            "**Testing:** Pytest\n"
            "**Infrastructure:** Docker · Linux · Cloudflare · Nginx\n"
            "**Frontend:** React · Vite · Tailwind CSS\n"
            "**Tools:** Git · GitHub · GitHub Actions"
        ),
        "location": "",
        "availability": "",
    },
    "es": {
        "title": "Sobre mí",
        "body": (
            "Soy desarrollador backend especializado en **Python**, enfocado en construir aplicaciones "
            "web y APIs con una arquitectura clara, mantenible y bien estructurada.\n\n"
            "Trabajo principalmente con **Python, Django, FastAPI, PostgreSQL, SQLModel, Docker y Pytest**, "
            "desarrollando desde la lógica de negocio y el diseño de APIs hasta persistencia de datos, "
            "autenticación, testing y despliegue.\n\n"
            "He desarrollado proyectos reales para clientes, incluyendo plataformas web y sistemas de "
            "administración, ocupándome tanto del backend como de su puesta en producción. También mantengo "
            "mi propio **homelab**, donde despliego y administro aplicaciones contenerizadas, bases de datos, "
            "monitorización y servicios de infraestructura.\n\n"
            "Me interesa especialmente entender qué ocurre detrás de cada herramienta: diseño de bases de "
            "datos, arquitectura, concurrencia, rendimiento, testing e infraestructura. La IA forma parte "
            "de mi flujo de trabajo como herramienta para acelerar el desarrollo, investigar y resolver "
            "problemas, pero mantengo el foco en comprender y controlar el código que construyo.\n\n"
            "Actualmente continúo profundizando en **Python y desarrollo backend**, mientras amplío mis "
            "conocimientos de **Docker, PostgreSQL, CI/CD, Linux y arquitectura de software**.\n\n"
            "**Stack principal**\n\n"
            "**Backend:** Python · Django · Django REST Framework · FastAPI · SQLModel\n"
            "**Bases de datos:** PostgreSQL · MySQL · SQLite · Redis\n"
            "**Testing:** Pytest\n"
            "**Infraestructura:** Docker · Linux · Cloudflare · Nginx\n"
            "**Frontend:** React · Vite · Tailwind CSS\n"
            "**Herramientas:** Git · GitHub · GitHub Actions"
        ),
        "location": "",
        "availability": "",
    },
}


def seed_about(apps, schema_editor):
    About = apps.get_model("about", "About")
    AboutTranslation = apps.get_model("about", "AboutTranslation")
    about, _ = About.objects.get_or_create(singleton=True, defaults={"is_visible": True})

    for language_code, content in TRANSLATIONS.items():
        AboutTranslation.objects.update_or_create(
            master=about,
            language_code=language_code,
            defaults=content,
        )


def remove_seeded_about(apps, schema_editor):
    About = apps.get_model("about", "About")
    About.objects.filter(singleton=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("about", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_about, remove_seeded_about),
    ]
