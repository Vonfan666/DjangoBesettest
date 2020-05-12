#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年04月16日22时50分19秒
import  json
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
    name = serializers.CharField( max_length=5,help_text="密码",error_messages={
        "max_length":"最多输入五位数"
    })
    username=serializers.CharField(required=True,help_text="账号",error_messages={
        "required":"账号已存在",
    })
    def get_det(self,obj):   #处理自定义字段的返回值-OBJ就是当前的整个UserProfiled的对象
        obj=getattr(obj,"det")
        return {"name": getattr(obj,"name",""), "department_id":getattr(obj,"department_id","")}

    def get_grp(self,obj):
        obj=getattr(obj,"grp")  #
        return {"user_group_id":getattr(obj,"user_group_id","")}
    class Meta:
        model=models.UserProfile
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
        print("det" in attrs.keys())
        if "det" not in self.initial_data.keys():
            raise  ValidationError("缺少部门ID")
        # attrs["det"]=self.initial_data["det"]
        return attrs
    def create(self,  validated_data):
        if  "det"  in  self.initial_data:
            validated_data["det"]=models.Department.objects.get(id=self.initial_data["det"])
        user=super().create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

