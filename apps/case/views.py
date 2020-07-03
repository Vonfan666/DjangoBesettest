from django.shortcuts import render
from  rest_framework.views import APIView,status
from libs.api_response import APIResponse
from . import models,serializers
import  json,os
from case.libs.toRequests import InRequests
from project.models import Environments
# Create your views here
import  logging
from libs.Pagination import Pagination
from libs.public import StartMethod
from django.db.models import Q
from django_redis import get_redis_connection  as conn
from log.logFile import logger as logs
from  users.models import UserProfile


class RunCase(APIView):
    """单条用例执行
        全部id传o 部分传id列表
        :param projectId
        :param fidList=[]  用例集--一个项目下可能存在多个用例集
        :param idList=[]
        :param userId  执行人
        :id
    """


    def post(self,req):

        responses = []
        data=req.data
        listId=json.loads(req.data.get("id"))
        id=listId[0]
        l = []
        self.logRedis = conn("log")
        obj=models.CaseFile.objects.select_related("userId","CaseGroupId","postMethod","dataType","environmentId").filter(id=id)
        serializersObj=serializers.S_CaseRun(obj,many=True)
        res_data=serializersObj.data
        res_data=json.loads(json.dumps(res_data))
        res_data=res_data[0]
        start = StartMethod(data["userId"])
        start()
        self.logger = logs(self.__class__.__module__)
        self.logger.info("单位开始执行")
        s = InRequests(res_data["postMethod"],res_data["dataType"],res_data["environmentId"],res_data["name"],self.logger)
        response=s.run(res_data["attr"],res_data["headers"],res_data["data"])
        responses.append(response)
        self.logger.info("单位执行结束")
        redisListLog = self.logRedis.lrange("log:%s_%s" % (data["userId"], None), 0, -1)
        for log in redisListLog:
            l.append(log.decode("utf8"))
        response["logList"] = l
        # 根据errors判断执行是否成功  断言另外处理
        self.logRedis.delete("log:%s_%s" % (data["userId"], None))
        # response--存入CaseResult  type=1
        userId = UserProfile.objects.get(id=data["userId"])
        models.CaseResult.objects.create(result=response, type=1, c_id=data["id"], userId=userId)
        return  APIResponse(200,"sucess",results=responses,status=status.HTTP_200_OK)

class DebugCase(APIView):
    def post(self, req):
        l=[]
        self.logRedis = conn("log")
        data=req.data
        res_data=req.data.dict()
        validateObj=serializers.S_debugCase(data=data,many=False)
        environmentsObj=self.Environmented(validateObj,res_data)
        start = StartMethod(data["userId"])
        start()
        self.logger = logs(self.__class__.__module__)
        self.logger.info("单位开始执行")
        s = InRequests(res_data["postMethod"], res_data["dataType"], environmentsObj,res_data["name"],self.logger)
        response = s.run(res_data["attr"], res_data["headers"], res_data["data"])
        self.logger.info("单位执行结束")
        redisListLog = self.logRedis.lrange("log:%s_%s" % (data["userId"], None), 0, -1)
        for log  in redisListLog:
            l.append(log.decode("utf8"))
        response["logList"]=l
        #根据errors判断执行是否成功  断言另外处理
        self.logRedis.delete("log:%s_%s" % (data["userId"], None))
        #response--存入CaseResult  type=1
        userId=UserProfile.objects.get(id=data["userId"])
        models.CaseResult.objects.create(result=response,type=1,c_id=data["id"],userId=userId)
        return APIResponse(200, "sucess", results=response, status=status.HTTP_200_OK)

    def Environmented(self,validateObj,res_data):


        if validateObj.is_valid(raise_exception=True):

            environmentsObj = {}
            if res_data["environmentId"] == "":
                res_data["environmentId"] = 1
            else:
                pass
            environments = Environments.objects.filter(id=res_data["environmentId"])
            if len(environments) > 0:
                environments = serializers.S_Environments(environments, many=True)

                environments = json.loads(json.dumps(environments.data))

                environmentsObj["environment"] = json.loads(environments[0]["value"])
            else:
                environments["environment"] = []
            globals = Environments.objects.filter(id=1)
            if len(globals) > 0:
                globals = serializers.S_Environments(globals, many=True)
                globals = json.loads(json.dumps(globals.data))
                environmentsObj["global"] = json.loads(globals[0]["value"])
            else:
                environments["global"] = []

            return environmentsObj
class CaseGroup(APIView):
    """查询当前项目的用例文件夹以及用例
    :param id  项目id
    """
    def get(self,req):
        params = req.query_params
        id=params.get("id")
        obj=models.CaseGroupFiles.objects.select_related("projectId","userId").filter(projectId_id=id)
        serializersObj=serializers.S_CaseGroupFiles(obj,many=True)
        print(serializersObj.data)
        return APIResponse(200,"sucess",results=serializersObj.data,status=status.HTTP_200_OK)

class AddGroup(APIView):
    """新增接口分组
        :param projectId
        :param UserId
        :param name
        :param id   文件夹id
    """
    def post(self,req):
        serializersObj=serializers.S_AddGroup(data=req.data)
        if serializersObj.is_valid(raise_exception=True):
            validate_data=serializersObj.save()
            res_data=serializers.S_AddGroup(validate_data)
            res_data=res_data.data
            return APIResponse(200,"添加成功",results=res_data,status=status.HTTP_200_OK)

class EditGroup(APIView):
    """修改用例文件夹
        :param  id   用例文件夹id
        :param  name  修改后的文件夹name
    """
    def post(self,req):
        id=req.data["id"]
        obj=models.CaseGroupFiles.objects.get(id=id)
        serializersObj=serializers.S_AddGroup(data=req.data,instance=obj,partial=True)
        if serializersObj.is_valid(raise_exception=True):
            validate_data=serializersObj.save()
            res_data=serializers.S_AddGroup(validate_data)
            res_data=res_data.data
            return APIResponse(200,"修改成功",results=res_data,status=status.HTTP_200_OK)

class RemoveGroup(APIView):
    """删除用例文件夹"""
    def post(self,req):
        id = req.data["id"]
        models.CaseGroupFiles.objects.get(id=id).delete()
        return APIResponse(200, "删除成功",status=status.HTTP_200_OK)


class AddInterface(APIView):
    """新增用例接口"""
    def post(self,req):
        serializersObj=serializers.S_AddCase(data=req.data)
        if serializersObj.is_valid(raise_exception=True):
            validate_data=serializersObj.save()
            res_data=serializers.S_AddCase(validate_data)
            res_data=res_data.data
            return APIResponse(200,"添加成功",results=res_data,status=status.HTTP_200_OK)


class EditCase(APIView):
    """编辑接口文件名称"""
    def post(self,req):
        id = req.data["id"]
        obj = models.CaseGroup.objects.get(id=id)
        serializersObj = serializers.S_AddCase(data=req.data, instance=obj, partial=True)
        if serializersObj.is_valid(raise_exception=True):
            validate_data = serializersObj.save()
            res_data = serializers.S_AddCase(validate_data)
            res_data = res_data.data
            return APIResponse(200, "修改成功", results=res_data, status=status.HTTP_200_OK)

class RemoveInterface(APIView):
    """删除接口"""
    def post(self,req):
        id = req.data["id"]
        models.CaseGroup.objects.get(id=id).delete()
        return APIResponse(200, "删除成功", status=status.HTTP_200_OK)
class AddCase(APIView):
    """新增用例"""
    def  post(self,req):
        data=req.data

        if data["id"]:
            obj=models.CaseFile.objects.get(id=data["id"])
            serializersObj = serializers.S_AddInterface(data=data,instance=obj, many=False,partial=True)
            if serializersObj.is_valid(raise_exception=True):
                validate_data = serializersObj.save()
                res_data = serializers.S_AddInterface(validate_data)
                res_obj = res_data.data
                return APIResponse(200, "更新成功", results=res_obj, status=status.HTTP_200_OK)
        else:
            serializersObj=serializers.S_AddInterface(data=data,many=False)
            if serializersObj.is_valid(raise_exception=True):
                validate_data=serializersObj.save()
                res_data=serializers.S_AddInterface(validate_data)
                res_obj=res_data.data
                return  APIResponse(200,"添加成功",results=res_obj,status=status.HTTP_200_OK)
class CaseList(APIView):
    """查看用例列表
        :param id  用例id
    """
    def get(self,req):
        param= req.query_params
        id=param["id"]
        obj=models.CaseFile.objects.select_related("userId","CaseGroupId","postMethod","dataType","environmentId").filter(CaseGroupId_id=id).order_by("order")
        serializersObj=serializers.S_AddInterface(obj,many=True)
        res_obj=serializersObj.data
        return  APIResponse(200,"sucess",results=res_obj,status=status.HTTP_200_OK)
class CaseRemove(APIView):
    """删除用例
       :param id 用例id
    """
    def post(self,req):
        id=req.data["id"]
        models.CaseFile.objects.get(id=id).delete()
        return APIResponse(200,"删除成功",status=status.HTTP_200_OK)
class CaseEdit(APIView):
    """编辑用例"""
    def get(self,req):
        param= req.query_params
        id=param["id"]
        obj=models.CaseFile.objects.select_related("userId","CaseGroupId","postMethod","dataType","environmentId").filter(id=id)
        serializersObj=serializers.S_AddInterface(obj,many=True)
        res_obj=serializersObj.data
        return  APIResponse(200,"sucess",results=res_obj,status=status.HTTP_200_OK)
class CaseOrder(APIView):
    """修改用例执行顺序"""
    def post(self,req):
        models.CaseGroup.objects.filter(id=req.data["id"]).update(order=req.data["order"])
        order=models.CaseGroup.objects.get(id=req.data["id"]).order
        return APIResponse(200,"修改成功",order=order,status=status.HTTP_200_OK)
    def get(self,req):
        order = models.CaseGroup.objects.get(id=req.query_params["id"]).order
        return APIResponse(200, "修改成功", order=order, status=status.HTTP_200_OK)
class AddCasePlan(APIView):
    """新增测试计划
    :param projectId项目id
    :param userId用户id
    :param name  计划名称
    :param cname 脚本名称
    :param runType执行类型
    :param detail 描述
    """
    def post(self,req):

        data=req.data
        serializersObj=serializers.S_AddCasePlan(data=data,many=False)
        if serializersObj.is_valid(raise_exception=True):
            serializersObj.save()
            # res_data_obj=serializers.S_AddCasePlan(res_obj,many=False)
            # res_data=res_data_obj.data
            S = DeleteCasePlan()
            res = S.listPlan(req)
            return APIResponse(200, "计划创建成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                               status=status.HTTP_200_OK)
class UpdateCasePlan(APIView):
    def post(self,req):
        data=req.data
        id=req.data["id"]
        obj=models.CasePlan.objects.get(id=id)
        serializersObj=serializers.S_AddCasePlan(data=data, instance=obj,partial=True,many=False)
        if serializersObj.is_valid(raise_exception=True):
            res_obj=serializersObj.save()
            res_data_obj=serializers.S_AddCasePlan(res_obj)
            res_data=res_data_obj.data
            return APIResponse(200,"计划更新成功",results=res_data,status=status.HTTP_200_OK)
class GetCasePlan(APIView):
    """查看执行计划
    :param projectId
    :page 当前请求的页面
    :pageSize 每页展示的数量
    """

    def get(self,req):
        id=req.query_params["projectId"]
        page=req.query_params["page"]
        pageSize=req.query_params["pageSize"]
        obj=models.CasePlan.objects.select_related("projectId","userId").filter(projectId=id).order_by("createTime").reverse()
        serializersObj=serializers.S_AddCasePlan(obj,many=True)
        res_data=serializersObj.data
        total=len(res_data)  #数据总数
        PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
        all_page = PaginationObj.all_page()
        res_data = res_data[PaginationObj.start():PaginationObj.end()]

        return APIResponse(200, "success", results=res_data, total=total,allPage=all_page,
                           status=status.HTTP_200_OK)
class DeleteCasePlan(APIView):
    """删除"""

    def listPlan(self,req):
        id = req.data["projectId"]
        page = req.data["page"]
        pageSize = req.data["pageSize"]
        obj = models.CasePlan.objects.select_related("projectId", "userId").filter(projectId=id).order_by(
            "createTime").reverse()
        serializersObj = serializers.S_AddCasePlan(obj, many=True)
        res_data = serializersObj.data
        total = len(res_data)  # 数据总数
        PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
        all_page = PaginationObj.all_page()
        res_data = res_data[PaginationObj.start():PaginationObj.end()]
        return {"res_data":res_data,"total":total,"all_page":all_page}
    def post(self,req):
        models.CasePlan.objects.get(id=req.data["id"]).delete()
        res=self.listPlan(req)
        return APIResponse(200, "删除成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)
class SearchCasePlan(APIView):
    """搜索计划"""
    pass
class GetCaseList(APIView):
    def get(self,req):
        data=req.query_params
        projectId = data["projectId"]
        kwargs = {}
        if "name" in data.keys():
            kwargs["name__icontains"] = data["name"]
        if "isInterface" in data.keys():
            kwargs["CaseGroupId__name__icontains"] = data["isInterface"]
        if "postMethods" in data.keys():
            kwargs["postMethod"] = data["postMethods"]
        if "ctime" in data.keys():
            kwargs["createTime__gt"] = json.loads(data["ctime"])[0]
            kwargs["createTime__lt"] = json.loads(data["ctime"])[1]
        if "utime" in data.keys():
            kwargs["updateTime__gt"] = json.loads(data["utime"])[0]
            kwargs["updateTime__lt"] = json.loads(data["utime"])[1]
        kwargs["CaseGroupId__CaseGroupFilesId__projectId"]=projectId
        obj=models.CaseFile.objects.select_related\
            ("CaseGroupId","userId","postMethod","environmentId","update_userId","CaseGroupId__CaseGroupFilesId","CaseGroupId__CaseGroupFilesId__projectId")\
            .filter(**kwargs).order_by("CaseGroupId__order","order")
        serializersObj=serializers.S_GetCaseList(obj,many=True)
        res_data=serializersObj.data
        page = req.query_params["page"]
        pageSize = req.query_params["pageSize"]
        total = len(res_data)  # 数据总数
        PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
        all_page = PaginationObj.all_page()
        if  int(all_page)<int(page):
            PaginationObj = Pagination(total, all_page, perPageNum=pageSize, allPageNum=11)
        res_data = res_data[PaginationObj.start():PaginationObj.end()]
        return APIResponse(200, "success", results=res_data, total=total, allPage=all_page,
                           status=status.HTTP_200_OK)

class EditCaseOrder(APIView):
    """用例列表编辑用例
       :param id  用例id
       :param  corder 用例执行顺序
       :param   postMethod=None  请求类型
       :param   isInterface=None 所属接口
       :param  uUser
    """
    def post(self,req):
        id=req.data.get("id")
        obj=models.CaseFile.objects.get(id=id)
        serializersObj=serializers.S_EditCaseOrder(data=req.data,instance=obj,partial=True,many=False)
        if serializersObj.is_valid(raise_exception=True):
            res_obj=serializersObj.save()
            res_data=serializers.S_EditCaseOrder(res_obj)
            data=res_data.data
            return APIResponse(200,"编辑成功",results=data,status=status.HTTP_200_OK)

class CaseResults(APIView):
    """
    测试结果列表
    :param type==1  debug  type==2  allinterface  type==3 allrun
    :param id
    type==1 传caseId   type==2传interfaceId   type==3传casePlanId
    """
    def page_c(self,data):
        type = data["type"]
        page = data["page"]
        pageSize = data["pageSize"]
        obj = models.CaseResult.objects.filter(c_id=data["c_id"], type=type)
        serializersObj = serializers.S_CaseResults(obj, many=True)
        res_data = serializersObj.data
        total = len(res_data)  # 数据总数
        PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
        all_page = PaginationObj.all_page()
        res_data = res_data[PaginationObj.start():PaginationObj.end()]
        return res_data,all_page,total
    def get(self,req):
        data=req.query_params
        res_data,all_page,total=self.page_c(data)
        return APIResponse(200,"sucess",results=res_data,total=total,allPage=all_page,status=status.HTTP_200_OK)

    def post(self,req):
        """删除
        参数同上
        """
        data=req.data
        id=data["id"]
        try:
            models.CaseResult.objects.get(id=id).delete()
        except:
            return APIResponse(409, "删除异常",
                               status=status.HTTP_200_OK)
        res_data, all_page, total = self.page_c(data)
        return APIResponse(200, "删除成功", results=res_data, total=total, allPage=all_page,
                           status=status.HTTP_200_OK)



class CaseResultsDetail(APIView):
    """
    测试结果详情
    id
    """
    def get(self,req):
        data=req.query_params
        id=data["id"]
        obj=models.CaseResult.objects.get(id=id)
        serializersObj=serializers.S_CaseResults(obj)
        res_data=serializersObj.data["result"]
        return APIResponse(200, "sucess", results=eval(res_data),
                           status=status.HTTP_200_OK)
