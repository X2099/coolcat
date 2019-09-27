from rest_framework import serializers
from .models import Article, Category, Tag


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


class ArticleSerializer(serializers.ModelSerializer):
    """文章序列化类"""

    class Meta:
        model = Article
        fields = ('title', 'body', 'pub_time', 'author', 'category', 'tags')
