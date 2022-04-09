from django.shortcuts import get_object_or_404

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from accounts.views.user import decode_JWT
from server import basic_swagger_schema
from . import swagger_schema
from .models import Quiz, QuizSubmission
from .serializers import QuizSerializer, QuizDetailSerializer, QuizSubmissionSerialzier


class QuizViewSet(ViewSet):
    """About Quiz
    
    """
    model = Quiz
    queryset = Quiz.objects.all()
    serializer_classes = {
        'list': QuizSerializer,
        'create': QuizSerializer,
    }
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except:
            return QuizSerializer
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=QuizSerializer,
                description=swagger_schema.descriptions['QuizViewSet']['list'][200],
                examples=swagger_schema.examples['QuizViewSet']['quiz_list'],
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['QuizViewSet']['list']['description'],
        summary=swagger_schema.summaries['QuizViewSet']['list'],
        tags=['쪽지 시험',],
        examples=[
            basic_swagger_schema.examples[401],
        ],
    )
    def list(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        quizs = Quiz.objects.all()
        serializer = QuizSerializer(quizs, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

        
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=QuizSerializer,
                description=swagger_schema.descriptions['QuizViewSet']['create'][201],
                examples=swagger_schema.examples['QuizViewSet']['create'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['QuizViewSet']['create']['description'],
        summary=swagger_schema.summaries['QuizViewSet']['create'],
        tags=['쪽지 시험',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            *swagger_schema.examples['QuizViewSet']['create']['request']
        ]
    )
    
    def create(self, request):
        user = decode_JWT(request)
        if user == None or user.status == 'ST':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        data = {
            'title': request.data.get('title', None),
            'body': request.data.get('body', None),
            'answer': request.data.get('answer', None),
            'writer': user.pk,
        }
        serializer = QuizSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

class QuizDetailViewSet(ViewSet):
    """About Quiz
    
    """
    model = Quiz
    queryset = Quiz.objects.all()
    serializer_classes = {
        'retrieve': QuizDetailSerializer,
        'update': QuizDetailSerializer,
        'destroy': QuizDetailSerializer,
    }
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except:
            return QuizSerializer
            
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=QuizDetailSerializer,
                description=swagger_schema.descriptions['QuizDetailViewSet']['retrieve'][200],
                examples=swagger_schema.examples['QuizDetailViewSet']['quiz_detail']
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['QuizDetailViewSet']['retrieve']['description'],
        summary=swagger_schema.summaries['QuizDetailViewSet']['retrieve'],
        tags=['쪽지 시험',],
        examples=[
            basic_swagger_schema.examples[401],
        ],
    )
    def retrieve(self, request, quiz_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        quiz = get_object_or_404(Quiz, id=quiz_pk)
        serializer = QuizDetailSerializer(quiz)
        return Response(
            serializer.data,
        )
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=QuizDetailSerializer,
                description=swagger_schema.descriptions['QuizDetailViewSet']['update'][201],
                examples=swagger_schema.examples['QuizDetailViewSet']['update'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['QuizDetailViewSet']['update']['description'],
        summary=swagger_schema.summaries['QuizDetailViewSet']['update'],
        tags=['쪽지 시험',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            *swagger_schema.examples['QuizDetailViewSet']['create']['request'],
        ]
    )
    def update(self, request, quiz_pk):
        user = decode_JWT(request)
        if user == None or user.status == 'ST':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        homework = get_object_or_404(Quiz, id=quiz_pk)
        data = {
            'title': request.data.get('title', homework.title),
            'body': request.data.get('body', homework.body),
            'answer': request.data.get('answer', homework.answer),
            'writer': request.data.get('writer', user.pk),
        }
        serializer = QuizSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=QuizDetailSerializer,
                description=swagger_schema.descriptions['QuizDetailViewSet']['destroy'][200],
                examples=swagger_schema.examples['QuizDetailViewSet']['destroy'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['QuizDetailViewSet']['destroy']['description'],
        summary=swagger_schema.summaries['QuizDetailViewSet']['destroy'],
        tags=['쪽지 시험',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def destroy(self, request, quiz_pk):
        user = decode_JWT(request)
        if user == None or user.status == 'ST':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        quiz = get_object_or_404(Quiz, id=quiz_pk)
        quiz.delete()
        return Response(
            {'OK': 'No Content'},
            status=status.HTTP_200_OK
        )
    
   
class QuizSubmissionViewSet(ViewSet):
    model = QuizSubmission
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerialzier
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser, MultiPartParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=QuizSubmissionSerialzier,
                description=swagger_schema.descriptions['QuizSubmissionViewSet']['list'][200],
                examples=swagger_schema.examples['QuizSubmissionViewSet']['list'],
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['QuizSubmissionViewSet']['list']['description'],
        summary=swagger_schema.summaries['QuizSubmissionViewSet']['list'],
        tags=['쪽지 시험',],
        examples=[
            basic_swagger_schema.examples[401],
        ],
    )
    def list(self, request, quiz_pk):
        user = decode_JWT(request)
        if user == None or user.status == 'ST':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        quizsubmissions = QuizSubmission.objects.filter(quiz=quiz_pk)
        serializer = QuizSubmissionSerialzier(quizsubmissions, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=QuizSubmissionSerialzier,
                description=swagger_schema.descriptions['QuizSubmissionViewSet']['create'][201],
                examples=swagger_schema.examples['QuizSubmissionViewSet']['submission'],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['QuizSubmissionViewSet']['create']['description'],
        summary=swagger_schema.summaries['QuizSubmissionViewSet']['create'],
        tags=['쪽지 시험'],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
        ]
    )
    def create(self, request, quiz_pk):
        user = decode_JWT(request)
        if user == None or user.status == 'TE':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {
            'quiz': quiz_pk,
            'answer': request.data.get('answer', None),
            'submitter': user.pk,
        }
        
        serializer = QuizSubmissionSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )