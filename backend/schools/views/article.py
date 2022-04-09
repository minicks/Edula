from django.shortcuts import get_object_or_404

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from accounts.views.user import decode_JWT
from server import basic_swagger_schema
from . import swagger_schema
from ..models import Lecture, Article
from ..serializers import ArticleSerializer, ArticleDetailSerializer
from .lecture import verify_user_lecture


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleViewSet(ViewSet):
    """About article from lecture
    
    """
    model = Article
    queryset = Article.objects.all()
    serializer_classes = {
        'list': ArticleSerializer,
        'create': ArticleSerializer,
        'retrieve': ArticleDetailSerializer,
        'update': ArticleSerializer,
        'destroy': ArticleSerializer,
    }
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]
    pagination_class = ArticlePagination
    
    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except:
            return ArticleSerializer
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=ArticleSerializer,
                description=swagger_schema.descriptions['ArticleViewSet']['list'][200],
                examples=swagger_schema.examples['ArticleViewSet']['article_list'],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ArticleViewSet']['list']['description'],
        summary=swagger_schema.summaries['ArticleViewSet']['list'],
        tags=['게시판',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def list(self, request, lecture_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif not Lecture.objects.filter(pk=lecture_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif not verify_user_lecture(user, lecture_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        articles = Article.objects.filter(lecture=lecture_pk).order_by('-pk')
        paginator = ArticlePagination()
        serializer = ArticleSerializer(
            paginator.paginate_queryset(articles, request), 
            many=True,
        )
        augmented_serializer = {
            'totla_count': articles.count(),
            'page_count': len(serializer.data),
            'articles': list(serializer.data),
        }
        return Response(augmented_serializer)
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=ArticleSerializer,
                description=swagger_schema.descriptions['ArticleViewSet']['create'][201],
                examples=swagger_schema.examples['ArticleViewSet']['article'],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ArticleViewSet']['create']['description'],
        summary=swagger_schema.summaries['ArticleViewSet']['create'],
        tags=['게시판',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            *swagger_schema.examples['ArticleViewSet']['create_article'],
        ]
    )
    def create(self, request, lecture_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif not Lecture.objects.filter(pk=lecture_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif not verify_user_lecture(user, lecture_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        notice = request.data.get('notice', False)
        if notice:
            if user.status == 'ST':
                notice = False
        data = {
            'title': request.data.get('title', None),
            'content': request.data.get('content', None),
            'notice': notice,
            'writer': user.pk,
            'lecture': lecture_pk,
        }
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=ArticleDetailSerializer,
                description=swagger_schema.descriptions['ArticleViewSet']['retrieve'][200],
                examples=swagger_schema.examples['ArticleViewSet']['article_detail'],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ArticleViewSet']['retrieve']['description'],
        summary=swagger_schema.summaries['ArticleViewSet']['retrieve'],
        tags=['게시판',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def retrieve(self, request, lecture_pk, article_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif not Lecture.objects.filter(pk=lecture_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif not verify_user_lecture(user, lecture_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        article = get_object_or_404(
            Article.objects.filter(lecture=lecture_pk), 
            id=article_pk,
        )
        serialier = ArticleDetailSerializer(article)
        return Response(
            serialier.data,
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=ArticleSerializer,
                description=swagger_schema.descriptions['ArticleViewSet']['update'][201],
                examples=swagger_schema.examples['ArticleViewSet']['article'],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ArticleViewSet']['update']['description'],
        summary=swagger_schema.summaries['ArticleViewSet']['update'],
        tags=['게시판',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
            *swagger_schema.examples['ArticleViewSet']['create_article'],
        ]
    )
    def update(self, request, lecture_pk, article_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif not Lecture.objects.filter(pk=lecture_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif not verify_user_lecture(user, lecture_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        article = get_object_or_404(
            Article.objects.filter(lecture=lecture_pk), 
            id=article_pk,
        )
        if article.writer.pk != user.pk:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        notice = request.data.get('notice', article.notice)
        if notice:
            if user.status == 'ST':
                notice = False
        data = {
            'title': request.data.get('title', article.title),
            'content': request.data.get('content', article.content),
            'notice': notice,
            'writer': user.pk,
            'lecture': lecture_pk,
        }
        serializer = ArticleSerializer(
            instance=article,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=ArticleSerializer,
                description=swagger_schema.descriptions['ArticleViewSet']['destroy'][200],
                examples=swagger_schema.examples['ArticleViewSet']['destroy'][200],
            ),
            401: basic_swagger_schema.open_api_response[401],
            404: basic_swagger_schema.open_api_response[404],
        },
        description=swagger_schema.descriptions['ArticleViewSet']['destroy']['description'],
        summary=swagger_schema.summaries['ArticleViewSet']['destroy'],
        tags=['게시판',],
        examples=[
            basic_swagger_schema.examples[401],
            basic_swagger_schema.examples[404],
        ]
    )
    def destroy(self, request, lecture_pk, article_pk):
        user = decode_JWT(request)
        if user == None:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif not Lecture.objects.filter(pk=lecture_pk).exists():
            return Response(
                {'error': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif not verify_user_lecture(user, lecture_pk):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        article = get_object_or_404(
            Article.objects.filter(lecture=lecture_pk), 
            id=article_pk,
        )
        if article.writer.pk == user.pk or user.status in ['TE', 'SA']:
            article.delete()
            return Response(
                {'OK': 'deleted'},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
