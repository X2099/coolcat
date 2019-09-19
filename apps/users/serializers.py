from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
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
    password1 = serializers.CharField(write_only=True, help_text="密码")
    password2 = serializers.CharField(write_only=True, help_text="校验密码")
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message="该邮箱已经注册")],
                                   help_text="邮箱")

    def validate_code(self, code):
        email = self.initial_data.get('email')
        verify_code = cache.get(email)
        if verify_code:
            cache.delete(email)
            if code == verify_code:
                return code
            else:
                raise serializers.ValidationError("验证码错误，请重试")
        else:
            raise serializers.ValidationError("验证码已过期，请重新发送")

    def velidate_password1(self, password1):
        if password1 == self.initial_data.get('password2'):
            return password1
        else:
            raise serializers.ValidationError("两次密码不一致")

    def validate(self, attrs):
        del attrs['code']
        del attrs['password2']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'code', 'email']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   password=make_password(validated_data['password1']),
                                   email=validated_data['email'])
        return user
