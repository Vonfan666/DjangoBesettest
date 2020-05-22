import  json,os
from rest_framework import serializers
from rest_framework.validators import ValidationError
from  . import  models


class S_CaseGroup(serializers.ModelSerializer):
    """查询用例文件分组以及其下内容序列化类"""
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    isInterface=serializers.SerializerMethodField()
    def get_isInterface(self,obj):
        a=obj
        print(obj.id)
        print(obj.idCaseGroupFiles.all().values("name"))

        return  obj.idCaseGroupFiles.all().values()
    class Meta:
        model=models.CaseGroupFiles
        fields="__all__"