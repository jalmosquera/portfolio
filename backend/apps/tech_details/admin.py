from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import TechDetail, TechDetailContent



admin.site.register(TechDetail)
admin.site.register(TechDetailContent, TranslatableAdmin)
