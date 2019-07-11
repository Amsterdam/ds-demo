from django.contrib.postgres.fields import JSONField
from django.db import models


class Data(models.Model):

    dataset = models.CharField(max_length=255)
    instance_id = models.CharField(max_length=255)
    instance = JSONField()

    class Meta:
        unique_together = [['dataset', 'instance_id']]

