from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from accounts.views.user import decode_JWT
from accounts.models import User, Teacher, Student
from server import basic_swagger_schema
from . import swagger_schema
from .school import school_validation
from ..models import School, Classroom
from ..serializers import ClassroomSerializer, ClassroomDetailSerializer


def verify_user_school(user: User, school_pk: int) -> bool:
    """유저가 학교에 권한이 있는지 확인합니다

    Parameters
    ----------
    user : User
    school_pk : int

    Returns
    -------
    bool
    """
    if user.status == 'ST':
        if user.student.school.pk == school_pk:
            return True
    elif user.status == 'TE':
        if user.teacher.school.pk == school_pk:
            return True
    elif user.status == 'SA':
        if user.school_admin.school.pk == school_pk:
            return True
    return False


class ClassroomViewSet(ViewSet):
    """Classroom View Set
    """
    model = Classroom
    serializer_classes = {
        'list': ClassroomSerializer,
        'create': ClassroomSerializer,
        'retrieve': ClassroomDetailSerializer,
        'update': ClassroomSerializer,
        'destroy': ClassroomSerializer,
    }
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except:
            return ClassroomSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=ClassroomSerializer,
                description=swagger_schema.descriptions['ClassroomViewSet']['list'][200],
            ),
            401: basic_swagger_schema.open_api_response[401]
        },
        description=swagger_schema.descriptions['ClassroomViewSet']['list']['description'],
        summary=swagger_schema.summaries['ClassroomViewSet']['list'],
        tags=['교실',],
        examples=[
            basic_swagger_schema.examples[401],
            *swagger_schema.examples['ClassroomViewSet']['classroom_list'],
        ],
    )
    def list(self, request, school_pk):
        """school_pk의 모든 교실 조회

        Parameters
        ----------
        school_pk : int
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not School.objects.filter(pk=school_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not verify_user_school(user, school_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        classrooms = Classroom.objects.filter(school_id=school_pk)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=ClassroomSerializer,
                description=swagger_schema.descriptions['ClassroomViewSet']['create'][201],
                examples=swagger_schema.examples['ClassroomViewSet']['classroom_output'],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401]
        },
        description=swagger_schema.descriptions['ClassroomViewSet']['create']['description'],
        summary=swagger_schema.summaries['ClassroomViewSet']['create'],
        tags=['교실', '학교 관리자',],
        examples=[
            *swagger_schema.examples['ClassroomViewSet']['request'],
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401]
        ],
    )
    def create(self, request, school_pk):
        """교실 생성

        Parameters
        ----------
        request : int
        """
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not School.objects.filter(pk=school_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not verify_user_school(user, school_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {
            'class_grade': request.data.get('class_grade', None),
            'class_num': request.data.get('class_num', None),
            'school': school_pk,
            'teacher': request.data.get('teacher', None),
            'student_list': request.data.get('student_list', None),
        }
        serializer = ClassroomSerializer(data=data)
        if serializer.is_valid():
            class_grade, class_num = data['class_grade'], data['class_num']
            if (
                    Classroom.objects.filter(
                        school=school_pk,
                        class_grade=class_grade,
                        class_num=class_num
                    ).exists()
                ):
                return Response(
                    {'error': 'Bad Request'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'error': 'Bad Request'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=ClassroomDetailSerializer,
                description=swagger_schema.descriptions['ClassroomViewSet']['retrieve'][200],
                examples=swagger_schema.examples['ClassroomViewSet']['classroom_detail'],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ClassroomViewSet']['retrieve']['description'],
        summary=swagger_schema.summaries['ClassroomViewSet']['retrieve'],
        tags=['교실',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ],
    )
    def retrieve(self, request, school_pk, classroom_pk):
        """수업 상세 조회

        Parameters
        ----------
        school_pk : int
        classroom_pk : int
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        classroom = get_object_or_404(
            Classroom,
            pk=classroom_pk, school_id=school_pk,
        )
        if not verify_user_school(user, school_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ClassroomDetailSerializer(classroom)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=ClassroomSerializer,
                description=swagger_schema.descriptions['ClassroomViewSet']['update'][201],
                examples=swagger_schema.examples['ClassroomViewSet']['classroom_detail'],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ClassroomViewSet']['update']['description'],
        summary=swagger_schema.summaries['ClassroomViewSet']['update'],
        tags=['교실',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            *swagger_schema.examples['ClassroomViewSet']['request'],
        ]
    )
    def update(self, request, school_pk, classroom_pk):
        """[summary]

        Parameters
        ----------
        school_pk : int
        classroom_pk : int
        """
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not verify_user_school(user, school_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        classroom = get_object_or_404(
            Classroom,
            pk=classroom_pk, school_id=school_pk
        )
        data = {
            'class_grade': request.data.get('class_grade', classroom.class_grade),
            'class_num': request.data.get('class_num', classroom.class_num),
            'school': school_pk,
            'teacher_pk': request.data.get(
                'teacher',
                classroom.get_teacher().pk
            ),
            'student_pk_list': request.data.get(
                'student_list',
                classroom.student_list.all()
            ),
        }
        if (
            not school_validation(school_pk, data['teacher_pk']) or
            not school_validation(school_pk, data['student_pk_list'], many=True)
        ):
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClassroomDetailSerializer(instance=classroom, data=data)
        if serializer.is_valid():
            class_grade_before, class_num_before = classroom.class_grade, classroom.class_num
            class_grade_after, class_num_after = data['class_grade'], data['class_num']
            if (
                    not (class_grade_before == class_grade_after and
                        class_num_before == class_num_after) and
                    Classroom.objects.filter(
                        school=school_pk,
                        class_grade=class_grade_after,
                        class_num=class_num_after
                    ).exists()
                ):
                return Response(
                    {'error': 'Bad Request'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=ClassroomSerializer,
                description=swagger_schema.descriptions['ClassroomViewSet']['destroy'][200],
                examples=swagger_schema.examples['ClassroomViewSet']['classroom_list'],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ClassroomViewSet']['destroy']['description'],
        summary=swagger_schema.summaries['ClassroomViewSet']['destroy'],
        tags=['교실',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def destroy(self, request, school_pk, classroom_pk):
        """교실을 삭제합니다

        Parameters
        ----------
        school_pk : int
        classroom_pk : int
        """
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        classroom = get_object_or_404(
            Classroom,
            pk=classroom_pk, school_id=school_pk
        )
        if not verify_user_school(user, school_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        classroom.delete()
        classrooms = Classroom.objects.filter(school=school_pk)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
