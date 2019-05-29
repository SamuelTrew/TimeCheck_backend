from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email',)
        read_only_fields = fields   # Ensure that the serializer is always read-only
