from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化类"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'birthday', 'gender']


class UserRegSerializer(serializers.ModelSerializer):
    """用户注册序列化类"""
    code = serializers.CharField(required=True, min_length=6, max_length=6, write_only=True, help_text="验证码")
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已经存在")],
                                     help_text="用户名")
    password = serializers.CharField(write_only=True, help_text="密码")

    def validate_code(self, code):
        if code == '888888':
            return code
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'password', 'code']
