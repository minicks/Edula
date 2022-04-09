from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from accounts.views.user import decode_JWT
from accounts.models import User
from server import basic_swagger_schema
from . import swagger_schema
from ..models import Lecture
from accounts.models import User, Teacher, Student
from ..serializers import LectureSerializer, LectrueDetailSerializer


def verify_user_lecture(user: User, lecture_pk: int) -> bool:
    """유저와 수업의 권한이 있는지 판별

    Parameters
    ----------
    user : User
    lecture_pk : int

    Returns
    -------
    bool
    """
    lecture = Lecture.objects.get(pk=lecture_pk)
    if user.status == 'ST':
        if lecture.student_list.filter(user_id=user.pk).exists():
            return True
    elif user.status == 'TE':
        if lecture.teacher.pk == user.pk:
            return True
    elif user.status == 'SA':
        if lecture.school.pk == user.school_admin.school.pk:
            return True
    return False


class LectureView(APIView):
    """
    수업 목록 & 생성
    """
    model = Lecture
    serializer_class = LectureSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=LectureSerializer,
                description=swagger_schema.descriptions['LectureView']['get'][200],
                examples=swagger_schema.examples['LectureView']['get'][200]
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['LectureView']['get']['description'],
        summary=swagger_schema.summaries['LectureView']['get'],
        tags=['수업',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ],
    )
    def get(self, request):
        """유저가 속한 학교의 모든 수업 조회
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user.status == 'ST':
            school_pk = user.student.school.pk
        elif user.status == 'TE':
            school_pk = user.teacher.school.pk
        elif user.status == 'SA':
            school_pk = user.school_admin.school.pk
        else:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lectures = Lecture.objects.filter(school_id=school_pk)
        serializer = LectureSerializer(lectures, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=LectureSerializer,
                description=swagger_schema.descriptions['LectureView']['post'][201],
                examples=swagger_schema.examples['LectureView']['post'][201]
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401]
        },
        description=swagger_schema.descriptions['LectureView']['post']['description'],
        summary=swagger_schema.summaries['LectureView']['post'],
        tags=['수업', '학교 관리자'],
        examples=[
            swagger_schema.examples['LectureView']['post']['input'],
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401]
        ],
    )
    def post(self, request):
        """수업생성
        학교 관리자 기능
        """
        user = decode_JWT(request)
        if user is None or user.status!= 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        data = {
            'name': request.data.get('name', None),
            'time_list': request.data.get('time_list', None),
            'school': user.school_admin.school.pk,
            'teacher': request.data.get('teacher', None),
            'student_list': request.data.get('student_list', None)
        }
        serializer = LectureSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
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


class LectureDetailView(APIView):
    """
    수업 상세
    """
    model = Lecture
    serializer_class = LectrueDetailSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=LectrueDetailSerializer,
                description=swagger_schema.descriptions['LectureDetailView']['get'][200],
                examples=swagger_schema.examples['LectureDetailView']['get'][200]
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['LectureDetailView']['get']['description'],
        summary=swagger_schema.summaries['LectureDetailView']['get'],
        tags=['수업',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ],
    )
    def get(self, request, lecture_pk):
        """수업 상세 정보 조회

        Parameters
        ----------
        lecture_pk : int
            조회하고자 하는 수업의 pk
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lecture = Lecture.objects.filter(pk=lecture_pk)
        if not lecture:
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif not verify_user_lecture(user, lecture_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = LectrueDetailSerializer(lecture[0])
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=LectrueDetailSerializer,
                description=swagger_schema.descriptions['LectureDetailView']['put'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401]
        },
        description=swagger_schema.descriptions['LectureDetailView']['put']['description'],
        summary=swagger_schema.summaries['LectureDetailView']['put'],
        tags=['수업', '학교 관리자',],
        examples=[
            swagger_schema.examples['LectureDetailView']['put']['input'],
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401]
        ],
    )
    def put(self, request, lecture_pk):
        """수업 정보 수정

        Parameters
        ----------
        lecture_pk : int
            수정하고자 하는 수업의 pk
        """
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lecture = get_object_or_404(Lecture, pk=lecture_pk)
        if user.school_admin.school.pk != lecture.school.pk:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {
            'name': request.data.get('name', lecture.name),
            'time_list': request.data.get('time_list', lecture.time_list),
            'school': user.school_admin.school.pk,
            'teacher': request.data.get('teacher', lecture.teacher),
            'student_list': request.data.get('student_list', lecture.student_list.all())
        }
        serializer = LectureSerializer(instance=lecture, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        responses={
            204: OpenApiResponse(
                response=LectureSerializer,
                description=swagger_schema.descriptions['LectureDetailView']['delete'][204],
                examples=swagger_schema.examples['LectureDetailView']['delete'][204],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404]
        },
        description=swagger_schema.descriptions['LectureDetailView']['delete']['description'],
        summary=swagger_schema.summaries['LectureDetailView']['delete'],
        tags=['수업', '학교 관리자',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404]
        ],
    )
    def delete(self, request, lecture_pk):
        """유저 정보 삭제

        Parameters
        ----------
        lecture_pk : int
            삭제하고자 하는 수업의 pk
        """
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lecture = get_object_or_404(Lecture, pk=lecture_pk)
        if user.school_admin.school.pk != lecture.school.pk:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lecture.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
