from rest_framework import serializers
from .models import Message
from accounts.serializers.user import UserBasicSerializer


class MessageSerializer(serializers.ModelSerializer):
    from_user = UserBasicSerializer()

    class Meta:
        model = Message
        exclude = ('user',)
