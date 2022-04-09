from rest_framework import serializers

from ..models import Student
from .user import UserBasicSerializer, UserDetailSerializer
from schools.serializers import (
    SchoolSerializer, LectureSerializer, ClassroomSerializer
)


class StudentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    classroom = ClassroomSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
    
    def update(self, instance, validated_data):
        if 'user' in validated_data:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_data = validated_data.pop('user')
            nested_serializer.update(nested_instance, nested_data)
        return super(StudentSerializer, self).update(instance, validated_data)


class StudentPostSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    school = SchoolSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'


class StudentLectureSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    lecture_list = LectureSerializer(many=True)
    
    class Meta:
        model = Student
        fields = ('user', 'lecture_list')
