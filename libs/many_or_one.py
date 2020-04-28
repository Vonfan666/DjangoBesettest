#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年04月16日23时07分17秒
from rest_framework.views import APIView
from .api_response import APIResponse
from rest_framework import status

class ManyOrOne(APIView,APIResponse):
    def IsMany(self,request_data):
        # request_data=request_data.dict()
        # if("QuerySet" in type(request_data)):
        #     Many = True
        #     return Many
        if isinstance(request_data, dict) and request_data is not None:
            Many = False
            return Many
        elif isinstance(request_data, list) and request_data is not None:
            Many = True
            return Many
        elif len(request_data)>1:
            Many=True
            return Many
        elif len(request_data)<=1:
            Many=False
            return Many
        else:
            print("草你爹")
            return APIResponse(
                401, "数据错误,无法新增",
                results=[],
                status=status.HTTP_400_BAD_REQUEST
            )

ManyOrOne=ManyOrOne()
