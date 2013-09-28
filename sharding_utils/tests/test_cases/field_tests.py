from mock import patch

from django.test import TestCase

from sharding_utils.tests.test_project.id_generation.models import SimpleExternalIdFieldModel


class ExternalIdFieldTestCase(TestCase):

    def test_auto_id_field_pulls_from_get_id_method(self):

        with patch('sharding_utils.tests.test_project.id_generation.generate_id') as mock:

            instance = SimpleExternalIdFieldModel()
            instance.save()
            # TODO: figure out how to patch this properly - suspect issue with meta class.
