from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Poll, PollOption, Vote


class PollOptionSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    selected = serializers.SerializerMethodField()

    class Meta:
        model = PollOption
        fields = ('id', 'text', 'votes', 'order', 'selected',)
        read_only_fields = ('id', 'votes', 'selected',)

    def get_votes(self, obj):
        return obj.vote_set.count()

    def get_selected(self, obj):
        request = self.context['request']
        if not request:
            raise APIException()
        return Vote.objects.filter(user=request.user, option=obj).exists()


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'question', 'options', 'event', 'multiple', 'change', 'hide_results',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            PollOption.objects.create(poll=poll, **option_data)
        return poll


# Used for the activity feed (less data required)
class PollActivityOptionSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = PollOption
        fields = ('id', 'text', 'votes', 'order',)
        read_only_fields = fields

    def get_votes(self, obj):
        return obj.vote_set.count()


# Used for the activity feed (less data required)
class PollActivitySerializer(serializers.ModelSerializer):
    options = PollActivityOptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'question', 'options',)
        read_only_fields = fields
