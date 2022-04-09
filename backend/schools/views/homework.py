from django.shortcuts import get_object_or_404

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from accounts.models import User
from accounts.views.user import decode_JWT
from server import basic_swagger_schema
from notifications.models import Notification
from . import swagger_schema
from ..models import Lecture, Homework
from ..serializers import HomeworkSerializer, HomeworkDetailSerializer


class HomeworkViewSet(ViewSet):
    """About Homework
    """
    model = Homework
    queryset = Homework.objects.all()
    serializer_classes = {
        'list': HomeworkSerializer,
        'create': HomeworkSerializer,
        'retrieve': HomeworkDetailSerializer,
        'update': HomeworkDetailSerializer,
        'destroy': HomeworkDetailSerializer,
    }
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except:
            return HomeworkSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=HomeworkSerializer,
                description=swagger_schema.descriptions['HomeworkViewSet']['list'][200],
                examples=swagger_schema.examples['HomeworkViewSet']['homework_list'],
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['HomeworkViewSet']['list']['description'],
        summary=swagger_schema.summaries['HomeworkViewSet']['list'],
        tags=['숙제',],
        examples=[
            basic_swagger_schema.examples[401],
        ],
    )
    def list(self, request, lecture_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        homeworks = Homework.objects.filter(lecture_id=lecture_pk)\
            .prefetch_related('submission')
        if user.status == 'ST':
            data = {
                'homework_count': homeworks.count(),
                'homework': [
                    {
                        'id': homework.pk,
                        'title': homework.title,
                        'content': homework.content,
                        'created_at': homework.created_at,
                        'deadline': homework.deadline,
                        'writer': {
                            'id': homework.writer.pk,
                            'username': homework.writer.username,
                        },
                        'lecture': homework.lecture.pk,
                        'submission': homework.submission.filter(writer=user.pk).exists(),
                    } for homework in homeworks
                ],
            }
            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        elif user.status in ['TE', 'SA']:
            data = {
                'homework_count': homeworks.count(),
                'homework': [
                    {
                        'id': homework.pk,
                        'title': homework.title,
                        'content': homework.content,
                        'created_at': homework.created_at,
                        'deadline': homework.deadline,
                        'writer': {
                            'id': homework.writer.pk,
                            'username': homework.writer.username,
                        },
                        'lecture': homework.lecture.pk,
                        'submission_list': [
                            {
                                'id': submission.writer.pk,
                                'username': submission.writer.username,
                            }
                            for submission in homework.submission.all()
                        ],
                    } for homework in homeworks
                ],
            }
            return Response(
                data,
                status=status.HTTP_200_OK,
            )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=HomeworkSerializer,
                description=swagger_schema.descriptions['HomeworkViewSet']['create'][201],
                examples=swagger_schema.examples['HomeworkViewSet']['create'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['HomeworkViewSet']['create']['description'],
        summary=swagger_schema.summaries['HomeworkViewSet']['create'],
        tags=['숙제',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            *swagger_schema.examples['HomeworkViewSet']['create']['request']
        ]
    )
    def create(self, request, lecture_pk):
        user = decode_JWT(request)
        if user == None or user.status == 'ST':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lecture = get_object_or_404(Lecture, pk=lecture_pk)
        data = {
            'title': request.data.get('title', None),
            'content': request.data.get('content', None),
            'deadline': request.data.get('deadline', None),
            'writer': user.pk,
            'lecture':lecture_pk,
        }
        serializer = HomeworkSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            for student in lecture.student_list.all():
                Notification.objects.create(
                    user=User.objects.get(pk=student.pk),
                    notification_type='HC',
                    content=data['title'],
                    from_user=user,
                    lecture=lecture
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=HomeworkDetailSerializer,
                description=swagger_schema.descriptions['HomeworkViewSet']['retrieve'][200],
                examples=swagger_schema.examples['HomeworkViewSet']['homework_detail']
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['HomeworkViewSet']['retrieve']['description'],
        summary=swagger_schema.summaries['HomeworkViewSet']['retrieve'],
        tags=['숙제',],
        examples=[
            basic_swagger_schema.examples[401],
        ],
    )
    def retrieve(self, request, lecture_pk, homework_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        homework = get_object_or_404(Homework, lecture_id=lecture_pk, id=homework_pk)
        serializer = HomeworkDetailSerializer(homework)
        return Response(
            serializer.data,
        )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=HomeworkDetailSerializer,
                description=swagger_schema.descriptions['HomeworkViewSet']['update'][201],
                examples=swagger_schema.examples['HomeworkViewSet']['update'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['HomeworkViewSet']['update']['description'],
        summary=swagger_schema.summaries['HomeworkViewSet']['update'],
        tags=['숙제',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            *swagger_schema.examples['HomeworkViewSet']['create']['request'],
        ]
    )
    def update(self, request, lecture_pk, homework_pk):
        user = decode_JWT(request)
        if user == None or user.status == 'ST':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lecture = get_object_or_404(Lecture, pk=lecture_pk)
        homework = get_object_or_404(Homework, lecture_id=lecture_pk, id=homework_pk)
        data = {
            'title': request.data.get('title', homework.title),
            'content': request.data.get('content', homework.content),
            'deadline': request.data.get('deadline', homework.deadline),
            'writer': request.data.get('writer', user.pk),
            'lecture': lecture_pk,
        }
        serializer = HomeworkSerializer(instance=homework, data=data)
        if serializer.is_valid():
            serializer.save()
            for student in lecture.student_list.all():
                Notification.objects.create(
                    user=User.objects.get(pk=student.pk),
                    notification_type='HU',
                    content=data['title'],
                    from_user=user,
                    lecture=lecture
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=HomeworkDetailSerializer,
                description=swagger_schema.descriptions['HomeworkViewSet']['destroy'][200],
                examples=swagger_schema.examples['HomeworkViewSet']['destroy'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['HomeworkViewSet']['destroy']['description'],
        summary=swagger_schema.summaries['HomeworkViewSet']['destroy'],
        tags=['숙제',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def destroy(self, request, lecture_pk, homework_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        homework = get_object_or_404(Homework, lecture_id=lecture_pk, id=homework_pk)
        homework.delete()
        return Response(
            {'OK': 'No Content'},
            status=status.HTTP_200_OK
        )
