from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """基础抽象类"""
    create_time = models.DateTimeField(auto_created=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class Article(BaseModel):
    """
    文章模型类
    """
    title = models.CharField(max_length=200, verbose_name="标题")
    body = models.TextField(max_length=5000, verbose_name="正文")
    pub_time = models.DateTimeField(null=True, blank=True, verbose_name="发布时间")
    status = models.CharField(max_length=1, choices=(('d', "草稿"), ('p', "发布")), default='p', verbose_name="文章状态")
    commit_status = models.BooleanField(default=True, verbose_name="是否可以评论")
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    type = models.BooleanField(default=False, verbose_name="是否为封面文章")
    order_score = models.IntegerField(default=0, verbose_name="排序比重")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.DO_NOTHING,
                               verbose_name="作者")
    category = models.ForeignKey('Category', related_name='articles', on_delete=models.DO_NOTHING, verbose_name="所属分类")
    tags = models.ManyToManyField('Tag', related_name='articles', blank=True, verbose_name="标签")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-update_time']


class Category(BaseModel):
    """
    文章分类
    """
    name = models.CharField(max_length=40, verbose_name="分类名称")
    parent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="父级分类")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name
        ordering = ['name']


class Tag(BaseModel):
    """
    文章标签
    """
    name = models.CharField(max_length=40, unique=True, verbose_name="标签名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name
        ordering = ['name']
