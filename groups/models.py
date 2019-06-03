from django.db import models

from users.models import User
from utility.color import ColorField
from utility.methods import generate_key
from utility.mixins import ModelDateMixin

MAXIMUM_GROUP_SIZE = 100

# Should be a multiple of 4, or actual length may differ
GROUP_KEY_LENGTH = 16
MEMBERSHIP_KEY_LENGTH = 20
INVITE_KEY_LENGTH = 20


def _generate_group_key():
    return generate_key(GROUP_KEY_LENGTH)


def _generate_membership_key():
    return generate_key(GROUP_KEY_LENGTH)


def _generate_invite_key():
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
    # colour = ColorField(
    #     "Colour",
    #     blank=True,
    #     null=True,
    # )
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    id = models.CharField(
        "Membership ID",
        primary_key=True,
        max_length=MEMBERSHIP_KEY_LENGTH,
        default=_generate_membership_key,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='unique_membership'),
        ]


class Invite(models.Model):
    id = models.CharField(
        "Invite ID",
        primary_key=True,
        max_length=INVITE_KEY_LENGTH,
        default=_generate_invite_key,
        editable=False,
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_created = models.DateTimeField("Date created", auto_now_add=True)

    def __str__(self):
        return self.id
