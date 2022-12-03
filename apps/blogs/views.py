import datetime
import os

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
# from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Article, Category, Tag
from .serializers import (
    ArticleCreateSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    CategorySerializer,
    TagSerializer
)


class CategoryViewSet(ModelViewSet):
    """文章分类"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        获取数据查询集
        """
        return Category.objects.filter(owner=self.request.user, parent=None)


class TagViewSet(ModelViewSet):
    """标签"""
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        获取数据查询集
        """
        return Tag.objects.filter(owner=self.request.user)


class ArticleViewSet(ModelViewSet):
    """文章"""
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.order_by('title', '-pub_time')

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

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
        if self.action == 'list' or self.action == 'retrieve':
            context.pop('request')
        return context

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

    @action(methods=['post'], detail=False)
    def upload(self, request):
        """
        上传图片
        """
        file_data = request.data.get('image')
        file_suffix = file_data.name.split('.')[-1]
        file_name = 'IMAGE' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + (
                '%09d' % request.user.id) + '.' + file_suffix
        try:
            with open('static/media/inner/' + file_name, 'wb') as f:
                f.write(file_data.read())
        except Exception as e:
            print(e)
            return Response({'msg': "上传图片失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        url = settings.STATIC_HTTP + 'image/inner/' + file_name
        return Response(url)

    @action(methods=['delete'], detail=False)
    def remove(self, request):
        """
        删除图片
        """
        article_id = request.query_params.get('article_id')
        img_url = request.query_params.get('url')
        if article_id:
            article = Article.objects.get(id=article_id)
            cover_name = article.cover_image.name
            if cover_name:
                article.cover_image = None
                article.save()
                os.remove(settings.MEDIA_ROOT + '/' + cover_name)
        else:
            image_name = img_url.split('/')[-1]
            os.remove('static/media/inner/' + image_name)
        return Response({'msg': "图片已删除"})
