#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年07月12日18时27分58秒


from __future__ import absolute_import

from celery import shared_task
from  case.runCase import RunCaseAll

@shared_task
def runAll(req):
    RunCaseAll().post(req)
   