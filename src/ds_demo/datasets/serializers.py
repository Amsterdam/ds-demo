import json
import os

from jsonschema import validate, RefResolver
from rest_framework import serializers
from rest_framework.fields import JSONField
from rest_framework.serializers import ListSerializer

from ds_demo.datasets.models import Data
from ds_demo.schemas.models import Schema


def _amsterdam_schema_handler(_):
    filename = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'json_schemas', 'amsterdam.schema.json')
    with open(filename) as schema:
        amsterdam_schema = json.load(schema)

    return amsterdam_schema


class DataListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def is_valid(self, *args, **kwargs):
        schema = Schema.objects.get(pk=self.initial_data[0]['dataset']).schema
        resolver = RefResolver(base_uri="",
                               handlers={"https": _amsterdam_schema_handler}, referrer=None, cache_remote=False)
        list_of_instances = self.initial_data
        if len(list_of_instances) > 0:
            for instance in list_of_instances:
                validate(instance=instance['instance'], resolver=resolver, schema=schema)

        return super().is_valid(*args, **kwargs)


class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Data
        fields = ('dataset', 'instance_id', 'instance',)
        list_serializer_class = DataListSerializer

    def is_valid(self, *args, **kwargs):
        schema = Schema.objects.get(pk=self.initial_data['dataset']).schema
        resolver = RefResolver(base_uri="",
                               handlers={"https": _amsterdam_schema_handler}, referrer=None, cache_remote=False)
        validate(instance=self.initial_data['instance'], resolver=resolver, schema=schema)

        return super().is_valid(*args, **kwargs)

    def to_representation(self, instance):
        if isinstance(instance, Data):
            return instance.instance
        return instance['instance']
