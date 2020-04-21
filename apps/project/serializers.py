from  rest_framework import serializers

from  project import models


class  S_ProjectList(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
    class Meta:
        model= models.ProjectList
        fields="__all__"


class S_AddProject(serializers.ModelSerializer):

    user=serializers.SerializerMethodField()
    create_time=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    def get_user(self,obj):
        return {"id":obj.user.id,"userName":obj.user.name}
    class Meta:
        model= models.ProjectList
        fields=["name","dev_attr","test_attr","product_attr","user","create_time","id"]


    def create(self, validated_data):
        user=super().create(validated_data=validated_data)
        user.save()
        return user


class S_UpdateProject(serializers.ModelSerializer):

    user=serializers.SerializerMethodField()
    create_time=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
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