from rest_framework import viewsets
from ds_demo.schemas.models import Schema
from ds_demo.schemas.serializers import SchemaSerializer


class SchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schemas to be viewed or edited.
    """
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer