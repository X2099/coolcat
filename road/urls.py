from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include_docs_urls("road博客")),  # 接口文档
    path('users/', include(('users.urls', 'users'), namespace='users')),
]
