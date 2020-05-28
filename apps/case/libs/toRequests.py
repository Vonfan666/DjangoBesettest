#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月26日21时59分47秒

import requests,json
from case.libs.dataChange import dataChange
from log.logFile import logger

# from requests.packages import urllib3
# urllib3.disable_warnings()
logger = logger(__file__)
class InRequests():

    def __init__(self,postMethod,dataType,environmentId):
        self.postMethod=postMethod
        self.dataType=dataType
        self.environmentId=environmentId


    def run(self,url,headers,data=None):
        s = dataChange(headers, data,self.environmentId)
        obj = s.run()
        headers = obj[0]
        logger.info("传入headers值为:%s"%headers)
        data = obj[1]
        logger.info("传入data值为:%s" % data)
        if self.postMethod==1:
            logger.info("执行get请求")
            res=self.get(url,headers,data)
            print("_____", res)
            return res
        if self.postMethod==2:
            logger.info("执行post请求")
            res=self.post(url, headers, data)
            print("_____",res)
            return res
    def post(self,url,headers,data=None):
        """如果type==1则是标准的form表单请求,如果是form-data则type传3"""
        res=None
        if self.dataType==1:
            logger.info("校验传参类型为:x-www-form-urlencoded")
            res=requests.post(url,headers=headers,data=data,verify=False,timeout=30)
            logger.info("接口响应头为:%s"%res.headers)
            logger.info("接口响应结果为:%s" % res.json())
        if self.dataType==3:
            logger.info("校验传参类型为:form-data")
            res=requests.post(url,headers=headers,data=data,verify=False,timeout=30)
            logger.info("接口响应头为:%s" % res.headers)
            logger.info("接口响应结果为:%s" % res.json())
        return {"resStatus":res.status_code,"postHeader":headers,"postData":data,"resHeaders":res.headers,"resData":res.json(),"resText":res.raw,"errors":res.raise_for_status()}
    def get(self,url,headers,data=None):
        res=None
        if self.dataType==1:
            logger.info("校验传参类型为:x-www-form-urlencoded")

            res=requests.get(url,headers=headers,json=data,verify=False,timeout=30)
            logger.info("接口响应ResHeader为%s" % res.headers)
            logger.info("接口响应data为%s" % res.json())
        if self.dataType==3:
            logger.info("校验传参类型为:form-data")
            res=requests.get(url,headers=headers,data=data,verify=False,timeout=30)
            logger.info("接口响应头为:%s" % res.headers)
            logger.info("接口响应结果为:%s" % res.json())
        return {"resStatus":res.status_code,"postHeader":headers,"postData":data,"resHeaders":res.headers,"resData":res.json(),"resText":res.raw,"errors":res.raise_for_status()}



