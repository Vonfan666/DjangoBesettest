import  json
from django.shortcuts import render
from  rest_framework.views import APIView,status
from . import models,serializers
from libs.api_response import APIResponse
from libs.many_or_one import ManyOrOne
# Create your views here.
from  users.models import UserProfile
import json
from collections import OrderedDict

from  libs.Pagination import Pagination


class ProjectList(APIView):
    """查找项目"""
    def  get(self,req):
        params=req.query_params
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
class AddProject(APIView):
    """新增项目"""
    def post(self,req):
        data=req.data
        Many = ManyOrOne.IsMany(data)
        obj=serializers.S_AddProject(data=data,many=Many)
        currentPage = int(data["page"])  # 当前请求的是第几页
        size = int(data["page_size"])  # 每页展示输了

        if obj.is_valid(raise_exception=True):
            a=obj.save()
            res_data=serializers.S_AddProject(a)

            obj = models.ProjectList.objects.all().order_by("create_time").reverse()
            Many1=ManyOrOne.IsMany(obj)
            valid_data = serializers.S_ProjectList(obj,many=Many1)
            totalCount = len(valid_data.data)  # 总数

            PaginationObj = Pagination(totalCount, currentPage, perPageNum=size, allPageNum=11)
            all_page = PaginationObj.all_page()
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



class PostMethods(APIView):
    """返回所有的请求数据"""
    def get(self,req):
        postMthodObj=models.PostMethods.objects.all()
        postTypeObj=models.PostType.objects.all()
        resTypeObj=models.ResType.objects.all()
        res_post_methods=serializers.S_PostMethods(postMthodObj,many=True)
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
    """新增接口文档"""
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
            res_data["post_header"]=json.loads(res_data["post_header"])
            res_data["post_data"]=json.loads(res_data["post_data"])
            res_data["res_header"]=json.loads( res_data["res_header"])
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
            return  APIResponse(401,"修改失败,请联系管理员",status=status.HTTP_200_OK)

class RmoveFiles(APIView):
    """删除接口文件"""
    def  post(self,req):
        id=req.data["id"]
        try:
            models.InterfaceFiles.objects.filter(id=id).delete()
            return  APIResponse(200,"sucess",status=status.HTTP_200_OK)
        except:
            return  APIResponse(401,"修改失败,请联系管理员",status=status.HTTP_200_OK)
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
