from django.db import models

from groups.models import Group
from utility.methods import generate_key
from utility.mixins import ModelDateMixin

MAXIMUM_GROUP_SIZE = 100

# Should be a multiple of 4, or actual length may differ
EVENT_KEY_LENGTH = 16


def _generate_event_key():
    return generate_key(EVENT_KEY_LENGTH)


class Event(ModelDateMixin):
    id = models.CharField(
        "Event ID",
        primary_key=True,
        max_length=EVENT_KEY_LENGTH,
        default=_generate_event_key,
        editable=False,
    )
    name = models.CharField(
        "Name",
        max_length=150,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
