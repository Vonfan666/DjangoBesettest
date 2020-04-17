#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年04月16日21时54分33秒

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import UserProfile
from rest_framework.exceptions import ValidationError

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """


    def authenticate(self,request,username=None, password=None, **kwargs):

        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobil=username))
            if user.check_password(password):
                print(user)
                return user
            else:
                raise ValidationError("用户名或密码错误")

        except:
            raise ValidationError("用户名或密码错误")
def jwt_success_response(token, user=None, request=None):
    print(token)
    print(user)
    data = {
        "status":"200",
        'token': token,
        "results":{
        'username': user.username,
        'user_id': user.id,
    },
        "message":"登录成功"
    }
    #这里不能用APIResponse返回，无提示APIResponse无法序列化--
    return data


def jwt_error_response(serializer , request = None):
    data={
        "msg":"用户名或密码错误",
        "status":200,

        "detail":serializer.errors

    }
    return data