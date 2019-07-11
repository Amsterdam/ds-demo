import json
import os

from django.test import TestCase
from rest_framework.test import APIClient

from ds_demo.datasets.models import Data
from ds_demo.schemas.models import Schema


class APITestCase(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossiers.schema.json')
        with open(filename) as schema:
            loaded_schema = json.load(schema)
            Schema(
                name='bouwdossiers',
                description='Het schema van bouwdossiers',
                schema=loaded_schema
            ).save()
        self.client = APIClient()

    # def test_get_data(self):
    #     filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossier.json')
    #     with open(filename) as instance:
    #         instance_data = json.load(instance)
    #
    #     self.client.post('/ds_demo/datasets/bouwdossiers/', instance_data, format='json')
    #
    #     response = self.client.get('/ds_demo/datasets/bouwdossiers/')
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(response.data['count'], 1)
    #
    #     response = self.client.get('/ds_demo/datasets/bouwdossiers/')
    #     self.assertEquals(response.status_code, 200)
    #     self.assertListEqual(response.data['id'], instance_data['id'])

    def test_upload_instance(self):
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossier.json')
        with open(filename) as instance:
            instance_data = json.load(instance)

        response = self.client.post('/ds_demo/datasets/bouwdossiers/', instance_data, format='json')
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Data.objects.count(), 1)
        self.assertEquals(Data.objects.all()[0].instance_id, "sa12153")

    def test_upload_instances(self):
        filename = os.path.join(os.path.dirname(__file__), 'fixtures', 'bouwdossiers.json')
        with open(filename) as instance:
            instances_data = json.load(instance)

        response = self.client.post('/ds_demo/datasets/bouwdossiers/', instances_data, format='json')
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Data.objects.count(), 3)

    def test_upload_instances_ndjson(self):
        pass