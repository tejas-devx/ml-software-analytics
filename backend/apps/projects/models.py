from django.conf import settings
from django.db import models


class Project(models.Model):
    class SourceType(models.TextChoices):
        GITHUB = 'github', 'GitHub'
        ZIP = 'zip', 'ZIP Upload'

    class Language(models.TextChoices):
        JAVA = 'java', 'Java'
        PYTHON = 'python', 'Python'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
    )
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=10, choices=SourceType.choices)
    source_reference = models.CharField(max_length=500)
    primary_language = models.CharField(
        max_length=10, choices=Language.choices, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'source_reference'],
                condition=models.Q(source_type='github'),
                name='unique_owner_source_reference_for_github',
            )
        ]

    def __str__(self):
        return self.name

class AnalysisRun(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RUNNING = 'running', 'Running'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    class Language(models.TextChoices):
        JAVA = 'java', 'Java'
        PYTHON = 'python', 'Python'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='analysis_runs',
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    detected_language = models.CharField(
        max_length=10, choices=Language.choices, null=True, blank=True
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'AnalysisRun {self.id} ({self.project.name})'