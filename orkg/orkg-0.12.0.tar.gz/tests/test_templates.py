from unittest import TestCase
from orkg import ORKG


class TestTemplates(TestCase):
    """
    Some test scenarios might need to be adjusted to the content of the running ORKG instance
    """
    orkg = ORKG()

    def test_materialize(self):
        self.orkg.templates.materialize_templates()
        tp = self.orkg.templates
        instance = tp.confidence_interval_95(has_unit='C', upper_confidence_limit=0.5, lower_confidence_limit=0.01)
        instance.save()
        self.assertTrue(True)
