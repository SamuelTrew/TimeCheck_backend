from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.serializers import UserSerializer
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'thumb', 'members',)
        read_only_fields = ('id', 'thumb', 'members',)

    def validate(self, attrs):
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise ValidationError("Cannot include unknown field(s): {}".format(", ".join(unknown)))
        read_only = set(self.initial_data).intersection(set(self.Meta.read_only_fields))
        if read_only:
            raise ValidationError("Cannot include read only field(s): {}".format(", ".join(read_only)))
        return attrs


# class GroupReceiveSerializer(serializers.ModelSerializer):
#     members = serializers.ListField(
#         child=serializers.UUIDField(),
#         min_length=None,
#         max_length=MAXIMUM_GROUP_SIZE
#     )
#
#     class Meta:
#         model = Group
#         fields = ('name', 'members',)
#
#     def validate(self, attrs):
#         unknown = set(self.initial_data) - set(self.fields)
#         if unknown:
#             raise ValidationError("Cannot include unknown field(s): {}".format(", ".join(unknown)))
#         return attrs
