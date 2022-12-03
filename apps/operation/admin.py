from django.contrib import admin
from .models import LeavingMessage


class LeavingMessageAdmin(admin.ModelAdmin):
    """留言后台管理"""

    list_display = ('id', 'body', 'author')


admin.site.register(LeavingMessage, LeavingMessageAdmin)
