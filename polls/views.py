from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Poll, PollOption, Vote
from .serializers import PollSerializer, PollOptionSerializer


class PollViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PollSerializer
    # TODO: Evaluate if this 'prefetch_related' actually benefits performance
    queryset = Poll.objects.prefetch_related('options')

    def perform_create(self, serializer):
        group_id = self.kwargs['parent_lookup_group']
        serializer.save(creator=self.request.user, group_id=group_id)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk, parent_lookup_group):
        # Get vote option id from POST data
        option_id = request.data.get('option', None)

        # If option id not found, return error
        if not option_id:
            raise ParseError(detail="Vote request must supply an option id.")

        poll = self.get_object()

        try:
            option = poll.options.get(id=option_id)
        except PollOption.DoesNotExist:
            raise ParseError(detail="Invalid option id for this poll.")

        # Do not allow a user to vote for the same option twice
        if Vote.objects.filter(user=request.user, option=option).exists():
            raise ParseError(detail="Already voted for this option.")

        # If poll is single-voting, do not allow a user to vote for an additional option (unvote if allowed)
        if not poll.multiple:
            if poll.change:
                # Can change vote, so unvote for existing selection (if exists), then vote for this option
                Vote.objects.filter(user=request.user, option__poll=poll).delete()
            elif Vote.objects.filter(user=request.user, option__poll=poll).exists():
                raise ParseError(detail="Already voted in this poll.")

        Vote.objects.create(user=request.user, option=option)
        serializer = PollSerializer(instance=poll, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unvote(self, request, pk, parent_lookup_group):
        # Get vote option id from POST data
        option_id = request.data.get('option', None)

        # If option id not found, return error
        if not option_id:
            raise ParseError(detail="Vote request must supply an option id.")

        poll = self.get_object()

        try:
            option = poll.options.get(id=option_id)
        except PollOption.DoesNotExist:
            raise ParseError(detail="Invalid option id for this poll.")

        # Do not allow a user to unvote if poll prohibits changing votes
        if not poll.change:
            raise ParseError(detail="You may not change your vote in this poll.")

        # Check that the user has already voted for this option
        try:
            vote = Vote.objects.get(user=request.user, option=option)
        except Vote.DoesNotExist:
            # User has not previously voted for this option (so no vote to remove, cannot unvote)
            raise ParseError(detail="You have not previously voted for this option")

        vote.delete()
        serializer = PollSerializer(instance=poll, context={'request': request})
        return Response(serializer.data)
