from django.shortcuts import render
from . import models,serializers
from  libs.api_response import APIResponse
# Create your views here.
from  rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

class Department(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,request):
        data=models.Department.objects.all()
        data=serializers.S_Department(data,many=True)
        return APIResponse(200,"success",results=data.data,status=status.HTTP_200_OK)

class Registers(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        data=request.data
        print(data)

        validate_data=serializers.S_Register(data=data,many=False)
        if validate_data.is_valid(raise_exception=True):
            a=validate_data.save()
            print("data",validate_data)
            res_data=serializers.S_Register(a).data
            print(res_data)
            return APIResponse(200, "注册成功",results=res_data, status=status.HTTP_200_OK)
        else:
            return APIResponse(200,"注册失败",results={},status=status.HTTP_200_OK)

