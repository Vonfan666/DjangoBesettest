#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月18日21时15分58秒
import json,time,logging,unittest,os,sys
from case import models,serializers
from case.libs.toRequests import InRequests
from libs.api_response import APIResponse
from  rest_framework.views import APIView,status
import time,django



from case.libs.findeSqlCase import CaseAction
from log.logFile import logger as logs
os.environ.setdefault("DJANGO_SETTINGS_MODULE","besettest.settings")
django.setup()
s=CaseAction()

class TestCase_0000002(unittest.TestCase):

    def setUp(self):
        self.__class__.__name__ = "用户信息"
        self.logger = logs(self.__class__.__name__)
        self.logger.info("执行前置操作")

    def tearDown(self):
        self.logger.info("后置操作")
    def test_0000002(self):
        self.__dict__["_testMethodName"] = "登录"
        data={'name': '登录', 'order': 2, 'status': '未完成', 'postMethod': 1, 'dataType': 1, 'attr': 'http://192.168.0.66:8081/users/select_file/', 'detail': 'zhushi henduo', 'headers': {'keys': [{'headerKey': 'Accept', 'headerValue': ' application/json, text/plain, */*', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Encoding', 'headerValue': ' gzip, deflate', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Language', 'headerValue': ' zh-CN,zh;q=0.9', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Authorization', 'headerValue': ' JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxMTIwOTc2LCJlbWFpbCI6IiJ9.rouZ13zc8zvXghFFTs1K-XO4mw7I0SSfw4DAU3tB6vc', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Connection', 'headerValue': ' keep-alive', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Host', 'headerValue': ' 192.168.0.66', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Referer', 'headerValue': ' http', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'User-Agent', 'headerValue': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'headerDetail': '', 'key': 1590838606174}]}, 'data': {'keys': [{'isRequestsData': True, 'dataKey': 'projectId', 'dataValue': '80', 'dataDetail': '', 'key': 1590838606174}]}, 'environmentId': {'environment': [], 'global': [{'3123': '312312312'}, {'3123': '32131231'}, {'3123': '31231213'}, {'恶趣味': '恶趣味群翁'}, {'啊啊啊': '大萨达'}, {'ed': '的'}, {'的': ''}, {'冯凡': 'test'}, {'token': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxODAwMzI4LCJlbWFpbCI6IiJ9.J_BMttS90xrz5GdPxAECEGj5P9JOnMH3f9GMie9HwfY'}]}}
        res=s.action(data,self.logger)
        self.assertEqual(200, 200)

    def test_0000004(self):
        self.__dict__["_testMethodName"] = "获取项目列表"
        data={'name': '获取项目列表', 'order': 4, 'status': '未完成', 'postMethod': 2, 'dataType': 1, 'attr': 'http://192.168.0.66:8081/users/select_file/', 'detail': None, 'headers': {'keys': [{'headerKey': 'Accept', 'headerValue': ' application/json, text/plain, */*', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Encoding', 'headerValue': ' gzip, deflate', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Language', 'headerValue': ' zh-CN,zh;q=0.9', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Authorization', 'headerValue': '{{token}}', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Connection', 'headerValue': ' keep-alive', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Host', 'headerValue': ' 192.168.0.66', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Referer', 'headerValue': ' http', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'User-Agent', 'headerValue': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'headerDetail': '', 'key': 1590838606174}]}, 'data': {'keys': [{'isRequestsData': True, 'dataKey': 'projectId', 'dataValue': '80', 'dataDetail': '', 'key': 1590838606174}]}, 'environmentId': {'environment': [], 'global': [{'3123': '312312312'}, {'3123': '32131231'}, {'3123': '31231213'}, {'恶趣味': '恶趣味群翁'}, {'啊啊啊': '大萨达'}, {'ed': '的'}, {'的': ''}, {'冯凡': 'test'}, {'token': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxODAwMzI4LCJlbWFpbCI6IiJ9.J_BMttS90xrz5GdPxAECEGj5P9JOnMH3f9GMie9HwfY'}]}}
        res=s.action(data,self.logger)
        self.assertEqual(200, res['status'])

    def test_0000005(self):
        self.__dict__["_testMethodName"] = "获取请求方法"
        data={'name': '获取请求方法', 'order': 5, 'status': '未完成', 'postMethod': 2, 'dataType': 1, 'attr': 'http://192.168.0.66:8081/users/select_file/', 'detail': None, 'headers': {'keys': [{'headerKey': 'Accept', 'headerValue': ' application/json, text/plain, */*', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Encoding', 'headerValue': ' gzip, deflate', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Language', 'headerValue': ' zh-CN,zh;q=0.9', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Authorization', 'headerValue': '{{token}}', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Connection', 'headerValue': ' keep-alive', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Host', 'headerValue': ' 192.168.0.66', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Referer', 'headerValue': ' http', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'User-Agent', 'headerValue': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'headerDetail': '', 'key': 1590838606174}]}, 'data': {'keys': [{'isRequestsData': True, 'dataKey': 'projectId', 'dataValue': '80', 'dataDetail': '', 'key': 1590838606174}]}, 'environmentId': {'environment': [], 'global': [{'3123': '312312312'}, {'3123': '32131231'}, {'3123': '31231213'}, {'恶趣味': '恶趣味群翁'}, {'啊啊啊': '大萨达'}, {'ed': '的'}, {'的': ''}, {'冯凡': 'test'}, {'token': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxODAwMzI4LCJlbWFpbCI6IiJ9.J_BMttS90xrz5GdPxAECEGj5P9JOnMH3f9GMie9HwfY'}]}}
        res=s.action(data,self.logger)
        self.assertEqual(200, res['status'])

    def test_0000006(self):
        self.__dict__["_testMethodName"] = "查看所有接口"
        data={'name': '查看所有接口', 'order': 6, 'status': '未完成', 'postMethod': 2, 'dataType': 1, 'attr': 'http://192.168.0.66:8081/users/select_file/', 'detail': None, 'headers': {'keys': [{'headerKey': 'Accept', 'headerValue': ' application/json, text/plain, */*', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Encoding', 'headerValue': ' gzip, deflate', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Accept-Language', 'headerValue': ' zh-CN,zh;q=0.9', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Authorization', 'headerValue': '{{token}}', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Connection', 'headerValue': ' keep-alive', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Host', 'headerValue': ' 192.168.0.66', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'Referer', 'headerValue': ' http', 'headerDetail': '', 'key': 1590838606174}, {'headerKey': 'User-Agent', 'headerValue': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'headerDetail': '', 'key': 1590838606174}]}, 'data': {'keys': [{'isRequestsData': True, 'dataKey': 'projectId', 'dataValue': '80', 'dataDetail': '', 'key': 1590838606174}]}, 'environmentId': {'environment': [], 'global': [{'3123': '312312312'}, {'3123': '32131231'}, {'3123': '31231213'}, {'恶趣味': '恶趣味群翁'}, {'啊啊啊': '大萨达'}, {'ed': '的'}, {'的': ''}, {'冯凡': 'test'}, {'token': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxODAwMzI4LCJlbWFpbCI6IiJ9.J_BMttS90xrz5GdPxAECEGj5P9JOnMH3f9GMie9HwfY'}]}}
        res=s.action(data,self.logger)
        self.assertEqual(200, res['status'])



class TestCase_0000003(unittest.TestCase):

    def setUp(self):
        self.__class__.__name__ = "错误密码登录"
        self.logger = logs(self.__class__.__name__)
        self.logger.info("执行前置操作")

    def tearDown(self):
        self.logger.info("后置操作")
    def test_0000002(self):
        self.__dict__["_testMethodName"] = "错误密码登录"
        data={'name': '错误密码登录', 'order': 2, 'status': '已完成', 'postMethod': 2, 'dataType': 1, 'attr': 'http://192.168.0.66:8081/users/login/', 'detail': None, 'headers': {'keys': [{'headerKey': 'Accept', 'headerValue': ' application/json, text/plain, */*', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'Accept-Encoding', 'headerValue': ' gzip, deflate', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'Accept-Language', 'headerValue': ' zh-CN,zh;q=0.9', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'Authorization', 'headerValue': ' JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxMTIwOTc2LCJlbWFpbCI6IiJ9.rouZ13zc8zvXghFFTs1K-XO4mw7I0SSfw4DAU3tB6vc', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'Connection', 'headerValue': ' keep-alive', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'Host', 'headerValue': ' 192.168.0.66', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'Referer', 'headerValue': ' http', 'headerDetail': '', 'key': 1591368451915}, {'headerKey': 'User-Agent', 'headerValue': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36', 'headerDetail': '', 'key': 1591368451915}]}, 'data': {'keys': [{'isRequestsData': 'true', 'dataKey': 'username', 'dataValue': '00000000000', 'dataDetail': '', 'key': 1591368451916}, {'isRequestsData': 'true', 'dataKey': 'password', 'dataValue': '000000', 'detaDetail': '', 'key': 1591368519437}]}, 'environmentId': {'environment': [], 'global': [{'3123': '312312312'}, {'3123': '32131231'}, {'3123': '31231213'}, {'恶趣味': '恶趣味群翁'}, {'啊啊啊': '大萨达'}, {'ed': '的'}, {'的': ''}, {'冯凡': 'test'}, {'token': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6IjAwMDAwMDAwMDAwIiwiZXhwIjoxNTkxODAwMzI4LCJlbWFpbCI6IiJ9.J_BMttS90xrz5GdPxAECEGj5P9JOnMH3f9GMie9HwfY'}]}}
        res=s.action(data,self.logger)
        self.assertEqual(200, res['status'])

if __name__=="__main__":
    unittest.main()
