from django.contrib import admin
from .models import Projects




@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']



