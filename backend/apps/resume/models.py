from django.db import models
from django.core.exceptions import ValidationError
from parler.models import TranslatableModel, TranslatedFields


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
    name = models.CharField(max_length=160, default="Jalberth Mosquera")
    email = models.EmailField(default="Jmosquera2305@gmail.com")
    phone = models.CharField(max_length=40, blank=True)
    linkedin_url = models.URLField(max_length=300, blank=True)
    github_url = models.URLField(max_length=300, blank=True)
    portfolio_url = models.URLField(
        max_length=300,
        blank=True,
        default="https://portfolio.mosquerasoft.com/",
    )
    portrait = models.ImageField(upload_to="resumes/portrait/", blank=True)
    public_filename = models.CharField(max_length=160, default="Jalberth_Mosquera_CV.pdf")
    download_count = models.PositiveIntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dynamic CV"
        verbose_name_plural = "Dynamic CV"

    def __str__(self):
        return self.name


class ResumeContent(TranslatableModel):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="content")
    translations = TranslatedFields(
        headline=models.CharField(max_length=220),
        location=models.CharField(max_length=160, blank=True),
        profile=models.TextField(),
    )

    def __str__(self):
        return self.safe_translation_getter("headline", any_language=True) or self.resume.name


class OrderedResumeItem(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["order", "pk"]


class ResumeHighlight(TranslatableModel, OrderedResumeItem):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="highlights")
    translations = TranslatedFields(text=models.CharField(max_length=240))

    def __str__(self):
        return self.safe_translation_getter("text", any_language=True) or "Highlight"


class ResumeSkill(OrderedResumeItem):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80, default="Core skills")
    icon_name = models.CharField(max_length=80, blank=True, help_text="SVG filename without path")

    def __str__(self):
        return self.name


class ResumeExperience(TranslatableModel, OrderedResumeItem):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=160)
    period = models.CharField(max_length=120)
    translations = TranslatedFields(
        role=models.CharField(max_length=180),
        location=models.CharField(max_length=160, blank=True),
        summary=models.TextField(blank=True),
    )

    def __str__(self):
        role = self.safe_translation_getter("role", any_language=True) or "Experience"
        return f"{self.company} - {role}"


class ResumeExperienceBullet(TranslatableModel, OrderedResumeItem):
    experience = models.ForeignKey(
        ResumeExperience,
        on_delete=models.CASCADE,
        related_name="bullets",
    )
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experience_bullets")
    translations = TranslatedFields(text=models.CharField(max_length=300))

    def __str__(self):
        return self.safe_translation_getter("text", any_language=True) or "Experience detail"


class ResumeEducation(TranslatableModel, OrderedResumeItem):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education")
    period = models.CharField(max_length=100, blank=True)
    translations = TranslatedFields(
        institution=models.CharField(max_length=180),
        qualification=models.CharField(max_length=220),
        location=models.CharField(max_length=160, blank=True),
    )

    def __str__(self):
        return self.safe_translation_getter("institution", any_language=True) or "Education"
