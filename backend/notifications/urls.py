from django.urls import path

from .views import NotificationViewSet


notification_list = NotificationViewSet.as_view({
    'get': 'list',
})
notification_detail = NotificationViewSet.as_view({
    'patch': 'partial_update',
    'delete': 'destroy',
})
notification_count_all = NotificationViewSet.as_view({
    'get': 'count_all',
})
notification_count_none_read = NotificationViewSet.as_view({
    'get': 'count_none_read',
})

urlpatterns = [
    path(
        '',
        notification_list,
    ),
    path(
        '<int:notification_pk>/',
        notification_detail,
    ),
    path(
        'count/',
        notification_count_none_read,
    ),
    path(
        'count/all/',
        notification_count_all,
    ),
]
