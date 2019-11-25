from random import choice
import re

from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .serializers import UserDetailSerializer, UserRegSerializer

User = get_user_model()


class UserAuthViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """用户认证"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer
        else:
            return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'logout':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def get_object(self):
        return self.request.user

    @action(methods=['POST'], detail=False)
    def send_code(self, request):
        """发送验证码"""

        to_email = request.data.get('email')
        if not to_email:
            return Response({'msg': "缺少参数email"}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", to_email):
            return Response({'msg': "参数email格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        if cache.get(to_email):
            return Response({'msg': "请求太频繁，请稍后再试"}, status=status.HTTP_403_FORBIDDEN)
        # 随机生成验证码
        seeds = '0123456789'
        code = []
        for i in range(6):
            code.append(choice(seeds))
        code = ''.join(code)
        # 发送邮件验证码
        try:
            result = send_mail(subject="road博客验证码",
                               message=f"您的验证码是：{code}",
                               from_email=settings.DEFAULT_FROM_EMAIL,
                               recipient_list=[to_email])
            if result == 1:
                # 把验证码存入redis
                cache.set(to_email, code, 60 * 10)
                return Response({'msg': "验证码已发送到您的邮箱"})
            else:
                return Response({'msg': "验证码发送失败"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail=False)
    def check(self, request):
        """检查用户名或邮箱是否已经注册"""
        username = request.data.get('username')
        email = request.data.get('email')
        if username:
            if User.objects.filter(username=username).exists():
                return Response({'msg': "该用户名已经注册"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': "OK"})
        elif email:
            if User.objects.filter(email=email).exists():
                return Response({'msg': "该邮箱已经注册"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': "OK"})
        else:
            return Response({'msg': "缺少参数"}, status=status.HTTP_403_FORBIDDEN)
