from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from re import S
import smtplib

from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db.models import Prefetch, Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import (
    extend_schema, OpenApiResponse
)

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

import serect
from server import basic_swagger_schema
from schools.models import School
from . import swagger_schema
from ..models import FriendRequest, User, Student, Teacher, SchoolAdmin
from ..serializers.user import(
    UserBasicSerializer, UserCUDSerialzier, ResisterSerializer,
    FindUsernameSerializer, PasswordChangeSerializer, PasswordResetSerializer,
    FriendSerializer,
    UserProfileImageSerializer, UserInformationSerializer,
)


def decode_JWT(request) -> User:
    """return User from JWT token 

    decode JWT token userin simpleJWT

    Parameters
    ----------
    requset

    Returns
    -------
    User
    """
    JWT = JWTAuthentication()
    try:
        header = JWT.get_header(request).split()[1]
        validate_token = JWT.get_validated_token(header)
        user = JWT.get_user(validate_token)
        return user
    except:
        return None


def send_email(recipient_email, mail_type, context):
    """Send username or password through email

    get user email and type, which is username or password
    send email with username or password

    Parameters
    ----------
    recipient: str
        email who will receive

    type : str[username | password]
        request type

    context : str
        if type is username, it should be username
        if type is password, it should be password

    returns
    -------
    None
    """
    try:
        if mail_type == 'username':
            title = '회원님의 아이디입니다'
            context = f'''안녕하세요 Edula 입니다.
            아이디 : {context}
            '''
        elif mail_type == 'password':
            title = '회원님의 비밀번호입니다'
            context = f'''안녕하세요, Edula 입니다.
            새로운 비밀번호 : {context}
            '''
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('edula.gugugugugugu@gmail.com', serect.gmail_password)
        message = MIMEMultipart()
        message['Subject'] = title
        message.attach(MIMEText(context))
        server.sendmail(
            "edula.gugugugugugu@gmail.com",
            recipient_email,
            message.as_string()
        )
        return True
    except:
        return False


def create_username(preset: str, length: int=7) -> str:
    """
    Create username function
    """
    username = preset
    random_num = random.choices(
        [str(i) for i in range(10)], k=length-len(preset)
    )
    username += ''.join(random_num)
    return username


def create_password():
    """Make new random password

    make new random password of length 14

    returns
    -------
    str
    """
    base_alpabet = [chr(97 + i) for i in range(26)]
    base_num = [str(i) for i in range(10)]
    base_special_char = ['!', '@', '#', '$']
    new_password = random.choices(base_alpabet, k=8)\
        + random.choices(base_num, k=4)\
        + random.choices(base_special_char, k=2)
    random.shuffle(new_password)
    return ''.join(new_password)


def check_friend_request(friend_requests: FriendRequest, from_user: int, to_user: User):
    if to_user.friend_list.all():
        return 'friend'
    else:
        if friend_requests.filter(from_user=from_user, to_user=to_user):
            return 'requestReveive'
        elif friend_requests.filter(from_user=to_user, to_user=from_user):
            return 'requsetSend'
    return None


class UserView(APIView):
    """About user
    """
    model = User
    serializer_class = UserBasicSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=UserBasicSerializer,
                description=swagger_schema.descriptions['UserView']['get'][200],
                examples=swagger_schema.examples['UserView']['get'][200]
            ),
            401: basic_swagger_schema.open_api_response[401]
        },
        description=swagger_schema.descriptions['UserView']['get']['description'],
        summary=swagger_schema.summaries['UserView']['get'],
        tags=['유저',],
        examples=[
            basic_swagger_schema.examples[401],
        ],
    )
    def get(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserBasicSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserSpecifyingView(APIView):
    """User specifying
    
    search about user's id | username | first_name | status
    """
    model = User
    serializer_class = UserBasicSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=UserBasicSerializer,
                description=swagger_schema.descriptions['UserSpecifyingView']['get'][200],
                examples=swagger_schema.examples['UserSpecifyingView']['get'][200]
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['UserSpecifyingView']['get']['description'],
        summary=swagger_schema.summaries['UserSpecifyingView']['get'],
        tags=['유저',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ],
    )
    def get(self, request, user_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        requset_user = get_object_or_404(User, pk=user_pk)
        serializer = UserBasicSerializer(requset_user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ResisterViewSet(ViewSet):
    """학교 관리자로 회원가입
    """
    model = User
    queryset = User.objects.all()
    serializer_class = ResisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=ResisterSerializer,
                description=swagger_schema.descriptions['ResisterViewSet']['create'][201],
                examples=swagger_schema.examples['ResisterViewSet']['create'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
        },
        description=swagger_schema.descriptions['ResisterViewSet']['create']['description'],
        summary=swagger_schema.summaries['ResisterViewSet']['create'],
        tags=['유저', '학교 관리자',],
        examples=[
            basic_swagger_schema.examples[400],
            *swagger_schema.examples['ResisterViewSet']['request'],
        ]
    )
    def create(self, request):
        school_data = request.data.get('school', None)
        if school_data is None:
            return Response(
                {'error': 'school'},
                status=status.HTTP_400_BAD_REQUEST
            )
        abbreviation = school_data.get('abbreviation', None)
        if abbreviation is None:
            return Response(
                {'error': 'abbreviation not exist'},
                status.HTTP_400_BAD_REQUEST
            )
        elif len(abbreviation) < 3 or len(abbreviation) > 5:
            return Response(
                {'error': 'abbreviation length'},
                status=status.HTTP_400_BAD_REQUEST
            )
        school, create = School.objects.get_or_create(
            abbreviation=school_data.get('abbreviation', None)
        )
        if not create:
            return Response(
                {'error': 'abbreviation'}
            )
        school.name = school_data.get('name', None)
        school.save()
        username = f'{school.abbreviation}00000'
        
        first_name = request.data.get('first_name', None)
        password = request.data.get('password', None)
        user = User.objects.create(
            username=username,
            first_name=first_name,
            password=make_password(password),
            status='SA'
        )
        school_admin = SchoolAdmin.objects.create(
            user=user,
            school=school,
        )
        serializer = ResisterSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class UserCUDView(ViewSet):
    """User create / update / delete view
    use user UserView or UserSpecifyingView if you want read user
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserCUDSerialzier
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=UserCUDSerialzier,
                description=swagger_schema.descriptions['UserCUDView']['post'][201],
                examples=[
                    swagger_schema.examples['UserCUDView']['post'][201]
                ]
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['UserCUDView']['post']['description'],
        summary=swagger_schema.summaries['UserCUDView']['post'],
        tags=['학교 관리자',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['UserCUDView']['post']['input'],
        ],
    )
    def create(self, request):
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        school_pk = user.school_admin.school.pk
        abbreviation = user.school_admin.school.abbreviation
        account_type = user.school_admin.account_type

        max_creation = 10
        if account_type == 'B':
            max_creation = 50
        elif account_type == 'E':
            max_creation = 10_000
        accounts_count = Student.objects.filter(school_id=school_pk).count()\
            + Teacher.objects.filter(school_id=school_pk).count()
        accounts_available = max(max_creation - accounts_count, 0)

        student_creation_count_list = request.data.get('student_creation_count_list',None)
        
        if isinstance(student_creation_count_list, dict): 
            for year, count in student_creation_count_list.items():
                if count > accounts_available:
                    student_creation_count_list[year] = accounts_available
                    accounts_available = 0
                else:
                    accounts_available -= count

            students = []
            for year in student_creation_count_list.keys():
                try:
                    abb_num = (int(year) % 6) + 1
                    student_list = Student.objects.select_related('user')\
                        .filter(school_id=school_pk,user__username__startswith=abbreviation+str(abb_num))\
                        .order_by('-pk').values('user__username')
                    if student_list.exists():
                        last_student = student_list[0]['user__username']
                        start_num = int(last_student[len(abbreviation) + 1:]) + 1
                    else:
                        start_num = 0
                    students += [
                        {'username': abbreviation + str(abb_num) + str(i).zfill(4), 'password': create_password()}
                        for i in range(
                            start_num, start_num + student_creation_count_list[year]
                        )
                    ]
                except:
                    pass
        else:
            students = []
            
        teacher_creation_count = request.data.get('teacher_creation_count',None)    
        
        if isinstance(teacher_creation_count,int):
            if teacher_creation_count > accounts_available:
                teacher_creation_count = accounts_available
            
            teacher_list = Teacher.objects.select_related('user')\
                .filter(school_id=school_pk,user__username__startswith=abbreviation + str(0))\
                .order_by('-pk').values('user__username')
            if teacher_list.exists():
                last_student = teacher_list[0]['user__username']
                start_num = int(last_student[len(abbreviation) + 1:]) + 1
            else:
                start_num = 1
            teachers = [
                {'username': abbreviation + str(0) + str(i).zfill(4), 'password': create_password()}
                for i in range(
                    start_num, start_num + teacher_creation_count
                )
            ]
        else:
            teachers = []

        data = {
            'students': students,
            'teachers': teachers,
        }
        for student in students:
            info = {
                'username': student['username'],
                'password': make_password(student['password']),
                'status': 'ST'
            }
            serializer = UserCUDSerialzier(data=info)
            if serializer.is_valid():
                serializer.save()
                Student(user_id=serializer.data['id'],school_id=school_pk).save()
        for teacher in teachers:
            info = {
                'username': teacher['username'],
                'password': make_password(teacher['password']),
                'status': 'TE'
            }
            serializer = UserCUDSerialzier(data=info)
            if serializer.is_valid():
                serializer.save()
                Teacher(user_id=serializer.data['id'],school_id=school_pk).save()
        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=UserCUDSerialzier,
                description=swagger_schema.descriptions['UserCUDView']['delete'][200],
                examples=swagger_schema.examples['UserCUDView']['delete'][200],
            ),
            204: OpenApiResponse(
                description=swagger_schema.descriptions['UserCUDView']['delete'][204],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404]
        },
        description=swagger_schema.descriptions['UserCUDView']['delete']['description'],
        summary=swagger_schema.summaries['UserCUDView']['delete'],
        tags=['학교 관리자',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404]
        ],
    )
    def destroy(self, request,YS,num):
        """Delete lecture information
        
        Delete lecture information
        """
        user = decode_JWT(request)
        if user == None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if YS == "S":
            student = get_object_or_404(User,pk=num)
            student.delete()
        elif YS == "Y":
            abb_num = (int(num) % 6) + 1
            abbreviation = user.school_admin.school.abbreviation
            User.objects.filter(username__startswith=abbreviation+str(abb_num)).delete()
        else:
            return Response(
                    {'error': 'wrong information'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        tags=['학교 관리자',],
        examples=[
            *swagger_schema.examples['UserCUDView']['request_update']
        ]
    )
    def update(self, request):
        user = decode_JWT(request)
        if user is None or user.status != 'SA':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        target_user = get_object_or_404(
            User, pk=request.data.get('user', None)
        )
        data = {
            'first_name': request.data.get('first_name', target_user.first_name),
            'email': request.data.get('email', target_user.email),
            'phone': request.data.get('phone', target_user.phone),
        }
        serializer = UserInformationSerializer(target_user, data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FindUsernameView(APIView):
    """Find username
    
    """
    model = User
    serializer_class = FindUsernameSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=FindUsernameSerializer,
                description=swagger_schema.descriptions['FindUsernameView']['post'][200],
                examples=[
                    swagger_schema.examples['FindUsernameView']['post'][200]
                ]
            ),
            401: basic_swagger_schema.open_api_response[400],
            404: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['FindUsernameView']['post']['description'],
        summary=swagger_schema.summaries['FindUsernameView']['post'],
        tags=['유저',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            swagger_schema.examples['FindUsernameView']['post']['request'],
        ],
    )
    def post(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {
            'id': user.pk,
            'first_name': request.data.get('first_name'),
            'email': request.data.get('email'),
        }
        serializer = FindUsernameSerializer(data=data)
        if not serializer.is_valid()\
            or data['email'] != user.email\
            or data['first_name'] != user.first_name:
                return Response(
                    {'error': 'wrong information'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif send_email(data['email'], 'username', user.username):
            return Response(
                {'success': 'email send'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'email send failure'},
                status=status.HTTP_400_BAD_REQUEST
            )    


class PasswordChangeView(APIView):
    """Password change
    
    password chang from old password to new password
    """
    model = User
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=PasswordChangeSerializer,
                description=swagger_schema.descriptions['PasswordChangeView']['put'][201],
            ),
            401: basic_swagger_schema.open_api_response[400],
            404: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['PasswordChangeView']['put']['description'],
        summary=swagger_schema.summaries['PasswordChangeView']['put'],
        tags=['유저',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
        ],
    )
    def put(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password_confirmation = data.get('new_password_confirmation')
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'wrong password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = PasswordChangeSerializer(
                data={
                    'old_password': old_password,
                    'new_password': new_password,
                    'new_password_confirmation': new_password_confirmation,
                }
            )
            if new_password != new_password_confirmation:
                return Response(
                    {'error': 'check new password and new password confirmaion'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif serializer.is_valid():
                user.set_password(new_password)
                user.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


class PasswordResetView(APIView):
    """Reset user password
    
    """
    model = User
    serializer_class = PasswordResetSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=PasswordResetSerializer,
                description=swagger_schema.descriptions['PasswordResetView']['put'][201],
            ),
            401: basic_swagger_schema.open_api_response[400],
            404: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['PasswordResetView']['put']['description'],
        summary=swagger_schema.summaries['PasswordResetView']['put'],
        tags=['유저',],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
        ],
    )
    def put(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {
            'id': user.pk,
            'username': request.data.get('username'),
            'email': request.data.get('email'),
        }
        new_password = create_password()
        serializer = PasswordResetSerializer(data=data)
        if not serializer.is_valid()\
            or data['username'] != user.username\
            or data['email'] != user.email:
            return Response(
                {'error': 'wrong information'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif send_email(data['email'], 'password', new_password):
            user.set_password(new_password)
            user.save()
            return Response(
                {'success': 'email send'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'email send failure'},
                status=status.HTTP_400_BAD_REQUEST
            )


class FriendViewSet(ViewSet):
    """About user friends list   
    """
    model = User
    queryset = User.objects.all()
    serializer_class = FriendSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=FriendSerializer,
                description=swagger_schema.descriptions['FriendViewSet']['list'][200],
                examples=swagger_schema.examples['FriendViewSet']['list'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['FriendViewSet']['list']['description'],
        summary=swagger_schema.summaries['FriendViewSet']['list'],
        tags=['친구',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ],
    )
    def list(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        friends = get_list_or_404(user.friend_list)
        serializer = FriendSerializer(friends, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=FriendSerializer,
                description=swagger_schema.descriptions['FriendViewSet']['destroy'][200],
                examples=swagger_schema.examples['FriendViewSet']['destroy'][200],
            ),
            204: OpenApiResponse(
                description=swagger_schema.descriptions['FriendViewSet']['destroy'][204],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['FriendViewSet']['destroy']['description'],
        summary=swagger_schema.summaries['FriendViewSet']['destroy'],
        tags=['친구',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def destroy(self, request, friend_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        friend = get_object_or_404(user.friend_list, pk=friend_pk)
        user.friend_list.remove(friend)
        friends = user.friend_list.all()
        if friends:
            serializer = FriendSerializer(friends, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class FriendSearchViewSet(ViewSet):
    """
    Friend search viewset
    """
    model = User
    queryset = User.objects.all()
    serializer_class = FriendSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=FriendSerializer,
                description=swagger_schema.descriptions['FriendSearchViewSet']['list']['description'],
                examples=swagger_schema.examples['FriendSearchViewSet']['list'][200]
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['FriendSearchViewSet']['list']['description'],
        summary=swagger_schema.summaries['FriendSearchViewSet']['list'],
        tags=['친구',],
        examples=[
            basic_swagger_schema.examples[401],
        ]
    )
    def list(self, request, search):
        """
        Search user
        - 같은 학교 학생 + 교사 검색
        - 한글 완성형일때만 검색됨
        """
        user = decode_JWT(request)
        if user == None:
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
        students = User.objects.filter(first_name__contains=search, status='ST')\
                .prefetch_related(
                    Prefetch('student', queryset=Student.objects.filter(school_id=school_pk)),
                    Prefetch('friend_list', queryset=User.objects.filter(id=user.pk)))
        teachers = User.objects.filter(first_name__contains=search, status='TE')\
                .prefetch_related(
                    Prefetch('teacher', queryset=Teacher.objects.filter(school_id=school_pk)),
                    Prefetch('friend_list', queryset=User.objects.filter(id=user.pk)))
        friend_requests = FriendRequest.objects.filter(Q(from_user=user.pk)|Q(to_user=user.pk))
        data = {
            'students': [
                {
                    'id': student.pk,
                    'username': student.username,
                    'first_name': student.first_name,
                    'friend_request': check_friend_request(friend_requests, user.pk, student),
                } for student in students if student.pk != user.pk
            ],
            'teachers': [
                {
                    'id': teacher.pk,
                    'username': teacher.username,
                    'first_name': teacher.first_name,
                    'friend_request': check_friend_request(friend_requests, user.pk, teacher),
                } for teacher in teachers if teacher.pk != user.pk
            ]
        }
        data['student_count'] = len(data['students'])
        data['teacher_count'] = len(data['teachers'])
        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class UserProfileImageView(APIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserProfileImageSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    @extend_schema(
        tags=['유저',]
    )
    def post(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {'profile_image': request.FILES.get('profile_image')}
        serializer = UserProfileImageSerializer(user, data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
