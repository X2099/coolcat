# -*- coding:utf-8 -*-
# @Time : 2019/11/8 下午5:57
# @Author: 王国强
# @File : serializers.py

from rest_framework import serializers

from operation.models import LeavingMessage


class LeavingMsgSerializer(serializers.ModelSerializer):
    """留言序列化"""

    author_info = serializers.SerializerMethodField(label="作者姓名", read_only=True)

    class Meta:
        model = LeavingMessage
        fields = '__all__'

    def get_author_info(self, instance):
        """
        获取作者信息
        :param instance:LeavingMessage实例
        """
        data = {
            'name': instance.author.username,
            'avatar': instance.author.avatar
        }
        return data
