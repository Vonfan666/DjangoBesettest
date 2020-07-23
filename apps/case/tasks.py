#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年07月12日18时27分58秒


from __future__ import absolute_import, unicode_literals
import  json
from celery import shared_task
from  celery import Task
import time
from  case.runCase import RunCaseAll
from celery.result import AsyncResult
from  case import models
from django_redis import get_redis_connection  as conn
from users.models import UserProfile
from django.db.models import Q

# from log.logFile import logger as logs
# from libs.public import StartMethod
# 这里不再使用@app.task,而是用@shared_task，是指定可以在其他APP中也可以调用这个任务




@shared_task(bind=True)  #绑定任务为实力方法
def allRun(self,tasks_data):

    #数据库创建case_results新增数据 status为初始化。。。
    try:
        s=RunCaseAll()

        s.post(tasks_data)
        self.update_state(state="Progress",meta={})
        return "success"
    except:
        return "fail"

@shared_task(bind=True)
def celeryTasks(self,tasks_data):
    """
    '{"id": "67", "timeStr": "20200717180838", "tasksId": "f76c488c-fa29-42f1-9b4a-4c80ade939bf"}'
    :param self:
    :param tasks_data:
    :return:
    """

    tasks_data=json.loads(tasks_data)
    print(tasks_data)
    tasks_id=tasks_data["tasksId"]
    timeStr=tasks_data["timeStr"]
    userId=tasks_data["userId"]
    c_id =tasks_data["id"]
    CaseCount=tasks_data["CaseCount"]
    startTime=time.time()
    self.l = {
        "results": [],
        "logList": [],
    }
    while True:
        endTime=time.time()
        try:
            res=AsyncResult(tasks_id).status
        except:
            if endTime-startTime>60*30:
                break
            else:
                continue
        else:
            if res=="SUCCESS":
                #存入库中之后推出循环
                Redis=conn()
                RedisCount=conn()
                redisListLog=Redis.lrange("log:%s_%s"%(tasks_data["id"],timeStr),0,-1)
                RedisCountLog=RedisCount.get("status:%s_%s"%(c_id,timeStr))
                for log in redisListLog:
                    self.l["logList"].append(log.decode("utf8"))
                RedisCountLog=json.loads(RedisCountLog)
                print(RedisCountLog)
                userId = UserProfile.objects.get(id=userId)
                if int(tasks_data["againScript"])==1:
                    CaseCount=models.CaseFile.objects.filter(
                        Q(CaseGroupId__CaseGroupFilesId__projectId=int(tasks_data["projectId"])) & Q(status=1)).count()
                models.CasePlan.objects.filter(id=c_id).update(CaseCount=int(CaseCount))
                models.CaseResult.objects.create(
                    result=self.l,
                    type=3,
                    c_id=c_id,
                    userId=userId,
                    caseCount=int(CaseCount),
                    assertSuccess=RedisCountLog["count"]["assertSuccess"],
                    assertFailed=RedisCountLog["count"]["assertFailed"],
                    runFailed=RedisCountLog["count"]["runFailed"],
                )

                break
    print("退出")

# @shared_task
# def minus(x,y):
#     time.sleep(30)
#     print('########## running minus #####################')
#     return x - y


   