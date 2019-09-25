from rest_framework import serializers
from .models import Article, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """分章分类序列化"""

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class TagSerializer(serializers.ModelSerializer):
    """标签序列化类"""

    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    """文章序列化类"""

    class Meta:
        model = Article
        fields = ['title', 'body', 'pub_time', 'author', 'category', 'tags']
