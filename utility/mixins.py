from django.db import models


class ModelDateMixin(models.Model):
    date_created = models.DateTimeField("Date created", auto_now_add=True)
    date_updated = models.DateTimeField("Date updated", auto_now=True)

    class Meta:
        abstract = True
