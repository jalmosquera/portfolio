from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class About(TranslatableModel):
    singleton = models.BooleanField(default=True, unique=True, editable=False)
    is_visible = models.BooleanField(default=True)
    translations = TranslatedFields(
        title=models.CharField(max_length=160),
        body=models.TextField(),
        location=models.CharField(max_length=160, blank=True),
        availability=models.CharField(max_length=220, blank=True),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About me"
        verbose_name_plural = "About me"

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or "About me"
