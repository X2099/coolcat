from rest_framework.viewsets import ModelViewSet
from .models import Article, Category, Tag
from .serializers import ArticleSerializer, CategorySerializer, TagSerializer


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
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        else:
            return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []
        else:
            return [permission() for permission in self.permission_classes]
