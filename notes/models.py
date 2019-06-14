from django.core.validators import MinLengthValidator
from django.db import models

from activities.models import ActivityItem


class Note(ActivityItem):
    title = models.CharField(
        "Title",
        max_length=100,
    )
    text = models.TextField(
        "Text",
        # TODO: Add validators to most other fields throughout the codebase
        validators=[MinLengthValidator(limit_value=1)]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ActivityItem.NOTE_ACTIVITY.value

    def __str__(self):
        return self.title
