from rest_framework.viewsets import ModelViewSet
from .models import Article, Category, Tag
from .serializers import ArticleCreateSerializer, ArticleListSerializer, ArticleDetailSerializer, \
    CategorySerializer, TagSerializer


class CategoryViewSet(ModelViewSet):
    """文章分类"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user, parent=None)


class TagViewSet(ModelViewSet):
    """标签"""
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)


class ArticleViewSet(ModelViewSet):
    """文章"""
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        """
        根据不同的请求方式分别获取queryset
        """
        if self.action == 'list' or self.action == 'retrieve':
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)

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
