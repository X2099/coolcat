from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import UserDetailSerializer, UserRegSerializer

User = get_user_model()


class CodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """发送验证码"""
    pass


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """用户注册和详情"""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer
        else:
            return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        else:
            return [permissions.IsAuthenticated()]
