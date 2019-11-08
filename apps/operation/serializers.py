# -*- coding:utf-8 -*-
# @Time : 2019/11/8 下午5:57
# @Author: 王国强
# @File : serializers.py

from rest_framework import serializers

from operation.models import LeavingMessage


class LeavingMsgSerializer(serializers.ModelSerializer):
    """留言序列化"""

    author_name = serializers.SerializerMethodField(label="作者姓名", read_only=True)

    class Meta:
        model = LeavingMessage
        fields = '__all__'

    def get_author_name(self, instance):
        """
        获取作者姓名
        :param instance:LeavingMessage实例
        """
        return instance.author.username
