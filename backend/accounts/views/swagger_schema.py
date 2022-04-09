from drf_spectacular.utils import (
    OpenApiExample, inline_serializer
)
from rest_framework import serializers


schema_serializers = {
    'FriendRequestViewSet': {
        'request_list': inline_serializer(
                name='RequestList',
                fields={
                    'request_send': serializers.ListField(),
                    'request_reveive': serializers.ListField(),
                },
        ),
        'create': {
            'request': inline_serializer(
                name='CreateRequest',
                fields={
                    'to_user': serializers.IntegerField(),
                },
            ),
        },
        'update': {
            'request': inline_serializer(
                name='UpdateRequest',
                fields={
                    'request_status': serializers.CharField(),
                },
            ),
        },
    },
}

descriptions = {
    'UserView': {
        'get': {
            'description': 
    '''
    Decode JWT token, return user infromation
from JWT, return primary key of user and user's satatus
    ''',
            200: 
    '''
    Successfully get user information
successfully get user information from JWT token
    ''',
        },
    },
    'UserSpecifyingView': {
        'get': {
            'description': 
    '''
    Get User's id, username and status
User's id is same with user_pk
    ''',
            200: 
    '''
    Successfully get user
    ''',
        },
    },
    'FindUsernameView': {
        'post': {
            'description':
    '''
    Get username through email
input with first_name(user name) and email
    ''',
            200:
    '''
    Successfully get username through email
    ''',
        },
    },
    'PasswordChangeView': {
        'put': {
            'description': 
    '''
    Change one's own self password
only one's own self password could be chagned
    ''',
            201: 
    '''
    Successfully password changed
    ''',
        },
    },
    'PasswordResetView': {
        'put': {
            'description':
    '''
    Reset one's own self password, get through email
only one'w own slef password could be reset
and get reset password through email
    ''',
            201:
    '''
    Successfully reset password and send email
successfully reset password, and set as password
reset password send through email
    ''',
        },
    },
    'FriendViewSet': {
        'list' : {
            'description':
    '''
    친구 목록을 받습니다
    ''',
            200:
    '''
    유저의 친구 목록을 받았습니다
유저의 친구목록을 받았고, 각 친구의 id, username, firstName, status를 받습니다\n
친구가 없으면 404를 받습니다
    ''',
        },
        'destroy': {
            'description':
    '''
    친구를 삭제합니다
성공적으로 삭제 후 친구 리스트를 200번으로 반환합니다\n
만약 친구 삭제 후 친구가 남아있지 않으면 204를 반환합니다\n
해당 유저가 friend_pk에 해당하는 유저를 친구로 두지 않은 경우 404를 반환합니다
    ''',
            200:
    '''
    성공적으로 친구 삭제 후 친구 목록을 반환합니다
    ''',
            204:
    '''
    성공적으로 친구 삭제 후 남은 친구가 없습니다
    ''',
        }
    },
    'StudentView': {
        'get': {
            'description':
    '''
    Get student information
student information using student_pk
    ''',
            200:
    '''
    Successfully get student information
    ''',
        },
        'put': {
            'description':
    '''
    Update student's own self information
email, phone, guardian phone could be updated
    ''',
            201:
    '''
    Successfully update student information
and get updated information
    ''',
        },
    },
    'StudentLectureView': {
        'get': {
            'description':
    '''
    Get student's lecture lists
    ''',
            200:
    '''
    Successfully get student's lecture list
    ''',
        },
    },
    'TeacherView': {
        'get': {
            'description':
    '''
    Get teacher information
teacher information using teacher_pk
    ''',
        200 : 
    '''
    Successfully get teacher information
    ''',
        },
        'put': {
            'description':
    '''
    Update teacher's own self information
email and phone could be updated
    ''',
            201:
    '''
    Successfully update teacher information
and get updated information
    ''',
        },
    },
    'TeacherLectureView': {
        'get': {
            'description':
    '''
    Get teacher lecture list
    ''',
            200:
    '''
    Successfully get teacher lecture list
    ''',
        }
    },
    'SchoolAdminView': {
        'get': {
            'description':
    '''
    학교 관리자 정보를 조회합니다
accountType에따라 생성 가능한 유저의수가 달라집니다
- F(free) : 10명
- B(Basic) : 50명
- E(Every) : 10,000명
    ''',
        200 : 
    '''
    Successfully get school admin information
    ''',
        },
        'put': {
            'description':
    '''
    Update school admin's own self information
email and phone could be updated
    ''',
            201:
    '''
    Successfully update school admin information
and get updated information
    ''',
        },
    },
    'FriendRequestViewSet': {
        'list': {
            'description':
    '''
    보낸 친구 신청 목록과 받은 친구 신청 목록을 표시합니다
보낸 친구 신청 목록과 받은 친구 신청 목록에 대하여 유저의 간략한 정보와 함께 requestStatus를 제공합니다\n
requestStatus는 RQ일때 친구 신청, RF일때 신청에 대한 거절, AC일때 신청에 대한 승인입니다\n
(RQ=Request, RF=Refusal, AC=Accept)
    ''',
            200:
    '''
    받은/보낸 친구 신청 목록을 성공적으로 받았습니다
    ''',
        },
        'create': {
            'description':
    '''
    친구 신청을 생성합니다
친구 신청을 원하는 유저의 id(friend_pk)를 입력으로 받습니다\n
이미 신청을 한 경우(RQ) 추가적으로 신청되지 않고 400을 반환합니다\n
또한 올바르지 않은 데이터인 경우 400을 반환할 수 있습니다\n
해당 유저를 찾을 수 없으면 404를 반환합니다\n
신청이 완료되었으면, 전체 신청 결과를 반환합니다
    ''',
            201:
    '''
    친구신청이 완료되었고, 전체 신청 리스트를 반환합니다
    ''',
        },
        'update': {
            'description':
    '''
    받은 친구 신청을 승인 또는 거절
받은 친구 신청을 승인 또는 거절합니다\n
승인하면 친구 신청의 fromUser와 toUser가 친구가됩니다\n
성공적으로 승인 또는 거절이 처리되면 200을 반환합니다\n
requset_pk에 해당하는 요청을 받은 유저가 아니라면 404를 반환합니다\n
잘못된 데이터가 있으면 400을 반환할 수 있습니다
    ''',
            200:
    '''
    성공적으로 친구 신청 승인/거절 되었습니다
    ''',
        },
        'destroy': {
            'description':
    '''
    보낸 친구 신청을 삭제(취소)합니다
기존 보낸 친구 신청을 삭제하고, 전체 보낸/받은 친구 신청 리스트를 반환합니다\n
request_pk에 해당하는 신청이 존재하지 않거나, 해당 유저가 보낸 요청이 아닌경우 404를 반환합니다
    ''',
            200:
    '''
    친구 신청을 삭제하고 친구 목록을 반환합니다
    ''',
        },
    },
    'FriendSearchViewSet': {
        'list': {
            'description':
    '''
    친구 검색을 합니다
search parameter를 통하여 친구 검색을 합니다\n
한글 완성형이 아니면 검색이 되지 않을 수 있습니다\n
같은 학교의 학생과 교사의 이름을 검색합니다\n
friendRequest는 해당 유저와 친구 상태에 따라 값이 결정됩니다
- friend: 이미 친구인 경우
- requestSend: 내가 친구 요청을 보낸 유저인 경우
- requestReveive : 내가 친구 요청을 받은 유저인 경우
- null : 아무런 관계가 없는 경우
    ''',
            200:
    '''
    학교의 학생, 교사를 조회했습니다
    ''',
        },
    },
    'UserCUDView': {
        'post': {
            'description': 
    '''
    학생 및 선생 생성
학생 및 선생의 수를 입력 받고 생성합니다.\n
학교 관리자만 생성이 가능합니다.\n
입력의 경우
- 학생 : 입학 연도와 학생 수를 dict로 입력
- 선생 : 선생 수만 입력

다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우

    ''',
            201: 
    '''
    학생 및 선생이 생성되었습니다.
해당 수 만큼 학생과 선생을 생성
    ''',
        },
        'delete': {
            'description':
    '''
    학생을 삭제합니다
특정 학생 한명을 삭제하거나 한 연도의 학생 모두를 삭제합니다.
학생이 없으면 204를 반환합니다\n
YS : 연도(Y)와 학생(S) 구분(대문자 하나 입력)\n
num : 연도일 경우 입학 4자리 연도, 학생일 경우 학생 pk
    ''',
            200:
    '''
    학년의 학생들을 삭제 완료하였습니다
    ''',
            204:
    '''
    학년의 학생이 없습니다
    ''',
        },
    },
    'ResisterViewSet': {
        'create': {
            'description':
    '''
    학교 관리자로 회원가입
다음의 경우 400을 반환하고, 각 값에 대한 설명입니다
- school : 학교와 관련한 입력값이 없는 경우
- abbreviation not exist : 학교 약어가 없는 경우
- abbreviation length : 학교 약어 길이가 3~5자가 아닌 경우
- abbreviation : 이미 사용되는 약어인 경우
    ''',
            201:
    '''
    학교 관리자 계정을 생성했습니다
accountType은 기본적으로 F(free)로 생성됩니다
    ''',
        }
    },
}

summaries = {
    'UserView': {
        'get': 'do it after login(get JWT token)',
    },
    'UserSpecifyingView': {
        'get': 'specify user using user_pk'
    },
    'FindUsernameView': {
        'post': 'get username through email',
    },
    'PasswordChangeView': {
        'put': 'one\'s own self password change',
    },
    'PasswordResetView': {
        'put': 'get reset password through email',
    },
    'FriendViewSet': {
        'list': '친구 목록',
        'destroy': '친구 삭제',
    },
    'StudentView': {
        'get': 'get studnet information',
        'put': 'update student information',
    },
    'StudentLectureView': {
        'get': 'get student lecture list'
    },
    'TeacherView': {
        'get': 'get teacher information',
        'put': 'update teacher information',
    },
    'TeacherLectureView':
    {
        'get': 'get teacher lecture list'
    },
    'SchoolAdminView': {
        'get': 'get school admin information',
        'put': 'update school admin information',
    },
    'FriendRequestViewSet':{
        'list': '친구 신청 목록',
        'create': '친구 신청 생성',
        'update': '친구 신청 승인/거절',
        'destroy': '보낸 친구 신청 취소',
    },
    'UserCUDView': {
        'post': '학생 및 선생 생성',
        'delete': '학생 삭제',
    },
    'FriendSearchViewSet': {
        'list': '친구 찾기',
    },
    'ResisterViewSet': {
        'create': '학교 관리자 회원가입'
    }
}

examples = {
    'UserView': {
        'get': {
            200: [
                OpenApiExample(
                    name='student',
                    value={
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'ST',
                    },
                ),
                OpenApiExample(
                    name='teacher',
                    value={
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'TE',
                    },
                ),
                OpenApiExample(
                    name='school admin',
                    value={
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'SA',
                    },
                ),
            ],
        },
    },
    'UserSpecifyingView': {
        'get': {
            200: [
                OpenApiExample(
                    name='student',
                    value={
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'ST',
                    },
                ),
                OpenApiExample(
                    name='teacher',
                    value={
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'TE',
                    },
                ),
                OpenApiExample(
                    name='school admin',
                    value={
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'SA',
                    },
                ),
            ],
        }
    },
    'FindUsernameView': {
        'post': {
            'request': OpenApiExample(
                name='request',
                value={
                    'firstName': '김싸피',
                    'email': 'ssafy@example.com'
                },
                request_only=True,
            ),
            200: OpenApiExample(
                name='user information',
                value={
                    'id': 0,
                    'firstName': '김싸피',
                    'email': 'ssafy@example.com',
                },
                status_codes=['200'],
                response_only=True,
            ),
        },
    },
    'FriendViewSet': {
        'list': {
            200: [
                OpenApiExample(
                    name='friends',
                    value=[
                        {
                            'id': 0,
                            'username': 'ssafy0001',
                            'firstName': '김싸피',
                            'status': 'ST',
                        },
                        {
                            'id': 2,
                            'username': 'ssafy0005',
                            'firstName': '이싸피',
                            'status': 'ST',
                        },
                    ],
                    status_codes=['200'],
                    response_only=True,
                ),
            ],
        },
        'destroy': {
            200: [
                OpenApiExample(
                    name='friends',
                    value=[
                        {
                            'id': 0,
                            'username': 'ssafy0001',
                            'firstName': '김싸피',
                            'status': 'ST',
                        },
                        {
                            'id': 2,
                            'username': 'ssafy0005',
                            'firstName': '이싸피',
                            'status': 'ST',
                        },
                    ],
                    status_codes=['200'],
                    response_only=True,
                ),
            ],
        },
    },
    'StudentView': {
        'get': {
            200: OpenApiExample(
                name='student',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'email': 'ssafy@example.com',
                        'phone': '999-9999-9999',
                        'status': 'ST',
                    },
                    'classroom': {
                        'id': 0,
                        'classGrage': 1,
                        'calssNum': 3,
                    },
                    'school': {
                        'id': 0,
                        'name': '싸피 초등학교',
                    },
                    'guardianPhone': '999-9999-9990',
                },
                status_codes=['200'],
                response_only=True,
            ),
        },
        'put': {
            'request': OpenApiExample(
                name='request',
                value={
                    'user': {
                        'email': 'new-ssafy@example.com',
                        'phone': '998-9999-9999',
                    },
                    'guardianPhone': '998-9999-9990',
                },
                request_only=True,
            ),
            201: OpenApiExample(
                name='student',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'email': 'new-ssafy@example.com',
                        'phone': '998-9999-9999',
                        'status': 'ST',
                    },
                    'classroom': {
                        'id': 0,
                        'classGrage': 1,
                        'calssNum': 3,
                    },
                    'school': {
                        'id': 0,
                        'name': '싸피 초등학교',
                    },
                    'guardianPhone': '998-9999-9990',
                },
                status_codes=['201'],
                response_only=True,
            ),
        },
    },
    'StudentLectureView': {
        'get': {
            200: OpenApiExample(
                name='student',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'ST',
                    },
                    'lectureList': [
                        {
                            'id': 1,
                            'name': 'math',
                            'timeList': {
                                
                            },
                            'school': 1,
                            'teacher': 1,
                            'studentList': [
                                1,
                                2,
                                3
                            ]
                        }
                    ],
                },
                status_codes=['200'],
                response_only=True,
            ),
        }
    },
    'TeacherView': {
        'get': {
            200: OpenApiExample(
                name='teacher',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'email': 'ssafy@example.com',
                        'phone': '999-9999-9999',
                        'status': 'TE',
                    },
                    'classroom': {
                        'id': 0,
                        'classGrage': 1,
                        'calssNum': 3,
                    },
                    'school': {
                        'id': 0,
                        'name': '싸피 초등학교',
                    },
                },
                status_codes=['200'],
                response_only=True,
            ),
        },
        'put': {
            'request': OpenApiExample(
                name='request',
                value={
                    'user': {
                        'email': 'new-ssafy@example.com',
                        'phone': '998-9999-9999',
                    },
                },
                request_only=True,
            ),
            201: OpenApiExample(
                name='teacher',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'email': 'new-ssafy@example.com',
                        'phone': '998-9999-9999',
                        'status': 'TE',
                    },
                    'classroom': {
                        'id': 0,
                        'classGrage': 1,
                        'calssNum': 3,
                    },
                    'school': {
                        'id': 0,
                        'name': '싸피 초등학교',
                    },
                },
                status_codes=['201'],
                response_only=True,
            ),
        },
    },
    'TeacherLectureView': {
        'get': {
            200: OpenApiExample(
                name='teacher',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'status': 'TE',
                    },
                    'lectureList': [
                        {
                            'id': 1,
                            'name': 'math',
                            'timeList': {
                                
                            },
                            'school': 1,
                            'teacher': 1,
                            'studentList': [
                                1,
                                2,
                                3
                            ]
                        }
                    ],
                },
                status_codes=['200'],
                response_only=True,
            ),
        }
    },
    'SchoolAdminView': {
        'get': {
            200: OpenApiExample(
                name='school admin',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'email': 'ssafy@example.com',
                        'phone': '999-9999-9999',
                        'status': 'SA',
                    },
                    'classroom': {
                        'id': 0,
                        'classGrage': 1,
                        'calssNum': 3,
                    },
                    'school': {
                        'id': 0,
                        'name': '싸피 초등학교',
                    },
                    'accountType': 'F'
                },
                status_codes=['200'],
                response_only=True,
            ),
        },
        'put': {
            'request': OpenApiExample(
                name='request',
                value={
                    'user': {
                        'email': 'new-ssafy@example.com',
                        'phone': '998-9999-9999',
                    },
                },
                request_only=True,
            ),
            201: OpenApiExample(
                name='school admin',
                value={
                    'user': {
                        'id': 0,
                        'username': 'ssafy1234',
                        'firstName': '김싸피',
                        'email': 'new-ssafy@example.com',
                        'phone': '998-9999-9999',
                        'status': 'TE',
                    },
                    'classroom': {
                        'id': 0,
                        'classGrage': 1,
                        'calssNum': 3,
                    },
                    'school': {
                        'id': 0,
                        'name': '싸피 초등학교',
                    },
                },
                status_codes=['201'],
                response_only=True,
            ),
        },
    },
    'FriendRequestViewSet': {
        'request_list': OpenApiExample(
            name='request list',
            value={
                'requestSend': [
                    {
                        'id': 5,
                        'fromUser': {
                            'id': 2,
                            'username': 'ssafy0001',
                            'firstName': '김싸피',
                            'status': 'ST',
                        },
                        'toUser': {
                            'id': 1,
                            'username': 'ssafy0006',
                            'firstName': '이싸피',
                            'status': 'St',
                        },
                        'requestStatus': 'RQ',
                    },
                ],
                'requestReveive': [
                    {
                        'id': 6,
                        'fromUser': {
                            'id': 5,
                            'username': 'ssafy0009',
                            'firstName': '박싸피',
                            'status': 'St',
                        },
                        'toUser': {
                            'id': 2,
                            'username': 'ssafy0001',
                            'firstName': '김싸피',
                            'status': 'ST',
                        },
                        'requestStatus': 'RF',
                    },
                ],
            },
            status_codes=['200', '201'],
            response_only=True
        ),
        'create': {
            'request': OpenApiExample(
                name='create friend request',
                value={
                    'toUser': 1,
                },
                request_only=True,
            ),
        },
        'update': {
            'request': [
                OpenApiExample(
                    name='accept',
                    value={
                        'requestStatus': 'AC'
                    },
                    request_only=True,
                ),
                OpenApiExample(
                    name='refusal',
                    value={
                        'requestStatus': 'RF'
                    }
                )
            ],
            200: [
                OpenApiExample(
                    name='accept',
                    value={
                        'id': 1,
                        'fromUser': 1,
                        'toUser': 2,
                        'requestStatus': 'AC',
                    },
                    status_codes=['200'],
                    response_only=True,
                ),
                OpenApiExample(
                    name='refusal',
                    value={
                        'id': 1,
                        'fromUser': 1,
                        'toUser': 2,
                        'requestStatus': 'RF',
                    },
                    status_codes=['200'],
                    response_only=True,
                ),
            ],
        },
    },
    'UserCUDView': {
        'request_update': [
            OpenApiExample(
                name='request',
                value={
                    'user': 5,
                    'firstName': 'new name',
                    'email': 'new@email.com',
                    'phone': '000-0000-0000',
                },
                request_only=True,
            ),
        ],
        'post': {
            'input': OpenApiExample(
                name='request',
                value={
                    "student_creation_count_list": {
                        "2014": 1
                    },
                    "teacher_creation_count": 0
                },
                request_only=True,
            ),
            201: OpenApiExample(
                name='user information',
                value={
                    'students' : [
                        {
                            'username': 'ABC30010',
                            'password': 'test1234!',
                        },
                    ],
                    'teachers' : [
                        {
                            'username': 'ABC00015',
                            'password': 'apple234@',
                        }
                    ],
                },
                status_codes=['201'],
                response_only=True,
            ),
        },
        'delete': {
            200: [
                OpenApiExample(
                    name='delete',
                    value={
                        'OK': 'deleted',
                    },
                    status_codes=['200'],
                    response_only=True,
                ),
            ],
        },
    },
    'FriendSearchViewSet': {
        'list': {
            200: [
                OpenApiExample(
                    name='friends',
                    value={
                        'studentCount': 2,
                        'teacherCount': 1,
                        'students': [
                            {
                                'id': 10,
                                'username': 'ssafy0001',
                                'firstName': '김싸피',
                                'friendRequest': 'friend',
                            },
                            {
                                'id': 16,
                                'username': 'ssafy0006',
                                'firstName': '박싸피',
                                'friendRequest': 'requestSend',
                            },
                        ],
                        'teachers': [
                            {
                                'id': 5,
                                'username': 'ssafy1000',
                                'firstName': '이싸피',
                                'friendRequest': 'requestReveive',
                            },
                        ],
                    },
                ),
            ],
        },
    },
    'ResisterViewSet': {
        'request': [
            OpenApiExample(
                name='request',
                value={
                    'firstName': '김싸피',
                    'password': 'ssafy1234!',
                    'school': {
                        'name': '싸피초등학교',
                        'abbreviation': 'SFE'
                    },
                },
                request_only=True
            ),
        ],
        'create': {
            201: [
                OpenApiExample(
                    name='user information',
                    value={
                        'id': 30,
                        'username': 'ABC00000',
                        'firstName': '김싸피',
                        'schoolAdmin': {
                            'school': {
                                'id': 15,
                                'name': '싸피초등학교',
                                'abbreviation': 'ABC',
                            },
                            'accountType': 'F',
                        },
                    },
                    status_codes=['200', '201'],
                    response_only=True,
                ),
            ],
        },
    },
}
