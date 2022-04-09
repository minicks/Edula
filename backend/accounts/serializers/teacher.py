from rest_framework import serializers

from ..models import Teacher
from .user import UserBasicSerializer, UserDetailSerializer
from schools.serializers import (
    SchoolSerializer, LectureSerializer, ClassroomSerializer
)


class TeacherSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    classroom = ClassroomSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = '__all__'
    
    def update(self, instance, validated_data):
        if 'user' in validated_data:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_data = validated_data.pop('user')
            nested_serializer.update(nested_instance, nested_data)
        return super(TeacherSerializer, self).update(instance, validated_data)


class TeacherLectureSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    lecture_list = LectureSerializer(many=True)
    
    class Meta:
        model = Teacher
        fields = ('user', 'lecture_list')