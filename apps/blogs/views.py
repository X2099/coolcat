from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Article, Category, Tag
from .serializers import (
    ArticleCreateSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    CategorySerializer,
    TagSerializer
)


class CategoryViewSet(CacheResponseMixin, ModelViewSet):
    """文章分类"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        获取数据查询集
        """
        return Category.objects.filter(owner=self.request.user, parent=None)


class TagViewSet(CacheResponseMixin, ModelViewSet):
    """标签"""
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        获取数据查询集
        """
        return Tag.objects.filter(owner=self.request.user)


class ArticleViewSet(CacheResponseMixin, ModelViewSet):
    """文章"""
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all().order_by('-pub_time')

    def get_queryset(self):
        """
        根据不同的请求方式分别获取queryset
        """
        if self.action == 'list' or self.action == 'retrieve':
            return self.queryset
        else:
            return self.queryset.filter(author=self.request.user)

    def get_serializer_class(self):
        """
        根据不同的请求方式获取不同的serializer_class
        """
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        else:
            return ArticleCreateSerializer

    def get_authenticators(self):
        """
        根据不同的请求方式获取不同的认证权限
        """
        if self.request.method == 'GET':
            return []
        else:
            return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
        """
        根据不同的请求方式获取不同的认证权限
        """
        if self.action == 'list' or self.action == 'retrieve':
            return []
        else:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        """
        重写创建文章方法，添加pub_time字段数据
        """
        if request.data.get('status', 'p') == 'p':
            request.data.update({'pub_time': timezone.now()})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        重写更新文章方法，添加pub_time字段数据
        """
        if request.data.get('status', 'p') == 'p':
            request.data.update({'pub_time': timezone.now()})
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        文章列表
        """
        author_id = request.query_params.get('author', None)
        article_status = request.query_params.get('status', None)
        if author_id:
            queryset = self.queryset.filter(author_id=author_id)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        if article_status == 'd':
            queryset = queryset.filter(status='d', author_id=author_id)
        else:
            queryset = queryset.filter(status='p')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
