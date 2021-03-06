import  json,requests,os
from django.shortcuts import render
from  rest_framework.views import APIView,status
from  users.models import UserProfile
from rest_framework import permissions
# Create your views here.
from  libs.Pagination import Pagination
from . import models,serializers
from libs.api_response import APIResponse,MockResponse
from libs.many_or_one import ManyOrOne
from  libs.public import Public
from  case import  models as caseModels
from  users import  models as usersModels
from django.db.models import  Q
from log.logFile import logger as logs
logger=logs(__name__)
class ProjectList(APIView):
    """查找项目"""
    def  get(self,req):
        params=req.query_params

        print(params)
        print(params.get("id"))
        print(params.keys())
        if "id"  in params:
            #查询当前用户是否为该项目的创建人--如果是创建人则返回1-可以允许同步 否则不允许同步
            id=params.get("id")
            userId = params.get("userId")
            obj=models.ProjectList.objects.filter(Q(id=id) & Q(user_id=userId) &Q(status=0))
            if obj:
                res_data=serializers.S_ProjectList(obj[0],many=False)
                obj=res_data.data
                return  APIResponse(200,"",results=obj,code=1,status=status.HTTP_200_OK)
            else:
                return APIResponse(200, "", code=0, status=status.HTTP_200_OK)
        else:
            try:
                obj=models.ProjectList.objects.all().order_by("create_time").reverse() #根据创建时间从大到小排序
                currentPage = int(params["page"])  #当前请求的是第几页
                size=int(params["page_size"])  #每页展示输了
                totalCount=len(obj)  #总数
                PaginationObj=Pagination(totalCount, currentPage, perPageNum=size,allPageNum=11)
                all_page=PaginationObj.all_page()
                Many = ManyOrOne.IsMany(obj)
                valid_data=serializers.S_ProjectList(obj,many=Many)
                res_data=valid_data.data[PaginationObj.start():PaginationObj.end()]
                return APIResponse(200,"success",results=res_data,total=totalCount,page_size=all_page,status=status.HTTP_200_OK)

            except:
                obj = models.ProjectList.objects.all().order_by("create_time").reverse()  # 根据创建时间从大到小排序
                Many = ManyOrOne.IsMany(obj)
                valid_data = serializers.S_ProjectList(obj, many=Many)
                return APIResponse(200, "success", results=valid_data.data,
                                   status=status.HTTP_200_OK)
class ProjectUnityStatus(APIView):
    """修改同步状态
        :param id  项目id
        :param key==1 放弃修改
        :param key==2 下次修改
        :param key==3 确认同步
    """
    def  post(self,req):
        print(req)
        key=req.data.get("key")
        id=req.data.get("id")
        userId=req.data.get("userId")
        if int(key)==1:
            models.ProjectList.objects.filter(Q(id=int(id)) & Q(user_id=int(userId))).update(status=1)
            return APIResponse(200, "操作成功", status=status.HTTP_200_OK)
        if int(key)==2:
            return APIResponse(200, "操作成功", status=status.HTTP_200_OK)
        if int(key)==3:
            #这里需要判断已经同步过了--防止接口请求过来搞乱数据
            models.ProjectList.objects.filter(Q(id=int(id)) & Q(user_id=int(userId))).update(status=1)
            #接口文件以及其下类容 为这个id的 name并 存入数据库
            obj=models.InterfaceFilesName.objects.filter(project_id=id)
            obj=serializers.S_ProjectUnityStatus(obj,many=True)
            print(obj)
            validate_data=serializers.S_ProjectUnityCreate(data=obj.data,many=True)
            print(validate_data)
            if validate_data.is_valid(raise_exception=True):
                res_data=validate_data.save()
                serializers.S_ProjectUnityCreate(res_data,many=True)
            interfaceObj=models.InterfaceFiles.objects.filter(Q(project=id) & Q(file__isnull=False))
            print("interfaceObj",interfaceObj)
            Interface_obj=serializers.S_ProjectUnityInterface(interfaceObj,many=True)
            Interface_obj=Interface_obj.data
            print(Interface_obj)
            Interface_validate_data=serializers.S_ProjectUnityInterfaceCreate(data=Interface_obj,many=True,context={"n":0})
            if Interface_validate_data.is_valid(raise_exception=True):
                Interface_validate_data.save()

            return APIResponse(200, "同步成功", status=status.HTTP_200_OK)
class AddProject(APIView):
    """新增项目"""
    def post(self,req):
        data=req.data
        Many = ManyOrOne.IsMany(data)
        obj=serializers.S_AddProject(data=data)
        currentPage = int(data["page"])  # 当前请求的是第几页
        size = int(data["page_size"])  # 每页展示输了

        if obj.is_valid(raise_exception=True):
            a=obj.save()
            res_data=serializers.S_AddProject(a)

            obj = models.ProjectList.objects.select_related().all().order_by("create_time").reverse()
            print(obj)
            Many1=ManyOrOne.IsMany(obj)
            valid_data = serializers.S_ProjectList(obj,many=Many1)
            totalCount = len(valid_data.data)  # 总数

            PaginationObj = Pagination(totalCount, currentPage, perPageNum=size, allPageNum=11)
            all_page = PaginationObj.all_page()
            print(res_data)
            print(res_data.data)
            id=res_data.data["id"]
            userId=res_data.data["user"]["id"]

            #添加项目时,同步users和projectLsit多对多的表
            # projectObj=models.ProjectList.objects.get(id=id)
            # usersObj=usersModels.UserProfile.objects.get(id=userId)
            # models.UsersToProject.objects.create(projectId=projectObj,userId=usersObj)

            return APIResponse(200,"新增成功",results=res_data.data,total=totalCount,page_size=all_page,status=status.HTTP_200_OK)
class EditProject(APIView):
    """编辑项目"""
    def post(self,req):
        data=req.data
        print(data)
        id=int(data["id"])
        print(id)
        edit_obj=models.ProjectList.objects.get(id=id)
        print(edit_obj)
        valida=serializers.S_UpdateProject(data=data,instance=edit_obj,many=False,partial=True)
        if valida.is_valid(raise_exception=True):
            a=valida.save()
            print(a)
            res_data=serializers.S_UpdateProject(a).data
            print((res_data))
            return APIResponse(200, "修改成功", results=res_data, status=status.HTTP_200_OK)
class RmoveProject(APIView):
    """删除项目"""
    def post(self,req):
        data = req.data
        print(data)
        id = int(data["id"])
        if (models.ProjectList.objects.filter(id=id)):
            models.ProjectList.objects.filter(id=int(id)).delete()

            obj = models.ProjectList.objects.all()
            currentPage = int(data["page"])  # 当前请求的是第几页
            size = int(data["page_size"])  # 每页展示输了
            totalCount = len(obj)  # 总数
            PaginationObj = Pagination(totalCount, currentPage, perPageNum=size, allPageNum=11)
            all_page = PaginationObj.all_page()
            Many = ManyOrOne.IsMany(obj)
            valid_data = serializers.S_ProjectList(obj, many=Many)
            return APIResponse(200, "删除成功", results=valid_data.data, total=totalCount, page_size=all_page,
                               status=status.HTTP_200_OK)
        else:
            return APIResponse(400, "项目不存在", results=[], status=status.HTTP_200_OK)
class  LastProject(APIView):
    """用户最后一次访问项目"""
    def get(self,req):
        print(req)
        userId=req.query_params
        print(userId["userId"])
        project_id=UserProfile.objects.filter(id=userId["userId"]).values("user_last_project")
        print(project_id)
        return APIResponse(200,"",project_id[0],status=status.HTTP_200_OK,)
    def post(self,req):
        userId=req.data["userId"]
        projectId=req.data["projectId"]
        UserProfile.objects.filter(id=userId).update(user_last_project=projectId)
        return APIResponse(200,"success",status=status.HTTP_200_OK)
# from django.forms.models import model_to_dict
class PostMethods(APIView):
    """返回所有的请求数据"""
    def get(self,req):
        postMthodObj=models.PostMethods.objects.all()
        postTypeObj=models.PostType.objects.all()
        resTypeObj=models.ResType.objects.all()
        res_post_methods=serializers.S_PostMethods(postMthodObj,many=True)
        a=res_post_methods.data
        res_post_type=serializers.S_PostType(postTypeObj,many=True)
        res_res_type=serializers.S_ResType(resTypeObj,many=True)
        return  APIResponse(200,"sucess",res_post_methods=res_post_methods.data,
                            res_post_type=res_post_type.data,
                            res_res_type=res_res_type.data
                            ,status=status.HTTP_200_OK)
class addFilesName(APIView):
    """新增文件夹"""
    def post(self,req):
        data=req.data
        valid_data=serializers.S_InterfaceFilesName(data=data,many=False)
        if  valid_data.is_valid(raise_exception=True):
            res_data=valid_data.save()
            res_data=serializers.S_InterfaceFilesName(res_data)
            return APIResponse(200,"添加成功",data=res_data.data,status=status.HTTP_200_OK)
class EditFilesName(APIView):
    """修改文件夹名称
        :param
        id      文件夹id
        name    修改后的文件夹名称
    """
    def post(self,req):
        data=req.data
        editObj=models.InterfaceFilesName.objects.get(id=data["id"])
        valid_data=serializers.S_InterfaceFilesName(data=data,instance=editObj,many=False,partial=True)
        if  valid_data.is_valid(raise_exception=True):
            valid_data=valid_data.save()
            res_data=serializers.S_InterfaceFilesName(valid_data)
            res_data=res_data.data
            return APIResponse(200,"修改成功",results=res_data,status=status.HTTP_200_OK)
class RemoveFilesName(APIView):
    """
    删除接口文件夹
    :param
    id 文件夹ID
    """
    def  post(selfs,req):
        id=req.data["id"]
        models.InterfaceFilesName.objects.get(id=id).delete()
        return APIResponse(200,"删除成功",status=status.HTTP_200_OK)

class  SelectFilesName(APIView):
    """
    查看接口文件夹，以及其下内容
    :param projectId
    """
    def get(self,req):
        projectId=req.query_params["projectId"]
        obj=models.InterfaceFilesName.objects.filter(project_id=projectId)
        print(obj,"1111")
        res_data=serializers.S_select_InterfaceFilesName(obj,many=True)
        res_data=res_data.data
        print(res_data)
        return APIResponse(200,"sucess",results=res_data,status=status.HTTP_200_OK)

class  addFiles(APIView):
    """新增接口文档
    :param
    """
    def post(self,req):
        data=req.data
        print(data)
        Many =ManyOrOne.IsMany(data)
        # obj=serializers.S_AddFiles(data=data, many=Many)
        obj=serializers.S_AddFiles(data=data, many=Many)
        if obj.is_valid(raise_exception=True):
            save_data=obj.save()
            res_data=serializers.S_AddFiles(save_data).data
            #将数据库取出来的序列化列表数据读出来
            if res_data["post_header"]:
                res_data["post_header"]=json.loads(res_data["post_header"])
            if res_data["post_data"]:
                res_data["post_data"]=json.loads(res_data["post_data"])
            if res_data["res_header"]:
                res_data["res_header"]=json.loads( res_data["res_header"])
            if res_data["res_data"]:
                res_data["res_data"]=json.loads(res_data["res_data"])
            return APIResponse(200,"sussces",results=res_data,status=status.HTTP_200_OK)
class EditFiles(APIView):
    """编辑接口文件"""
    def post(self,req):
        id=req.data["id"]
        name=req.data["name"]
        try:
            models.InterfaceFiles.objects.filter(id=id).update(filesName=name)
            return  APIResponse(200,"sucess",status=status.HTTP_200_OK)
        except:
            return  APIResponse(409,"修改失败,请联系管理员",status=status.HTTP_200_OK)

class RmoveFiles(APIView):
    """删除接口文件"""
    def  post(self,req):
        id=req.data["id"]
        try:
            models.InterfaceFiles.objects.filter(id=id).delete()
            return  APIResponse(200,"sucess",status=status.HTTP_200_OK)
        except:
            return  APIResponse(409,"修改失败,请联系管理员",status=status.HTTP_200_OK)
from django.forms.models import model_to_dict
class CopyFiles(APIView):
    """复制接口文件
        :param 儿子id    项目id  oldFileId   newFileId
        首先复制一个文件，然后复制一份数据，且数据关联到这个文件的id

    """

    def  post(self,req):
        id=req.data["id"]
        # projectId=req.data["projectId"]
        userId=req.data["userId"]
        fileId=req.data["fileId"]
        oldObj=models.InterfaceFiles.objects.filter(id=int(id))
        # Many=ManyOrOne.IsMany(oldObj)
        data=serializers.S_CopyFiles(oldObj,many=True)
        a=data.data
        try:
            b = json.loads(json.dumps(a))[0]
            b["resTypeId"]=b["res_type"]
            b["postMethodsId"]=b["post_methods"]
            b["postTypeId"]=b["post_type"]
            b["fileId"]=fileId
            b["projectId"]=b["project"]
            b["createUserId"]=userId
            del b["res_type"]
            del b["post_methods"]
            del b["post_type"]
            del b["file"]
            del b["id"]
            del b["update_time"]
            del b["create_time"]
            del b["project"]
            obj = serializers.S_AddFiles(data=b, many=False)
            if obj.is_valid(raise_exception=True):
                save_data = obj.save()
                res_data = serializers.S_AddFiles(save_data).data
                # 将数据库取出来的序列化列表数据读出来
                res_data["post_header"] = json.loads(res_data["post_header"])
                res_data["post_data"] = json.loads(res_data["post_data"])
                res_data["res_header"] = json.loads(res_data["res_header"])
                res_data["res_data"] = json.loads(res_data["res_data"])
                return APIResponse(200, "sussces", results=res_data, status=status.HTTP_200_OK)
        except:
            return  APIResponse(200,"SUCESS",results=a,status=status.HTTP_200_OK)



#接口文档数据类型操作
class  InterfaceDetailGet(APIView):
    """查询接口文档数据"""
    def get(self,req):
        data=req.query_params
        obj=models.InterfaceFiles.objects.filter(project=int(data["projectId"]),id=int(data["id"]))
        obj=serializers.S_interfaceDetail(obj,many=True)
        obj=obj.data

        return APIResponse(200,"sucess",obj,status=status.HTTP_200_OK)

class EditInterfaceDetail(APIView):
    """修改接口文档数据"""
    def  post(self,req):
        data= req.data
        print(data.dict())
        id= req.data["id"]
        # print(data["postMethodsId"])
        # print(models.PostMethods.objects.get(id=data["postMethodsId"]))
        # data["postMethodsId"]=models.PostMethods.objects.get(id=data["postMethodsId"])
        oldObj=models.InterfaceFiles.objects.get(id=id)
        valida_obj=serializers.S_updateFiles(data=data,instance=oldObj,partial=True,many=False)
        if valida_obj.is_valid(raise_exception=True):
            res_obj=valida_obj.save()
            res_obj=serializers.S_updateFiles(res_obj)
            res_data=res_obj.data
            if res_data["post_header"]:
                res_data["post_header"]=json.loads(res_data["post_header"])
            if res_data["post_data"]:
                res_data["post_data"]=json.loads(res_data["post_data"])
            if res_data["res_header"]:
                res_data["res_header"]=json.loads( res_data["res_header"])
            if res_data["res_data"]:
                res_data["res_data"]=json.loads(res_data["res_data"])

            return APIResponse(200,"sucess",results=res_data,status=status.HTTP_200_OK)


class MockPost(APIView):
    """前端传一个mockattr  后端处理 resdata返回键值对格式数据
    :param dada{url:"",data:"",headers:""}
    """
    permission_classes = (permissions.AllowAny,)
    def post(self,req):
        data=req.data
        print(data)
        headers=json.loads(data["headers"])
        url=data["url"]
        data=data["data"]
        try:
            res=requests.post(url,headers=headers,data=json.loads(data))
        except:
            res=requests.post(url,headers=headers,json=data)
        return  MockResponse(res.json(),status=status.HTTP_200_OK)
    def get(self,req):
        data = req.query_params
        print(data)
        headers = data["headers"]
        url = data["url"]
        data = data["data"]
        try:
            res=requests.get(url,headers=headers,data=json.loads(data))
        except:
            res=requests.get(url,headers=headers,json=data)
        return  MockResponse(res.json(),status=status.HTTP_200_OK)
class MockRes(APIView):
    """
    ：:param   mock_type ==1  是文档返回  2是自定义返回  默认文档返回
    """
    permission_classes = (permissions.AllowAny,)

    def  post(self,req):
        # # logger.info("哲哥传入参数:%s"%req.data.dict())
        # logger.info("哲哥传入参数:%s" % json.load(req))
        path=req.path
        obj=models.InterfaceFiles.objects.filter(mock_attr__contains=path).values("res_header","res_data","mock_type","mock_data")
        # res_data={}
        if str(obj[0]["mock_type"])=="2":
            res_data_c=obj[0]["mock_data"]
            res_data_c=json.loads(res_data_c)
        else:
            res_data=obj[0]["res_data"]
            res_data=json.loads(res_data)
            res_data_c={}
            res_data_c=Public().forData(res_data,res_data_c)
        return MockResponse(res_data_c,status=status.HTTP_200_OK)
    def  get(self,req):
        # logger.info("哲哥传入参数:%s"%req.query_params.dict())
        logger.info("哲哥传入参数:%s" % json.load(req))
        path=req.path
        obj=models.InterfaceFiles.objects.filter(mock_attr__contains=path).values("res_header","res_data","mock_type","mock_data")
        print(obj[0])
        # res_data={}
        if str(obj[0]["mock_type"])=="2":
            res_data_c=obj[0]["mock_data"]
            res_data_c=json.loads(res_data_c)
        else:
            res_data=obj[0]["res_data"]
            res_data=json.loads(res_data)
            res_data_c={}
            res_data_c=Public().forData(res_data,res_data_c)
        return MockResponse(res_data_c,status=status.HTTP_200_OK)
class MockResData(APIView):
    """
    修改模拟返回数据的类型
    :param typpe  is  str  1返回文档  2返回自定义mockData字段
    :param mockData   自定义mock字段--可以接受为空-但必须是标准jon数据
    """
    permission_classes = (permissions.AllowAny,)
    def  post(self,req):
        data=req.data
        print(data)
        id=data["id"]
        obj=models.InterfaceFiles.objects.get(id=id)
        validate_data=serializers.S_interfaceDetail(data=data,instance=obj,many=False,partial=True)
        if validate_data.is_valid(raise_exception=True):
            validate_data.save()
            type = str(data["mock_type"])
            msg = "当前返回自定义mock数据"
            msg = "当前返回文档mock数据" if type=="1" else msg
            return APIResponse(200,msg,status=status.HTTP_200_OK)


class  EnvironmentsAdd(APIView):
    """新增环境/修改 新增 删除变量
    :param id 环境变量id
    :param  name  环境名称
    :param  value  环境变量的值  [{}]
    :param  is_eg  变量类型   #1是全局变量  0是环境变量
    """
    def  post(self,req):
        #加一个判断-如果存在就更新数据库
        data = req.data
        id=None
        if "id"  in data.keys() and data["id"]!="":
            print(data.keys())
            id=data["id"]
        validate_data = serializers.S_Environments(data=data)
        if validate_data.is_valid(raise_exception=True):
            data = json.loads(json.dumps(data))
            obj, created=models.Environments.objects.update_or_create(defaults=data,id=id)
            res_obj = serializers.S_Environments(obj)
            data = res_obj.data
            data["value"]=json.loads(data["value"])
            return APIResponse(200,"操作成功",results=data,status=status.HTTP_200_OK)

class  EnvironmentsSelect(APIView):
    """查询环境
    """
    def  get(self,req):
        g = models.Environments.objects.all()  # 查询全局变量
        print(g)
        globalEnt=models.Environments.objects.filter(is_eg=1) #查询全局变量
        globalEnt=serializers.S_EnvironmentsSelect(globalEnt,many=True)
        G_data= globalEnt.data
        print(G_data)
        Ent=models.Environments.objects.filter(is_eg=0) #查询环境变量
        Ent = serializers.S_EnvironmentsSelect(Ent, many=True)
        E_data= Ent.data
        return APIResponse(200,"sucess",results={"G_data":G_data,"E_data":E_data},status=status.HTTP_200_OK)

class  EnvironmentsDelete(APIView):
    """删除环境"""
    def post(self,req):
        id=req.data["id"]
        a = models.Environments.objects.all()
        obj=models.Environments.objects.filter(id=id).select_related()
        if obj:
            models.Environments.objects.filter(id=id).delete()
            return APIResponse(200,"删除成功",status=status.HTTP_200_OK)

        return APIResponse(200, "删除失败,环境不存在", status=status.HTTP_200_OK)

class MenuView(APIView):
    def get(self, request, format=None):
        menus = models.Menu.objects.filter(parent=None)
        serializer = serializers.MenuSerializer(menus, many=True)
        return APIResponse(200,"sucess",results=serializer.data,status=status.HTTP_200_OK)