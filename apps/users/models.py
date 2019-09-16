from django.db import models


class User(AbstractUser):
    """
    用户模型类
    """
    id = models.Charfield(primary_key=True, verbose_name="用户ID")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="最近登录时间")
