#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年04月16日23时08分50秒

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class APIResponse(Response):
    def __init__(self, data_status, data_msg, results=None,
                 status=None, headers=None, content_type=None,*args ,**kwargs):
        data = {
            'status': data_status,
            'msg': data_msg
        }
        if results is not None:
            data['results'] = results
        data.update(kwargs)
        super().__init__(data=data, status=status, headers=headers, content_type=content_type)