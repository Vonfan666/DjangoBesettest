from django.shortcuts import render
from  rest_framework.views import APIView,status
from django.db.models import  Q
from libs.api_response import APIResponse
from . import models,serializers
import  json,requests,os
# Create your views here


class CaseGroup(APIView):
    """查询当前项目的用例文件夹以及用例
    :param id  项目id
    """
    def get(self,req):
        params = req.query_params
        id=params.get("id")
        obj=models.CaseGroupFiles.objects.filter(projectId_id=id)
        serializersObj=serializers.S_CaseGroup(obj,many=True)
        print(serializersObj.data)
        return APIResponse(200,"sucess",results=serializersObj.data,status=status.HTTP_200_OK)