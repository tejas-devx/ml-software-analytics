from django.db import models

from apps.projects.models import AnalysisRun


class SoftwareModule(models.Model):
    class ModuleType(models.TextChoices):
        CLASS = 'class', 'Class'
        FILE = 'file', 'File'

    analysis_run = models.ForeignKey(
        AnalysisRun,
        on_delete=models.CASCADE,
        related_name='software_modules',
    )
    module_path = models.CharField(max_length=1000)
    module_type = models.CharField(max_length=10, choices=ModuleType.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['analysis_run', 'module_path'],
                name='unique_module_path_per_analysis_run',
            )
        ]

    def __str__(self):
        return self.module_path

class SoftwareMetric(models.Model):
    module = models.ForeignKey(
        SoftwareModule,
        on_delete=models.CASCADE,
        related_name='metrics',
    )
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['module', 'metric_name'],
                name='unique_metric_name_per_module',
            )
        ]

    def __str__(self):
        return f'{self.metric_name}={self.metric_value} ({self.module.module_path})'