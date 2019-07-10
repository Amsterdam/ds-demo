import json
import os

from jsonschema import validate, ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ds_demo.schemas.models import Schema

json_schema = None
schema_filename = os.path.join(os.path.dirname(__file__), 'json_schemas', 'amsterdam.object.meta.schema.json')
with open(schema_filename) as schema_file:
    json_schema = json.load(schema_file)


class SchemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schema
        fields = ('name', 'description', 'schema')

    def create(self, request, *args, **kwargs):
        try:
            validate(request['schema'], json_schema)
        except ValidationError as err:
            raise ParseError(err)
        return super().create(request, *args, **kwargs)
