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

class S_AddInterface(serializers.ModelSerializer):
        createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
        updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
        CaseGroupId=serializers.SerializerMethodField()
        data=serializers.SerializerMethodField()
        headers=serializers.SerializerMethodField()
        # dataType=serializers.SerializerMethodField
        # postMethod=serializers.SerializerMethodField()
        # environmentId=serializers.SerializerMethodField()

        userId=serializers.SerializerMethodField()
        status=serializers.SerializerMethodField()
        def  get_CaseGroupId(self,obj):
            return  {"id":obj.CaseGroupId.id,"name":obj.CaseGroupId.name}

        def get_userId(self,obj):
            return  {"id":obj.userId.id,"name":obj.userId.name}

        def get_status(self,obj):
            return {"id":obj.status,"name":obj.get_status_display()}
        def get_data(self,obj):
            if obj.data:
                return json.loads(obj.data)
        def get_headers(self,obj):
            if obj.headers:
                print(obj.headers)
                return json.loads(obj.headers)
        class Meta:
            model=models.CaseFile
            fields="__all__"

        def  create(self, validated_data):
            s.validated_data_add(validated_data,self.initial_data,  usersModels.UserProfile,"userId","userId")
            s.validated_data_add(validated_data, self.initial_data, models.CaseGroup, "CaseGroupId", "CaseGroupId")
            s.validated_data_add(validated_data, self.initial_data, projectModels.PostMethods, "postMethod", "postMethod")
            s.validated_data_add(validated_data, self.initial_data, projectModels.PostType, "dataType", "dataType")
            s.validated_data_add(validated_data, self.initial_data, projectModels.Environments, "environmentId", "environmentId")
            validated_data["status"]=self.initial_data["status"]
            validated_data["data"]=self.initial_data["data"]
            validated_data["headers"] = self.initial_data["headers"]
            user=super().create(validated_data=validated_data)
            user.save()
            return  user

        def update(self, instance, validated_data):
            validated_data["status"] = self.initial_data["status"]
            validated_data["data"] = self.initial_data["data"]
            validated_data["headers"] = self.initial_data["headers"]
            s.validated_data_add(validated_data, self.initial_data, models.CaseGroup, "CaseGroupId", "CaseGroupId")
            s.validated_data_add(validated_data, self.initial_data, projectModels.PostType, "dataType", "dataType")
            s.validated_data_add(validated_data, self.initial_data, projectModels.Environments, "environmentId",
                                 "environmentId")
            user = super().update(instance=instance,validated_data=validated_data)
            user.save()
            return user

class S_CaseRun(serializers.ModelSerializer):
    """"""
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    CaseGroupId = serializers.SerializerMethodField()
    environmentId=serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()
    headers = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    def get_environmentId(self,obj):
        item = projectModels.Environments.objects.get(is_eg=1).value
        if not obj.environmentId:

            return {"environment":[],"global":json.loads(item)}
        return {"environment":json.loads(obj.environmentId.value),"global":json.loads(item)}

    def get_data(self, obj):
        if obj.data:
            return json.loads(obj.data)

    def get_headers(self, obj):
        if obj.headers:
            print(obj.headers)
            return json.loads(obj.headers)

    def get_CaseGroupId(self, obj):
        return {"id": obj.CaseGroupId.id, "name": obj.CaseGroupId.name}

    def get_userId(self, obj):
        return {"id": obj.userId.id, "name": obj.userId.name}

    def get_status(self, obj):
        return {"id": obj.status, "name": obj.get_status_display()}
    class Meta:
        model=models.CaseFile
        fields="__all__"


class S_Environments(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    def validate(self, attrs):
        if attrs.get("postMethod")=="":
            raise ValidationError("请求类型为必须填写")
    class Meta:
        model=projectModels.Environments
        fields="__all__"
    # def create(self, validated_data):
    #     user=super().create(validated_data=validated_data)
    #     user.save()
    #     return user

class S_debugCase(serializers.Serializer):
    # name=serializers.CharField(required=False)
    # order=serializers.IntegerField(required=False)
    # postMethod=serializers.CharField()
    # dataType = serializers.CharField()
    # attr = serializers.CharField()
    # headers = serializers.CharField()
    # data = serializers.CharField()
    def validate(self, attrs):
        print(self.initial_data)
        postMethod=self.initial_data.get("postMethod")
        dataType=self.initial_data.get("dataType")
        attr=self.initial_data.get("attr")
        if postMethod == "" or postMethod == None:
            raise ValidationError("请求方法必须填写")
        if dataType == "" or dataType == None:
            raise ValidationError("请求数据类型必须填写")
        if attr == "" or attr == None:
            raise ValidationError("请求地址必须填写")
        # if attrs.get("headers") == "":
        #     raise ValidationError("请求类型为必须填写")
        # if attrs.get("data")=="":
        #     raise ValidationError("请求类型为必须填写")
        return attrs


class  S_CaseFilesDetail(serializers.ModelSerializer):
    """获取接口文档下面的用例以及其他数据"""
    caseGroup=serializers.SerializerMethodField()
    # environmentId=serializers.SerializerMethodField()
    #
    # def get_environmentId(self,obj):
    #     item = projectModels.Environments.objects.get(is_eg=1).value
    #     if not obj.environmentId:
    #
    #         return {"environment":[],"global":json.loads(item)}
    #     return {"environment":json.loads(obj.environmentId.value),"global":json.loads(item)}
    def get_caseGroup(self,obj):
        # obj.get_status_display()
        res=[]

        CaseGroupObj=obj.idCaseGroupFiles.all()
        for  item  in CaseGroupObj:
            code = {"child":[]}
            code["name"] = item.name
            code["order"] = item.order
            caseObj=item.IdCaseGroup.all()
            for rows in  caseObj:
                Env = projectModels.Environments.objects.get(is_eg=1).value
                if not rows.environmentId:
                    a={"environment":[],"global":json.loads(Env)}
                    print(a)
                else:
                    a={"environment":json.loads(rows.environmentId.value),"global":json.loads(Env)}
                    print(a)
                dict_obj = {
                    "name": rows.name,
                    "order": rows.order,
                    "status": rows.get_status_display(),
                    "postMethod": rows.postMethod.id,
                    "dataType": rows.dataType.id,
                    "attr": rows.attr,
                    "detail": rows.detail,
                    "headers": json.loads(rows.headers),
                    "data": json.loads(rows.data),
                    "environmentId":a
                }
                code["child"].append(dict_obj)
            res.append(code)
        return  res
    class Meta:
        model=models.CaseGroupFiles
        fields=("id","caseGroup")
