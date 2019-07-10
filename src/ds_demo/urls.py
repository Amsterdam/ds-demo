from django.db import connection
from django.http import HttpResponse
from django.urls import include, path
from rest_framework import routers

from ds_demo.schemas import views


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
router.register(r'schemas', views.SchemaViewSet)

urlpatterns = [
    path('status/health', health),
    path('ds_demo/', include(router.urls)),
]
