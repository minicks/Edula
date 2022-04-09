from rest_framework import serializers

from ..models import User, SchoolAdmin
from schools.models import School


class UserProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('profile_image',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'phone', 'status', 'profile_image',)
        read_only_fields = ('id', 'username', 'first_name', 'status')


class UserBasicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'status', 'profile_image',)
        read_only_fields = ('id', 'username', 'first_name', 'status')


class ResisterSerializer(serializers.ModelSerializer):

    class SchoolAdminResisterSerializer(serializers.ModelSerializer):
        from schools.serializers import SchoolSerializer
        school = SchoolSerializer()

        class Meta:
            model = SchoolAdmin
            fields = ('school', 'account_type')

    school_admin = SchoolAdminResisterSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'school_admin')


class UserCUDSerialzier(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'status')


class UserInformationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'phone',)


class FindUsernameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields = ('id', 'first_name', 'email',)


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'old_password', 'status',\
            'new_password', 'new_password_confirmation')
        read_only_fields = ('id', 'username', 'status')


class PasswordResetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class FriendSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'status',)
