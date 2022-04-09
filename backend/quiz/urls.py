from django.urls import path, include
from .views import QuizViewSet, QuizDetailViewSet, QuizSubmissionViewSet

quiz_list = QuizViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

quiz_detail = QuizDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

quiz_submission_list = QuizSubmissionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})


urlpatterns = [
    path(
        'quizs/', include([
            path('', 
                quiz_list, 
                name="quiz_list"
            ),
            path(
                '<int:quiz_pk>/', include([
                    path('',
                        quiz_detail,
                        name='quiz_detail',
                    ),
                    path(
                        'submissions/',
                        quiz_submission_list,
                        name='quiz_submission_list'
                    ),
                ])
            ),
        ]) 
    ), 
]
    