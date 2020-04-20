from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from enum import  Enum

class  UserProfile(AbstractUser):
    """
    用户信息
    """
    username = models.CharField(unique=True ,verbose_name="手机号码",max_length=12)  #因为django JWT-token验证必须传username所以这里就用这个
    name = models.CharField(verbose_name="姓名", max_length=5)
    password = models.CharField(verbose_name="密码", max_length=255)
    create_time=models.DateField(auto_now_add=True, verbose_name="创建时间")  #创建对象时更新这个时间，以后sava都不会更新
    update_time=models.DateField(auto_now=True, verbose_name="更新时间")  #每次save都更新这个时间
    user_last_project=models.IntegerField(default=0,verbose_name="用户最后一次访问项目id")
    grp=models.ForeignKey("UserGroup", to_field="id", on_delete=models.SET_DEFAULT, related_name="isUserGroup", default=1)
    det=models.ForeignKey("Department", to_field="department_id",on_delete=models.SET_DEFAULT, related_name="isDepartment", default=1)

    class Meta:
        db_table="user_profile"

class Department(models.Model):
    """
    部门
    """

    name=models.CharField(max_length=10,verbose_name="部门",default="研发部")
    department_id=models.IntegerField(default=1,unique=True)
    class Meta:
        db_table="department"

class UserGroup(models.Model):
    """用户属组
    """
    authority=(
        (1,"查"),
        (2,"增查改"),
        (3,"增查改删"),

    )
    user_group_id=models.CharField(choices=authority,max_length=2,unique=True,default=1)

    class Meta:
        db_table="user_group"



