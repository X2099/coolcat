import datetime

from rest_framework import serializers

from .models import Article, Category, Tag
from users.models import User


class CategorySubSerializer(serializers.ModelSerializer):
    """子分类序列化"""

    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    """文章分类序列化"""
    subs = CategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'owner', 'subs')
        extra_kwargs = {
            'parent': {'write_only': True},
            'owner': {'write_only': True}
        }


class TagSerializer(serializers.ModelSerializer):
    """标签序列化类"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'owner')


class ArticleCreateSerializer(serializers.ModelSerializer):
    """创建文章序列化类"""

    class Meta:
        model = Article
        fields = ('title', 'body', 'status', 'pub_time', 'author', 'category', 'tags', 'status', 'cover_image')

    def validate_cover_image(self, file):
        """对上传的图片重命名"""
        uid = self.context.get('request').user.id
        file_suffix = file.name.split('.')[-1]
        file_name = 'COVER' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '%09d' % uid + '.' + file_suffix
        file.name = file_name
        return file


class AuthorSerializer(serializers.ModelSerializer):
    """文章作者序列化类"""

    class Meta:
        model = User
        fields = ('id', 'username')


class CategoryArticleSerializer(serializers.ModelSerializer):
    """文章所属类序列化类"""

    class Meta:
        model = Category
        fields = ('id', 'name')


class TagArticleSerializer(serializers.ModelSerializer):
    """文章标签序列化类"""

    class Meta:
        model = Tag
        fields = ('id', 'name',)


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化类"""
    author = AuthorSerializer()
    category = CategoryArticleSerializer()
    tags = TagArticleSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'pub_time', 'author', 'category', 'tags', 'update_time', 'cover_image')


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化类"""
    author = AuthorSerializer()
    category = CategoryArticleSerializer()
    tags = TagArticleSerializer(many=True)

    class Meta:
        model = Article
        fields = ('title', 'body', 'pub_time', 'author', 'category', 'tags', 'views', 'cover_image')
