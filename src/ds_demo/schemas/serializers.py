from rest_framework import serializers

from ds_demo.schemas.models import Schema


class SchemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schema
        fields = ('name', 'description', 'schema')
