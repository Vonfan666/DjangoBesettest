#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月05日23时43分29秒
"""前端传一个项目id-通过id在数据找到用例所属接口 以及用例"""
"""判断用例是否完成---给用例排序"""
"""返回一个list

list=[{"接口id":id,"接口名称":name,child:["用例名称":name]}]

自动生成py脚本名称--Test_项目id_all_case

每次执行都需要重新生成脚本---根据项目id清空对应的脚本文件然后重新写入

"""
import json
from .toRequests import InRequests
class FindCase():
    def __init__(self,obj):
        self.obj=obj
        self.listGroup=[]

    def forObj(self,item):
        pass

    def run(self):
        for  item  in self.obj:
            for row in item["caseGroup"]:
                if row["order"]==None:
                    row["order"]=1
                self.listGroup.append(row)
        a=self.listGroup
        return sorted(a,key=lambda a:a["order"])


class CaseAction():


    def beforeAction(self):
        """前置操作"""
        pass

    def afterAction(self):
        """后置操作"""
        pass

    def assertAction(self):
        """断言操作"""
        pass
    def action(self,data):
        """执行函数"""
        self.beforeAction()
        try:
            s = InRequests(data["postMethod"], data["dataType"], data["environmentId"], data["name"])
            response = s.run(data["attr"], data["headers"],data["data"])
            print(response["resData"])
            return response["resData"]
        except:
            pass