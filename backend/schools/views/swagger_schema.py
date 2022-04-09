from drf_spectacular.utils import OpenApiExample


descriptions = {
    'HomeworkViewSet': {
        'list': {
            'description':
    '''
    lecture_pk에 해당하는 모든 숙제를 조회합니다
    ''',
            200:
    '''
    해당 수업의 숙제 정보 조회를 성공했습니다
    ''',
        },
        'create': {
            'description':
    '''
    lecture_pk의 숙제를 생성합니다
입력으로 받는 deadline은 YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z] 포멧으로 작성되야 합니다\n
(ex. 2020-02-01T00:00, 2020-02-01T23:59:59)
    ''',
            201:
    '''
    해당 수업의 숙제를 생성했습니다
    '''
        },
        'retrieve': {
            'description':
    '''
    lecture_pk의 특정 숙제 상세정보를 확인합니다
    ''',
            200:
    '''
    수업 상세정보를 성공적으로 조회했습니다
    ''',
        },
        'update': {
            'description':
    '''
    lecture_pk의 특정 숙제 정보를 수정합니다
    ''',
            201:
    '''
    수업 정보 수정이 완료되었습니다
    ''',
        },
        'destroy': {
            'description':
    '''
    lecture_pk의 특정 숙제를 삭제합니다
    ''',
            200:
    '''
    성공적으로 삭제되었습니다
    ''',
        },
    },
    'HomeworkSubmissionViewSet': {
        'list': {
            'description':
    '''
    homework_pk의 모든 숙제 제출을 확인합니다
homework_pk와 lecture_pk를 모두 확인한 후 요청이 정당한 경우 제출될 숙제를 반환합니다\n
- 학생의 경우 자신의 숙제만 반환하거나, 없다면 204를 반환합니다 
- 교사 또는 학교 관리자는 해당 숙제의 모든 제출을 확입합니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우\n
다음의 경우 404를 반환합니다
- homework_pk가 존재하지 않는 경우
- homework_pk가 lecture_pk의 수업이 아닌경우
    ''',
            200:
    '''
    제출된 숙제 목록입니다
학생이 요청하면, 제출한 숙제가 있을 때만 200번 반환이 있습니다\n
교사 또는 학교 관리자는 해당 숙제의 모든 제출(없더라도) 확입합니다
    ''',
            204:
    '''
    학생이 요청하고, 제출한 숙제가 없는 경우입니다
    ''',
        },
        'create': {
            'description':
    '''
    숙제를 제출(생성)합니다
추가 파일이 있으면 file이름으로 전송합니다\n
기존 숙제가 있으면, 숙제 내용을 수정하고, 없으면 생성합니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우
다음의 경우 404를 반환합니다
- homework_pk가 존재하지 않는 경우
- homework_pk가 lecture_pk의 수업이 아닌경우
    ''',
            201:
    '''
    숙제 생성이 완료되었습니다
    '''
        },
        'retrieve': {
            'description':
    '''
    유저의 숙제를 확인합니다
학생의 경우 user_pk없이 GET 방식과 동일하게 작동합니다\n
교사의 경우 숙제의 상세정보 확인할 때 사용할 수 있습니다
    ''',
            200:
    '''
    해당 학생이 제출한 숙제를 성공적으로 받았습니다
    ''',
            204:
    '''
    해당 학생이 제출한 숙제가 없습니다
    ''',
        },
        'destroy': {
            'description':
    '''
    유저의 숙제를 삭제합니다
제출한 숙제가 없으면 204를 반환합니다\n
올바르지 않은 parameter가 있을 경우 404를 반환할 수 있습니다
    ''',
            200:
    '''
    유저의 숙제 삭제를 완료하였습니다
    ''',
            204:
    '''
    유저가 제출한 숙제가 없습니다
    ''',
        },
    },
    'ArticleViewSet': {
        'list': {
            'description':
    '''
    게시글 목록을 출력합니다
게시판은 해당 수업의 교사, 학생 또는 해당 수업이 속한 학교 관리자만 조회할 수 있습니다\n
이 API는 pagination이 적용되어 있습니다
- page : 없다면 1쪽이 조회되고, 입력이 있으면 해당 쪽을 조회합니다
- page_size : 한 쪽마다 몇개의 게시글을 조회할지 지정하고, 기본적으로 10개를 조회합니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우\n
다음의 경우 404를 반환합니다
- lecture_pk가 존재하지 않는 경우
    ''',
            200:
    '''
    게시글 목록을 조회했습니다
totalCount는 해당 게시판의 전체 게시글의 수, pageCount는 조회한 페이지의 게시글 수 입니다
    ''',
        },
        'create': {
            'description':
    '''
    게시글을 생성합니다
게시판은 해당 수업의 교사, 학생 또는 해당 수업이 속한 학교 관리자만 조회할 수 있습니다\n
공지사항(notice)는 교사 또는 학교 관리자만 할 수 있습니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우\n
다음의 경우 404를 반환합니다
- lecture_pk가 존재하지 않는 경우
    ''',
            201:
    '''
    게시글이 생성되었습니다
학생이 공지사항으로 요청한 경우, 자동적으로 공지사항 항목은 취소됩니다
    '''
        },
        'retrieve': {
            'description':
    '''
    게시글 상세 조회를 합니다
게시판은 해당 수업의 교사, 학생 또는 해당 수업이 속한 학교 관리자만 조회할 수 있습니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우\n
다음의 경우 404를 반환합니다
- lecture_pk가 존재하지 않는 경우
- article_pk가 없거나 lecture_pk의 게시글이 아닌 경우
    ''',
            200:
    '''
    게시글의 상세 항목을 조회합니다
    '''
        },
        'update': {
            'description':
    '''
    게시글을 수정합니다
게시판은 해당 수업의 교사, 학생 또는 해당 수업이 속한 학교 관리자만 조회할 수 있습니다\n
게시글 수정은 작성자만 할 수 있습니다\n
공지사항(notice)는 교사 또는 학교 관리자만 할 수 있습니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우
- 게시글의 작성자가 아닌 경우\n
다음의 경우 404를 반환합니다
- lecture_pk가 존재하지 않는 경우
- article_pk가 없거나 lecture_pk의 게시글이 아닌 경우
    ''',
            201:
    '''
    게시글을 수정했습니다
학생이 공지사항으로 등록하려는 경우 자동적으로 취소됩니다
    ''',
        },
        'destroy': {
            'description':
    '''
    게시글을 삭제합니다
게시판은 해당 수업의 교사, 학생 또는 해당 수업이 속한 학교 관리자만 조회할 수 있습니다\n
게시글 삭제는 작성 유저 또는 교사, 학교 관리자만 할 수 있습니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우\n
다음의 경우 404를 반환합니다
- lecture_pk가 존재하지 않는 경우
- article_pk가 없거나 lecture_pk의 게시글이 아닌 경우
    ''',
            200:
    '''
    게시글을 삭제했습니다
    ''',
        }
    },
    'ClassroomViewSet': {
        'list': {
            'description': 
    '''
    학교의 모든 교실을 조회합니다
다음의 경우 404를 반환합니다
- school_pk에 해당하는 학교가 없을 경우
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- school_pk에 속하지 않는 유저인 경우
    ''',
            200: 
    '''
    교실 목록 조회를 완료했습니다
    ''',
        },
        'create': {
            'description': 
    '''
    교실을 생성합니다
classGrade, classNum은 필수입니다\n
teacher와 studentList는 선택적 입력 가능합니다\n
다음의 경우 400을 반환합니다\n
- 입력값이 잘못된 경우
- 해당 학교에 이미 해당하는 교실이 있는 경우
    ''',
            201: 
    '''
    교실 생성이 완료되었습니다
    ''',
        },
        'retrieve': {
            'description': 
    '''
    교실 상세 조회 합니다
    ''',
            200:
    '''
    교실 상세 조회를 했습니다
    ''',
        },
        'update': {
            'description': 
    '''
    교실 정보를 수정합니다
classGrade, classNum정보도 수정할 수 있지만, 이미 다들 교실이 존재하면 400을 반환합니다
classGrade, classNum은 선택적 입력 가능합니다\n
teacher와 studentList는 선택적 입력 가능합니다\n
teacher와 studentList는 선택적 입력 가능합니다\n
다음의 경우 400을 반환합니다\n
- 입력값이 잘못된 경우
- 해당 학교에 이미 해당하는 교실이 있는 경우
    ''',
            201:
    '''
    교실 정보 수정이 완료되었습니다
    ''',
        },
        'destroy': {
            'description':
    '''
    교실을 삭제합니다
해당 교실을 삭제하고, 전체 교실 정보를 반환합니다
    ''',
            200:
    '''
    교실 삭제를 완료했고, 교실 목록을 반환합니다
    ''',
        },
    },
    'LectureView': {
        'get': {
            'description': 
    '''
    해당 학교의 모든 수업을 조회를 합니다
학생, 교사, 학교 관리자의 학교에 대한 모든 수업을 조회할 수 있습니다\n
다음의 경우 401을 반환합니다
- 토큰이 존재하지 않거나 만료 된 경우
- 허가되지 않은 사용자인 경우\n
    ''',
            200: 
    '''
    모든 수업을 조회했습니다
id : 수업 pk\n
name : 수업 이름\n
time_list : 수업 시간\n
school : 학교 pk\n
teacher : 선생의 상세 정보\n
student_list : 학생의 상세 정보 리스트
    ''',
        },
        'post': {
            'description': 
    '''
    수업을 생성합니다.
수업을 작성하여 생성합니다.\n
name : 수업이름\n
time_list : 요일, 시간\n
teacher : 선생 pk\n
student_list : 학생 pk 리스트\n
    ''',
            201: 
    '''
    수업이 생성되었습니다
수업이 생성됩니다.
    ''',
        },
    },
    'LectureDetailView': {
        'get': {
            'description': 
    '''
    수업의 상세 정보에 대해 조회한다.
해당 수업의 상세 정보를 조회해준다.
    ''',
            200: 
    '''
    수업 상세 정보를 조회하였습니다.
id : 수업 pk\n
name : 수업 이름\n
time_list : 수업 시간\n
school : 학교 pk\n
teacher : 선생의 상세 정보\n
student_list : 학생의 상세 정보 리스트
    ''',
        },
        'put': {
            'description': 
    '''
    Change lecture information
lecture information changed
    ''',
            201: 
    '''
    Successfully Put lecture
successfully change lecture
    ''',
        },
        'delete': {
            'description': 
    '''
    Delete lecture information
lecture information deleted
    ''',
            204: 
    '''
    Successfully Delete lecture
successfully deleted lecture
    ''',
        },
    },
    'StudentView': {
        'get': {
            'description': 
    '''
    Get total student of school information
Use school_pk, return total student of school infromation
    ''',
            200: 
    '''
    Successfully get total student list
successfully get total student information from school_pk
    ''',
        },
    },
    'ClassroomStudentView': {
        'get': {
            'description': 
    '''
    Get total student of classroom information
Use school_pk and classroom_pk, return total student of classroom infromation
    ''',
            200: 
    '''
    Successfully get total student list
successfully get total student information from school_pk and classroom_pk
    ''',
        },
    },
    'TeacherView': {
        'get': {
            'description': 
    '''
    Get total teacher of school information
Use school_pk, return total teacher of school infromation
    ''',
            200: 
    '''
    Successfully get total teacher list
successfully get total teacher information from school_pk
    ''',
        },
    },
    'SchoolAbbreviationViewSet': {
        'retrieve': {
            'description':
    '''
    학교 약어의 유효성을 겁사합니다
사용여부만 확인할 수 있고, 규칙(길이 등)에 대한 유효성은 검사하지 않습니다\n
사용 가능하면 200, 불가능하면 400을 반환합니다
    '''
        }
    }
}

summaries = {
    'HomeworkViewSet': {
        'list': '수업의 모든 숙제',
        'create': '수업의 숙제 생성',
        'retrieve': '수업 숙제 상세 정보',
        'update': '수업 숙제 정보 변경',
        'destroy': '수업 숙제 삭제',
    },
    'HomeworkSubmissionViewSet': {
        'list': '숙제의 모든 제출 확인',
        'create': '숙제 제출',
        'retrieve': '숙제 상세 확인',
        'destroy': '숙제 제출 삭제',
    },
    'ArticleViewSet': {
        'list': '게시글 전체 조회',
        'create': '게시글 생성',
        'retrieve': '게시글 상세 조회',
        'update': '게시글 수정',
        'destroy': '게시글 삭제',
    },
    'ClassroomViewSet': {
        'list' : '학교의 전체 교실 정보',
        'create' : '학교에 교실 생성',
        'retrieve': '특정 교실 조회',
        'update': '특정 교실 정보 수정',
        'destroy': '특정 교실 삭제',
    },
    'LectureView': {
        'get' : 'Get lecture information',
        'post' : 'Post lecture',
    },
    'LectureDetailView': {
        'get' : 'Get detail lecture information',
        'put' : 'Put lecture information',
        'delete' : 'Delete lecture' 
    },
    'StudentView': {
        'get' : 'Get students of school information',
    },
    'ClassroomStudentView': {
        'get' : 'Get students of classroom information',
    },
    'TeacherView': {
        'get' : 'Get teacher of school information',
    },
    'SchoolAbbreviationViewSet': {
        'retrieve': '학교 약어 유효성 검사'
    }
}

examples = {
    'HomeworkViewSet': {
        'homework_list':  [
            OpenApiExample(
                name='homework list teacher',
                value=[
                    {
                        'id': 1,
                        'title': '수학 숙제',
                        'content': '수학 익힘책 인수분해 문제 풀기',
                        'createdAt': '2022-02-01T02:00:00.000000',
                        'deadline': '2022-02-08T00:00:00',
                        'writer': {
                            'id': 5,
                            'username': '김싸피',
                        },
                        'lecture': 1,
                        'submission_list': [
                            {
                                'id': 10,
                                'username': '박싸피',
                            },
                            {
                                'id': 15,
                                'username': '황싸피',
                            },
                        ],
                    },
                ],
                status_codes=['200', '201',],
                response_only=True,
            ),
            OpenApiExample(
                name='homework list student',
                value=[
                    {
                        'id': 1,
                        'title': '수학 숙제',
                        'content': '수학 익힘책 인수분해 문제 풀기',
                        'createdAt': '2022-02-01T02:00:00.000000',
                        'deadline': '2022-02-08T00:00:00',
                        'writer': {
                            'id': 5,
                            'username': '김싸피',
                        },
                        'lecture': 1,
                        'submission': True,
                    },
                ],
            ),
        ],
        'homework_detail': [
            OpenApiExample(
                name='homework list',
                value=[
                    {
                        'id': 1,
                        'title': '수학 숙제',
                        'content': '수학 익힘책 인수분해 문제 풀기',
                        'createdAt': '2022-02-01T02:00:00.000000',
                        'deadline': '2022-02-08T00:00:00',
                        'writer': 4,
                        'lecture': 1,
                        'submission': [
                            {
                                'id': 1,
                                'title': '수학 숙제!!',
                                'content': '다 풀었습니다~',
                                'createdAt': '2022-02-01T02:00:00.000000',
                                'file': None,
                                'homework': 1,
                                'writer': 10,
                            },
                        ],
                    },
                ],
                status_codes=['200', '201',],
                response_only=True,
            ),
        ],
        'create': {
            'request': [
                OpenApiExample(
                    name='request',
                    value={
                        'title': '수학 숙제',
                        'content': '수학 익힘책 인수분해 문제 풀기',
                        'deadline': '2022-02-08T00:00:00',
                    },
                    request_only=True,
                ),
            ],
            201: [
                OpenApiExample(
                    name='homework list',
                    value=[
                        {
                            'id': 1,
                            'title': '수학 숙제',
                            'content': '수학 익힘책 인수분해 문제 풀기',
                            'createdAt': '2022-02-01T02:00:00.000000',
                            'deadline': '2022-02-08T00:00:00',
                            'writer': 4,
                            'lecture': 1
                        },
                    ],
                    status_codes=['200', '201',],
                    response_only=True,
                ),
            ]
        },
        'update': {
            'request': [
                OpenApiExample(
                    name='request',
                    value={
                        'title': '수학 숙제',
                        'content': '수학 익힘책 인수분해 문제 풀기',
                        'deadline': '2022-02-08T00:00:00',
                    },
                    request_only=True,
                ),
            ],
            201: [
                OpenApiExample(
                    name='homework list',
                    value=[
                        {
                            'id': 1,
                            'title': '수학 숙제',
                            'content': '수학 익힘책 인수분해 문제 풀기',
                            'createdAt': '2022-02-01T02:00:00.000000',
                            'deadline': '2022-02-08T00:00:00',
                            'writer': 4,
                            'lecture': 1
                        },
                    ],
                    status_codes=['200', '201',],
                    response_only=True,
                ),
            ],
        },
        'destroy': {
            200: [
                OpenApiExample(
                    name='user',
                    value={
                        'OK': 'No Content'
                    },
                    status_codes=['200'],
                    response_only=True
                ),
            ],
        },
    },
    'HomeworkSubmissionViewSet': {
        'submission_list': [
            OpenApiExample(
                name='teacher',
                value=[
                    {
                        'id': 1,
                        'title': '수학 숙제 제출',
                        'content': '다 풀었습니다',
                        'cretedAt': '2022-02-05T17:05:27.928675',
                        'file': None,
                        'homework': 1,
                        'writer': 10,
                    },
                    {
                        'id': 2,
                        'title': '이번 숙제 너무 어려워요 ㅠㅠ',
                        'content': '절반밖에 못풀었어요',
                        'cretedAt': '2022-02-05T17:06:27.928675',
                        'file': None,
                        'homework': 1,
                        'writer': 15,
                    },
                ],
                status_codes=['200'],
                response_only=True,
            ),
            OpenApiExample(
                name='student',
                value={
                    'id': 1,
                    'title': '수학 숙제 제출',
                    'content': '다 풀었습니다',
                    'cretedAt': '2022-02-05T17:05:27.928675',
                    'file': None,
                    'homework': 1,
                    'writer': 10,
                },
            ),
        ],
        'submission': [
            OpenApiExample(
                name='submission',
                value={
                    'id': 1,
                    'title': '수학 숙제 제출',
                    'content': '다 풀었습니다',
                    'cretedAt': '2022-02-05T17:05:27.928675',
                    'file': None,
                    'homework': 1,
                    'writer': 10,
                },
            ),
        ],
    },
    'ArticleViewSet': {
        'article_list': [
            OpenApiExample(
                name='article list pagination',
                value={
                    'totalCount': 20,
                    'pageCount': 2,
                    'articles': [
                        {
                            'id': 20,
                            'title': '수학 숙제 너무 어려워요',
                            'content': 'ㅠㅠㅠ',
                            'createdAt': '2022-02-01T00:00:00',
                            'updatedAt': '2022-02-01T00:00:00',
                            'notice': False,
                            'writer': 10,
                            'lecture': 1,
                        },
                        {
                            'id': 20,
                            'title': '같이 공부해봐요',
                            'content': '다들 시험 화이팅',
                            'createdAt': '2022-02-01T00:00:00',
                            'updatedAt': '2022-02-01T00:00:00',
                            'notice': True,
                            'writer': 10,
                            'lecture': 1,
                        },
                    ],
                },
                status_codes=['200'],
                response_only=True
            )
        ],
        'article_detail': [
            OpenApiExample(
                name='article list pagination',
                value={
                            'id': 20,
                            'title': '수학 숙제 너무 어려워요',
                            'content': 'ㅠㅠㅠ',
                            'createdAt': '2022-02-01T00:00:00',
                            'updatedAt': '2022-02-01T00:00:00',
                            'notice': False,
                            'writer': {
                                'id': 10,
                                'username': 'ssafy0001',
                                'firstName': '김싸피',
                                'status': 'ST',
                            },
                            'lecture': 1,
                },
                status_codes=['200', '201'],
                response_only=True,
            ),
        ],
        'article': [
            OpenApiExample(
                name='article list pagination',
                value={
                            'id': 20,
                            'title': '수학 숙제 너무 어려워요',
                            'content': 'ㅠㅠㅠ',
                            'createdAt': '2022-02-01T00:00:00',
                            'updatedAt': '2022-02-01T00:00:00',
                            'notice': False,
                            'writer': 10,
                            'lecture': 1,
                },
                status_codes=['200', '201'],
                response_only=True,
            ),
        ],
        'create_article': [
            OpenApiExample(
                name='create or update',
                value={
                    'title': '수학 숙제 너무 어려워요',
                    'content': 'ㅠㅠㅠ',
                    'notice': True,
                },
                request_only=True,
            )
        ],
        'destroy': {
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
    'ClassroomViewSet': {
        'classroom_list': [
            OpenApiExample(
                name='classroom list',
                value=[
                    {
                        'id': 3,
                        'classGrade': 3,
                        'classNum': 1,
                        'school': 3
                    },
                    {
                        'id': 4,
                        'classGrade': 3,
                        'classNum': 2,
                        'school': 3
                    },
                ],
                status_codes=['200', '201',],
                response_only=True,
            ),
        ],
        'classroom_output': [
            OpenApiExample(
                name='classroom output',
                value={
                    'id': 10,
                    'classGrade': 3,
                    'classNum': 1,
                    'school': 3,
                },
                status_codes=['200', '201'],
                response_only=True,
            )
        ],
        'classroom_detail': [
            OpenApiExample(
                name='classroom detail',
                value={
                    'id': 10,
                    'school': {
                        'id': 3,
                        'name': '싸피 초등학교',
                        'abbreviation': 'sfe'
                    },
                    'studentList': [
                        {
                            'user': {
                                'id': 20,
                                'username': 'ssafy00020',
                                'firstName': '김싸피',
                                'status': 'ST'
                            },
                        },
                    ],
                    'teacher': {
                        'user': {
                            'id': 5,
                            'username': 'ssafy10001',
                            'firstName': '박싸피',
                            'status': 'TE'
                        },
                    },
                    'classGrade': 3,
                    'classNum': 1,
                },
                status_codes=['200', '201',],
                response_only=True,
            ),
        ],
        'request': [
            OpenApiExample(
                name='request',
                value={
                    'classGrade': 1,
                    'classNum': 1,
                },
                request_only=True,
            ),
            OpenApiExample(
                name='request with teacher, student',
                value={
                    'classGrade': 1,
                    'classNum': 1,
                    'teacher': 10,
                    'studentList': [
                        20,
                        21,
                        22,
                    ],
                },
                request_only=True,
            ),
        ],
        'list': {
            200: [
            OpenApiExample(
                name='user',
                value={
                    "class_grade": 6,
                    "class_num": 0
                },
            ),
            ],
        },
        'create': {
            'input': OpenApiExample(
                name='input example',
                value={
                    "class_grade": 6,
                    "class_num": 0
                },
                request_only=True,
            ),
            201: [
            OpenApiExample(
                name='user',
                value={
                    "class_grade": 6,
                    "class_num": 0
                },
            ),
            ],
        }
    },
    'LectureView': {
        'get': {
            200: [
            OpenApiExample(
                name='user',
                value={
                    "id": 0,
                    "name": "string",
                    "time_list": {
                        "count": 1, 
                        "lectures": 
                            [{
                                "day": "fri", 
                             "st": "1200", 
                             "end": "1330"
                            }]
                    },
                    "school": 0,
                    "teacher": 0,
                    "student_list": [
                        0
                    ]
                }
            ),
            ],
        },
        'post': {
            'input': OpenApiExample(
                name='input example',
                value={
                    "id": 0,
                    "name": "string",
                    "time_list": {
                        "count": 1, 
                        "lectures": 
                            [{
                                "day": "fri", 
                             "st": "1200", 
                             "end": "1330"
                            }]
                    },
                    "school": 0,
                    "teacher": 0,
                    "student_list": [
                        0
                    ]
                },
                request_only=True,
            ),
            201: [
            OpenApiExample(
                name='user',
                value={
                    "id": 0,
                    "name": "string",
                    "time_list": {
                        "count": 1, 
                        "lectures": 
                            [{
                                "day": "fri", 
                             "st": "1200", 
                             "end": "1330"
                            }]
                    },
                    "school": 0,
                    "teacher": 0,
                    "student_list": [
                        0
                    ]
                },
            ),
            ],
        }
    },
    'LectureDetailView': {
        'get': {
            200: [
            OpenApiExample(
                name='user',
                value={
                    "id": 0,
                    "name": "string",
                    "time_list": {
                        "count": 1, 
                        "lectures": 
                            [{
                                "day": "fri", 
                             "st": "1200", 
                             "end": "1330"
                            }]
                    },
                    "school": 0,
                    "teacher": 0,
                    "student_list": [
                        0
                    ]
                },
            ),
            ],
        },
        'put': {
            'input': OpenApiExample(
                name='input example',
                value={
                    "id": 0,
                    "name": "string",
                    "time_list": {
                        "count": 1, 
                        "lectures": 
                            [{
                                "day": "fri", 
                             "st": "1200", 
                             "end": "1330"
                            }]
                    },
                    "school": 0,
                    "teacher": 0,
                    "student_list": [
                        0
                    ]
                },
                request_only=True,
            ),
            201: [
            OpenApiExample(
                name='user',
                value={
                    "id": 0,
                    "name": "string",
                    "time_list": {
                        "count": 1, 
                        "lectures": 
                            [{
                                "day": "fri", 
                             "st": "1200", 
                             "end": "1330"
                            }]
                    },
                    "school": 0,
                    "teacher": 0,
                    "student_list": [
                        0
                    ]
                },
            ),
            ],
        },
        'delete': {
            204: [
            OpenApiExample(
                name='user',
                value={
                    'OK': 'No Content'
                },
                status_codes=['204'],
                response_only=True
            ),
            ],
        }
    },
    'StudentView': {
        'get': {
            200: [
            OpenApiExample(
                name='user',
                value=[{
                    "user": {
                        "id": 0,
                        "username": "string",
                        "email": "user@example.com",
                        "phone": "string",
                        "status": "ST"
                    },
                    "classroom": {
                        "id": 0,
                        "class_grade": 6,
                        "class_num": 0
                    },
                    "school": {
                        "id": 0,
                        "name": "string"
                    },
                    "guardian_phone": "string"
                }],
            ),
            ],
        },
    },
    'ClassroomStudentView': {
        'get': {
            200: [
            OpenApiExample(
                name='user',
                value={
                    "user": {
                        "id": 0,
                        "username": "string",
                        "email": "user@example.com",
                        "phone": "string",
                        "status": "ST"
                    },
                    "classroom": {
                        "id": 0,
                        "class_grade": 6,
                        "class_num": 0
                    },
                    "school": {
                        "id": 0,
                        "name": "string"
                    },
                    "guardian_phone": "string"
                },
            ),
            ],
        },
    },
    'TeacherView': {
        'get': {
            200: [
            OpenApiExample(
                name='user',
                value=[{
                    "user": {
                        "id": 0,
                        "username": "string",
                        "email": "user@example.com",
                        "phone": "string",
                        "status": "ST"
                    },
                    "classroom": {
                        "id": 0,
                        "class_grade": 6,
                        "class_num": 0
                    },
                    "school": {
                        "id": 0,
                        "name": "string"
                    }
                }],
            ),
            ],
        },
    },
}
