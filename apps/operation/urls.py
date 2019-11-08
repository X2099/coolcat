# -*- coding:utf-8 -*-
# @Time : 2019/11/8 下午5:56
# @Author: 王国强
# @File : urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeavingMsgViewSet

router = DefaultRouter()
router.register('leavingmsgs', LeavingMsgViewSet, basename='leavingmsg')

urlpatterns = [
    path('', include(router.urls))
]
