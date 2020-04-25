import json
from  rest_framework import serializers
from  project import models
from users.models import UserProfile
from  rest_framework.exceptions import ValidationError


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
    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
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



class S_AddFiles(serializers.ModelSerializer):
    post_methods = serializers.SerializerMethodField()
    post_type = serializers.SerializerMethodField()
    res_type = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    def get_post_methods(self,obj):
        return {"id": obj.post_methods.id, "name": obj.post_methods.name}

    def get_post_type(self, obj):
        return {"id": obj.post_type.id, "name": obj.post_type.name}
    def get_res_type(self,obj):
        return {"id":obj.res_type.id, "name": obj.res_type.name}
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
        # "create_time":{
        #     "write_only":True,
        #     "format":'%Y-%m-%d %H:%M:%S'
        # },
        # "update_time":{
        #     "write_only":True,
        #     "format":'%Y-%m-%d %H:%M:%S'
        # }
    }



    def create(self, validated_data):
        projectId=self.initial_data["projectId"]
        try:
            validated_data["project"]=models.ProjectList.objects.get(id=projectId)

            create_user=self.initial_data["createUserId"]
            create_user_obj=UserProfile.objects.get(id=create_user)
            validated_data["create_user"]=create_user_obj

            post_methods=self.initial_data["postMethodsId"]
            post_methods_obj=models.PostMethods.objects.get(id=post_methods)

            post_type=self.initial_data["postTypeId"]
            post_type_obj=models.PostType.objects.get(id=post_type)

            res_type=self.initial_data["resTypeId"]
            res_type_obj=models.ResType.objects.get(id=res_type)

            validated_data["post_methods"]=post_methods_obj
            validated_data["post_type"]=post_type_obj
            validated_data["res_type"]=res_type_obj

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
