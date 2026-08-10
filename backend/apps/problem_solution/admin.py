from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import ProblemSolution, ProblemSolutionContent


admin.site.register(ProblemSolution)
admin.site.register(ProblemSolutionContent, TranslatableAdmin)
