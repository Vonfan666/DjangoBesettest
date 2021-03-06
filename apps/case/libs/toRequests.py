#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月26日21时59分47秒

import requests,json
from case.libs.dataChange import dataChange
import  logging
from rest_framework.validators import ValidationError



# from requests.packages import urllib3
# urllib3.disable_warnings()
class InRequests():

    def __init__(self,postMethod,dataType,environmentId,name,logger,requestsMethods=None):
        self.postMethod=int(postMethod)
        self.dataType=int(dataType)
        self.name=name
        self.logger=logger
        self.environmentId=environmentId
        self.requestsMethods=requestsMethods

    def run(self,url,headers,data=None):
        self.url = url
        try:
            s = dataChange(headers, data,self.logger,self.url,environment=self.environmentId)
            obj = s.run()
        except Exception as f:
            f_obj=json.loads(f.args[0])
            self.headers=f_obj["header"]
            self.data=f_obj["data"]
            self.url=f_obj["url"]
            res=self.resData(code=0)
            res["errors"] = f_obj["msg"]
            return res
        self.headers = obj[0]
        self.logger.info("传入headers值为:%s"%self.headers)
        self.data = obj[1]
        self.url=obj[2]
        self.logger.info("传入data值为:%s" % self.data)
        if self.postMethod==1:
            self.requestsMethods="GET"
            self.logger.info("执行get请求")
            res=self.get()
            return res
        if self.postMethod==2:
            self.requestsMethods = "POST"
            self.logger.info("执行post请求")
            res=self.post()
            return res
    def post(self):

        return self.postCode()
    def get(self):
        # self.url=url
        # self.headers=headers
        # self.data=data
        return self.getCode()
    def getCode(self):
        fixRes = self.resData()
        res={}
        try:
            if  self.dataType==1:
                res=self.form_get()

            if  self.dataType==3:
                res=self.data_get()
        except Exception as f:
            self.logger.info("requests请求报错,错误信息为：%s" % f.args[0])
            fixRes["errors"] = f.args[0]
            fixRes["code"] = 0
            return fixRes

        self.logger.info("接口响应ResHeader为%s" % res.headers)
        self.logger.info("接口响应data为%s" %res.text)


        return self.resResults(fixRes,res)

    def postCode(self):
        fixRes = self.resData()
        res = {}
        try:
            if self.dataType == 1:
                res = self.form_post()

            if self.dataType == 3:
                res = self.data_post()
        except Exception as f:
            self.logger.info("requests请求报错,错误信息为：%s" % f.args[0])

            fixRes["errors"] = f.args[0]
            fixRes["code"]=0
            return fixRes

        self.logger.info("接口响应ResHeader为%s" %res.headers)
        self.logger.info("接口响应data为%s" %res.text)

        return self.resResults(fixRes, res)

    def resData(self,code=None):
        """正常是返回1  报错返回0 断言失败返回2"""
        if code==None:
            code=1
        return {"name": self.name,"postMethods": self.requestsMethods,"code":code,
                "postHeader": self.headers,"postData": self.data,"postUrl":self.url}

    def resResults(self,fixRes,res):
        fixRes["postUrl"] = res.url
        fixRes["resStatus"] = res.status_code
        fixRes["resHeaders"] = json.loads(json.dumps(dict(res.headers)))
        try:
            fixRes["resData"] = json.loads(res.text)
        except:
            fixRes["resData"]=res.text
        try:
            fixRes["resText"] = json.loads(res.text)   #测试接口返回类容
        except:
            fixRes["resText"] = res.text
        return fixRes

    def form_get(self):
        self.logger.info("校验传参类型为:x-www-form-urlencoded")
        return requests.get(self.url, headers=self.headers, params=self.data, verify=False, timeout=30)

    def data_get(self):
        self.logger.info("校验传参类型为:form-data")
        return  requests.get(self.url, headers=self.headers, params=self.data, verify=False, timeout=30)
    def form_post(self):
        self.logger.info("校验传参类型为:x-www-form-urlencoded")
        return requests.post(self.url, headers=self.headers, data=self.data, verify=False, timeout=30)

    def data_post(self):
        self.logger.info("校验传参类型为:form-data")
        return  requests.post(self.url, headers=self.headers, data=self.data, verify=False, timeout=30)
