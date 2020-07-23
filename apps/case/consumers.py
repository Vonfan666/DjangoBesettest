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
from django_redis import get_redis_connection  as conn

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
        # self.logger =  logging.getLogger("log")
        self.logRedis = conn("log")

    def receive(self, text_data=None, bytes_data=None):
        print(text_data,"上面的")
        user = self.scope['user']  # 获取当前用户，没有登录显示匿名用户
        path = self.scope['path']  # Request请求的路径，HTTP，WebSocket
        textObj=json.loads(text_data)
        listId=textObj["idList"]
        self.userId=textObj["userId"]
        self.interface=textObj["interface"]
        self.count=len(listId)
        listIdSort=[]
        n=1
        self.l={
            "results":[],
            "logList":[],
        }
        for id in listId:

            order=models.CaseFile.objects.get(id=id).order

            listIdSort.append((order,id))
        listId=sorted(listIdSort,key=lambda x:x[0])
        #开始执行的时候插入数据--但是状态还是执行中-- 前端查看数据时用websockt 五秒获取一次状态---获取之后自动断开
        for id in listId:

            # 1封装环境变量取值---返回url  headers data
            id=id[1]
            caseName=models.CaseFile.objects.get(id=id).name

            start = StartMethod(self.userId,self.interface)
            start()
            self.logger = logs(self.__class__.__module__)
            obj = models.CaseFile.objects.select_related("userId", "CaseGroupId", "postMethod", "dataType",
                                                         "environmentId").filter(id=id)
            serializersObj = serializers.S_CaseRun(obj, many=True)
            res_data = serializersObj.data
            res_data = json.loads(json.dumps(res_data))
            res_data = res_data[0]
            self.logger.info("%s>>>第{{%s}}个单位开始执行"%(caseName,n))
            s = InRequests(res_data["postMethod"], res_data["dataType"], res_data["environmentId"], res_data["name"],self.logger)
            res= s.run(res_data["attr"], res_data["headers"], res_data["data"])
            self.logger.info("%s>>>第{{%s}}个单位执行结束"%(caseName,n))
            self.send(json.dumps(res))
            n=n+1
            self.l["results"].append(res)
        self.close()
    def disconnect(self, close_code):
        #断开时清除redis数据
        redisListLog=self.logRedis.lrange("log:%s_%s" % (self.userId, self.interface), 0, -1)  # 存到数据库
        for log in redisListLog:
            self.l["logList"].append(log.decode("utf8"))
        userId = UserProfile.objects.get(id=self.userId)
        models.CaseResult.objects.create(result=self.l, type=2, c_id=self.interface, userId=userId)  #批量执行type传2--
        self.logRedis.delete("log:%s_%s"%(self.userId,self.interface))  #删除key
        print("断开")

class selectLog(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.logRedis = conn("log")
        self.len=0
    def receive(self, text_data=None, bytes_data=None):
        textObj = json.loads(text_data)
        listId = textObj["idList"]
        self.userId = textObj["userId"]
        self.interface = textObj["interface"]
        self.count = len(listId)
        self.indexStart=0
        while  1:
            flag=0
            redisListLog=self.logRedis.lrange("log:%s_%s"%(self.userId,self.interface), self.indexStart, -1)
            indexEnd=len(redisListLog)
            self.indexStart = self.indexStart+indexEnd
            for log  in  redisListLog:
                if "第{{%s}}个单位执行结束"%self.count  in  log.decode("utf8"):
                    log = log.decode("utf8")
                    self.send(json.dumps(log))
                    flag=1
                    break
                else:
                    log=log.decode("utf8")
                    self.send(json.dumps(log))
            if  flag==1:
                self.close()
                break
            time.sleep(0.1)
    def disconnect(self, close_code):
        print("断开连接")

class runCaseSelectLog(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.redisLog=conn()

    def receive(self, text_data=None, bytes_data=None):

        data=json.loads(text_data)
        startTime=time.time()
        Start=0
        msg={
            "log":"",
            "status":None
        }
        while True:
            try:
                res=self.redisLog.lrange("log:%s"%data["log_id"],Start,-1)
                resStatus=self.redisLog.get("status:%s"%data["log_id"])
                msg["status"]=json.loads(resStatus)
                if res:
                    listLog=list(map(lambda x:x.decode("utf8"),res))
                    print(json.dumps(listLog))
                    for  log  in listLog:
                        msg["log"]=log
                        self.send(json.dumps(msg))
                        if log=="结束":
                            break

                    Start = len(res) + Start
                    continue
                else:
                    endTime=time.time()
                    if endTime-startTime<20:
                        time.sleep(0.5)
                        continue
                    else:
                        break
            except:
                continue
        self.close()
    def disconnect(self, code):
        print("断开连接")
