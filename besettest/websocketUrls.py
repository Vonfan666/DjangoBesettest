#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月30日22时04分52秒

from django.conf.urls import url
from case  import consumers

urlpatterns = [
    # url(r"a/b/", consumers.EchoConsumer, name="DebugCase"),  # 用例调试
    url(r"ws/users/case_run/", consumers.RunCase, name="RunCases"),  # 执行接口下所有用例
    url(r"ws/users/logList/", consumers.selectLog, name="selectLog"),  # 执行单个接口下的所有用例

    # path('ws/<str:username>/',MessagesConsumer) # 如果是传参的路由在连接中获取关键字参数方法：self.scope['url_route']['kwargs']['username']
]

