from drf_spectacular.utils import (
    extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
)

from server import basic_swagger_schema
from .serializers import NotificationSerializer


notification_page = OpenApiExample(
    name='notification page',
    value={
        'totalCount': 36,
        'pageCount': 2,
        'notifications': [
            {
                'id': 55,
                'fromUser': {
                    'id': 15,
                    'username': 'ssafy00000',
                    'fristName': '이싸피',
                    'status': 'ST',
                },
                'lecture': {
                    'id': 10,
                    'teacher': {
                        'id': 55,
                        'username': 'ssafy00000',
                        'firstName': '이싸피',
                        'status': 'TE',
                    },
                    'name': '수학',
                    'timeList': None,
                    'shcool': 3,
                    'studentList': [
                        66,
                        67,
                    ],
                },
                'notificationType': 'HC',
                'content': '이차방정식 수학익힘책 문제풀이',
                'read': True,
            },
            {
                'id': 54,
                'fromUser': {
                    'id': 15,
                    'username': 'ssafy00011',
                    'fristName': '김싸피',
                    'status': 'ST',
                },
                'lecture': None,
                'notificationType': 'FQ',
                'content': None,
                'read': True,
            },
        ],
    },
    status_codes=['200'],
    response_only=True
)


notification_view_set_list = extend_schema(
    responses={
        200: OpenApiResponse(
            response=NotificationSerializer,
            description='''
    알림을 페이지별로 조회 완료했습니다
totalCount에 전체 알림수를, pageCount에 지금 페이지의 알림을 표시합니다\n
notification에서 fromUser의 상세정보, lecture의 상세정보를 포함합니다
            ''',
            examples=[
                notification_page
            ],
        ),
        401: basic_swagger_schema.open_api_response[401],
        404: basic_swagger_schema.open_api_response[404],
    },
    description='''
    알림 목록을 확인합니다
알림의 종류는 크게 5가지로 분류되고, 각각은 다음과 같은 방식으로 기록됩니다\n
알림은 notificationType(알림 종류), content, fromUser로 나뉘지만,\n
알림의 종류에따라 일부 항목들은 기록되지 않을 수도 있습니다
1. FR(Friend) : 친구 신청의 수락, 거절에 따른 알림입니다
    - fromUser에 친구 신청을 보낸 유저를 나타냅니다
    - content에 받은 친구 요청이면 null, 보낸 친구 요청 수락, 거절은 AC, RF입니다
2. HC(Homework Create) : 숙제 생성
    - 숙제가 생성되면, 해당 교실 모든 학생에게 알림을 생성합니다
    - content에 숙제 제목이 저장됩니다
    - fromUser에 숙제 작성자(교사)가 저장됩니다
    - 수업 정보가 lecture에 저장됩니다
3. HU(Homework Update) : 숙제 수정
    - 2.와 생성, 수정 차이만 있습니다
4. HS(Homework Submission) : 숙제 제출
    - 학생이 숙제를 제출하면, 담당 교사에게 알림이 생성됩니다
    - content에 숙제의 제목이 저장됩니다
    - fromUser에 숙제 작성자(학생)이 저장됩니다
    - 수업 정보가 lecture에 저장됩니다
조회하려는 페이지가 없으면 404를 반환합니다
    ''',
    summary='알림 전체 조회',
    tags=['알림',],
    examples=[
        basic_swagger_schema.examples[401],
        basic_swagger_schema.examples[404],
    ]
)

notification_view_set_partial_update = extend_schema(
    responses={
        201: OpenApiResponse(
            description='''
    모든 알림 읽음 처리 했습니다
            '''
        ),
        401: basic_swagger_schema.open_api_response[401],
        404: basic_swagger_schema.open_api_response[404],
    },
    request=inline_serializer('EmtpyRequest', {}),
    description='''
    특정 알림을 읽음 처리 합니다
notificaiton_pk로 0을 받으면 전체 알림에 대하여 읽음처리 합니다\n
notification_pk가 0이 아니고, 요청한 유저의 알림에 없다면 404를 반환합니다\n
요청에 따라 알림을 수정하고, 200과 함께 수정된 알림을 반환합니다
    ''',
    summary='알림 읽음',
    tags=['알림',],
    examples=[
        basic_swagger_schema.examples[401],
        basic_swagger_schema.examples[404],
    ],
)

notification_view_set_destroy = extend_schema(
    responses={
        204: OpenApiResponse(
            description='''
    알림 삭제를 완료했습니다
            '''
        ),
        401: basic_swagger_schema.open_api_response[401],
        404: basic_swagger_schema.open_api_response[404],
    },
    description='''
    특정 알림을 삭제합니다
notificaiton_pk로 0을 받으면 전체 알림에 대하여 삭제 합니다\n
notification_pk가 0이 아니고, 요청한 유저의 알림에 없다면 404를 반환합니다\n
요청에 따라 알림을 삭제하고, 204를 반환합니다
    ''',
    summary='알림 삭제',
    tags=['알림',],
    examples=[
        basic_swagger_schema.examples[401],
        basic_swagger_schema.examples[404],
    ]
)

notification_view_set_count = extend_schema(
    responses={
        200: OpenApiResponse(
            response=NotificationSerializer,
            description='''
    알림 개수 조회를 완료했습니다
            ''',
            examples=[
                OpenApiExample(
                    name='notification count',
                    value={
                        'count': 23,
                    },
                    response_only=True,
                ),
            ],
        ),
        401: basic_swagger_schema.open_api_response[401]
    },
    description='알림 개수를 확인합니다',
    summary='알림 개수',
    tags=['알림'],
    examples=[
        basic_swagger_schema.examples[401],
    ],
)
