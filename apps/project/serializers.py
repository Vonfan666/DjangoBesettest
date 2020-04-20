from  rest_framework import serializers
from  . import models
from  rest_framework.validators import ValidationError


class  S_ProjectList(serializers.ModelSerializer):
    class Meta:
        model=models.ProjectList
        fields="__all__"


class S_AddProject(serializers.ModelSerializer):

    create_user_id=serializers.SerializerMethodField(read_only=False)

    def get_create_user_id(self,obj):
        return {"id":obj.create_user_id.name}
    class Meta:
        model=models.ProjectList
        fields=["name","dev_attr","test_attr","product_attr","create_user_id"]


    def create(self, validated_data):
        user=super().create(validated_data=validated_data)
        user.save()
        return user