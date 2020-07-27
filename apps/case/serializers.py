import  json,os
from rest_framework import serializers
from rest_framework.validators import ValidationError
from libs.validated_update import Validated_data
from project import models as projectModels
from users import  models as usersModels
from django.db.models import Q

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
            s.validated_data_add(validated_data,self.initial_data,  usersModels.UserProfile,"userId","update_userId")

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

        CaseGroupObj=obj.idCaseGroupFiles.select_related("projectId","userId","CaseGroupFilesId").all()
        for  item  in CaseGroupObj:
            code = {"child":[]}
            code["name"] = item.name
            code["order"] = item.order
            caseObj=item.IdCaseGroup.all()
            for rows in  caseObj:
                Env = projectModels.Environments.objects.get(is_eg=1).value
                if not rows.environmentId:
                    a={"environment":[],"global":json.loads(Env)}
                else:
                    a={"environment":json.loads(rows.environmentId.value),"global":json.loads(Env)}
                dict_obj = {
                    "name": rows.name,
                    "order": rows.order,
                    "status": {"id": rows.status, "name": rows.get_status_display()},
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
        fields=("id","caseGroup","name")


class S_AddCasePlan(serializers.ModelSerializer):
    caseStartTime=serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    caseEndTime=serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    # cron = serializers.CharField()
    projectId=serializers.SerializerMethodField()
    userId=serializers.SerializerMethodField()
    status=serializers.SerializerMethodField()
    runType=serializers.SerializerMethodField()
    cron=serializers.SerializerMethodField()
    def get_projectId(self,obj):
        return {"id":obj.projectId.id,"name":obj. projectId.name}

    def get_userId(self,obj):
        return {"id":obj.userId.id,"name":obj.userId.name}

    def get_status(self,obj):
        return {"id":obj.status,"name":obj.get_status_display()}

    def get_runType(self,obj):
        return {"id":obj.runType,"name":obj.get_runType_display()}
    def get_cron(self,obj):
        if int(obj.runType)==1:
            return obj.cron
        if int(obj.runType)==0:
            return "-"
    def validate(self, attrs):
        cname=attrs.get("cname")
        data = self.initial_data.dict()
        print(data)
        if "cron"  in  data.keys():
            if data["cron"]=="-":
                raise ValidationError("定时策略不合法")

        if "id"  in  self.initial_data.dict().keys():  #编辑传id验证脚本是否重复
            idCode=self.initial_data["id"]
            if  models.CasePlan.objects.filter(Q(cname=cname) & ~Q(id=idCode)):
               raise  ValidationError("脚本名称不能重复")
        else:  #不传id就是新增--直接查脚本名称是否重复
            if models.CasePlan.objects.filter(Q(cname=cname)):
                raise ValidationError("脚本名称不能重复")

        return attrs
    class Meta:
        model=models.CasePlan
        fields="__all__"


    def  create(self, validated_data):
        s.validated_data_add(validated_data, self.initial_data, projectModels.ProjectList, "projectId", "projectId")
        s.validated_data_add(validated_data, self.initial_data, usersModels.UserProfile, "userId", "userId")
        validated_data["runType"]=int(self.initial_data["runType"])
        validated_data["CaseCount"]=models.CaseFile.objects.select_related("CaseGroupId__CaseGroupFilesId__projectId","CaseGroupId__CaseGroupFilesId","CaseGroupId").filter(Q(CaseGroupId__CaseGroupFilesId__projectId=int(self.initial_data["projectId"])) & Q(status=1)).count()
        user= super().create(validated_data=validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        # if validated_data["againScript"]:  #如果重新创建脚本则更新用例数量
        #     validated_data["CaseCount"] = models.CaseFile.objects.filter(
        #         Q(CaseGroupId__CaseGroupFilesId__projectId=int(self.initial_data["projectId"])) & Q(status=1)).count()

        validated_data["runType"]=int(self.initial_data["runType"])
        if int(validated_data["runType"])==1:
            validated_data["cron"]=self.initial_data["cron"]
        user=super().update(instance=instance,validated_data=validated_data)
        user.save()
        return user

class  S_GetCaseList(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    isInterface=serializers.SerializerMethodField()
    isClass = serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
    updateUser = serializers.SerializerMethodField()
    postMethod=serializers.SerializerMethodField()
    order=serializers.SerializerMethodField()
    def get_isInterface(self,obj):
        return {"id":obj.CaseGroupId.id,"name":obj.CaseGroupId.name,"order":obj.CaseGroupId.order}
    def get_isClass(self,obj):
       return {"id": obj.CaseGroupId.CaseGroupFilesId.id, "name": obj.CaseGroupId.CaseGroupFilesId.name, }
    def get_user(self,obj):
        return {"id":obj.userId.id,"name":obj.userId.name}
    def get_updateUser(self,obj):
        res=getattr(obj, "update_userId", None)
        if  res:
            return {"id":res.id,"name":res.name}
        else:
            return {"id": obj.userId.id, "name": obj.userId.name}
    def get_postMethod(self,obj):
        return {"id":obj.postMethod.id,"name":obj.postMethod.name}

    def get_order(self,obj):
        order_1=obj.CaseGroupId.order
        order_2=obj.order
        return  "{0}-{1}".format(order_1,order_2)
    class  Meta:
        model=models.CaseFile
        fields=("id","name","postMethod","isInterface","isClass","detail","user","updateUser","createTime","updateTime","order")

class S_EditCaseOrder(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    isInterface = serializers.SerializerMethodField()
    isClass = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    updateUser = serializers.SerializerMethodField()
    postMethod = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    def get_isInterface(self,obj):
        return {"id":obj.CaseGroupId.id,"name":obj.CaseGroupId.name,"order":obj.CaseGroupId.order}
    def get_isClass(self,obj):
       return {"id": obj.CaseGroupId.CaseGroupFilesId.id, "name": obj.CaseGroupId.CaseGroupFilesId.name, }
    def get_user(self,obj):
        return {"id":obj.userId.id,"name":obj.userId.name}
    def get_updateUser(self,obj):
        res=getattr(obj, "update_userId", None)
        if  res:
            return {"id":res.id,"name":res.name}
        else:
            return {"id": obj.userId.id, "name": obj.userId.name}
    def get_postMethod(self,obj):
        return {"id":obj.postMethod.id,"name":obj.postMethod.name}

    def get_order(self,obj):
        order_1=obj.CaseGroupId.order
        order_2=obj.order
        return  "{0}-{1}".format(order_1,order_2)

    class Meta:
        model=models.CaseFile
        fields=("id","name","postMethod","isInterface","isClass","detail","user","updateUser","createTime","updateTime","order")

    def validate(self, attrs):
        data=self.initial_data.dict()
        if isinstance(data.get("corder"),str):
            if data.get("corder") in (None, ""):
                raise ValidationError("用例执行顺序为必填项")
            elif not isinstance(eval(data.get("corder")),int):
                raise ValidationError("用例执行顺序必须是整数")
        if isinstance(data.get("iorder"),str):
            if data.get("iorder") in  (None,""):
                 raise ValidationError("接口执行顺序为必填项")
            elif not isinstance(eval(data.get("iorder")),int) :
                raise ValidationError("接口执行顺序必须是整数")

        return attrs
    def update(self, instance, validated_data):
        s.validated_data_add(validated_data, self.initial_data, projectModels.PostMethods, "postMethod", "postMethod")
        s.validated_data_add(validated_data, self.initial_data, models.CaseGroup, "isInterface", "CaseGroupId")
        s.validated_data_add(validated_data, self.initial_data, usersModels.UserProfile, "updateUser", "update_userId")
        #跨表修改接口表的执行顺序
        print(validated_data["CaseGroupId"].order)
        validated_data["CaseGroupId"].order=self.initial_data["iorder"]
        validated_data["CaseGroupId"].save()
        print(validated_data["CaseGroupId"].order)
        validated_data["order"]=self.initial_data["corder"]
        user=super().update(instance=instance,validated_data=validated_data)
        user.save()
        return user

class S_CaseResults(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updateTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    user=serializers.SerializerMethodField()
    def  get_user(self,obj):
        return {"id":obj.userId.id,"name":obj.userId.name}


    class Meta:
        model=models.CaseResult
        fields="__all__"
