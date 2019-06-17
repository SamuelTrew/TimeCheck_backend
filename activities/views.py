from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import ActivityItem
from .serializers import ActivityItemSerializer


class GroupActivityViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivityItemSerializer
    queryset = ActivityItem.objects.all()


class HomeActivityViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivityItemSerializer
    queryset = ActivityItem.objects.all()
