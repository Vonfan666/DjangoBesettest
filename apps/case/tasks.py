#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年07月12日18时27分58秒


from __future__ import absolute_import, unicode_literals
import  json
from celery import shared_task
import time
from  case.runCase import RunCaseAll
# from django_redis import get_redis_connection  as conn
# from log.logFile import logger as logs
# from libs.public import StartMethod
# 这里不再使用@app.task,而是用@shared_task，是指定可以在其他APP中也可以调用这个任务
@shared_task(bind=True)
def allRun(self,tasks_data):

    #数据库创建case_results新增数据 status为初始化。。。
    s=RunCaseAll()
    print(tasks_data)
    s.post(tasks_data)
    self.update_state(state="Progress",meta={})
    return "success"

@shared_task(bind=True)
def celeryTasks(self,tasksId):
    #检查上一个异步是否执行完毕--如果执行完毕则将redis日志存入数据库，
    #然后前端起一个websockt查询redis日志
    #检测任务状态修改并插入数据库
    #并实时读取产生的日志
    print(tasksId)
# @shared_task
# def minus(x,y):
#     time.sleep(30)
#     print('########## running minus #####################')
#     return x - y


   