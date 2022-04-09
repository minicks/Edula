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
from . import swagger_schema
from .user import decode_JWT
from ..models import SchoolAdmin
from ..serializers.school_admin import SchoolAdminSerializer


class SchoolAdminView(APIView):
    model = SchoolAdmin
    serializer_class = SchoolAdminSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=SchoolAdminSerializer,
                description=swagger_schema.descriptions['SchoolAdminView']['get'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['SchoolAdminView']['get']['description'],
        summary=swagger_schema.summaries['SchoolAdminView']['get'],
        tags=['학교 관리자'],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['SchoolAdminView']['get'][200],
        ],
    )
    def get(self, request, school_admin_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        school_admin = get_object_or_404(SchoolAdmin, pk=school_admin_pk)
        if school_admin.user.pk != user.pk:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = SchoolAdminSerializer(school_admin)
        return Response(serializer.data)
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=SchoolAdminSerializer,
                description=swagger_schema.descriptions['SchoolAdminView']['put'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['SchoolAdminView']['put']['description'],
        summary=swagger_schema.summaries['SchoolAdminView']['put'],
        tags=['학교 관리자'],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['SchoolAdminView']['put']['request'],
            swagger_schema.examples['SchoolAdminView']['put'][201],
        ],
    )
    def put(self, request, school_admin_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        school_admin = get_object_or_404(SchoolAdmin, pk=school_admin_pk)
        if school_admin.user.pk != user.pk:
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
        serializer = SchoolAdminSerializer(school_admin, data=data)
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
