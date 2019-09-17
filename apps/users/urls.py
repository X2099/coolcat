from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet

router = SimpleRouter()
# 用户注册
router.register('', UserViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls))
]
