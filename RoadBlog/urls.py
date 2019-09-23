from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs', include_docs_urls("road博客", authentication_classes=[], permission_classes=[])),  # 接口文档
    path('api/', include(('users.urls', 'users'), namespace='users')),
    path('api/', include(('blogs.urls', 'blogs'), namespace='articles')),
]
