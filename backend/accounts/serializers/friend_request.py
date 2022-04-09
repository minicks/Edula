from rest_framework import serializers

from ..models import FriendRequest
from .user import UserBasicSerializer

class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'request_status',)


class FriendRequestDetailSerializer(serializers.ModelSerializer):
    from_user = UserBasicSerializer(read_only=True)
    to_user = UserBasicSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'request_status',)
