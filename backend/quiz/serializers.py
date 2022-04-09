from rest_framework import serializers
from .models import Quiz, QuizSubmission


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        
class QuizDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        fields = '__all__'        
        
class QuizSubmissionSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = QuizSubmission
        fields = '__all__'