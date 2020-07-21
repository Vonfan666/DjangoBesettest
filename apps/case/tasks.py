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
from django_redis import get_redis_connection  as conn
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
    tasksId="%s-%s"%("celery-task-meta",tasks_data["tasksId"])
    tasks_id=tasks_data["tasksId"]
    #检查上一个异步是否执行完毕--如果执行完毕则将redis日志存入数据库，
    #然后前端起一个websockt查询redis日志
    #检测任务状态修改并插入数据库
    #并实时读取产生的日志
    while True:
        try:
            res=AsyncResult(tasks_id).status
            if res=="SUCCESS":
                #存入库中之后推出循环
                print(res)
                break
        except:
            continue
        time.sleep(1)

# @shared_task
# def minus(x,y):
#     time.sleep(30)
#     print('########## running minus #####################')
#     return x - y


   