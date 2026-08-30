from django.contrib import admin

from .models import AnalysisRun, Project

admin.site.register(Project)
admin.site.register(AnalysisRun)