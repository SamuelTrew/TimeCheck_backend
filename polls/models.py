from django.db import models
from django.db.models import UniqueConstraint

from events.models import Event
from groups.models import Group
from users.models import User
from utility.methods import generate_key


# Should be a multiple of 4, or actual length may differ
from utility.mixins import ModelDateMixin

POLL_KEY_LENGTH = 16
POLL_OPTION_KEY_LENGTH = 16
VOTE_KEY_LENGTH = 16


def _generate_poll_key():
    return generate_key(POLL_KEY_LENGTH)


def _generate_poll_option_key():
    return generate_key(POLL_OPTION_KEY_LENGTH)


def _generate_vote_key():
    return generate_key(VOTE_KEY_LENGTH)


class Poll(ModelDateMixin):
    id = models.CharField(
        "Poll ID",
        primary_key=True,
        max_length=POLL_KEY_LENGTH,
        default=_generate_poll_key,
        editable=False,
    )
    question = models.CharField(
        "Question",
        max_length=100,
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
    multiple = models.BooleanField(
        "Allow Multiple Votes",
        default=False,   # Default: Allow only one vote
    )
    change = models.BooleanField(
        "Allow Changing Vote",
        default=True,   # Default: Allow changing vote
    )
    # TODO: Actually hide results from frontend until voted (if hide_results true)
    hide_results = models.BooleanField(
        "Hide Results Until Voted",
        default=True,   # Default: Hide results until voted
    )

    def __str__(self):
        return self.question


def _poll_option_order_default(data):
    print("#########")
    print(data)


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
