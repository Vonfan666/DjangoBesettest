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
        print(data)
        data=serializers.S_Department(data,many=True)
        print(data)

        return APIResponse(200,"success",results=data.data,status=status.HTTP_200_OK)

class Registers(APIView):
    def post(self,request):
        return APIResponse(200, "success", results={}, status=status.HTTP_200_OK)
