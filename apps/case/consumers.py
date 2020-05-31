#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月30日22时45分30秒

from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from users.models import UserProfile
import json,time,logging
from . import models,serializers
from case.libs.toRequests import InRequests
from libs.api_response import APIResponse
from  rest_framework.views import APIView,status

logger =  logging.getLogger("log")
#
# class EchoConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def receive(self,text_data=None, bytes_data=None):
#         print(text_data)
#
#         # user = self.scope['user']  # 获取当前用户，没有登录显示匿名用户
#         # path = self.scope['path']  # Request请求的路径，HTTP，WebSocket
#         # print(user,path)
#         # ORM 同步代码 假如要查询数据库
#         # user = UserProfile.objects.filter(username=username)
#         a={"cap":1}
#         for  b   in range(1,20):
#             a["cap"]=b
#             time.sleep(1)
#             self.send(json.dumps(a))
#
#     def disconnect(self, close_code):
#         pass

class RunCase(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        user = self.scope['user']  # 获取当前用户，没有登录显示匿名用户
        path = self.scope['path']  # Request请求的路径，HTTP，WebSocket
        print(user,path)
        print(text_data)
        print(type(text_data))
        listId=json.loads(text_data)
        for id in listId:
            # 1封装环境变量取值---返回url  headers data

            obj = models.CaseFile.objects.select_related("userId", "CaseGroupId", "postMethod", "dataType",
                                                         "environmentId").filter(id=id)
            serializersObj = serializers.S_CaseRun(obj, many=True)
            res_data = serializersObj.data
            res_data = json.loads(json.dumps(res_data))
            res_data = res_data[0]
            logger.info("单位开始执行")
            s = InRequests(res_data["postMethod"], res_data["dataType"], res_data["environmentId"], res_data["name"])
            res= s.run(res_data["attr"], res_data["headers"], res_data["data"])

            # try:
            #     resc=json.loads(json.dumps(res))
            #     print(resc)
            # except:
            #     pass
            # print(res)
            print(res)
            logger.info("单位执行结束")
            self.send(json.dumps(res))
    def disconnect(self, close_code):
        pass

from datetime import date, datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

