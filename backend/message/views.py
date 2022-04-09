from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from drf_spectacular.utils import extend_schema

from accounts.views.user import decode_JWT
from accounts.models import User
from .models import Message
from .serializers import MessageSerializer

# Create your views here.
class MessagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageViewSet(ViewSet):
    """Message View Set
    """
    model = Message
    serializer_class = MessageSerializer
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    pagination_class = MessagePagination

    @extend_schema(
        tags=['쪽지',]
    )
    def list(self, request, user_pk):
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user_pk == 0:
            messages = Message.objects.filter(
                user=user.pk, send=False).order_by('-pk')
        elif user_pk == user.pk:
            messages = Message.objects.filter(
                user=user.pk, send=True).order_by('-pk')
        else:
            messages = Message.objects.filter(
                user=user.pk, from_user=user_pk
            ).order_by('-pk')
        paginator = MessagePagination()
        serializer = MessageSerializer(
            paginator.paginate_queryset(messages, request), 
            many=True
        )
        augmented_serializer = {
            'total_count': messages.count(),
            'page_count': len(serializer.data),
            'messages': serializer.data,
        }
        return Response(
            augmented_serializer,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        tags=['쪽지',]
    )
    def create(self, request, user_pk):
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        another_user = get_object_or_404(User, pk=user_pk)
        content = request.data.get('content', None)
        if content is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        Message.objects.create(
            user=user,
            from_user=another_user,
            content=content,
            send=True,
            read=False
        )
        Message.objects.create(
            user=another_user,
            from_user=user,
            content=content,
            send=False
        )
        return Response(
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['쪽지',]
    )
    def partial_update(self, request, user_pk, message_pk):
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        another_user = get_object_or_404(User, pk=user_pk)
        if message_pk == 0:
            messages = Message.objects.filter(
                user=user, from_user=another_user, read=False
            )
            for message in messages:
                message.read = True
                message.save()
        else:
            message = get_object_or_404(
                Message, 
                pk=message_pk,
                user=user,
                from_user=another_user
            )
            message.read = True
            message.save()
        return Response(
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['쪽지',]
    )
    def destroy(self, request, user_pk, message_pk):
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        another_user = get_object_or_404(User, pk=user_pk)
        if message_pk == 0:
            Message.objects.filter(
                user=user, from_user=another_user
            ).delete()
        else:
            message = get_object_or_404(
                Message, 
                pk=message_pk,
                user=user,
                from_user=another_user
            )
            message.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        tags=['쪽지',]
    )
    def count_all(self, request):
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                'count_all': Message.objects.filter(
                user=user, send=False
                ).count(),
                'count': Message.objects.filter(
                user=user, send=False, read=False
                ).count(),
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        tags=['쪽지',]
    )
    def count_user_all(self, request, user_pk):
        user = decode_JWT(request)
        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        another_user = get_object_or_404(User, pk=user_pk)
        return Response(
            {
                'count_all': Message.objects.filter(
                user=user, from_user=another_user, send=False
                ).count(),
                'count': Message.objects.filter(
                user=user, from_user=another_user, send=False, read=False
                ).count(),
            },
            status=status.HTTP_200_OK
        )
