from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from drf_spectacular.utils import extend_schema

from accounts.views.user import decode_JWT
from .models import Notification
from .serializers import NotificationSerializer
from . import swagger_schema

# Create your views here.
class NotificationPagination(PageNumberPagination):
    """Notification Pagination
    기본 한 페이지 10개, 최대 100개로 요청 가능
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class NotificationViewSet(ViewSet):
    """알림
    """
    model = Notification
    serializer_class = NotificationSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    pagination_class = NotificationPagination

    @swagger_schema.notification_view_set_list
    def list(self, request):
        """알림 목록 조회
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        notifications = Notification.objects.filter(user=user.pk).order_by('-pk')
        paginaotr = NotificationPagination()
        serializer = NotificationSerializer(
            paginaotr.paginate_queryset(notifications, request),
            many=True
        )
        augmented_serializer = {
            'total_count': notifications.count(),
            'page_count': len(serializer.data),
            'notifications': serializer.data,
        }
        return Response(
            augmented_serializer,
            status=status.HTTP_200_OK,
        )

    @swagger_schema.notification_view_set_partial_update
    def partial_update(self, request, notification_pk):
        """알림 읽음 처리
        notification_pk : int
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if notification_pk == 0:
            notifications = Notification.objects.filter(user=user.pk)
            for notification in notifications:
                notification.read = True
                notification.save()
        else:
            notification = get_object_or_404(Notification, pk=notification_pk, user=user.pk)
            notification.read = True
            notification.save()
        return Response(
            status=status.HTTP_201_CREATED,
        )

    @swagger_schema.notification_view_set_destroy
    def destroy(self, request, notification_pk):
        """알림 삭제
        notification_pk : int
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if notification_pk == 0:
            Notification.objects.filter(user=user.pk).delete()
        else:
            notification = get_object_or_404(Notification, pk=notification_pk)
            notification.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @swagger_schema.notification_view_set_count
    def count_all(self, request):
        """전체 알림 개수
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                'count': Notification.objects.filter(user=user.pk).count()
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        tags=['알림',]
    )
    def count_none_read(self, request):
        """읽지 않은 알림 개수
        """
        user = decode_JWT(request)
        if user is None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                'count': Notification.objects.filter(user=user.pk, read=False).count()
            },
            status=status.HTTP_200_OK
        )
