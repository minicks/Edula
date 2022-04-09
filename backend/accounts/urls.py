from django.urls import path
from .views import user, student, teacher, school_admin, friend_request


friend_list = user.FriendViewSet.as_view({
    'get': 'list',
})
friend_detail = user.FriendViewSet.as_view({
    'delete': 'destroy',
})

request_list = friend_request.FriendRequestViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
request_detail = friend_request.FriendRequestViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

user_C = user.UserCUDView.as_view({
    'post': 'create',
    'put': 'update',
})
user_D = user.UserCUDView.as_view({
    'delete': 'destroy',
})

urlpatterns = [
    # User Information
    path('', user.UserView.as_view(), name='user_self_information'),
    path('resister/',
        user.ResisterViewSet.as_view({'post': 'create'}),
        name='resister',
    ),
    path('user/', user_C),
    path('user/<str:YS>/<int:num>/', user_D),
    path('<int:user_pk>/',
        user.UserSpecifyingView.as_view(),
        name='user_other_information',
    ),
    path('profile-image/', user.UserProfileImageView.as_view()),
    # Friend
    path('friend/',
        friend_list,
        name='friend_list',
    ),
    path('friend/<int:friend_pk>/',
        friend_detail,
        name='friend_detail',
    ),
    path('friend/request/',
        request_list,
        name='friend_list',
    ),
    path('friend/request/<int:request_pk>/',
        request_detail,
        name='request_detail',
    ),
    path('friend/search/<str:search>/',
        user.FriendSearchViewSet.as_view({'get': 'list'}),
        name='friend_search',
    ),
    # student / teacher / school admin
    path('student/<int:student_pk>/', student.StudentView.as_view()),
    path('student/<int:student_pk>/lecture/',
        student.StudentLectureView.as_view()
    ),
    path('teacher/<int:teacher_pk>/', teacher.TeacherView.as_view()),
    path('teacher/<int:teacher_pk>/lecture/',
        teacher.TeacherLectureView.as_view()
    ),
    path('school-admin/<int:school_admin_pk>/',
        school_admin.SchoolAdminView.as_view()
    ),
    # User Infromation find and change
    path('username/find/', user.FindUsernameView.as_view()),
    path('password/change/', user.PasswordChangeView.as_view()),
    path('password/reset/', user.PasswordResetView.as_view()),
]
