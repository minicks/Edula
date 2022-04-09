from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from accounts.views.user import decode_JWT
from accounts.models import Teacher
from accounts.serializers.teacher import TeacherSerializer
from server import basic_swagger_schema
from . import swagger_schema

class TeacherView(APIView):
    '''Teacher
    '''
    model = Teacher
    serializer_class = TeacherSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=TeacherSerializer,
                description=swagger_schema.descriptions['TeacherView']['get'][200],
                examples=swagger_schema.examples['TeacherView']['get'][200]
            ),
            401: basic_swagger_schema.open_api_response[401]
        },
        description=swagger_schema.descriptions['TeacherView']['get']['description'],
        summary=swagger_schema.summaries['TeacherView']['get'],
        tags=['교사', '목록',],
        examples=[
            basic_swagger_schema.examples[401]
        ],
    )
    def get(self, request,school_pk):
        """Get total teacher of school information
        
        Use school_pk, return total teacher of school infromation
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        teachers = Teacher.objects.filter(school_id=school_pk)
        serializer = TeacherSerializer(teachers, many=True)  
        return Response(serializer.data)