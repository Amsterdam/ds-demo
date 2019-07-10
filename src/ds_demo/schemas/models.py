from django.contrib.postgres.fields import JSONField
from django.db import models


class Schema(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    schema = JSONField()
