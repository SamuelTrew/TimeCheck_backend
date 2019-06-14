from django.db import models
from django.db.models import UniqueConstraint

from activities.models import ActivityItem
from users.models import User
from utility.methods import generate_key
from utility.mixins import ModelDateMixin

# Should be a multiple of 4, or actual length may differ
POLL_OPTION_KEY_LENGTH = 16
VOTE_KEY_LENGTH = 16


def _generate_poll_option_key():
    return generate_key(POLL_OPTION_KEY_LENGTH)


def _generate_vote_key():
    return generate_key(VOTE_KEY_LENGTH)


class Poll(ActivityItem):
    question = models.CharField(
        "Question",
        max_length=100,
    )
    multiple = models.BooleanField(
        "Allow Multiple Votes",
        default=False,  # Default: Allow only one vote
    )
    change = models.BooleanField(
        "Allow Changing Vote",
        default=True,  # Default: Allow changing vote
    )
    # TODO: Actually hide results from frontend until voted (if hide_results true)
    hide_results = models.BooleanField(
        "Hide Results Until Voted",
        default=True,  # Default: Hide results until voted
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ActivityItem.POLL_ACTIVITY.value

    def __str__(self):
        return self.question


class PollOption(ModelDateMixin):
    id = models.CharField(
        "Poll Option ID",
        primary_key=True,
        max_length=POLL_OPTION_KEY_LENGTH,
        default=_generate_poll_option_key,
        editable=False,
    )
    poll = models.ForeignKey(
        Poll,
        related_name='options',
        on_delete=models.CASCADE
    )
    text = models.CharField(
        "Option Text",
        max_length=250
    )
    order = models.SmallIntegerField(
        "Order",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('order', 'date_created',)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.order is None and self._state.adding:
            # Set a default order if poll option is new
            existing_options = self.poll.options.count()
            self.order = existing_options + 1

        super().save(*args, **kwargs)


class Vote(ModelDateMixin):
    id = models.CharField(
        "Vote ID",
        primary_key=True,
        max_length=VOTE_KEY_LENGTH,
        default=_generate_vote_key,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    option = models.ForeignKey(
        PollOption,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'option'], name='unique_vote')
        ]

    def __str__(self):
        return f"Vote for {self.option} by {self.user}"
