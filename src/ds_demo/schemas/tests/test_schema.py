import json
import os

from django.test import TestCase
from jsonschema import validate, Draft7Validator
from jsonschema.exceptions import ValidationError

from ds_demo.schemas.views import schema_filename


class SchemaValidationTest(TestCase):
    filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossiers.schema.json')
    json_schema = None

    def setUp(self):
        with open(schema_filename) as schema_file:
            self.json_schema = json.load(schema_file)

    def test_valid_schema_with_validator(self):
        with open(self.filename) as schema:
            loaded_schema = json.load(schema)

        Draft7Validator.check_schema(self.json_schema)
        validator = Draft7Validator(self.json_schema)
        self.assertTrue(validator.is_valid(loaded_schema))

    def test_valid_schema(self):
        with open(self.filename) as schema:
            loaded_schema = json.load(schema)

        validate(instance=loaded_schema, schema=self.json_schema)

    def test_invalid_schema(self):
        with open(self.filename) as schema:
            loaded_schema = json.load(schema)

        del(loaded_schema['properties'])

        with self.assertRaises(ValidationError):
            validate(instance=loaded_schema, schema=self.json_schema)
