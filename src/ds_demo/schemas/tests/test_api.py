import json
import os

from django.test import TestCase
from rest_framework.test import APIClient

from ds_demo.schemas.models import Schema


class SchemaTest(TestCase):
    bouwdossiers = {
        'name': "bouwdossiers",
        'description': "Het bouwdossier schema",
        'schema': None
    }
    invalid_schema = None
    new_description = "Het nieuwe bouwdossier schema"

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossiers.schema.json')
        with open(filename) as schema:
            loaded_schema = json.load(schema)
            self.bouwdossiers['schema'] = json.dumps(loaded_schema)
            del(loaded_schema['properties'])
            self.invalid_schema = json.dumps(loaded_schema)
        self.client = APIClient()

    def test_get_schema(self):
        response = self.client.get('/ds_demo/schemas/')
        self.assertEquals(response.status_code, 200)
        self.assertListEqual(response.data['results'], [])

    def test_upload_schema(self):
        response = self.client.post('/ds_demo/schemas/', self.bouwdossiers)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Schema.objects.count(), 1)
        self.assertEquals(Schema.objects.all()[0].name, "bouwdossiers")

    def test_update_schema(self):
        self.client.post('/ds_demo/schemas/', self.bouwdossiers)
        updated = self.bouwdossiers.copy()
        updated['description'] = self.new_description

        response = self.client.put('/ds_demo/schemas/'+self.bouwdossiers['name']+'/', updated)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Schema.objects.count(), 1)
        self.assertEquals(Schema.objects.all()[0].description, self.new_description)

    def test_invalid_schema(self):
        invalid = self.bouwdossiers.copy()
        invalid['schema'] = self.invalid_schema

        response = self.client.post('/ds_demo/schemas/', invalid)
        self.assertEquals(response.status_code, 400)
