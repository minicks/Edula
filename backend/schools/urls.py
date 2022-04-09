"""urls for schools app
"""
from django.urls import path, include
from .views import (
    school, classroom, lecture, student, teacher, 
    homework, homework_submission,
    article
)


classroom_list = classroom.ClassroomViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
classroom_detail = classroom.ClassroomViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

homework_list = homework.HomeworkViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
homework_detail = homework.HomeworkViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

homework_submission_list = homework_submission.HomeworkSubmissionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
homework_submission_detail = homework_submission.HomeworkSubmissionViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

article_list = article.ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
article_detail = article.ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


urlpatterns = [
    path(
        '<int:school_pk>/', include([
            # 유저
            path('student/', student.StudentView.as_view()),
            path('teacher/', teacher.TeacherView.as_view()),
            # 교실
            path('classroom/',
                classroom_list,
                name='classroom_list'
            ),
            path('classroom/<int:classroom_pk>/',
                classroom_detail,
                name='classroom_detail'
            )
        ]),
    ),
    path(
        'lecture/', include([
            # 수업
            path('',
                lecture.LectureView.as_view(),
                name='lecture_list',
            ),
            path(
                '<int:lecture_pk>/', include([
                    # 수업
                    path('',
                        lecture.LectureDetailView.as_view(),
                        name='lecture_detail',
                    ),
                    # 숙제
                    path('homework/', homework_list),
                    path('homework/<int:homework_pk>/', homework_detail),
                    path(
                        'homework/<int:homework_pk>/submission/',
                        homework_submission_list
                    ),
                    path(
                        'homework/<int:homework_pk>/submission/<int:user_pk>/',
                        homework_submission_detail
                    ),
                    # 게시판
                    path('article/', article_list),
                    path('article/<int:article_pk>/', article_detail),
                ]),
            ),
        ]),
    ),
    path(
        '<str:abbreviation>/',
        school.SchoolAbbreviationViewSet.as_view({'get': 'retrieve'}),
    ),
]
