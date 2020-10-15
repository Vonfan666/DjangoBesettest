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
from db_tools.connectSql import Con_sql
from case import models
from project.models import Environments

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

    def  saveEnv(self,key,value,envId):
        obj=Environments.objects.get(id=envId)
        value_list=json.loads(obj.value)
        value_key_list=list(map(lambda  x:list(x.keys())[0],value_list))
        if key  in value_key_list:
            index=value_key_list.index(key)
            value_list[index]={key:value}

        else:
            value_list.append({key:value})
        obj.value=json.dumps(value_list)
        obj.save()
    def keysAction(self,data):
        if data:
            data=json.loads(data)["keys"]
        return data
    def searchMySql(self,id):
        boxObj=models.SqlBox.objects.get(id=id)
        return boxObj
    def searchSql(self,id):
        sqlObj=models.SqlStatement.objects.get(id=id)
        return sqlObj.sql
    def beforeAction_M(self):

        """前置操作

        {"code":0,"msg":"连接数据库报错:%s"%f}
         {"code":1,"msg":"Sql执行成功","data":data}
          {"code":2,"msg":"SQL操作失败，已完成回滚%s"%e}
          {"code":5,"msg":"变量取值失败}
        """

        runSqlRes = None
        data=json.loads(self.data["beforeAction"])["keys"]
        [data.remove(rows) for  rows  in  data if rows["beforeIndex"]==""]
        if data:
            list(map(lambda x: x.setdefault("beforeIndex", int(x.pop("beforeIndex"))), data))  #将beforeIndex字符串改成int类型
            data.sort(key=lambda x:x["beforeIndex"])#排序

            for index, item in enumerate(data,1):
                if item["beforeType"]==1:  #数据库操作
                    boxObj=self.searchMySql(item["beforeSqlBoxType"])
                    s=Con_sql(
                       host= boxObj.host,
                        port= int(boxObj.port),
                        user= boxObj.userName,
                        passwd= boxObj.passWord,
                        database= boxObj.database)
                    sql=self.searchSql(item["beforePlan"])
                    runSqlRes=s.runSql(item["beforePlan"])
                    self.logger.info("前置操作执行：%s" % sql)
                    self.logger.info("前置执行结果-%s:%s" % (index, runSqlRes))
            self.logger.info("前置操作执行完成")
            return runSqlRes  # 返回执行结果
    def afterAction_M(self):
        """后置操作  断言失败code返回2"""

        runSqlRes = None
        data = json.loads(self.data["afterAction"])["keys"]
        [data.remove(rows) for rows in data if rows["afterIndex"] == ""]
        if data:
            list(map(lambda x: x.setdefault("afterIndex", int(x.pop("afterIndex"))), data))  # 将beforeIndex字符串改成int类型
            data.sort(key=lambda x: x["afterIndex"])  # 排序
            for index,item in enumerate(data,1):
                if item["afterType"] == 1:  # 数据库操作
                    boxObj = self.searchMySql(item["afterSqlBoxType"])
                    s = Con_sql(
                        host=boxObj.host,
                        port=int(boxObj.port),
                        user=boxObj.userName,
                        passwd=boxObj.passWord,
                        database=boxObj.database)
                    sql = self.searchSql(item["afterPlan"])
                    runSqlRes = s.runSql(item["afterPlan"])
                    self.logger.info("后置操作执行：%s" % sql)
                    self.logger.info("后置执行结果-%s:%s"%(index,runSqlRes))
            self.logger.info("后置操作执行完成")
            return runSqlRes  # 返回执行结果
    def assertAction(self):
        """断言操作"""
        pass

    def addEnv(self,response,envList):
        """将返回结果加入环境或者全局变量"""
        if response["code"] == 1 and  envList:  # 这里执行
            res = response["resData"]
            for  item  in envList:
                try:
                    if  item["action"]:
                        value=eval(item["action"])
                        self.saveEnv(item["name"],value,item["envId"])
                except Exception as f:
                    response["code"]=0
                    response["errors"]="新增变量失败,异常操作为:%s,msg=%s"%(item["action"],f)
                    return response

    def action(self,data,logger):
        """执行函数"""
        self.logger=logger
        self.data=data
        beforeRes=self.beforeAction_M()
        try:
            s = InRequests(self.data["postMethod"], self.data["dataType"], self.data["environmentId"], self.data["name"],self.logger)
            response = s.run(self.data["attr"], self.data["headers"],self.data["data"])
            # s = InRequests(self.postMethod, self.dataType, self.environmentId, self.name,self.logger)
            # response = s.run(self.attr, self.headers,self.data)
            afterRes = self.afterAction_M()

            self.assertAction()
            response["beforeAction"] = beforeRes
            response["afterAction"] = afterRes


            self.addEnv(response,self.keysAction(self.data["addEnv"]))

            return response
        except Exception as f:
            print(f)


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
