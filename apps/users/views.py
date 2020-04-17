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

        validate_data=serializers.S_Register(data=data,many=True,context={"det":data})
        if validate_data.is_valid(raise_exception=True):
            validate_data.save()
            print("data",validate_data)
            res_data=serializers.S_Register(data).data
            print(res_data)
        return APIResponse(200, "success", status=status.HTTP_200_OK)
