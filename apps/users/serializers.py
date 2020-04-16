#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年04月16日22时50分19秒

from  rest_framework import serializers
from  . import models



class  S_Department(serializers.ModelSerializer):
    class Meta:
        model=models.Department
        exclude=["id"]

class S_Register(serializers.ModelSerializer):
    create_time=serializers.SerializerMethodField()
    update_time=serializers.SerializerMethodField()

    class Meta:
        model=models.UserProfile
        fields=["username","name","password","department_id"]

