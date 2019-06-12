from django.db import models


class ModelDateMixin(models.Model):
    date_created = models.DateTimeField(
        "Date Created",
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated",
        auto_now=True
    )

    class Meta:
        abstract = True
