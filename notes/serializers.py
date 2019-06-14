from rest_framework import serializers

from users.models import User
from users.serializers import BasicUserSerializer
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    creator = BasicUserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'event', 'creator', 'date_created',)
        read_only_fields = ('id',)

    # def create(self, validated_data):
    #     options_data = validated_data.pop('options')
    #     poll = Poll.objects.create(**validated_data)
    #     for option_data in options_data:
    #         PollOption.objects.create(poll=poll, **option_data)
    #     return poll


class NoteActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'text',)
        read_only_fields = fields
