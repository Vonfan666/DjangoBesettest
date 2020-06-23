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
import time
from libs.public import StartMethod
from log.logFile import logger as logs

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
        listId=json.loads(text_data)
        listIdSort=[]

        for id in listId:
            caseName=models.CaseFile.objects.get(id=id).name
            order=models.CaseFile.objects.get(id=id).order
            start=StartMethod(caseName, "23", "3")
            start()
            self.logger = logs(self.__class__.__module__)
            listIdSort.append((order,id))
        listId=sorted(listIdSort,key=lambda x:x[0])
        #开始执行的时候插入数据--但是状态还是执行中-- 前端查看数据时用websockt 五秒获取一次状态---获取之后自动断开
        for id in listId:
            # 1封装环境变量取值---返回url  headers data
            id=id[1]
            obj = models.CaseFile.objects.select_related("userId", "CaseGroupId", "postMethod", "dataType",
                                                         "environmentId").filter(id=id)
            serializersObj = serializers.S_CaseRun(obj, many=True)
            res_data = serializersObj.data
            res_data = json.loads(json.dumps(res_data))
            res_data = res_data[0]
            self.logger.info("单位开始执行")
            s = InRequests(res_data["postMethod"], res_data["dataType"], res_data["environmentId"], res_data["name"],self.logger)
            res= s.run(res_data["attr"], res_data["headers"], res_data["data"])
            self.logger.info("单位执行结束")
            self.send(json.dumps(res))
            time.sleep(1)
            #执行完成之后把状态改成执行完成-
    def disconnect(self, close_code):
        pass



