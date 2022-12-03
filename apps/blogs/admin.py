from django.contrib import admin
from .models import Article, Category, Tag


class ArticleAdmin(admin.ModelAdmin):
    """文章后台管理"""
    list_display = ('title', 'id', 'author', 'category', 'pub_time')
    search_fields = ('title',)
    list_filter = ('author', 'category')
    date_hierarchy = 'pub_time'
    filter_horizontal = ('tags',)


class CategoryAdmin(admin.ModelAdmin):
    """文章分类管理"""
    list_display = ('name', 'id', 'parent', 'owner')
    list_filter = ('owner',)


class TagAdmin(admin.ModelAdmin):
    """标签后台管理"""
    list_display = ('name', 'id', 'owner')
    list_filter = ('owner',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
