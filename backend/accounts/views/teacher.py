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
from ..models import Teacher
from ..serializers.teacher import TeacherSerializer, TeacherLectureSerializer


class TeacherView(APIView):
    model = Teacher
    serializer_class = TeacherSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=TeacherSerializer,
                description=swagger_schema.descriptions['TeacherView']['get'][200],
                examples=[
                    swagger_schema.examples['TeacherView']['get'][200],
                ]
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['TeacherView']['get']['description'],
        summary=swagger_schema.summaries['TeacherView']['get'],
        tags=['교사',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
        ],
    )
    def get(self, request, teacher_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        teacher = get_object_or_404(Teacher, pk=teacher_pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=TeacherSerializer,
                description=swagger_schema.descriptions['TeacherView']['put'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['TeacherView']['put']['description'],
        summary=swagger_schema.summaries['TeacherView']['put'],
        tags=['교사',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['TeacherView']['put']['request'],
            swagger_schema.examples['TeacherView']['put'][201],
        ],
    )
    def put(self, request, teacher_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        teacher = get_object_or_404(Teacher, pk=teacher_pk)
        school = get_object_or_404(School, pk=teacher.get_school_pk())
        if teacher.user.pk != user.pk\
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
        }
        serializer = TeacherSerializer(teacher, data=data)
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


class TeacherLectureView(APIView):
    model = Teacher
    serializer_class = TeacherLectureSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=TeacherLectureSerializer,
                description=swagger_schema.descriptions['TeacherLectureView']['get'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['TeacherLectureView']['get']['description'],
        summary=swagger_schema.summaries['TeacherLectureView']['get'],
        tags=['교사', '수업',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['TeacherLectureView']['get'][200],
        ]
    )
    def get(self, request, teacher_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        student = get_object_or_404(Teacher, pk=teacher_pk)
        serializer = TeacherLectureSerializer(student)
        return Response(serializer.data)
