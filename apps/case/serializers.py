import  json,os
from rest_framework import serializers
from rest_framework.validators import ValidationError
from libs.validated_update import Validated_data
from project import models as projectModels
from users import  models as usersModels


from  . import  models
s=Validated_data()
class S_caseGtoupInterface(serializers.ModelSerializer):
    """序列化接口"""
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    CaseGroupFilesId=serializers.SerializerMethodField()
    def get_CaseGroupFilesId(self,obj):
        return obj.CaseGroupFilesId_id
    class Meta:
        model=models.CaseGroup
        fields="__all__"
class S_CaseGroupFiles(serializers.ModelSerializer):
    """查询用例文件分组以及其下内容序列化类"""
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    # isInterface=serializers.SerializerMethodField()
    idCaseGroupFiles=S_caseGtoupInterface(many=True,read_only=True)
    class Meta:
        model=models.CaseGroupFiles
        fields="__all__"

class S_AddGroup(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    idCaseGroupFiles = S_caseGtoupInterface(many=True, read_only=True)
    class Meta:
        model=models.CaseGroupFiles
        fields="__all__"

    def create(self, validated_data):

        s.validated_data_add(validated_data,self.initial_data,projectModels.ProjectList,"projectId","projectId")
        s.validated_data_add(validated_data,self.initial_data,usersModels.UserProfile,"userId","userId")
        user=super().create(validated_data=validated_data)
        user.save()
        return user


class S_AddCase(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.CaseGroup
        fields = "__all__"

    def create(self, validated_data):
        s.validated_data_add(validated_data, self.initial_data, models.CaseGroupFiles, "CaseGroupFilesId", "CaseGroupFilesId")
        s.validated_data_add(validated_data, self.initial_data, usersModels.UserProfile, "userId", "userId")
        user = super().create(validated_data=validated_data)
        user.save()
        return user