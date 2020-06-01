#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月01日22时50分56秒

import json,time,logging,unittest,os
from case import models,serializers
from case.libs.toRequests import InRequests
from libs.api_response import APIResponse
from  rest_framework.views import APIView,status
import time
logger =  logging.getLogger("log")
# def allCase():
#     #待执行用例的目录
#     case_dir=os.path.dirname(os.path.dirname(__file__))+'/feng_test_case'
#     #构造测试集合
#     #suite=unittest.TestSuite()
#     #获取到一个list集合
#     allTest = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
#     #pattern————匹配脚本名称规则，test*.py是匹配所有test开头的所有脚本
#     #top_level_dir 这个是顶层目录的名称 ，一般为空就可以了
#     # for test_suite in allTest:
#     #     for test_case in test_suite:
#     #         suite.addTests(test_case)
#     return  allTest

class TestCases(unittest.TestCase):
    def setup(self, request, *args, **kwargs):
        logger.info("执行前置操作")
    def tearDown(self):
        logger.info("后置操作")
    def test_case(self):
        logger.info("操作中")


class test(object):
    def a(self):
        print("test")
        return "test"


class test1(object):
    def a(self):
        print("test1")
        return "test1"
if __name__=="__main__":
    suite=unittest.TestSuite()