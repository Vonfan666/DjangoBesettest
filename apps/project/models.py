from django.db import models
# Create your models here.

class ProjectList(models.Model):
    """项目列表"""
    name=models.CharField(max_length=20,verbose_name="项目名称")
    dev_attr=models.CharField(max_length=100,verbose_name="开发地址")
    test_attr=models.CharField(max_length=100,verbose_name="测试地址")
    product_attr=models.CharField(max_length=100,verbose_name="生产地址")
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    user=models.ForeignKey("users.UserProfile",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="创建用户id")
    class Meta:
        db_table= "project_list"



class PostMethods(models.Model):
    """请求方法"""
    name=models.CharField(max_length=10,verbose_name="请求方法名称")
    class Meta:
        db_table= "post_methods"

class PostType(models.Model):
    """请求类型"""

    name = models.CharField(max_length=100, verbose_name="请求类型名称")
    class Meta:
        db_table= "post_type"

class ResType(models.Model):
    """返回类型"""
    name = models.CharField(max_length=10, verbose_name="返回类型名称")
    class Meta:
        db_table= "res_type"

class InterfaceFiles(models.Model):
    """文档列表"""

    project=models.ForeignKey("ProjectList", to_field="id", on_delete=models.SET_NULL,null=True, related_name="project_id", verbose_name="所属项目id")
    create_user=models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_DEFAULT, default=None, related_name="create_user_id", verbose_name="创建用户")
    filesName=models.CharField(max_length=255, verbose_name="接口文档名称")

    post_methods=models.ForeignKey("PostMethods",to_field="id",on_delete=models.SET_DEFAULT,default=None,verbose_name="该接口请求方法id")
    post_type=models.ForeignKey("PostType",to_field="id",on_delete=models.SET_DEFAULT,default=None,verbose_name="该接口请求类型id")

    post_attr=models.CharField(max_length=255,verbose_name="请求地址")
    interface_detail = models.CharField(max_length=255, verbose_name="接口描述")
    mock_attr=models.CharField(max_length=255,verbose_name="mock地址")
    post_header=models.CharField(max_length=255,verbose_name="请求头")
    post_data = models.CharField(max_length=255, verbose_name="请求数据")
    res_header = models.CharField(max_length=255, verbose_name="返回头部")
    res_data = models.CharField(max_length=255, verbose_name="返回数据")

    res_type=models.ForeignKey("ResType",to_field="id",on_delete=models.SET_DEFAULT,default=None,verbose_name="该接口返回方法id")

    create_time=models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time=models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table= "interface_files"






