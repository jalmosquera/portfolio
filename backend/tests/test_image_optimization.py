from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from PIL import Image

from apps.project_images.models import ProjectImage
from .conftest import ProjectFactory


def uploaded_image(name, size, mode='RGB', image_format='JPEG'):
    output = BytesIO()
    Image.new(mode, size, (220, 80, 40, 128) if mode == 'RGBA' else (220, 80, 40)).save(
        output,
        format=image_format,
    )
    return SimpleUploadedFile(name, output.getvalue(), content_type=f'image/{image_format.lower()}')


@pytest.mark.django_db
def test_project_upload_is_resized_and_converted_to_webp(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path

    project = ProjectFactory(image=uploaded_image('hero.jpg', (2400, 1200)))

    assert project.image.name.endswith('.webp')
    with Image.open(project.image.path) as optimized:
        assert optimized.format == 'WEBP'
        assert optimized.size == (1920, 960)


@pytest.mark.django_db
def test_gallery_upload_preserves_transparency_in_webp(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path

    gallery_image = ProjectImage.objects.create(
        project=ProjectFactory(),
        image=uploaded_image('gallery.png', (800, 600), mode='RGBA', image_format='PNG'),
    )

    assert gallery_image.image.name.endswith('.webp')
    with Image.open(gallery_image.image.path) as optimized:
        assert optimized.format == 'WEBP'
        assert optimized.mode == 'RGBA'


@pytest.mark.django_db
def test_non_raster_upload_is_left_unchanged(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    svg = SimpleUploadedFile('diagram.svg', b'<svg xmlns="http://www.w3.org/2000/svg"/>', content_type='image/svg+xml')

    project = ProjectFactory(image=svg)

    assert project.image.name.endswith('.svg')


@pytest.mark.django_db
def test_optimize_images_command_converts_existing_file_once(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    original = uploaded_image('legacy.jpg', (2400, 1200))
    original_name = default_storage.save('projects/legacy.jpg', ContentFile(original.read()))
    project = ProjectFactory()
    type(project).objects.filter(pk=project.pk).update(image=original_name)

    call_command('optimize_images')
    project.refresh_from_db()
    optimized_name = project.image.name
    call_command('optimize_images')
    project.refresh_from_db()

    assert optimized_name.endswith('.webp')
    assert project.image.name == optimized_name


@pytest.mark.django_db
def test_optimize_images_command_skips_missing_files(settings, tmp_path, capsys):
    settings.MEDIA_ROOT = tmp_path
    project = ProjectFactory()
    type(project).objects.filter(pk=project.pk).update(image='projects/missing.jpg')

    call_command('optimize_images')

    assert 'Skipped missing image: projects/missing.jpg' in capsys.readouterr().err
