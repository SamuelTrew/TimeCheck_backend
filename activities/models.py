import re

from django.db import models

from events.models import Event
from groups.models import Group
from users.models import User
from utility.methods import generate_key
from utility.mixins import ModelDateMixin

# Should be a multiple of 4, or actual length may differ
ACTIVITY_ITEM_KEY_LENGTH = 20


def _generate_activity_item_key():
    return generate_key(ACTIVITY_ITEM_KEY_LENGTH)


class ActivityType:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_choice_tuple(self):
        return tuple((self.value, self.name,))


class ActivityItem(ModelDateMixin):
    POLL_ACTIVITY = ActivityType("poll", 0)
    NOTE_ACTIVITY = ActivityType("note", 1)
    ACTIVITY_TYPE_CHOICES = (
        POLL_ACTIVITY.get_choice_tuple(),
        NOTE_ACTIVITY.get_choice_tuple(),
    )

    id = models.CharField(
        "Activity ID",
        primary_key=True,
        max_length=ACTIVITY_ITEM_KEY_LENGTH,
        default=_generate_activity_item_key,
        editable=False,
    )
    type = models.PositiveSmallIntegerField(
        "Activity Type",
        choices=ACTIVITY_TYPE_CHOICES,
        editable=False,
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    pinned = models.BooleanField(
        "Pinned",
        default=False,
    )

    class Meta:
        ordering = ('pinned', '-date_created',)

    def __str__(self):
        return f"Activity Item by {self.creator} in group {self.group}"

