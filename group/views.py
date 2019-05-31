from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Invite
from .serializers import GroupSerializer, InviteSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def get_queryset(self):
        """
        Only return groups that match the currently authenticated user
        """
        current_user = self.request.user
        return Group.objects.filter(members__in=[current_user])

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(self.request.user)
        group.save()

    @action(detail=True, methods=['get'])
    def generate_invite(self, request, pk=None):
        group = self.get_object()
        invite = Invite(group=group)
        invite.save()
        serializer = InviteSerializer(instance=invite)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def leave(self, request, pk=None):
        group = self.get_object()
        group.members.remove(self.request.user)
        if group.members.count() == 0:
            group.delete()
        else:
            # TODO: Make another user admin if group now has no admins
            group.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcceptInviteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, invite=None):
        queryset = Invite.objects.all()
        invite = get_object_or_404(queryset, pk=invite)
        group = invite.group
        group.members.add(request.user)
        return Response({'status': 'Success'})


class InviteGroupView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, invite=None):
        queryset = Invite.objects.all()
        invite = get_object_or_404(queryset, pk=invite)
        group = invite.group
        serializer = GroupSerializer(instance=group)
        return Response(serializer.data)
