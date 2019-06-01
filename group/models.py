from django.db import models

from user.models import User
from utility.methods import generate_key
from utility.mixins import ModelDateMixin

MAXIMUM_GROUP_SIZE = 100

# Should be a multiple of 4, or actual length may differ
GROUP_KEY_LENGTH = 16
INVITE_KEY_LENGTH = 20


def _generate_group_key():
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
    # colour = models.CharField(
    #     "Colour",
    #     max_length=20,
    # )
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


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
