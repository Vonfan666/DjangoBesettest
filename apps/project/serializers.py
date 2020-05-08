import json,os
from  rest_framework import serializers
from  project import models
from users.models import UserProfile
from  rest_framework.exceptions import ValidationError
from  libs.public import Public

from django.db.models import F

from  libs.validated_update import Validated_data
class  S_ProjectList(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
    class Meta:
        model= models.ProjectList
        fields="__all__"


class S_AddProject(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=serializers.SerializerMethodField()
    create_time=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model= models.ProjectList

        fields=["name","dev_attr","test_attr","product_attr","user","create_time","id"]

    def create(self, validated_data):
        a = self.initial_data["user"]
        validated_data["user"] = UserProfile.objects.get(id=a)
        user=super().create(validated_data=validated_data)

        user.save()
        return user


class S_UpdateProject(serializers.ModelSerializer):

    user=serializers.SerializerMethodField()
    create_time=serializers.DateTimeField(read_only=True)
    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
    class Meta:
        model= models.ProjectList
        #ID必传
        fields=["name","dev_attr","test_attr","product_attr","user","create_time","id"]


    def create(self, validated_data):
        user=super().create(validated_data=validated_data)
        user.save()
        return user

class S_PostMethods(serializers.ModelSerializer):
    class Meta:
        model=models.PostMethods
        fields = "__all__"

class S_PostType(serializers.ModelSerializer):
    class Meta:
        model=models.PostType
        fields = "__all__"

class S_ResType(serializers.ModelSerializer):
    class Meta:
        model=models.ResType
        fields="__all__"


class S_AddFiles(serializers.ModelSerializer):
    post_methods = serializers.SerializerMethodField()
    post_type = serializers.SerializerMethodField()
    res_type = serializers.SerializerMethodField()
    create_user=serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')



    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
    def get_post_methods(self,obj):
        obj=getattr(obj,"post_methods",None)
        if obj:
            return {"id": obj.id, "name": obj.name}

    def get_post_type(self, obj):
        obj=getattr(obj,"post_type",None)
        if obj:
            return {"id": obj.id, "name": obj.name}
    def get_res_type(self,obj):
        obj=getattr(obj,"res_type",None)
        if  obj:
            return {"id":obj.id, "name": obj.name}

    def get_create_user(self,obj):
        return obj.create_user.name
    class Meta:
        model=models.InterfaceFiles
        fields="__all__"
    extra_kwargs = {
        "id":{
          "write_only":True
        },
        "project":{
            "write_only":True
        }

    }
    def create(self, validated_data):

        try:
            projectId = self.initial_data["projectId"]
            validated_data["project"]=models.ProjectList.objects.get(id=projectId)

            create_user=self.initial_data["createUserId"]
            create_user_obj=UserProfile.objects.get(id=create_user)
            validated_data["create_user"]=create_user_obj

            if "postMethodsId" in  self.initial_data.keys():
                post_methods = self.initial_data["postMethodsId"]
                post_methods_obj=models.PostMethods.objects.get(id=post_methods)
                validated_data["post_methods"] = post_methods_obj

            if "postTypeId" in  self.initial_data.keys():
                post_type=self.initial_data["postTypeId"]
                post_type_obj=models.PostType.objects.get(id=post_type)
                validated_data["post_type"] = post_type_obj
            if "resTypeId" in  self.initial_data.keys():
                res_type=self.initial_data["resTypeId"]
                res_type_obj=models.ResType.objects.get(id=res_type)
                validated_data["res_type"] = res_type_obj
            if "fileId" in self.initial_data.keys():
                fileId = self.initial_data["fileId"]
                fileId_obj = models.InterfaceFilesName.objects.get(id=fileId)
                validated_data["file"] = fileId_obj

            # validated_data["post_header"]=json.dumps(self.initial_data["post_header"])
            # validated_data["post_data"] = json.dumps(self.initial_data["post_data"])
            # validated_data["res_header"] = json.dumps(self.initial_data["res_header"])
            # validated_data["res_data"] = json.dumps(self.initial_data["res_data"])

            user=super().create(validated_data=validated_data)
            user.save()
        except Exception as f:
            print(f)
            raise  ValidationError(f)
        return user

    def update(self, instance, validated_data):
        user = super().update(instance=instance, validated_data=validated_data)
        user.save()
        return user


class S_updateFiles(serializers.ModelSerializer):
    post_methods = serializers.SerializerMethodField()
    post_type = serializers.SerializerMethodField()
    res_type = serializers.SerializerMethodField()
    create_user=serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')



    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
    def get_post_methods(self,obj):
        obj=getattr(obj,"post_methods",None)
        if obj:
            return {"id": obj.id, "name": obj.name}

    def get_post_type(self, obj):
        obj=getattr(obj,"post_type",None)
        if obj:
            return {"id": obj.id, "name": obj.name}
    def get_res_type(self,obj):
        obj=getattr(obj,"res_type",None)
        if  obj:
            return {"id":obj.id, "name": obj.name}

    def get_create_user(self,obj):
        return obj.create_user.name
    class Meta:
        model=models.InterfaceFiles
        fields="__all__"
    extra_kwargs = {
        "id":{
          "write_only":True
        },
        "project":{
            "write_only":True
        },


    }



    def update(self, instance, validated_data):
        attr=Public().get_host_ip()
        s=Validated_data(validated_data, self.initial_data)
        s.validated_data_add(validated_data, models.PostMethods, "postMethodsId", "post_methods")
        s.validated_data_add(validated_data, models.PostType, "postTypeId", "post_type")
        s.validated_data_add(validated_data, models.ResType, "resTypeId", "res_type")
        # validated_data["mock_attr"] = attr+self.initial_data["post_attr"]
        validated_data["mock_attr"] = "http://%s:8081%smock/"%(attr,self.initial_data["post_attr"])

        user = super().update(instance=instance, validated_data=validated_data)
        user.save()
        return user

class S_CopyFiles(serializers.ModelSerializer):

    class Meta:
        model = models.InterfaceFiles
        fields = "__all__"

class  S_InterfaceFilesName(serializers.ModelSerializer):

    userName=serializers.SerializerMethodField()
    def get_userName(self,obj):
        return obj.project_id.user.name

    class Meta:
        model=models.InterfaceFilesName
        fields="__all__"


    def  create(self, validated_data):
        if  "projectId"  in self.initial_data:
            projectId=self.initial_data["projectId"]
            projectObj=models.ProjectList.objects.get(id=projectId)
            validated_data["project_id"]=projectObj
        user=super().create(validated_data=validated_data)
        user.save()
        return  user

    # def update(self, instance, validated_data):


class S_select_InterfaceFilesName(serializers.ModelSerializer):

    Clist=serializers.SerializerMethodField()

    def get_Clist(self,obj):
        return obj.files_name.all().annotate(name=F("filesName"),
                                             createUserName=F('project__user__name'),fid=F("file__id")).values("id", "name", "createUserName","fid")

    class Meta:
        model=models.InterfaceFilesName
        fields = "__all__"


#接口文档详情序列化
class S_interfaceDetail(serializers.ModelSerializer):
    """查询接口文档数据"""
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    post_header=serializers.SerializerMethodField()
    post_data = serializers.SerializerMethodField()
    res_header = serializers.SerializerMethodField()
    res_data = serializers.SerializerMethodField()
    def get_post_header(self,obj):
        obj=getattr(obj,"post_header",None)
        if obj:
            return json.loads(obj)
    def get_post_data(self,obj):
        obj=getattr(obj,"post_data",None)
        if obj:
            return json.loads(obj)
    def get_res_header(self,obj):
        obj=getattr(obj,"res_header",None)
        if obj:
            return json.loads(obj)
    def get_res_data(self,obj):
        obj=getattr(obj,"res_data",None)
        if obj:
            return json.loads(obj)
    class Meta:
        model=models.InterfaceFiles
        fields="__all__"


class S_Environments(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model=models.Environments
        fields="__all__"
    # def create(self, validated_data):
    #     user=super().create(validated_data=validated_data)
    #     user.save()
    #     return user

    def  validate(self, attrs):
        is_eg=attrs.get("is_eg")
        a=json.loads(json.dumps(attrs))
        print(json.loads(json.dumps(attrs)))
        if int(is_eg==2):  #环境变量必须有ename
            if "ename" not  in  a.keys():
                raise  ValidationError("环境名称为必填项")
            if not  attrs.get("ename"):
                raise ValidationError("环境名称为必填项")
        return attrs




