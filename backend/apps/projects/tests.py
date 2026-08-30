from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.projects.models import AnalysisRun, Project


class ProjectRelationshipTests(TestCase):
    def test_project_to_analysis_run_relationship(self):
        project = Project.objects.create(
            name='Test Project',
            source_type=Project.SourceType.GITHUB,
            source_reference='https://github.com/example/test-repo',
        )
        run = AnalysisRun.objects.create(project=project)

        self.assertEqual(project.analysis_runs.count(), 1)
        self.assertEqual(project.analysis_runs.first(), run)
        self.assertEqual(run.project, project)


class ProjectConstraintTests(TestCase):
    def test_github_source_reference_unique_per_owner(self):
        owner = User.objects.create_user(username='tejas')
        Project.objects.create(
            owner=owner,
            name='Repo A',
            source_type=Project.SourceType.GITHUB,
            source_reference='https://github.com/example/repo',
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Project.objects.create(
                    owner=owner,
                    name='Repo A duplicate',
                    source_type=Project.SourceType.GITHUB,
                    source_reference='https://github.com/example/repo',
                )

    def test_zip_source_reference_is_not_constrained(self):
        owner = User.objects.create_user(username='tejas2')
        Project.objects.create(
            owner=owner,
            name='Zip Upload 1',
            source_type=Project.SourceType.ZIP,
            source_reference='project.zip',
        )
        # Must NOT raise — the unique constraint only applies to source_type='github'
        Project.objects.create(
            owner=owner,
            name='Zip Upload 2',
            source_type=Project.SourceType.ZIP,
            source_reference='project.zip',
        )
        self.assertEqual(
            Project.objects.filter(source_reference='project.zip').count(), 2
        )