from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from drf_spectacular.utils import (
    extend_schema, OpenApiResponse
)

from server import basic_swagger_schema
from schools.models import School
from . import swagger_schema
from .user import decode_JWT
from ..models import Student
from ..serializers.student import StudentSerializer, StudentLectureSerializer


class StudentView(APIView):
    """Student View
    
    """
    model = Student
    serializer_class = StudentSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=StudentSerializer,
                description=swagger_schema.descriptions['StudentView']['get'][200],
                examples=[
                    swagger_schema.examples['StudentView']['get'][200],
                ]
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['StudentView']['get']['description'],
        summary=swagger_schema.summaries['StudentView']['get'],
        tags=['학생',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ],
    )
    def get(self, request, student_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        student = get_object_or_404(Student, pk=student_pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=StudentSerializer,
                description=swagger_schema.descriptions['StudentView']['put'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['StudentView']['put']['description'],
        summary=swagger_schema.summaries['StudentView']['put'],
        tags=['학생'],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['StudentView']['put']['request'],
            swagger_schema.examples['StudentView']['put'][201],
        ],
    )
    def put(self, request, student_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        student = get_object_or_404(Student, pk=student_pk)
        school = get_object_or_404(School, pk=student.get_school_pk())
        if student.user.pk != user.pk\
            and (user.status == 'SA' and user.school_admin.get_school_pk() != school.pk):
                return Response(
                    {'error': 'Unauthorized'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        data = {
            'user': {
                'id': user.pk,
                'email': request.data['user']['email'],
                'phone': request.data['user']['phone'],
            },
            'guardian_phone': request.data['guardian_phone'],
        }
        serializer = StudentSerializer(student, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class StudentLectureView(APIView):
    """Student Lecture View
    
    """
    model = Student
    serializer_class = StudentLectureSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=StudentLectureSerializer,
                description=swagger_schema.descriptions['StudentLectureView']['get'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['StudentLectureView']['get']['description'],
        summary=swagger_schema.summaries['StudentLectureView']['get'],
        tags=['학생', '수업'],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['StudentLectureView']['get'][200],
        ]
    )
    def get(self, request, student_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        student = get_object_or_404(Student, pk=student_pk)
        serializer = StudentLectureSerializer(student)
        return Response(serializer.data)
