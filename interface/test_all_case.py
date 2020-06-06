#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月01日22时50分56秒

import json,time,logging,unittest,os,sys
from case import models,serializers
from case.libs.toRequests import InRequests
from libs.api_response import APIResponse
from  rest_framework.views import APIView,status
import time
logger =  logging.getLogger("log")

class class_name_code(unittest.TestCase):

    def setUp(self):

        self.__class__.__name__ = "搞飞机"
        logger.info("执行前置操作")

    def tearDown(self):
        logger.info("后置操作")
    def test1(self):
        self.__dict__["_testMethodName"]="登录注册"
        """传一个id"""
        """通过id找相关数据"""



