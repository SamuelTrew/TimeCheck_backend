from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Group
from .serializers import GroupSerializer


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
