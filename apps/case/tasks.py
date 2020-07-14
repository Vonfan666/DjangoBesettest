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
@shared_task
def allRun(req):
    s=RunCaseAll()
    print(req)
    return s.post(req)

# @shared_task
# def minus(x,y):
#     time.sleep(30)
#     print('########## running minus #####################')
#     return x - y


   