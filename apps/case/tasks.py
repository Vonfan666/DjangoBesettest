#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年07月12日18时27分58秒


from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from  case.runCase import RunCaseAll

# 这里不再使用@app.task,而是用@shared_task，是指定可以在其他APP中也可以调用这个任务
@shared_task(bind=True)
def allRun(self,req):
    #数据库创建case_results新增数据 status为初始化。。。
    s=RunCaseAll()
    # res=
    # print(res)
    # print(res.tasks_id)
    s.post(req)
    # for  i  in range(1,11):
    #     time.sleep(0.1)
    self.update_state(state="Progress",meta={})
    return "执行完毕"

# @shared_task
# def minus(x,y):
#     time.sleep(30)
#     print('########## running minus #####################')
#     return x - y


   