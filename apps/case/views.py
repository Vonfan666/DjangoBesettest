from django.shortcuts import render
from  rest_framework.views import APIView,status
from django.db.models import  Q
from libs.api_response import APIResponse
from . import models,serializers
import  json,requests,os
from case.libs.toRequests import InRequests
# Create your views here

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
        #1封装环境变量取值---返回url  headers data
        # idList=req.query_params.get("idList")
        # if isinstance(idList,list):
        id = req.data.get("id")
        obj=models.CaseFile.objects.select_related("userId","CaseGroupId","postMethod","dataType","environmentId").filter(id=id)
        serializersObj=serializers.S_CaseRun(obj,many=True)
        res_data=serializersObj.data
        res_data=json.loads(json.dumps(res_data))
        res_data=res_data[0]
        print(res_data)
        print(res_data["environmentId"])
        s = InRequests(res_data["postMethod"],res_data["dataType"],res_data["environmentId"])
        response=s.run(res_data["attr"],res_data["headers"],res_data["data"])
        print(response)
        return  APIResponse(200,"sucess",results=response,status=status.HTTP_200_OK)






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


class AddCase(APIView):
    """新增用例接口"""
    def post(self,req):
        serializersObj=serializers.S_AddCase(data=req.data)
        if serializersObj.is_valid(raise_exception=True):
            validate_data=serializersObj.save()
            res_data=serializers.S_AddCase(validate_data)
            res_data=res_data.data
            return APIResponse(200,"添加成功",results=res_data,status=status.HTTP_200_OK)


class EditCase(APIView):
    """编辑用例文件"""
    def post(self,req):
        id = req.data["id"]
        obj = models.CaseGroup.objects.get(id=id)
        serializersObj = serializers.S_AddCase(data=req.data, instance=obj, partial=True)
        if serializersObj.is_valid(raise_exception=True):
            validate_data = serializersObj.save()
            res_data = serializers.S_AddCase(validate_data)
            res_data = res_data.data
            return APIResponse(200, "修改成功", results=res_data, status=status.HTTP_200_OK)

class RemoveCase(APIView):
    def post(self,req):
        id = req.data["id"]
        models.CaseGroup.objects.get(id=id).delete()
        return APIResponse(200, "删除成功", status=status.HTTP_200_OK)


class AddInterface(APIView):
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

class  CaseList(APIView):
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

