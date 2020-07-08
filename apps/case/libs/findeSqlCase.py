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
    def distinct(self,row,name):
        """判断接口下的用例order是否重复"""
        order = []
        data=row[name]
        for  item in  data:
            order.append(item["order"])
        if not len(set(order))==len(order):
            return False
        return True
    def run(self):

        for  item  in self.obj:  #遍历接口分类
            if  not  self.distinct(item, "caseGroup"):
                return {"msg": "分类【{}】下存在相同执行顺序接口".format(item["name"]),"code":False}

            for row in item["caseGroup"]:  #遍历接口文档
                if row["order"]==None:   #如果没有排序排序则默认1
                    row["order"]=1
                if not self.distinct(row,"child"):
                    return {"msg": "接口【{}】下存在相同执行顺序用例".format(row["name"]),"code":False}

                self.listGroup.append(row)
        a=self.listGroup
        return {"msg":sorted(a,key=lambda a:a["order"]),"code":True}


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
    def action(self,data,logger):
        """执行函数"""
        self.beforeAction()
        try:
            s = InRequests(data["postMethod"], data["dataType"], data["environmentId"], data["name"],logger)
            response = s.run(data["attr"], data["headers"],data["data"])
            print(response["resData"])
            return response["resData"]
        except:
            pass


# class OutputRedirector(object):
#     """ Wrapper to redirect stdout or stderr """
#
#     def __init__(self, fp):
#         self.fp = fp
#
#     def write(self, s):
#         self.fp.write(s)
#
#     def writelines(self, lines):
#         self.fp.writelines(lines)
#
#     def flush(self):
#         self.fp.flush()
#
#
#
# class cc(object):
#     def __init__(self,fp):
#         self.fp=fp
#
#     def c(self,s):
#         print(self.fp)
#         print(s)
# import sys
# stdout_redirector = cc(sys.stdout)
# stderr_redirector = cc(sys.stderr)
