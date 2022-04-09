from django.urls import path
from .views import MessageViewSet


message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
message_detail = MessageViewSet.as_view({
    'patch': 'partial_update',
    'delete': 'destroy',
})
message_all = MessageViewSet.as_view({
    'get': 'count_all'
})
message_user_all = MessageViewSet.as_view({
    'get': 'count_user_all'
})


urlpatterns = [
    path('<int:user_pk>/', message_list,),
    path('<int:user_pk>/<int:message_pk>/', message_detail),
    path('count/', message_all,),
    path('count/<int:user_pk>/', message_user_all,),
]
