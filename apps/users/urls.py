from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserAuthViewSet

router = SimpleRouter()
# 用户认证
router.register('auth', UserAuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('login', obtain_jwt_token)  # 登录认证
]
