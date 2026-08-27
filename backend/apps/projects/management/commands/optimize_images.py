from pathlib import Path

from django.core.management.base import BaseCommand

from apps.project_images.models import ProjectImage
from apps.projects.models import Project
from core.images import optimize_raster_image


class Command(BaseCommand):
    help = 'Convert existing project and gallery raster images to optimized WebP files.'

    def handle(self, *args, **options):
        converted = 0

        for model in (Project, ProjectImage):
            for instance in model.objects.exclude(image='').exclude(image__isnull=True).iterator():
                image = instance.image
                if Path(image.name).suffix.lower() == '.webp':
                    continue

                image.open('rb')
                try:
                    optimized = optimize_raster_image(image)
                finally:
                    image.close()

                if not optimized:
                    continue

                instance.image.save(optimized.name, optimized, save=False)
                instance.save(update_fields=['image'])
                converted += 1

        self.stdout.write(self.style.SUCCESS(f'Optimized {converted} project images.'))
