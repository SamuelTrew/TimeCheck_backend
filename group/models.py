from django.db import models

from user.models import User
from utility.methods import generate_key
from utility.mixins import ModelDateMixin

MAXIMUM_GROUP_SIZE = 100

# Should be a multiple of 4, or actual length may differ
GROUP_KEY_LENGTH = 16


def _generate_group_key():
    return generate_key(GROUP_KEY_LENGTH)


class Group(ModelDateMixin):
    id = models.CharField(
        "Group ID",
        primary_key=True,
        max_length=GROUP_KEY_LENGTH,
        default=_generate_group_key,
        editable=False,
    )
    name = models.CharField(
        "Name",
        max_length=150,
    )
    thumb = models.URLField(
        "Thumbnail",
        blank=True,
        null=True,
    )
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name