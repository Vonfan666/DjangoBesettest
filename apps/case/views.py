import json
import time,requests
from  datetime import datetime

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django_redis import get_redis_connection  as conn
from  rest_framework.views import APIView,status
from case.libs.findeSqlCase import CaseAction
from case.libs.toRequests import InRequests
from case.tasks import allRun,celeryTasks
from libs.Pagination import Pagination
from libs.api_response import APIResponse
from libs.public import StartMethod
from log.logFile import logger as logs
from project.models import Environments
from  users.models import UserProfile
from . import models,serializers
from .libs.timedTask import TimedTask,myTimedTask
from db_tools.connectSql  import Con_sql


from case.runCase import RunCaseAll
"""最新的"""

#非异步
# class  RunAll(APIView):
#     def post(self,req):
#         cc = req.data
#         cc = cc.dict()
#         cc=json.dumps(cc)
#         RunCaseAll().post(cc)
#         # res=tasks.allRun.delay(cc)
#         # print(res.task_id)
#         return APIResponse(200,"c",status=status.HTTP_200_OK)
class RunAll(APIView):
    def post(self,req):
        tasks_data = req.data
        tasks_data = tasks_data.dict()
        timeStr=time.strftime("%Y%m%d%H%M%S",time.localtime())
        tasks_data["timeStr"]=timeStr
        tasks_data_json=json.dumps(tasks_data)
        print("开始")
        res= allRun.delay(tasks_data_json)
        tasks_data["tasksId"]=res.task_id
        tasks_data_celeryTasks_json=json.dumps(tasks_data)
        celeryTasks.delay(tasks_data_celeryTasks_json)
        # rep=tasks.forEach.delay(res.task_id)
        #res存储的就是任务结果--当任务完成时 result.ready()为true，然后res.get()取结果即可
        return APIResponse(200,"success",task_id=res.task_id,log_id="%s_%s"%(tasks_data["id"],timeStr),status=status.HTTP_200_OK)
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
        listId=json.loads(data["id"])
        id=listId[0]
        l = {
            "results":[],
            "logList":[],
        }
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
        # s = InRequests(res_data["postMethod"],res_data["dataType"],res_data["environmentId"],res_data["name"],self.logger)
        # response=s.run(res_data["attr"],res_data["headers"],res_data["data"])
        caseAction = CaseAction()
        response = caseAction.action(res_data, self.logger)
        l["results"].append(response)
        self.logger.info("单位执行结束")
        redisListLog = self.logRedis.lrange("log:%s_%s" % (data["userId"], None), 0, -1)
        for log in redisListLog:
            l["logList"].append(log.decode("utf8"))

        # 根据errors判断执行是否成功  断言另外处理
        self.logRedis.delete("log:%s_%s" % (data["userId"], None))
        # response--存入CaseResult  type=1
        userId = UserProfile.objects.get(id=data["userId"])
        models.CaseResult.objects.create(result=l, type=1, c_id=id, userId=userId)
        return  APIResponse(200,"sucess",results=l,status=status.HTTP_200_OK)
class DebugCase(APIView):
    def post(self, req):
        l = {
            "results": [],
            "logList": [],
        }
        self.logRedis = conn("log")
        data=req.data
        res_data=req.data.dict()
        validateObj=serializers.S_debugCase(data=data,many=False)
        environmentsObj=self.Environmented(validateObj,res_data)
        res_data["environmentId"]=environmentsObj
        start = StartMethod(data["userId"])
        start()
        self.logger = logs(self.__class__.__module__)
        self.logger.info("单位开始执行")
        # s = InRequests(res_data["postMethod"], res_data["dataType"], environmentsObj,res_data["name"],self.logger)
        # response = s.run(res_data["attr"], res_data["headers"], res_data["data"])
        caseAction = CaseAction()
        response = caseAction.action(res_data,self.logger)
        l["results"].append(response)
        self.logger.info("单位执行结束")
        redisListLog = self.logRedis.lrange("log:%s_%s" % (data["userId"], None), 0, -1)
        for log in redisListLog:
            l["logList"].append(log.decode("utf8"))
        #根据errors判断执行是否成功  断言另外处理
        self.logRedis.delete("log:%s_%s" % (data["userId"], None))
        #response--存入CaseResult  type=1
        userId=UserProfile.objects.get(id=data["userId"])
        models.CaseResult.objects.create(result=l,type=1,c_id=data["id"],userId=userId)
        return APIResponse(200, "sucess", results=l, status=status.HTTP_200_OK)

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
        # print(serializersObj.data)
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
class GetBoxSqlList(APIView):
    def get(self,req):
        #操作类型前端写死
        data=req.query_params
        res_dict=[]
        obj=models.SqlBox.objects.filter(projectId_id=int(data["projectId"]))
        serializersObj=serializers.S_GetBoxSqlList(obj,many=True)
        res=serializersObj.data
        res_dict.extend([
            {"typeC": 1, "lists": res, "name": "数据库操作"},  # 只返回了sql的操作类型-其他操作类型后续新增
            # 文件处理是假数据
            {"typeC": 2, "lists": [ { "id": 1, "name": "文件处理是假数据" },{ "id": 2, "name": "上传文件" },{ "id": 3, "name": "文件遍历" }], "name": "文件操作"},
        ])

        return APIResponse(200,"",results=res_dict,status=status.HTTP_200_OK)


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
            data=json.loads(json.dumps(res["res_data"]))[0]
            # print(data)
            if int(data["runType"]["id"])==1:  #只要是选择定时都会去新建一个---只是该定时任务目前是暂停的
                arg={
                    "id":data["id"],
                    "runType":data["runType"]["id"],
                    "userId":data["userId"]["id"],
                    "CaseCount":data["CaseCount"],
                    "projectId":data["projectId"]["id"],
                    "againScript":data["againScript"],
                    "cron":data["cron"],
                    "name": data["cname"],
                    "timedId":data["timedId"],
                    "taskId": data["taskId"]
                }
                # print(arg)
                TimedTask().task(arg)
            #新建如果是定时任务--那么就在任务列表插入一条数据---同时创建定时任务到beat表
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
            data = res_data   #编辑需要操作任务表----如果执行方式是手动执行--则改为将任务状态改为失效
             #只要是选择定时都会去新建一个---只是该定时任务目前是暂停的
            arg = {
                "id": data["id"],
                "runType": data["runType"]["id"],
                "userId": data["userId"]["id"],
                "CaseCount": data["CaseCount"],
                "projectId": data["projectId"]["id"],
                "againScript": data["againScript"],
                "cron": data["cron"],
                "name": data["cname"],
                "timedId": data["timedId"]["id"],  #是否开启定时
                "taskId":data["taskId"]   #celery任务id
            }
            # print(arg)
            TimedTask().task(arg)
            obj = models.CasePlan.objects.get(id=id)
            serializersObj = serializers.S_AddCasePlan(obj)
            # print(serializersObj)
            res_data=serializersObj.data

            return APIResponse(200,"计划更新成功",results=res_data,status=status.HTTP_200_OK)
class GetCasePlan(APIView):
    """查看执行计划
    :param projectId
    :page 当前请求的页面
    :pageSize 每页展示的数量
    """

    def get(self,req):
        id=req.query_params["projectId"]
        total = None
        all_page = None
        page=None
        pageSize=None
        if "page" in req.query_params:
            page = req.query_params["page"]
            pageSize = req.query_params["pageSize"]

        obj=models.CasePlan.objects.select_related("projectId","userId").filter(projectId=id).order_by("createTime").reverse()
        serializersObj=serializers.S_AddCasePlan(obj,many=True)
        res_data=serializersObj.data
        if page:  #如果传了分页 则返回分页数据--否则返回所有数据
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
    def delete_task(self,task_id):
        TimedTask().deleteTask(task_id)
    def post(self,req):
        obj=models.CasePlan.objects.get(id=req.data["id"])
        #这里需要删除测试报告里面的内容。。。或者在测试结果里面加一个已经删除的标识
        task_id = obj.taskId
        if task_id:
            self.delete_task(task_id)
        obj.delete()

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
        obj = models.CaseResult.objects.filter(c_id=data["c_id"], type=type).order_by("createTime").reverse()
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
class addTimedTask(APIView):

    """新建定时任务

    """
    def taskList(self,data,kwarg={}):
        id = data["projectId"]
        page = data["page"]
        pageSize = data["pageSize"]

        kwarg["projectId"]=id
        obj = models.timedTask.objects.select_related("projectId", "userId").filter(**kwarg).order_by(
            "createTime").reverse()
        serializersObj = serializers.S_addTimedTask(obj, many=True)
        res_data = serializersObj.data
        total = len(res_data)  # 数据总数
        PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
        all_page = PaginationObj.all_page()
        if  int(all_page)>=int(page):
            print(PaginationObj.start(),PaginationObj.end())
            res_data = res_data[PaginationObj.start():PaginationObj.end()]
        else:
            PaginationObj = Pagination(total, int(page)-1, perPageNum=pageSize, allPageNum=11)
            res_data = res_data[PaginationObj.start():PaginationObj.end()]
        print(res_data)
        return {"res_data": res_data, "total": total, "all_page": all_page}
    def post(self,req):
        serializersObj = serializers.S_addTimedTask(data=req.data,many=False)
        if serializersObj.is_valid(raise_exception=True):
            res_data=serializersObj.save()
            res_data=serializers.S_addTimedTask(res_data)
            data_obj=res_data.data
            res=self.taskList(req.data)
            s=myTimedTask()
            data=models.CasePlan.objects.get(id=data_obj["casePlanId"])
            arg = {
                "id": data.id,  #计划的id
                "t_id":data_obj["id"],
                "runType": 1,  #新增的定时任务始终执行类型始终都是为1
                "userId": data.userId.id,
                "CaseCount": data.CaseCount,
                "projectId": data.projectId.id,
                "againScript": data.againScript,
                "cron": data.cron,
                "taskName": data_obj["taskName"],
                "timedId":data_obj["status"]["id"]
                # "timedId": data["timedId"],
                # "taskId": data["taskId"]
            }
            s.run(arg)
            return APIResponse(200, "计划创建成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                               status=status.HTTP_200_OK)
class  ValidCron(APIView):
    def CronValid(self,cron):
        url = "https://www.iamwawa.cn/home/crontab/ajax"
        data = {'expression': cron}
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
        }
        res = requests.post(url, headers=header, data=data)
        return res.json()
    def  post(self,req):
        cron=req.data["cron"]
        res=self.CronValid(cron)
        if  int(res["status"])==1:
            return  APIResponse(200,"",results=res,status=status.HTTP_200_OK)
        else:
            res["info"]="Cron表达式格式错误"
            return APIResponse(200,"",results=res,status=status.HTTP_200_OK)
class GetTimedTask(APIView):
    """操作自定义的任务列表"""
    def isValid(self,data):
        kwargs = {}

        if "taskName" in data.keys():
            kwargs["taskName__icontains"] = data["taskName"]
        if "casePlanId" in data.keys():
            kwargs["casePlanId__name__icontains"] = data["casePlanId"]
        if "userId" in data.keys():
            kwargs["userId__name__icontains"] = data["userId"]
        return kwargs
    def  get(self,req):
        data=req.query_params

        res =addTimedTask().taskList(data,kwarg=self.isValid(data))
        return APIResponse(200, "", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)
class RemoveTimedTask(APIView):
    def post(self,req):
        data=req.data
        id=data["id"]
        obj=models.timedTask.objects.get(id=id)
        task_id=obj.taskId
        myTimedTask().deleteMyTask(task_id)  #同步删除celery任务
        obj.delete()   #删除的时候需要级联删除celery 任务表中数据

        res = addTimedTask().taskList(data,GetTimedTask().isValid(data))
        return APIResponse(200, "删除成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)
class UpdateTimedTask(APIView):
    def  post(self,req):
        data=req.data
        id=data["id"]
        obj=models.timedTask.objects.get(id=id)
        serializersObj = serializers.S_addTimedTask(data=req.data,instance=obj,partial=True)
        if serializersObj.is_valid(raise_exception=True):
            res_obj=serializersObj.save()
            res_data=serializers.S_addTimedTask(res_obj)
            data=res_data.data
            myTimedTask().updateMyTask(data)  #处理celery任务
            return APIResponse(200,"编辑成功",results=data,status=status.HTTP_200_OK)

class addSqlBox(APIView):
    """新增数据库连接"""

    def post(self,req):
        data=req.data
        serializersObj=serializers.S_addSqlBox(data=data)
        print(serializersObj)
        if  serializersObj.is_valid(raise_exception=True):
            serializersObj.save()
            kwargs = {}
            if "s_name" in data.keys():
                kwargs["name__icontains"] = data["s_name"]
            if "s_type" in data.keys():
                kwargs["type__name__icontains"] = data["s_type"]
            if "s_userId" in data.keys():
                kwargs["userId__name__icontains"] = data["s_userId"]
            s = SqlBoxMethods()
            res = s.taskList(data, kwarg=kwargs)
            return APIResponse(200, "添加成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                               status=status.HTTP_200_OK)

class SqlBoxMethods():
    def taskList(self,data,kwarg={},page=None,pageSize=None):
        id = data["projectId"]

        kwarg["projectId"]=id
        obj = models.SqlBox.objects.select_related("projectId", "userId").filter(**kwarg).order_by(
            "createTime").reverse()
        serializersObj = serializers.S_addSqlBox(obj, many=True)
        res_data = serializersObj.data
        total=None
        all_page=None
        if "page"  in  data.keys():
            page = data["page"]
            pageSize = data["pageSize"]
            total = len(res_data)  # 数据总数
            PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
            all_page = PaginationObj.all_page()
            if  int(all_page)>=int(page):
                print(PaginationObj.start(),PaginationObj.end())
                res_data = res_data[PaginationObj.start():PaginationObj.end()]
            else:
                PaginationObj = Pagination(total, int(page)-1, perPageNum=pageSize, allPageNum=11)
                res_data = res_data[PaginationObj.start():PaginationObj.end()]
        return {"res_data": res_data, "total": total, "all_page": all_page}


    def isValid(self,data):
        kwargs = {}
        if "name" in data.keys():
            kwargs["name__icontains"] = data["name"]
        if "type" in data.keys():
            kwargs["type__name__icontains"] = data["type"]
        if "userId" in data.keys():
            kwargs["userId__name__icontains"] = data["userId"]
        return kwargs
class  GetSqlBox(APIView):
    def get(self,req):
        data=req.query_params

        s=SqlBoxMethods()
        res=s.taskList(data,kwarg=s.isValid(data))
        return APIResponse(200, "", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)

class removeSqlBox(APIView):
    def post(self,req):
        data = req.data
        id=data["id"]
        models.SqlBox.objects.filter(id=id).delete()
        s = SqlBoxMethods()
        res = s.taskList(data, kwarg=s.isValid(data))
        return APIResponse(200, "删除成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)


class  updateSqlBox(APIView):
    def  post(self,req):
        data=req.data
        id=data["id"]
        serializersObj=serializers.S_addSqlBox(data=data,instance=models.SqlBox.objects.get(id=int(id)),partial=True)
        if  serializersObj.is_valid(raise_exception=True):
            res=serializersObj.save()
            res=serializers.S_addSqlBox(res)
            res_data=res.data
            return  APIResponse(200,"更新成功",results=res_data,status=status.HTTP_200_OK)


class GetBoxOrSqlType(APIView):
    """# 查询当前项目所有的数据库连接以及SQL类型"""
    def get(self,req):
        data=req.query_params
        projectId=data["projectId"]
        obj=models.SqlBox.objects.filter(projectId_id=int(projectId))
        serializersObj=serializers.S_addSqlBox(obj,many=True)
        sqlBoxList=serializersObj.data
        sqlType= [
            {"id": 1,"name" : "查"},
            {"id": 2, "name": "改"},
            {"id": 3, "name": "增"},
            {"id": 4, "name": "删"},
        ]
        return APIResponse(200,"",results={"sqlBoxList":sqlBoxList,"sqlType":sqlType},status=status.HTTP_200_OK)


class PageMethod():
    def __init__(self,mod,S_serializers,data,):
        self.mod=mod
        self.S_serializers=S_serializers
        self.data=data
    def taskList(self,kwarg={}):
        id = self.data["projectId"]
        page = self.data["page"]
        pageSize = self.data["pageSize"]
        kwarg["projectId"]=id
        obj = self.mod.objects.select_related("projectId", "userId").filter(**kwarg).order_by(
            "createTime").reverse()
        serializersObj = self.S_serializers(obj, many=True)
        res_data = serializersObj.data
        total = len(res_data)  # 数据总数
        PaginationObj = Pagination(total, page, perPageNum=pageSize, allPageNum=11)
        all_page = PaginationObj.all_page()
        if  int(all_page)>=int(page):
            print(PaginationObj.start(),PaginationObj.end())
            res_data = res_data[PaginationObj.start():PaginationObj.end()]
        else:
            PaginationObj = Pagination(total, int(page)-1, perPageNum=pageSize, allPageNum=11)
            res_data = res_data[PaginationObj.start():PaginationObj.end()]
        print(res_data)
        return {"res_data": res_data, "total": total, "all_page": all_page}
    def isValid(self):
        kwargs = {}
        if "s_name" in self.data.keys():
            kwargs["name__icontains"] = self.data["s_name"]
        if "s_type" in self.data.keys():
            kwargs["type__name__icontains"] = self.data["s_type"]
        if "s_userId" in self.data.keys():
            kwargs["userId__name__icontains"] = self.data["s_userId"]
        return kwargs
class AddSql(APIView):
    def post(self,req):
        data=req.data
        serializersObj=serializers.S_addSql(data=data)
        if  serializersObj.is_valid(raise_exception=True):
            serializersObj.save()
            s=PageMethod(models.SqlStatement,serializers.S_addSql,data)
            res=s.taskList(s.isValid())

            return APIResponse(200, "新增成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                               status=status.HTTP_200_OK)

class GetSql(APIView):
    def get(self,req):
        data=req.query_params
        s = PageMethod(models.SqlStatement, serializers.S_addSql, data)
        res = s.taskList(s.isValid())
        return APIResponse(200, "", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)

class UpdateSql(APIView):

    def envAction(self,data):
        key = data["name"]
        envId=data["envId"]
        id=data["id"]
        sql_saveResultChoice = models.SqlStatement.objects.get(id=id).saveResultChoice#原列表
        if sql_saveResultChoice:
            sql_saveResultChoice=json.loads(sql_saveResultChoice)

            saveResultChoice=json.loads(data["saveResultChoice"])  #新传列表

            save_list=list(set(sql_saveResultChoice)  & set(saveResultChoice))  #并集去重
            if saveResultChoice!= sql_saveResultChoice:
                for  ele  in save_list:   #删除新老列表都存在的类容
                    sql_saveResultChoice.remove(ele)
                    saveResultChoice.remove(ele)
                for item_old  in sql_saveResultChoice:
                    if item_old=="保存到全局变量":
                        envObj=Environments.objects.get(id=1)
                    if item_old=="保存到环境变量":
                        envObj = Environments.objects.get(id=envId)
                    value_obj = json.loads(envObj.value)
                    list_key=list(map(lambda x:list(x.keys())[0],value_obj))
                    index=list_key.index(key)
                    value_obj.pop(index)
                    envObj.value = json.dumps(value_obj)
                    envObj.save()


    def  post(self,req):
        data=req.data
        id=data["id"]
        self.envAction(data)


        serializersObj=serializers.S_addSql(data=data,instance=models.SqlStatement.objects.get(id=int(id)),partial=True)
        if  serializersObj.is_valid(raise_exception=True):
            res=serializersObj.save()
            res=serializers.S_addSql(res)
            res_data=res.data
            return  APIResponse(200,"更新成功",results=res_data,status=status.HTTP_200_OK)
class RemoveSql(APIView):
    def post(self,req):
        data = req.data
        id=data["id"]
        models.SqlStatement.objects.filter(id=id).delete()
        s = PageMethod(models.SqlStatement, serializers.S_addSql, data)
        res = s.taskList(s.isValid())
        return APIResponse(200, "删除成功", results=res["res_data"], total=res["total"], allPage=res["all_page"],
                           status=status.HTTP_200_OK)


class ValidSql(APIView):
    def sql(self,data):
        BoxId = data["BoxId"]
        sql=data["sql"]
        sqlId=data["id"]
        SqlActionResults = data["SqlActionResults"]
        obj = models.SqlBox.objects.get(id=BoxId)
        s = Con_sql(action=SqlActionResults, host=obj.host, port=int(obj.port), user=obj.userName, passwd=obj.passWord,
                    database=obj.database)
        res = s.runSql(sqlId,sql,1)
        return res
    def box(self,data):

        s = Con_sql(host=data["host"], port=int(data["port"]), user=data["user"], passwd=data["passwd"],
                    database=data["database"])
        res=s.connectSql()
        return res

    def post(self,req):
        data=req.data
        if int(data["Stype"])==1:  #校验sql
            res=self.sql(data)
            return APIResponse(200, "SQL执行成功", results=res, status=status.HTTP_200_OK)
        else:
            res=self.box(data)
            return APIResponse(200, "数据库连接成功", results=res, status=status.HTTP_200_OK)








