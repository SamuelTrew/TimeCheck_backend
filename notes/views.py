from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer
    # TODO: Evaluate if this 'prefetch_related' actually benefits performance
    queryset = Note.objects.all()

    def perform_create(self, serializer):
        group_id = self.kwargs['parent_lookup_group']
        serializer.save(creator=self.request.user, group_id=group_id)

