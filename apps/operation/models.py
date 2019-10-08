from django.conf import settings
from django.db import models

from blogs.models import Article

User = settings.AUTH_USER_MODEL


class BaseModel(models.Model):
    """
    基础抽象类
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        abstract = True


class LeavingMessage(BaseModel):
    """留言"""
    body = models.TextField(verbose_name="留言内容")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='leaving_msgs', verbose_name="作者")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name="被留言者")
    parent = models.ForeignKey('self', related_name='sub_msgs', on_delete=models.CASCADE, verbose_name="上级留言")
    is_enable = models.BooleanField(default=True, verbose_name="是否显示")


class Comment(BaseModel):
    """评论"""
    body = models.TextField(verbose_name="评论内容")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments', verbose_name="评论者")
    target = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="被评论文章")
    parent = models.ForeignKey('self', related_name='sub_msgs', on_delete=models.CASCADE, verbose_name="上级评论")
    is_enable = models.BooleanField(default=True, verbose_name="是否显示")


class Collection(BaseModel):
    """收藏"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="被收藏文章")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="收藏者")


class Follow(BaseModel):
    """关注"""
    agent = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="追随者")
    target = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE, verbose_name="被关注者")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
