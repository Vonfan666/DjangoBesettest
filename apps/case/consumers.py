#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月30日22时45分30秒

from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from users.models import UserProfile
import json,time
class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self,text_data=None, bytes_data=None):
        print(text_data)

        # user = self.scope['user']  # 获取当前用户，没有登录显示匿名用户
        # path = self.scope['path']  # Request请求的路径，HTTP，WebSocket
        # print(user,path)
        # ORM 同步代码 假如要查询数据库
        # user = UserProfile.objects.filter(username=username)
        a={"cap":1}
        for  b   in range(1,20):
            a["cap"]=b
            time.sleep(1)
            self.send(json.dumps(a))

    def disconnect(self, close_code):
        pass