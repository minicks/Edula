from django.shortcuts import get_object_or_404
from django.test import tag

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_spectacular.utils import (
    extend_schema, OpenApiResponse
)

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from notifications.models import Notification
from . import swagger_schema
from server import basic_swagger_schema
from .user import decode_JWT
from ..models import User, FriendRequest
from ..serializers.friend_request import(
    FriendRequestSerializer, FriendRequestDetailSerializer
)


class FriendRequestViewSet(ViewSet):
    """About friend request
    
    """
    model = FriendRequest
    queryset = FriendRequest.objects.all()
    serializer_classes = {
        'list': FriendRequestDetailSerializer,
        'create': FriendRequestSerializer,
        'update': FriendRequestSerializer,
        'destroy': FriendRequestDetailSerializer,
    }
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except:
            return FriendRequestSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=swagger_schema.schema_serializers['FriendRequestViewSet']['request_list'],
                description=swagger_schema.descriptions['FriendRequestViewSet']['list'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
        },
        description=swagger_schema.descriptions['FriendRequestViewSet']['list']['description'],
        summary=swagger_schema.summaries['FriendRequestViewSet']['list'],
        tags=['친구'],
        examples=[
            basic_swagger_schema.examples[401],
            swagger_schema.examples['FriendRequestViewSet']['request_list'],
        ],
    )
    def list(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        friend_request_data = {
            'requset_send': FriendRequestDetailSerializer(
                FriendRequest.objects.filter(from_user=user.pk), many=True,
            ).data,
            'requset_receive': FriendRequestDetailSerializer(
                FriendRequest.objects.filter(to_user=user.pk), many=True
            ).data,
        }
        return Response(
            friend_request_data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=swagger_schema.schema_serializers['FriendRequestViewSet']['create']['request'],
        responses={
            201: OpenApiResponse(
                response=swagger_schema.schema_serializers['FriendRequestViewSet']['request_list'],
                description=swagger_schema.descriptions['FriendRequestViewSet']['create'][201],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['FriendRequestViewSet']['create']['description'],
        summary=swagger_schema.summaries['FriendRequestViewSet']['create'],
        tags=['친구'],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['FriendRequestViewSet']['request_list'],
            swagger_schema.examples['FriendRequestViewSet']['create']['request'],
        ],
    )
    def create(self, request):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        to_user = get_object_or_404(User, pk=request.data.get('to_user'))
        if FriendRequest.objects.filter(
                from_user=user.pk, to_user=to_user.pk, request_status='RQ',
            ).exists():
                return Response(
                    {'error': 'already exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        friend_request_data = {
            'from_user': user.pk,
            'to_user': to_user.pk,
            'request_status': 'RQ',
        }
        serializer = FriendRequestSerializer(data=friend_request_data)
        if serializer.is_valid():
            serializer.save()
            Notification.objects.create(
                user=to_user,
                notification_type='FQ',
                from_user=user,
            )
            return Response(
                {
                    'requset_send': FriendRequestDetailSerializer(
                        FriendRequest.objects.filter(from_user=user.pk), many=True,
                    ).data,
                    'requset_receive': FriendRequestDetailSerializer(
                        FriendRequest.objects.filter(to_user=user.pk), many=True
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        request=swagger_schema.schema_serializers['FriendRequestViewSet']['update']['request'],
        responses={
            200: OpenApiResponse(
                response=FriendRequestSerializer,
                description=swagger_schema.descriptions['FriendRequestViewSet']['update'][200],
                examples=swagger_schema.examples['FriendRequestViewSet']['update'][200],
            ),
            400: basic_swagger_schema.open_api_response[400],
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['FriendRequestViewSet']['update']['description'],
        summary=swagger_schema.summaries['FriendRequestViewSet']['update'],
        tags=['친구'],
        examples=[
            basic_swagger_schema.examples[400],
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            *swagger_schema.examples['FriendRequestViewSet']['update']['request'],
        ],
    )
    def update(self, request, request_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        friend_request = get_object_or_404(FriendRequest, pk=request_pk, to_user=user.pk)
        status_before = friend_request.request_status
        status_after = request.data['request_status']
        from_user = friend_request.from_user
        to_user = friend_request.to_user
        if status_before != 'RQ' or status_after == 'RQ':
            return Response(
                {'error': 'wrong data'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FriendRequestSerializer(
            instance=friend_request,
            data = {
                'from_user': from_user.pk,
                'to_user': to_user.pk,
                'request_status': status_after,
            }
        )
        if serializer.is_valid():
            serializer.save()
            Notification.objects.create(
                user=from_user,
                notification_type='FQ',
                from_user=to_user,
                content=f'{status_after}',
            )
            FriendRequest.objects.filter(from_user=from_user, to_user=to_user,).delete()
            FriendRequest.objects.filter(from_user=to_user, to_user=from_user,).delete()
            if status_after == 'AC':
                user.friend_list.add(from_user)
                user.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=swagger_schema.schema_serializers['FriendRequestViewSet']['request_list'],
                description=swagger_schema.descriptions['FriendRequestViewSet']['destroy'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['FriendRequestViewSet']['destroy']['description'],
        summary=swagger_schema.summaries['FriendRequestViewSet']['destroy'],
        tags=['친구'],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            swagger_schema.examples['FriendRequestViewSet']['request_list'],
        ]
    )
    def destroy(self, request, request_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        friend_request = get_object_or_404(FriendRequest, pk=request_pk, from_user=user.pk)
        friend_request.delete()
        return Response(
            {
                'requset_send': FriendRequestDetailSerializer(
                    FriendRequest.objects.filter(from_user=user.pk), many=True,
                ).data,
                'requset_receive': FriendRequestDetailSerializer(
                    FriendRequest.objects.filter(to_user=user.pk), many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )
