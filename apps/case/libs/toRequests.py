#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月26日21时59分47秒

import requests,json
from case.libs.dataChange import dataChange
# from requests.packages import urllib3
# urllib3.disable_warnings()
class InRequests():
    def __init__(self,postMethod,dataType,environmentId):
        self.postMethod=postMethod
        self.dataType=dataType
        self.environmentId=environmentId

    def run(self,url,headers,data=None):
        s = dataChange(headers, data,self.environmentId)
        obj = s.run()
        headers = obj[0]
        data = obj[1]
        if self.postMethod==1:
            res=self.get(url,headers,data)
            return res
        if self.postMethod==2:
            res=self.post(url, headers, data)
            return res
    def post(self,url,headers,data=None):
        """如果type==1则是标准的form表单请求,如果是form-data则type传3"""
        res=None
        if self.dataType==1:
            res=requests.post(url,headers=headers,data=data,verify=False,timeout=30)
        if self.dataType==3:
            res=requests.post(url,headers=headers,data=data,verify=False,timeout=30)
        return res.json()
    def get(self,url,headers,data=None):
        res=None
        if self.dataType==1:
            res=requests.get(url,headers=headers,json=data,verify=False,timeout=30)
        if self.dataType==3:
            res=requests.get(url,headers=headers,data=data,verify=False,timeout=30)
        return res.json()



