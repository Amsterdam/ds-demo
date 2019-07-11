from django.db import connection
from django.http import HttpResponse
from django.urls import include, path
from rest_framework import routers

from ds_demo.datasets.views import DataViewSet
from ds_demo.schemas.views import SchemaViewSet


def health(request):
    # check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except: # noqa E722
        log.exception("Database connectivity failed")
        return HttpResponse(
            "Database connectivity failed",
            content_type="text/plain", status=500)

    return HttpResponse(
        "Connectivity OK", content_type='text/plain', status=200)


router = routers.DefaultRouter()
router.register(r'schemas', SchemaViewSet)
router.register(r'datasets/(?P<dataset_and_id>.+)', DataViewSet)

urlpatterns = [
    path('status/health', health),
    path('ds_demo/', include(router.urls)),
]
