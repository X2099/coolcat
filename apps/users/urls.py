from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserAuthViewSet

router = SimpleRouter()
# 用户认证
router.register('auth', UserAuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls))
]
