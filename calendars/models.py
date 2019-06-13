from django.db import models

from events.models import Event
from groups.models import Group
from users.models import User
from utility.methods import generate_key

# Should be a multiple of 4, or actual length may differ
from utility.mixins import ModelDateMixin

EVENT_CALENDAR_KEY_LENGTH = 16
PERSONAL_CALENDAR_KEY_LENGTH = 16
SELECTION_KEY_LENGTH = 16


def _generate_event_calendar_key():
    return generate_key(EVENT_CALENDAR_KEY_LENGTH)


def _generate_personal_calendar_key():
    return generate_key(PERSONAL_CALENDAR_KEY_LENGTH)


def _generate_selection_key():
    return generate_key(SELECTION_KEY_LENGTH)


class EventCalendar(ModelDateMixin):
    id = models.CharField(
        "Event Calendar ID",
        primary_key=True,
        max_length=EVENT_CALENDAR_KEY_LENGTH,
        default=_generate_event_calendar_key(),
        editable=False,
    )
    note = models.CharField(
        "Note",
        max_length=100,
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

    def __str__(self):
        return f"{self.event}'s event calendar"


class PersonalCalendar(ModelDateMixin):
    id = models.CharField(
        "Personal Calendar ID",
        primary_key=True,
        max_length=PERSONAL_CALENDAR_KEY_LENGTH,
        default=_generate_personal_calendar_key(),
        editable=False,
    )
    eventCalendar = models.ForeignKey(
        EventCalendar,
        related_name='event',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user}'s personal calendar"


class Selection(ModelDateMixin):
    id = models.CharField(
        "Selection ID",
        primary_key=True,
        max_length=SELECTION_KEY_LENGTH,
        default=_generate_selection_key(),
        editable=False,
    )
    date = models.CharField(
        "Selected Date",
        max_length=10
    )
    calendar = models.ForeignKey(
        PersonalCalendar,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Select {self.date} for {self.calendar}"
