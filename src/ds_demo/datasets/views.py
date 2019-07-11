# class FileUploadView(views.APIView):
#     parser_classes = (FileUploadParser,)
#
#     def put(self, request, filename, format=None):
#         file_obj = request.FILES['file']
#         # do some stuff with uploaded file
#         return Response(status=204)
#
# urlpatterns = patterns('', url(r'^imageUpload', views.FileUploadView.as_view())
import copy

from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from ds_demo.datasets.models import Data
from ds_demo.datasets.serializers import DataSerializer


class CreateDataInstanceMixin(CreateModelMixin):
    """
    Create a data-model instance.
    """
    def create(self, request, *args, **kwargs):
        is_many = 'is_many' in kwargs and kwargs['is_many'] is True
        data = self._get_data_from_request(request, kwargs['dataset_and_id'], is_many)

        serializer = self.get_serializer(data=data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _get_data_from_request(self, request, dataset, is_many):
        if is_many:
            data = [{'dataset': dataset, 'instance_id': item['id'], 'instance': item}
                    for item in request.data]
        else:
            data = {'dataset': dataset, 'instance_id': request.data['id'], 'instance': request.data}
        return data


class DataViewSet(CreateDataInstanceMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Datasets and instances of data to be viewed or edited.
    """
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    def list(self, request, *args, **kwargs):
        if 'dataset_and_id' not in kwargs:
            pass   # list of datasets, not yet implemented

        if '/' in kwargs['dataset_and_id']:
            return super(DataViewSet, self).retrieve(request, *args, **kwargs)

        self.queryset = Data.objects.filter(dataset=kwargs['dataset_and_id']).values('instance').all()
        return super(DataViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        return super(DataViewSet, self).create(request, is_many=is_many, *args, **kwargs)

    def get_object(self):
        dataset, instance_id = self.kwargs['dataset_and_id'].split('/')
        obj = Data.objects.filter(dataset=dataset, instance_id=instance_id).values('instance').first()
        self.check_object_permissions(self.request, obj)

        return obj
