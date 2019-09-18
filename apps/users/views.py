from random import choice
import re

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import UserDetailSerializer, UserRegSerializer

User = get_user_model()


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
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(methods=['GET'], detail=False)
    def send_code(self, request):
        """发送验证码"""

        to_email = request.query_params.get('email')
        if not to_email:
            return Response({'msg': "缺少参数email"}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", to_email):
            return Response({'msg': "参数email格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        # 随机生成验证码
        seeds = '0123456789'
        code = []
        for i in range(6):
            code.append(choice(seeds))
        code = ''.join(code)
        # 把验证码存入redis
        cache.set(to_email, code, 60 * 5)
        try:
            result = send_mail(subject="road博客验证码",
                               message=f"您的验证码是：{code}",
                               from_email=settings.DEFAULT_FROM_EMAIL,
                               recipient_list=[to_email])
            if result == 1:
                return Response({'msg': "验证码已发送到您的邮箱"})
            else:
                return Response({'msg': "验证码发送失败"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
