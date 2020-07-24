#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月14日01时12分27秒
from  rest_framework.views import APIView,status
from libs.api_response import APIResponse
from . import models,serializers
import  json,os,time
from libs import HTMLTestRunner
from case.libs.findeSqlCase import FindCase
from libs.writeScript import MakeScript
# from case.tasks import UsersTask
import unittest
from django_redis import get_redis_connection  as conn
from log.logFile import logger as logs
from libs.public import StartMethod

"""最新的"""
PATH = lambda  p:os.path.abspath(
       os.path.join(os.path.dirname(__file__),p)
)
class RunCaseAll():
    """
    0  初始化
    1  创建脚本
    2  执行脚本
    3  执行完毕
    """
    def distinctFileName(self,file):

        # 这里需要判断该目录下是否存在同名的fileName.py文件
        files=[]
        dirPath=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        DIR=os.path.join(dirPath,"interface\\testFiles")
        for  fileName in  os.listdir(DIR):
            files.append(os.path.splitext(fileName)[0] )
        if file  in files:
             return True
        return False
    def removeFile(self,file):
        dirPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        DIR = os.path.join(dirPath, "interface\\testFiles","")
        if "".join([file,".py"]) in  os.listdir(DIR):
            os.remove(os.path.join(DIR,"".join([file,".py"])))
    def report_path(self,name):
        case_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface/results")
        curtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        report_path = os.path.join(case_dir, '%s_%s.html' % (name, curtime))
        return report_path
    def allCase(self,fileName):
        case_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface/testFiles")
        s=unittest.defaultTestLoader
        allTest = s.discover(case_dir, pattern="{}.py".format(fileName), top_level_dir=None)
        return allTest
    def serializers_data(self,projectId):
        obj = models.CaseGroupFiles.objects.select_related(
            "projectId", "userId"
        ).filter(projectId_id=projectId)
        serializersObj = serializers.S_CaseFilesDetail(obj, many=True)
        orderDictObj = serializersObj.data
        dictObj = json.loads(json.dumps(orderDictObj))
        res_list = FindCase(dictObj).run()
        return  res_list
    def post(self,req):

        """需要传一个项目id 然后通过项目id找到name"""

        req = json.loads(req)
        key = "%s_%s" % (req["id"], req["timeStr"])  # 把计划id+时间戳当做用户id传过去
        self.logRedis = conn()
        self.logRedis.set("status:%s"%key,self.resStatus(1))
        casePlanObj=models.CasePlan.objects.select_related("projectId").get(id=int(req["id"]))
        projectId=casePlanObj.projectId
        fileName=casePlanObj.cname #脚本名称
        name=casePlanObj.name   #计划名称
        description=casePlanObj.detail
        againScript=casePlanObj.againScript  #是否新建脚本(删除之前的在新建)   不删除直接使用之前的
        res_list=self.serializers_data(projectId)  #各种骚操作找到排序后的用例参数集

        if not res_list["code"]:  # 如果有接口或者用例执行顺序重复则直接返回
            return APIResponse(409, res_list["msg"], results=res_list["msg"], status=status.HTTP_200_OK)
        else:
            res_list = res_list["msg"]
        if int(againScript)==1:  #如果设置每次执行重新生成
            #### 数据库创建case_results新增数据 status为生成脚本。。。
            self.logRedis.set("status:%s" % key, self.resStatus(2))
            self.removeFile(fileName)  #检测存在脚本则删除--删除之后下面重新生成--如果没有下面新生成
            MakeScript().make_file(res_list, fileName)
        if  int(againScript)==0:
            if not self.distinctFileName(fileName):
                MakeScript().make_file(res_list, fileName)
        report_set = open(self.report_path(name), 'wb')
        runner=HTMLTestRunner.HTMLTestRunner(stream=report_set,description = description,title=name,key=key)
        self.logRedis.set("status:%s" % key, self.resStatus(3,createStatus=int(againScript)))
        runner.run(self.allCase(fileName))   #这里传一个任务id到HTMLTestRunner--然后根据这个加上时间戳生成id
        l={}
        l["assertSuccess"]=runner.runCase.success_count
        l["assertFailed"]=runner.runCase.failure_count
        l["runFailed"]=runner.runCase.error_count
        report_set.close()
        self.logRedis.set("status:%s" % key, self.resStatus(4,createStatus=int(againScript), count=l))
        self.logRedis.rpush("log:%s"%key,"结束")

        #### 数据库创建case_results新增数据 status为执行完毕。。。

    def resStatus(self,status,createStatus=None,count=None):
        """
        1  初始化
        2  创建脚本
        3  执行脚本
        4  执行完毕
        createStatus  #是否创新创建脚本

        """
        list = ["准备", "初始化", "创建脚本", "执行脚本", "执行完毕"]
        data = {"status": status, "msg": list[status], "count": count}
        if  createStatus==0:  #不需要重新创建脚本
            list.pop(2)
            data = {"status": status-1, "msg": list[status-1], "count": count}

        return json.dumps(data)




#非异步
# from  rest_framework.views import APIView,status
# from libs.api_response import APIResponse
# from . import models,serializers
# import  json,os,time
# from libs import HTMLTestRunner
# from case.libs.findeSqlCase import FindCase
# from libs.writeScript import MakeScript
# # from case.tasks import UsersTask
# import unittest
# from django_redis import get_redis_connection  as conn
# from log.logFile import logger as logs
# from libs.public import StartMethod
#
# PATH = lambda  p:os.path.abspath(
#        os.path.join(os.path.dirname(__file__),p)
# )
# class RunCaseAll():
#
#     def distinctFileName(self,file):
#         # 这里需要判断该目录下是否存在同名的fileName.py文件
#         files=[]
#         dirPath=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#         DIR=os.path.join(dirPath,"interface\\testFiles")
#         for  fileName in  os.listdir(DIR):
#             files.append(os.path.splitext(fileName)[0] )
#         if file  in files:
#              return True
#         return False
#     def removeFile(self,file):
#         dirPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#         DIR = os.path.join(dirPath, "interface\\testFiles","")
#         if "".join([file,".py"]) in  os.listdir(DIR):
#             os.remove(os.path.join(DIR,"".join([file,".py"])))
#     def report_path(self,name):
#         case_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface/results")
#         curtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
#         report_path = os.path.join(case_dir, '%s_%s.html' % (name, curtime))
#         return report_path
#     def allCase(self,fileName):
#         case_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface/testFiles")
#         s=unittest.defaultTestLoader
#         allTest = s.discover(case_dir, pattern="{}.py".format(fileName), top_level_dir=None)
#         return allTest
#     def serializers_data(self,projectId):
#         obj = models.CaseGroupFiles.objects.select_related(
#             "projectId", "userId"
#         ).filter(projectId_id=projectId)
#         serializersObj = serializers.S_CaseFilesDetail(obj, many=True)
#         orderDictObj = serializersObj.data
#         dictObj = json.loads(json.dumps(orderDictObj))
#         res_list = FindCase(dictObj).run()
#
#         return  res_list
#
#     def post(self,req):
#
#         """需要传一个项目id 然后通过项目id找到name"""
#
#         self.logRedis = conn("log")
#         req=json.loads(req)
#         print(req)
#         # self.userId="%s_%s"%(req["id"],req["timeStr"])  #把计划id+时间戳当做用户id传过去
#         time.sleep(10)
#         casePlanObj=models.CasePlan.objects.select_related("projectId").get(id=int(req["id"]))
#         projectId=casePlanObj.projectId
#         fileName=casePlanObj.cname #脚本名称
#         name=casePlanObj.name   #计划名称
#         description=casePlanObj.detail
#
#         againScript=casePlanObj.againScript  #是否新建脚本(删除之前的在新建)   不删除直接使用之前的
#         res_list=self.serializers_data(projectId)  #各种骚操作找到排序后的用例参数集
#
#         if not res_list["code"]:  # 如果有接口或者用例执行顺序重复则直接返回
#             return APIResponse(409, res_list["msg"], results=res_list["msg"], status=status.HTTP_200_OK)
#         else:
#             res_list = res_list["msg"]
#
#         if int(againScript)==1:  #如果设置每次执行重新生成
#             #### 数据库创建case_results新增数据 status为生成脚本。。。
#             self.removeFile(fileName)  #检测存在脚本则删除--删除之后下面重新生成--如果没有下面新生成
#             MakeScript().make_file(res_list, fileName)
#         if  int(againScript)==0:
#             #### 数据库创建case_results新增数据 status为执行脚本。。。
#             if not self.distinctFileName(fileName):
#                 MakeScript().make_file(res_list, fileName)
#         report_set = open(self.report_path(name), 'wb')
#         runner=HTMLTestRunner.HTMLTestRunner(stream=report_set,description = description,title=name)
#         runner.run(self.allCase(fileName))
#         report_set.close()
#         #### 数据库创建case_results新增数据 status为执行完毕。。。
#









