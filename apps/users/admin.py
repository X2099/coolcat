from django.contrib import admin
from .models import User

admin.site.site_header = "road博客管理后台"
admin.site.site_title = "ROAD博客"
admin.site.index_title = "欢迎访问road博客后台系统"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """用户后台管理"""
    list_display = ('username', 'id', 'email', 'mobile', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'mobile')
    list_filter = ('gender', 'birthday')
    ordering = ('id',)
