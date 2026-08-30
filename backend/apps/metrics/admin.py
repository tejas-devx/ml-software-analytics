from django.contrib import admin

from .models import SoftwareMetric, SoftwareModule

admin.site.register(SoftwareModule)
admin.site.register(SoftwareMetric)