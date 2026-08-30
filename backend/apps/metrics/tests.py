from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.metrics.models import SoftwareMetric, SoftwareModule
from apps.projects.models import AnalysisRun, Project


class MetricsRelationshipTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            source_type=Project.SourceType.GITHUB,
            source_reference='https://github.com/example/metrics-test',
        )
        self.run = AnalysisRun.objects.create(project=self.project)

    def test_analysis_run_to_software_module_relationship(self):
        module = SoftwareModule.objects.create(
            analysis_run=self.run,
            module_path='com/example/Foo.java',
            module_type=SoftwareModule.ModuleType.CLASS,
        )
        self.assertEqual(self.run.software_modules.count(), 1)
        self.assertEqual(self.run.software_modules.first(), module)
        self.assertEqual(module.analysis_run, self.run)

    def test_software_module_to_software_metric_relationship(self):
        module = SoftwareModule.objects.create(
            analysis_run=self.run,
            module_path='com/example/Bar.java',
            module_type=SoftwareModule.ModuleType.CLASS,
        )
        metric = SoftwareMetric.objects.create(
            module=module, metric_name='loc', metric_value=142.0
        )
        self.assertEqual(module.metrics.count(), 1)
        self.assertEqual(module.metrics.first(), metric)
        self.assertEqual(metric.module, module)


class MetricsConstraintTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            source_type=Project.SourceType.GITHUB,
            source_reference='https://github.com/example/constraints-test',
        )
        self.run = AnalysisRun.objects.create(project=self.project)

    def test_module_path_unique_within_analysis_run(self):
        SoftwareModule.objects.create(
            analysis_run=self.run,
            module_path='com/example/Dup.java',
            module_type=SoftwareModule.ModuleType.CLASS,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SoftwareModule.objects.create(
                    analysis_run=self.run,
                    module_path='com/example/Dup.java',
                    module_type=SoftwareModule.ModuleType.CLASS,
                )

    def test_metric_name_unique_within_module(self):
        module = SoftwareModule.objects.create(
            analysis_run=self.run,
            module_path='com/example/Baz.java',
            module_type=SoftwareModule.ModuleType.CLASS,
        )
        SoftwareMetric.objects.create(
            module=module, metric_name='loc', metric_value=100.0
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SoftwareMetric.objects.create(
                    module=module, metric_name='loc', metric_value=200.0
                )