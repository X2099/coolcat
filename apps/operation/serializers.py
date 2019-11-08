# -*- coding:utf-8 -*-
# @Time : 2019/11/8 下午5:57
# @Author: 王国强
# @File : serializers.py

from rest_framework import serializers

from operation.models import LeavingMessage


class LeavingMsgSerializer(serializers.ModelSerializer):
    """留言序列化"""

    author = serializers.StringRelatedField(label="作者姓名")

    class Meta:
        model = LeavingMessage
        fields = '__all__'
