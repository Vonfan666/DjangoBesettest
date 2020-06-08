from django.shortcuts import render
from  rest_framework.views import APIView,status
from libs.api_response import APIResponse
from . import models,serializers
import  json,os
from case.libs.toRequests import InRequests
from case.libs.findeSqlCase import FindCase
from project.models import Environments
# Create your views here
import  logging,unittest,time
from libs import HTMLTestRunner
from libs.writeScript import MakeScript

logger =  logging.getLogger("log")


class RunCaseAll(APIView):

    def allCase(self,fileName):
        case_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface")
        allTest = unittest.defaultTestLoader.discover(case_dir, pattern="{}.py".format(fileName), top_level_dir=None)
        return allTest
    def post(self,req):
        """需要传一个项目id 然后通过项目id找到name"""
        projectId=req.data["id"]
        fileName=req.data["name"]
        #这里需要判断该目录下是否存在同名的fileName.py文件
        obj=models.CaseGroupFiles.objects.filter(projectId_id=projectId)
        serializersObj=serializers.S_CaseFilesDetail(obj,many=True)
        orderDictObj=serializersObj.data
        dictObj=json.loads(json.dumps(orderDictObj))
        print(dictObj)  #传给写入文件的方法
        res_list=FindCase(dictObj).run()
        MakeScript().make_file(res_list,fileName)  #给创建用例的方法 传入数据以及文件名称
        name="待定"
        case_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface")
        curtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        report_path =os.path.join(case_dir,'%s_%s.html'%(name,curtime ))
        report_set = open(report_path, 'wb')
        runner=HTMLTestRunner.HTMLTestRunner(report_set)
        runner.run(self.allCase(fileName))
        report_set.close()

        return APIResponse(200, "sucess",results=dictObj, status=status.HTTP_200_OK)
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
        responses=[]
        listId=json.loads(req.data.get("id"))
        for id in listId:

        #1封装环境变量取值---返回url  headers data
        # idList=req.query_params.get("idList")
        # if isinstance(idList,list):
        # id = req.data.get("id")
            obj=models.CaseFile.objects.select_related("userId","CaseGroupId","postMethod","dataType","environmentId").filter(id=id)
            serializersObj=serializers.S_CaseRun(obj,many=True)
            res_data=serializersObj.data
            res_data=json.loads(json.dumps(res_data))
            res_data=res_data[0]
            logger.info("单位开始执行")
            s = InRequests(res_data["postMethod"],res_data["dataType"],res_data["environmentId"],res_data["name"])
            response=s.run(res_data["attr"],res_data["headers"],res_data["data"])
            responses.append(response)
            logger.info("单位执行结束")
        return  APIResponse(200,"sucess",results=responses,status=status.HTTP_200_OK)

class DebugCase(APIView):
    def post(self, req):
        data=req.data
        res_data=req.data.dict()
        validateObj=serializers.S_debugCase(data=data,many=False)
        environmentsObj=self.Environmented(validateObj,res_data)
        logger.info("单位开始执行")
        s = InRequests(res_data["postMethod"], res_data["dataType"], environmentsObj,res_data["name"])
        response = s.run(res_data["attr"], res_data["headers"], res_data["data"])
        logger.info("单位执行结束")
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

class CaseOrder(APIView):
    """修改用例执行顺序"""
    def post(self,req):
        models.CaseGroup.objects.filter(id=req.data["id"]).update(order=req.data["order"])
        order=models.CaseGroup.objects.get(id=req.data["id"]).order
        return APIResponse(200,"修改成功",order=order,status=status.HTTP_200_OK)
    def get(self,req):
        order = models.CaseGroup.objects.get(id=req.query_params["id"]).order
        return APIResponse(200, "修改成功", order=order, status=status.HTTP_200_OK)