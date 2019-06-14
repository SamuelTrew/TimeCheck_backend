from rest_framework import serializers

from notes.models import Note
from notes.serializers import NoteActivitySerializer
from polls.models import Poll
from polls.serializers import PollActivitySerializer
from users.serializers import BasicUserSerializer
from .models import ActivityItem


class ActivityItemSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    creator = BasicUserSerializer(read_only=True)
    data = serializers.SerializerMethodField()

    class Meta:
        model = ActivityItem
        fields = ('id', 'type', 'date_created', 'date_updated', 'pinned', 'creator', 'group', 'data',)
        read_only_fields = fields

    def get_data(self, obj):
        if obj.type is ActivityItem.POLL_ACTIVITY.value:
            instance = Poll.objects.get(id=obj.id)
            serializer = PollActivitySerializer(instance=instance)
        elif obj.type is ActivityItem.NOTE_ACTIVITY.value:
            instance = Note.objects.get(id=obj.id)
            serializer = NoteActivitySerializer(instance=instance)
        else:
            raise ValueError("Invalid ActivityItem type")

        return serializer.data
