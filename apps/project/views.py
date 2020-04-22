from django.shortcuts import render
from  rest_framework.views import APIView,status
from . import models,serializers
from libs.api_response import APIResponse
from libs.many_or_one import ManyOrOne
# Create your views here.
from  users.models import UserProfile


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
            valid_data = serializers.S_ProjectList(obj, many=Many1)
            totalCount = len(valid_data.data)  # 总数

            PaginationObj = Pagination(totalCount, currentPage, perPageNum=size, allPageNum=11)
            all_page = PaginationObj.all_page()
            return APIResponse(200,"新增成功",results=res_data.data,total=totalCount,page_size=all_page,status=status.HTTP_200_OK)

class EditProject(APIView):
    """编辑项目"""
    def post(self,req):
        data=req.data
        print(data)
        id=req.data["id"]
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

        data=req.data
        print(data)
        id=data["id"]

        if( models.ProjectList.objects.filter(id=id)):
            models.ProjectList.objects.filter(id=id).delete()
            obj = models.ProjectList.objects.all()
            currentPage = int(data["page"])  # 当前请求的是第几页
            size = int(data["page_size"])  # 每页展示输了
            totalCount = len(obj)  # 总数
            PaginationObj = Pagination(totalCount, currentPage, perPageNum=size, allPageNum=11)
            all_page = PaginationObj.all_page()
            Many = ManyOrOne.IsMany(obj)
            valid_data = serializers.S_ProjectList(obj, many=Many)
            return APIResponse(200, "删除成功", results=valid_data.data ,total=totalCount,page_size=all_page,status=status.HTTP_200_OK)
        else:
            return  APIResponse(400, "项目不存在", results=[] ,status=status.HTTP_200_OK)

class  LastProject(APIView):
    """用户最后一次访问项目"""
    def get(self,req):
        print(req)
        userId=req.query_params
        print(userId["userId"])
        project_id=UserProfile.objects.filter(id=userId["userId"]).values("user_last_project")
        print(project_id)
        return APIResponse(200,"",project_id[0],status=status.HTTP_200_OK,)

