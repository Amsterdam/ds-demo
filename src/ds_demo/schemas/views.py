import json
import os

from rest_framework import viewsets

from jsonschema import validate, ValidationError
from rest_framework.exceptions import ParseError

from ds_demo.schemas.models import Schema
from ds_demo.schemas.serializers import SchemaSerializer

json_schema = None
schema_filename = os.path.join(os.path.dirname(__file__), 'json_schemas', 'amsterdam.object.meta.schema.json')
with open(schema_filename) as schema_file:
    json_schema = json.load(schema_file)


class SchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schemas to be viewed or edited.
    """
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

    def create(self, request, *args, **kwargs):
        try:
            validate(request.data['schema'], json_schema)
        except ValidationError as err:
            raise ParseError(err)
        return super().create(request, *args, **kwargs)
