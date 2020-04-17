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
    # det=serializers.SerializerMethodField()  #自定义字段
    #
    # def get_det(self,obj):   #处理自定义字段的返回值-OBJ就是当前的整个UserProfiled的对象
    #     return {obj.det.}

    class Meta:
        model=models.UserProfile
        # department=models.Department
        fields=["username","name","password","det"]





    # def validate(self, attrs):
    #     attrs["det"]=attrs

    def create(self,  validated_data):
        user=super().create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        # validated_data["det"]=validated_data["department"].filter("det")
        user.save()
        return user(det=self.context["det"],**validated_data)

