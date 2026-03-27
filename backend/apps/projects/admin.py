from django.contrib import admin
from .models import Project




@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']



