from drf_spectacular.utils import OpenApiExample


descriptions = {
    'QuizSubmissionViewSet': {
        'list': {
            'description':
    '''
    quiz_pk에 해당하는 모든 답안 제출을 조회합니다
    ''',
            200:
    '''
    해당 답안 정보 조회를 성공했습니다
    ''',
        },
        'create': {
            'description':
    '''
    quiz_pk의 답안을 생성합니다
    ''',
            201:
    '''
    해당 답안을 생성했습니다
    '''
        },
    },
    'QuizDetailViewSet': {
        'retrieve': {
            'description':
    '''
    quiz_pk의 쪽지 시험을 확인합니다
    ''',
            200:
    '''
    쪽지 시험을 성공적으로 조회했습니다
    ''',
        },
        'update': {
            'description':
    '''
    quiz_pk의 쪽지 시험을 수정합니다
    ''',
            201:
    '''
    쪽지 시험 수정이 완료되었습니다
    ''',
        },
        'destroy': {
            'description':
    '''
    quiz_pk의 쪽지 시험을 삭제합니다
    ''',
            200:
    '''
    성공적으로 삭제되었습니다
    ''',
        },
    },
    'QuizViewSet': {
        'list': {
            'description':
    '''
    모든 쪽지 시험을 조회합니다
    ''',
            200:
    '''
    쪽지 시험 조회를 성공했습니다
    ''',
        },
        'create': {
            'description':
    '''
    쪽지 시험을 생성합니다
    ''',
            201:
    '''
    해당 쪽지 시험을 생성했습니다
    '''
        },
    },
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
    'ClassroomView': {
        'get': {
            'description': 
    '''
    Get total classroom information
Use school_pk, return total homework information
    ''',
            200: 
    '''
    Successfully get total classroom list
successfully get total classroom information from school_pk
    ''',
        },
        'post': {
            'description': 
    '''
    Post classroom information
Input classroom information
    ''',
            201: 
    '''
    Successfully post classroom
successfully input classroom
    ''',
        },
    },
    'LectureView': {
        'get': {
            'description': 
    '''
    Get total lecture of school information
Use lecture_pk, return total lecture information
    ''',
            200: 
    '''
    Successfully get total lecture list
successfully get total lecture information from lecture_pk
    ''',
        },
        'post': {
            'description': 
    '''
    Post lecture information
Input lecture information
    ''',
            201: 
    '''
    Successfully post lecture
successfully input lecture
    ''',
        },
    },
    'LectureDetailView': {
        'get': {
            'description': 
    '''
    Get lecture information
Use lecture_pk and school_pk, return lecture information
    ''',
            200: 
    '''
    Successfully get lecture information
successfully get lecture information from lecture_pk and school_pk
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
}

summaries = {
    'QuizSubmissionViewSet': {
        'list': '제출한 쪽지 시험 답안 정보',
        'create': '쪽지 시험 답안 제출',
    },
    'QuizViewSet': {
        'list': '쪽지 시험 조회',
        'create': '쪽지 시험 생성',
    },
    'QuizDetailViewSet': {
        'retrieve': '쪽지 시험 상세 정보',
        'update': '쪽지 시험 정보 변경',
        'destroy': '쪽지 시험 삭제',
    },
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
    'ClassroomView': {
        'get' : 'Get classroom information',
        'post' : 'Post classroom',
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
}

examples = {
    'QuizSubmissionViewSet': {
        'list': [
            OpenApiExample(
                name='student12',
                value=[
                    {
                        "id": 2,
                        "answer": {
                        "1": "1",
                        "2": "3",
                        "3": "2"
                        },
                        "submitter": 11,
                        "quiz": 7
                    },
                    {
                        "id": 3,
                        "answer": {
                        "1": "4",
                        "2": "3",
                        "3": "1"
                        },
                        "submitter": 10,
                        "quiz": 7
                    },
                ],
                status_codes=['200'],
                response_only=True,
            ),
            OpenApiExample(
                name='student1',
                value={
                    "id": 2,
                    "answer": {
                    "1": "1",
                    "2": "3",
                    "3": "2"
                    },
                    "submitter": 11,
                    "quiz": 7
                },
            ),
        ],
        'submission': [
            OpenApiExample(
                name='submission',
                value={
                    "id": 2,
                    "answer": {
                        "1": "1",
                        "2": "3",
                        "3": "2"
                    },
                    "submitter": 11,
                    "quiz": 7
                },
            ),
        ],
        
    },
    'QuizViewSet': {
        'quiz_list':  [
            OpenApiExample(
                name='quiz list',
                value=[
                    {
                        "id": 7,
                        "title": "수학 쪽지 시험1",
                        "body": {
                        "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                        "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                        "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                        },
                        "answer": {
                        "1": "2",
                        "2": "3",
                        "3": "1"
                        },
                        "writer": 11
                    },
                ],
                status_codes=['200', '201',],
                response_only=True,
            ),
            OpenApiExample(
                name='quiz list',
                value=[
                    {
                        "id": 7,
                        "title": "수학 쪽지 시험1",
                        "body": {
                        "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                        "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                        "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                        },
                        "answer": {
                        "1": "2",
                        "2": "3",
                        "3": "1"
                        },
                        "writer": 11
                    },
                ],
            ),
        ],
        'quiz_detail': [
            OpenApiExample(
                name='homework list',
                value=[
                    {
                        "id": 7,
                        "title": "수학 쪽지 시험1",
                        "body": {
                            "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                        },
                        "answer": {
                            "1": "2",
                            "2": "3",
                            "3": "1"
                        },
                        "writer": 11,
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
                        "title": "수학 쪽지 시험1",
                        "body": {
                            "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "2": "3",
                            "3": "4"
                        },
                        "answer":  {
                            "1": "1",
                            "2": "3",
                            "3": "4"
                        }
                    },
                    request_only=True,
                ),
            ],
            201: [
                OpenApiExample(
                    name='homework list',
                    value=[
                        {
                            "id": 7,
                            "title": "수학 쪽지 시험1",
                            "body": {
                                "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                                "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                                "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                            },
                            "answer": {
                                "1": "2",
                                "2": "3",
                                "3": "1"
                            },
                            "writer": 11
                            },
                    ],
                    status_codes=['200', '201',],
                    response_only=True,
                ),
            ]
        },
    },
    'QuizDetailViewSet': {
        'quiz_detail': [
            OpenApiExample(
                name='quiz list',
                value=[
                    {
                        "id": 7,
                        "title": "수학 쪽지 시험1",
                        "body": {
                            "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                        },
                        "answer": {
                            "1": "2",
                            "2": "3",
                            "3": "1"
                        },
                        "writer": 11,
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
                        "title": "수학 쪽지 시험1",
                        "body": {
                            "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                        },
                        "answer": {
                            "1": "2",
                            "2": "3",
                            "3": "2"
                        }
                    },
                    request_only=True,
                ),
            ],
            201: [
                OpenApiExample(
                    name='homework list',
                    value=[
                        {
                             "id": 8,
                             "title": "수학 쪽지 시험1",
                             "body": {
                                "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                                "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                                "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                            },
                            "answer": {
                                "1": "2",
                                "2": "3",
                                "3": "2"
                            },
                            "writer": 11
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
                        "title": "수학 쪽지 시험1",
                        "body": {
                            "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                            "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                        },
                        "answer": {
                            "1": "2",
                            "2": "3",
                            "3": "2"
                        }
                    },
                    request_only=True,
                ),
            ],
            201: [
                OpenApiExample(
                    name='homework list',
                    value=[
                        {
                             "id": 8,
                             "title": "수학 쪽지 시험1",
                             "body": {
                                "1": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                                "2": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래",
                                "3": "1. 다음 중 동물이 아닌 것은? 1. 사자 2. 복숭아 3. 호랑이 4. 고래"
                            },
                             "answer": {
                                "1": "2",
                                "2": "3",
                                "3": "2"
                             },
                             "writer": 11
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
}
