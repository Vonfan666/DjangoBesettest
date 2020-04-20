#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年04月16日22时50分19秒

from  rest_framework import serializers
from  . import models
from  rest_framework.validators import ValidationError


class  S_Department(serializers.ModelSerializer):
    class Meta:
        model=models.Department
        exclude=["id"]

class S_Register(serializers.ModelSerializer):
    det=serializers.SerializerMethodField()  #自定义字段
    grp=serializers.SerializerMethodField()
    name = serializers.CharField( max_length=5,error_messages={
        "max_length":"最多输入五位数"
    })
    #
    username=serializers.CharField(required=True,error_messages={
        "required":"账号已存在"
    })
    def get_det(self,obj):   #处理自定义字段的返回值-OBJ就是当前的整个UserProfiled的对象
        return {"name":obj.det.name,"department_id":obj.det.department_id}

    def get_grp(self,obj):
        return {"user_group_id":obj.grp.user_group_id}
    class Meta:
        model=models.UserProfile
        # department=models.Department
        fields=["username","name","password","det","grp"]


    def  validate(self, attrs):
        username=attrs.get("username")
        password = attrs.get("password")
        if len(username)!=11:
            raise ValidationError("账号长度不为11位")
        if len(password)<6:
            raise  ValidationError("密码长度过短")
        if models.UserProfile.objects.filter(username=username):
            raise  ValidationError("用户已存在")
        return attrs


    # def validate(self, attrs):
    #     attrs["det"]=attrs

    def create(self,  validated_data):
        user=super().create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

