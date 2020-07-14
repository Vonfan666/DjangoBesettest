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
PATH = lambda  p:os.path.abspath(
       os.path.join(os.path.dirname(__file__),p)
)
class RunCaseAll(APIView):
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
        print(os.listdir(DIR))
        print("".join([file,".py"]))
        print(332312321)
        if "".join([file,".py"]) in  os.listdir(DIR):
            print(444444)
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
        print("啥情况")
        print(req)
        req=json.loads(req)
        print()
        casePlanObj=models.CasePlan.objects.select_related("projectId").get(id=int(req["id"]))
        print(casePlanObj)
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
            self.removeFile(fileName)  #检测存在脚本则删除--删除之后下面重新生成--如果没有下面新生成
            print("5555555")
            MakeScript().make_file(res_list, fileName)
            print(66666)
        if  int(againScript)==0:
            if not self.distinctFileName(fileName):
                MakeScript().make_file(res_list, fileName)
        print("dsadsadas")
        report_set = open(self.report_path(name), 'wb')
        runner=HTMLTestRunner.HTMLTestRunner(stream=report_set,description = description,title=name)
        runner.run(self.allCase(fileName))
        report_set.close()

        return APIResponse(200, "sucess", status=status.HTTP_200_OK)