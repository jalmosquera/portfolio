from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


MAX_RESUME_SIZE = 10 * 1024 * 1024


def validate_resume_size(file):
    if file.size > MAX_RESUME_SIZE:
        raise ValidationError("The CV must not exceed 10 MB.")


def validate_pdf_signature(file):
    position = file.tell()
    try:
        file.seek(0)
        if file.read(5) != b"%PDF-":
            raise ValidationError("The uploaded file is not a valid PDF.")
    finally:
        file.seek(position)


class Resume(models.Model):
    singleton = models.BooleanField(default=True, unique=True, editable=False)
    file = models.FileField(
        upload_to="resumes/%Y/%m/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            validate_resume_size,
            validate_pdf_signature,
        ],
    )
    public_filename = models.CharField(max_length=160, default="Jalberth_Mosquera_CV.pdf")
    download_count = models.PositiveIntegerField(default=0, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CV"

    def __str__(self):
        return self.public_filename

    def save(self, *args, **kwargs):
        previous_file = None
        if self.pk:
            previous_file = type(self).objects.filter(pk=self.pk).values_list("file", flat=True).first()
        super().save(*args, **kwargs)
        if previous_file and previous_file != self.file.name:
            self.file.storage.delete(previous_file)

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        filename = self.file.name
        result = super().delete(*args, **kwargs)
        if filename:
            storage.delete(filename)
        return result
