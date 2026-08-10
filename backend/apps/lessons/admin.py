from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Lesson, LessonContent

admin.site.register(Lesson)
admin.site.register(LessonContent, TranslatableAdmin)
