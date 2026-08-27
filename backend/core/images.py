from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_IMAGE_DIMENSION = 1920
WEBP_QUALITY = 82
RASTER_FORMATS = {'JPEG', 'PNG', 'WEBP'}


def optimize_raster_image(image):
    try:
        image.seek(0)
        with Image.open(image) as source:
            if source.format not in RASTER_FORMATS:
                return None

            optimized = ImageOps.exif_transpose(source)
            optimized.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)
            mode = 'RGBA' if optimized.mode in {'RGBA', 'LA'} or 'transparency' in optimized.info else 'RGB'
            optimized = optimized.convert(mode)

            output = BytesIO()
            optimized.save(output, format='WEBP', quality=WEBP_QUALITY, method=6)
    except (OSError, UnidentifiedImageError):
        image.seek(0)
        return None

    return ContentFile(output.getvalue(), name=f'{Path(image.name).stem}.webp')
