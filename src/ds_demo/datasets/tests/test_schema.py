import json
import os

from django.test import TestCase
from jsonschema import Draft7Validator, RefResolver

from ds_demo.datasets.serializers import _amsterdam_schema_handler


class SchemaTestCase(TestCase):
    test_schema = None

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossiers.schema.json')
        with open(filename) as schema:
            self.test_schema = json.load(schema)

    def test_data(self):
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossier.json')
        with open(filename) as instance_json:
            instance = json.load(instance_json)

        Draft7Validator.check_schema(self.test_schema)

        _resolver = RefResolver(base_uri="defenitions",
                                handlers={"https": _amsterdam_schema_handler}, referrer=None, cache_remote=False)

        validator = Draft7Validator(self.test_schema, resolver=_resolver)
        self.assertTrue(validator.is_valid(instance))
